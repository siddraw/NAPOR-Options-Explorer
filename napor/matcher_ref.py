"""NAPOR: the "Your own option" matcher, Python reference (numpy). The page (explorer/index.html) has the same
steps in JavaScript; tests and the Playwright parity check make sure both give the same results.

What it does, in plain words: a viewer describes a US action. The matcher finds past cases of the SAME KIND:
  0. Words. The text is cut to a fixed length (by characters, not bytes), lower-cased, accents removed and split into plain
     letter words (digits, hyphens, apostrophes and other marks are separators). A word the matcher does not know is
     repaired when it is a close typo of a word it does know ("sanctoins" -> "sanctions"). Word endings are ignored
     ("bombed", "bombing", "bombs" are "bomb"; "struck" is "strike").
  1. "Not" and "stop". Words after a negation cue (not, never, without, avoid, instead of...) are what the US would NOT do: they
     are left out of every step below (rules, not the model). If that is all the viewer wrote, the US holds back: the matched
     cases are the hold weeks. A reversing verb (lift, stop, cancel, end...) with a move after it asks for the OPPOSITE move
     ("stop bombing" -> talks, "lift sanctions" -> relief or talks, "stop selling arms" -> the US holds back).
  2. Hard rules. Boxes the viewer filled are exact filters on the case tags. In the description, clear cue phrases
     ("pull troops out", "sell weapons to", "kill a general") pick the Type of move, and that is a hard filter too.
  3. Word meaning. Every case (title + kind) and the description become one vector (the weighted average of GloVe word
     vectors). Cases are ranked by closeness (cosine), a second score for how well each word of the description is matched by
     some word of the case, and a third for the rare words of the description that appear literally in the case title.
  4. A closeness cut-off and a maximum number of cases. If even the best case is not close enough, nothing is returned.
  5. Strength. "Very close" and "Close" are ABSOLUTE: a case needs a move that fits the move that was read, a closeness over a
     fixed line, every literal word the word model could not understand, and (for Very close) no relaxed box.
Without the word-meaning model (it did not load) steps 0-2 and the literal-words score still work; only the word vectors are missing.
The model only RETRIEVES cases. Every number on the page (five categories, risk index) is still counted from the
matched cases by the page's own code. All tuning numbers live in action_tags.MATCH (exported with the page data).
Relevance (further down) says how well the counted cases fit what was typed; it is never a risk and changes no number.
"""
import base64
import json
import math
import os
import re
import unicodedata

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXPLORER = os.path.join(HERE, "..", "explorer")
NOTSET = ["", "n/a", "na", "none", "-", "any"]
GAP = 4
NEG_SCOPE = 8       # a negation covers at most this many words
NEG_GAP = 2         # "not (completely) ruling out": two cues this close cancel each other
NEG_BREAK = {"but", "then", "instead", "however", "although", "though", "while", "whereas", "yet"}
WS = re.compile("[ \t\n\r\f\v   -     　﻿]+")
MARKS = re.compile("[̀-ͯ]")
PIECE = re.compile("[a-z]+|[,;:.!?()/+&—–…]")


# ---------------------------------------------------------------- the text: one tokenizer for boxes and description
def clean(s, n):
    """Whitespace collapsed to single spaces, trimmed, cut to n characters (Unicode code points, so an emoji counts as one)."""
    return WS.sub(" ", "" if s is None else str(s)).strip(" ")[:n]


def norm(s):
    """Lower case, accents removed (NFKD, then the combining marks are dropped)."""
    return MARKS.sub("", unicodedata.normalize("NFKD", "" if s is None else str(s)).lower())


def tokens_br(text):
    """-> (tokens, breaks): the words (letters a-z only) and the set of word positions that have a punctuation break (comma, ; : . ! ? / + & brackets, dashes) just before them."""
    toks, breaks = [], set()
    for m in PIECE.findall(norm(text)):
        if "a" <= m[0] <= "z":
            toks.append(m)
        else:
            breaks.add(len(toks))
    return toks, breaks


def tokens(text):
    return tokens_br(text)[0]


def form_list(t, irreg):
    """A word and its plain base forms, in a fixed order: the irregular base (struck -> strike), then -ies, -es, -s, -ed, -ing, -ly stripped (doubled letters undone).
    Forms of 1-2 letters are never used."""
    out = [t]

    def add(x):
        if len(x) >= 3 and x not in out:
            out.append(x)

    def und(x):
        if len(x) >= 4 and x[-1] == x[-2] and x[-1] not in "aeiou":
            add(x[:-1])
    b = irreg.get(t, t)
    if b != t:
        add(b)
    if b.endswith("ies"): add(b[:-3] + "y")
    if b.endswith("es"): add(b[:-2])
    if b.endswith("s") and not b.endswith("ss"): add(b[:-1])
    if b.endswith("ed"):
        add(b[:-2]); add(b[:-1]); und(b[:-2])
    if b.endswith("ing"):
        add(b[:-3]); add(b[:-3] + "e"); und(b[:-3])
    if b.endswith("ly") and len(b) >= 5: add(b[:-2])
    return out


def osa(a, b, maxd):
    """Edit distance (insert, delete, change one letter, swap two neighbours = 1 each); anything over maxd is returned as maxd + 1."""
    la, lb = len(a), len(b)
    if abs(la - lb) > maxd:
        return maxd + 1
    prev2, prev = None, list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        for j in range(1, lb + 1):
            c = 0 if a[i - 1] == b[j - 1] else 1
            v = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + c)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                v = min(v, prev2[j - 2] + 1)
            cur[j] = v
        prev2, prev = prev, cur
    return prev[lb] if prev[lb] <= maxd else maxd + 1


# ---------------------------------------------------------------- word model
class Model:
    def __init__(self, path=None):
        d = json.load(open(path or os.path.join(EXPLORER, "matcher_vectors.json")))
        self.dim = d["dim"]
        self.words = d["words"].split(" ")
        self.idx = {w: i for i, w in enumerate(self.words)}
        q = np.frombuffer(base64.b64decode(d["q"]), dtype=np.int8).reshape(len(self.words), self.dim)
        v = (q.astype(np.float64) * d["scale"]).astype(np.float32).astype(np.float64)   # what a browser Float32Array holds
        n = np.sqrt((v * v).sum(axis=1))
        n[n == 0] = 1.0
        self.U = v / n[:, None]
        self.w = np.frombuffer(base64.b64decode(d["w"]), dtype=np.uint8).astype(np.float64) / 255.0
        self.irreg = {}

    def find(self, t):
        """Index of a word, or of its plain base form (see form_list), or None."""
        fl = form_list(t, self.irreg)
        if t.endswith(("ed", "ing")) and len(fl) > 1:      # an -ed / -ing word is read as its base (bombed -> bomb): the base has the clearer meaning
            fl = fl[1:] + fl[:1]
        for x in fl:
            if x in self.idx:
                return self.idx[x]
        return None


def embed(model, toks, skip, factors=None):
    """-> (unit sentence vector or None, [(word index, weight)] unique words in index order) for a list of tokens (words in `skip` are left out)."""
    acc = {}
    for k, t in enumerate(toks):
        if t in skip:
            continue
        i = model.find(t)
        if i is None:
            continue
        acc[i] = acc.get(i, 0.0) + model.w[i] * (factors[k] if factors else 1.0)
    if not acc:
        return None, []
    s = np.zeros(model.dim)
    for i, w in acc.items():
        s += w * model.U[i]
    n = np.sqrt((s * s).sum())
    return (s / n if n > 0 else None), sorted(acc.items())


# ---------------------------------------------------------------- compiled rules (built once per page data)
def _terms(phrase, fs=None):
    """'pull ... out|back' -> [(alts, max_gap_before)]; an alt ending in * matches any ending. alts = [(word, is_prefix, forms or None)]; forms only when fs is given."""
    out, gap = [], 0
    for part in phrase.split(" "):
        if part == "...":
            gap = GAP
            continue
        alts = []
        for a in part.split("|"):
            if not a:
                continue
            pre = a.endswith("*")
            w = a[:-1] if pre else a
            alts.append((w, pre, None if (pre or fs is None) else fs(w)))
        out.append((alts, gap))
        gap = 0
    return out


class Comp:
    """Everything compiled from the page's matcher data (cues, language rules, synonyms): shared by all theaters of one data set."""

    def __init__(self, M):
        L = M["lang"]
        self.M, self.L = M, L
        self.irreg = L["irregular"]
        self.silent, self.fluff, self.say = set(L["silent"]), set(L["fluff"]), set(L["say"])
        self._fs = {}
        self.rows = {}
        self.neg_rows = [self._row(r) for r in L["neg_rows"]]
        self.not_neg = [self._row(r) for r in L["not_neg"]]
        self.nocue = [_terms(p, self.fset) for p in L["nocue"]]
        self.revmap = L["revmap"]
        self.relief_pre, self.anti_pre = tuple(L["relief_words"]), tuple(L["anti_relief_words"])
        lex = []
        for k, v in L["lexicon"].items():
            kt = tokens(k)
            if kt:
                lex.append((kt, tokens(v), " ".join(kt)))
        self.lex = sorted(lex, key=lambda x: (-len(x[0]), x[2]))
        self.vocab = self._vocab()
        self.box = {}

    def fset(self, t):
        s = self._fs.get(t)
        if s is None:
            s = self._fs[t] = frozenset(form_list(t, self.irreg))
        return s

    def _row(self, r):
        return dict(kind=r.get("kind", "neg"), can=bool(r.get("can")), adj=bool(r.get("adj")), solo=bool(r.get("solo")), terms=_terms(r["p"]),
                    before=set(r["before"].split("|")) if r.get("before") else None, pre=set(r["pre"].split("|")) if r.get("pre") else None, start=bool(r.get("start")))

    def _vocab(self):
        """Every plain word the rules know (cue words, synonyms, vocabulary, lexicon keys, negation words): a word in this set is never repaired as a typo."""
        M, L, out = self.M, self.L, set()
        for c in M["cues"]:
            for p in c["phrases"]:
                for part in p.split(" "):
                    if part != "...":
                        for a in part.split("|"):
                            if a:
                                out.add(a[:-1] if a.endswith("*") else a)
        for f, d in (M.get("synonyms") or {}).items():
            for ws in d.values():
                for w in ws:
                    out.update(tokens(w))
        for f, d in M["vocab"].items():
            for v, lab in d.items():
                out.update(tokens(v)); out.update(tokens(lab))
        for kt, et, _ in self.lex:
            out.update(kt); out.update(et)
        for r in L["neg_rows"] + L["not_neg"]:
            for part in r["p"].split(" "):
                for a in part.split("|"):
                    if a:
                        out.add(a[:-1] if a.endswith("*") else a)
        out.update(["gonna", "gotta", "wanna"])
        return out

    # --- cue rows (move cues) ---
    def cue_rows(self, names):
        key = "n" if names else "p"
        if key in self.rows:
            return self.rows[key]
        M = self.M
        rows = [(c["p"], c["moves"], [_terms(p, self.fset) for p in c["phrases"]], bool(c.get("relief"))) for c in M["cues"]]
        for v in M["vocab"]["move"]:
            words = list((M["synonyms"].get("move") or {}).get(v, []))
            if names:
                words.append(v)
            ph = []
            for w in words:
                t = re.findall("[a-z]+\\*?", norm(w))
                if t:
                    ph.append([([(x[:-1], True, None)] if x.endswith("*") else [(x, False, self.fset(x))], 0) for x in t])
            rows.append((3, [v], ph, False))
        self.rows[key] = rows
        return rows

    def hit(self, tok, alts):
        for a, pre, fa in alts:
            if pre:
                if tok.startswith(a):
                    return True
            elif tok == a or (fa is not None and (self.fset(tok) & fa)):
                return True
        return False

    def phrase_match(self, toks, terms):
        """First place where the terms occur in order (each within its gap of the one before): list of token positions, or None."""
        n = len(toks)

        def rec(k, pos):
            if k == len(terms):
                return []
            alts, gap = terms[k]
            hi = n - 1 if k == 0 else min(pos + gap, n - 1)
            for p in range(pos, hi + 1):
                if self.hit(toks[p], alts):
                    r = rec(k + 1, p + 1)
                    if r is not None:
                        return [p] + r
            return None
        return rec(0, 0)

    def match_at(self, toks, i, terms):
        """End position when the terms match the words starting at i one after the other (exact words), else None."""
        for k, (alts, _) in enumerate(terms):
            j = i + k
            if j >= len(toks) or not any((toks[j].startswith(a) if pre else toks[j] == a) for a, pre, _f in alts):
                return None
        return i + len(terms)

    def cue_at(self, toks, i, breaks):
        """The negation row that starts at word i -> (end, row), or None (also None when the words are an idiom that only looks like a negation)."""
        for r in self.not_neg:
            if r["pre"] is not None and (i == 0 or toks[i - 1] not in r["pre"]):
                continue
            if r["start"] and not (i == 0 or i in breaks):
                continue
            if self.match_at(toks, i, r["terms"]) is not None:
                return None
        for r in self.neg_rows:
            if r["before"] is not None and not any(toks[j] in r["before"] for j in range(max(0, i - 5), i)):
                continue
            e = self.match_at(toks, i, r["terms"])
            if e is not None:
                return e, r
        return None

    # --- boxes ---
    def box_phrases(self, f):
        """-> [(tokens, [values])] longest first: the box's values, synonyms and full labels."""
        if f in self.box:
            return self.box[f]
        M, mp = self.M, {}

        def add(v, p):
            t = tokens(p)
            if t:
                k = " ".join(t)
                if k not in mp:
                    mp[k] = (t, [])
                if v not in mp[k][1]:
                    mp[k][1].append(v)
        for v in M["vocab"][f]:
            if v != "none":
                add(v, v)
        for v, ws in ((M.get("synonyms") or {}).get(f) or {}).items():
            for w in ws:
                add(v, w)
        for v, lab in M["vocab"][f].items():
            add(v, str(lab))
        if f == "target":
            add("none", "no target")
        if f == "where":
            add("none", "no place"); add("none", "no location")
        out = sorted(mp.items(), key=lambda kv: (-len(kv[1][0]), kv[0]))
        self.box[f] = [v for _, v in out]
        return self.box[f]


def comp_of(M):
    c = M.get("_c")
    if c is None:
        c = M["_c"] = Comp(M)
    return c


# ---------------------------------------------------------------- reading words: negation, cue phrases, boxes
def said_index(toks, i, say):
    """Index of the first say/declare/announce word before word i (then a "not" there is part of what is said; "United States" is not a say word), or -1."""
    for k in range(i):
        if toks[k] in say and not (toks[k] == "states" and k > 0 and toks[k - 1] == "united"):
            return k
    return -1


def find_negations(toks, breaks, C, neutral=(), skip=()):
    """Negation and reversal cues and what they cover: a list of {cue: (start, end), scope: (start, end), kind, can, solo, cancelled, said, idle, say}
    in text order (word positions, end exclusive). The scope is the words after the cue up to the next clause break (comma, ; : . ! ? bracket, dash,
    "but", "then", "instead", "however"...) and at most NEG_SCOPE words. A cue after a say/declare word is part of what is said (said=True).
    A cue right after a neighbour's name ("Iran refuses...") is another party's act, not the US's: it is skipped. A second cue right after a first one
    ("not ruling out", "won't refuse", "don't stop") cancels both: a double negative is positive. A cue with nothing after it, after other words
    ("... or not"), is idle."""
    cues, i, n = [], 0, len(toks)
    while i < n:
        h = C.cue_at(toks, i, breaks)
        if h is None:
            i += 1
            continue
        end, row = h
        sw = said_index(toks, i, C.say)
        verb = any(pre and toks[i].startswith(w) for w, pre, _f in row["terms"][0][0])      # "Iran refuses ...": a verb of another party, not the US
        if sw < 0 and i > 0 and toks[i - 1] in neutral and not row["solo"] and verb:
            i = end
            continue
        e = end
        while e < n and e - end < NEG_SCOPE and e not in breaks and toks[e] not in NEG_BREAK:
            e += 1
        cues.append(dict(cue=(i, end), scope=(end, e), kind=row["kind"], can=row["can"], adj=row["adj"], solo=row["solo"], cancelled=False, said=sw >= 0, idle=False, say=sw))
        i = end
    live = None
    for c in cues:
        if c["said"]:
            continue
        if live is not None and live["scope"][0] <= c["cue"][0] < live["scope"][1] and ((c["can"] and c["cue"][0] - live["cue"][1] <= NEG_GAP) or (c["adj"] and c["cue"][0] == live["cue"][1])):
            live["cancelled"] = c["cancelled"] = True
            live = None
            continue
        live = c
    inside = set()
    for c in cues:
        inside.update(range(*c["cue"]))
    for c in cues:
        if not c["said"] and not c["cancelled"] and c["scope"][0] == c["scope"][1] and not c["solo"] and any(toks[j] not in skip and len(toks[j]) >= 2 and j not in inside for j in range(c["cue"][0])):
            c["idle"] = True
    return cues


def read_move(toks, matcher, names=False, union=False):
    """The Type of move a text points to: {moves: [values in VOCAB order], tier, covered: set of token positions, relief}."""
    return read_move_runs([(0, toks)], matcher, names, union)


def read_move_runs(runs, matcher, names=False, union=False, extra=()):
    """The same, for several separate runs of words [(offset, tokens)]: a cue phrase never reaches across the gap between two runs
    (the gap is a stretch of words the viewer said the US would NOT do). `extra` = readings made by other rules [(tier, moves, relief)].
    union=True (the Type-of-move box): every move named counts; a cue is only dropped when a better-tier cue covers some of the same words."""
    C = comp_of(matcher)
    hits = []
    for tier, mv, phs, rel in C.cue_rows(names):
        for terms in phs:
            for off, toks in runs:
                r = C.phrase_match(toks, terms)
                if r is not None:
                    hits.append((tier, mv, [off + x for x in r], rel))
    for tier, mv, rel in extra:
        hits.append((tier, mv, [], rel))
    if not hits:
        return dict(moves=[], tier=None, covered=set(), relief=False)
    if union:
        keep = [h for h in hits if not any(g[0] < h[0] and set(g[2]) & set(h[2]) for g in hits)]
        best = min(h[0] for h in keep)
        use = keep
    else:
        best = min(h[0] for h in hits)
        use = [h for h in hits if h[0] == best]
    moves, cov = set(), set()
    for h in hits:
        cov.update(h[2])
    for h in use:
        moves.update(h[1])
    order = list(matcher["vocab"]["move"])
    return dict(moves=[m for m in order if m in moves], tier=best, covered=cov, relief=any(h[3] for h in use))


def _runs(toks, positions):
    """Neighbouring positions -> [(offset, words)] runs."""
    runs = []
    for k in positions:
        if runs and k == runs[-1][0] + len(runs[-1][1]):
            runs[-1][1].append(toks[k])
        else:
            runs.append([k, [toks[k]]])
    return [(r[0], r[1]) for r in runs]


def show_words(ws):
    """Words as the viewer typed them: don t -> don't."""
    return re.sub(" (t|s|ll|re|ve|d|m)\\b", "'\\1", " ".join(ws))


def scan_values(toks, positions, f, C, breaks):
    """The values of box f that the words at `positions` name -> (values, positions read, positions not read). A phrase never joins words of different
    clauses (a comma, "/", "and", "or"), and full labels (which contain "or"/"and") are read first."""
    M = C.M
    hits, used_pos = [], set()
    live = list(positions)
    for v, lab in sorted(((v, tokens(str(l))) for v, l in M["vocab"][f].items()), key=lambda x: (-len(x[1]), x[0])):
        n = len(lab)
        for s in range(0, len(toks) - n + 1):
            span = list(range(s, s + n))
            if n and all(k in live and k not in used_pos for k in span) and all(toks[k] == lab[j] for j, k in enumerate(span)):
                if v not in hits:
                    hits.append(v)
                used_pos.update(span)
    segs, cur = [], []
    for k in live:
        if k in used_pos:
            if cur:
                segs.append(cur)
            cur = []
            continue
        if toks[k] in ("and", "or"):
            if cur:
                segs.append(cur)
            cur = []
            continue
        if cur and (k in breaks or k != cur[-1] + 1):
            segs.append(cur)
            cur = []
        cur.append(k)
    if cur:
        segs.append(cur)
    for seg in segs:
        i = 0
        while i < len(seg):
            k = seg[i]
            hit = None
            for pt, vs in C.box_phrases(f):
                if i + len(pt) <= len(seg) and all(toks[k + j] == w or (C.fset(toks[k + j]) & C.fset(w)) for j, w in enumerate(pt)):
                    hit = (pt, vs)
                    break
            if hit:
                for v in hit[1]:
                    if v not in hits:
                        hits.append(v)
                used_pos.update(range(k, k + len(hit[0])))
                i += len(hit[0])
            else:
                i += 1
    return hits, used_pos


def scan_box(text, f, th):
    """What one box's typed words mean: {vals (in VOCAB order), ignored words, neg (values said NOT), used words, fixes, negated (bool)}. The move box also reads
    cue phrases and keeps every move it names. "Not" works in boxes too."""
    M, C = th.matcher, th.C
    toks, br = tokens_br(text)
    toks, fixes = th.repair(toks)
    skip = C.silent | C.fluff | th.neutral
    cues = [c for c in find_negations(toks, br, C, th.neutral, skip) if not c["said"] and not (c["kind"] == "rev" and not c["cancelled"])]
    dead, negpos = set(), set()
    for c in cues:
        dead.update(range(*c["cue"]))
        if not c["cancelled"] and not c["idle"]:
            negpos.update(range(*c["scope"]))
    dead |= negpos
    order = list(M["vocab"][f])
    ignored, used, neg = [], [], []
    pos = [k for k in range(len(toks)) if k not in dead]
    if f == "move":
        r = read_move_runs(_runs(toks, pos), M, True, True)
        hits = list(r["moves"])
        read = r["covered"]
        if negpos:
            neg = read_move_runs(_runs(toks, sorted(negpos)), M, True, True)["moves"]
    else:
        hits, read = scan_values(toks, pos, f, C, br)
        if negpos:
            neg = scan_values(toks, sorted(negpos), f, C, br)[0]
    for k in pos:
        if k in read:
            used.append(toks[k])
        elif toks[k] not in skip and toks[k] not in ignored and toks[k] not in ("and", "or"):
            ignored.append(toks[k])
    return dict(vals=[v for v in order if v in hits], ignored=ignored, neg=[v for v in order if v in neg], used=used, fixes=fixes, negated=bool(negpos))


def read_spec(spec, th):
    """What the page understood from the boxes and the description."""
    M, C = th.matcher, th.C
    F = M["fields"]
    order = list(M["vocab"]["move"])
    skip = C.silent | C.fluff | th.neutral
    fields, sets, box_words, fixes, texts = {}, {}, [], [], []
    for f in F:
        typed = clean(spec.get(f), 200)
        unset = typed.lower() in NOTSET
        r = dict(vals=[], ignored=[], neg=[], used=[], fixes=[], negated=False) if unset else scan_box(typed, f, th)
        vals, excl = r["vals"], False
        if not vals and r["neg"] and f != "move":                      # "not nuclear": every value except the ones said NOT
            vals, excl = [v for v in M["vocab"][f] if v not in r["neg"]], True
        fields[f] = dict(typed=typed, unset=unset, vals=vals, ignored=r["ignored"], neg=r["neg"], excl=excl, negated=r["negated"], used=r["used"])
        if vals:
            sets[f] = vals
        if not unset:
            texts.append(typed)
            for w in r["used"]:
                if w not in box_words:
                    box_words.append(w)
            for fx in r["fixes"]:
                if fx not in fixes:
                    fixes.append(fx)
    dtext = clean(spec.get("desc"), 400)
    if dtext.lower() in NOTSET:
        dtext = ""
    dt0, br = tokens_br(dtext)
    dt, dfix = th.repair(dt0)
    for fx in dfix:
        if fx not in fixes:
            fixes.append(fx)
    n = len(dt)
    cues = find_negations(dt, br, C, th.neutral, skip)
    act = [c for c in cues if not c["said"] and not c["cancelled"]]
    cuew, negpos = set(), set()
    for c in cues:                                      # words of a negation cue (a reversing verb that does something is handled below)
        if not c["said"] and (c["kind"] == "neg" or c["cancelled"] or c["idle"]):
            cuew.update(range(*c["cue"]))
    for c in act:
        if c["kind"] == "neg" and not c["idle"]:
            negpos.update(range(*c["scope"]))
    # reversing verbs: "stop bombing" -> the opposite move; a verb with no move after it does nothing
    rev, extra, consumed, rev_hold = [], [], set(), []
    for c in act:
        if c["kind"] != "rev" or c["idle"] or c["cue"][0] in negpos or c["cue"][0] in consumed:
            continue
        sp = [k for k in range(*c["scope"]) if k not in negpos and k not in consumed]
        r = read_move_runs(_runs(dt, sp), M, False, False)
        if r["tier"] is None or not r["moves"]:
            continue
        back = []
        for m in r["moves"]:
            for x in C.revmap.get(m, []):
                if x not in back:
                    back.append(x)
        if back:
            back = [m for m in order if m in back]
            rev.append(dict(text=show_words(dt[c["cue"][0]:c["scope"][1]]), forward=r["moves"], moves=back))
            extra.append((1, back, any(m in ("sanctions", "legal") for m in r["moves"])))
            consumed.update(range(c["cue"][0], c["scope"][1]))
        else:
            rev_hold.append(c)
            cuew.update(range(*c["cue"]))
            negpos.update(range(*c["scope"]))
    # words that are not a move even though a cue word is in them ("labor strike", "oil drilling", "fire the general")
    gone = set()
    live = [k for k in range(n) if k not in negpos and k not in cuew and k not in consumed]
    for terms in C.nocue:
        for off, tk in _runs(dt, live):
            r = C.phrase_match(tk, terms)
            if r is not None:
                gone.update(off + x for x in r)
    # what is said ("the US says it will not strike") is a statement, whatever the sentence says
    quoted = set()
    for c in cues:
        if c["said"]:
            quoted.update(range(c["say"] + 1, c["scope"][1]))
            extra.append((1, ["statement"], False))
    pos = [k for k in range(n) if k not in negpos and k not in cuew and k not in gone]
    cpos = [k for k in pos if k not in consumed and k not in quoted]
    ptoks = [dt[k] for k in pos]
    # the lexicon: a rare word, acronym or operation name -> plain words
    lexhits, xtoks, xruns, taken = [], [], [], set()
    ct = [dt[k] for k in cpos]
    for kt, et, key in C.lex:
        for s in range(0, len(ct) - len(kt) + 1):
            if all(s + j not in taken for j in range(len(kt))) and all(ct[s + j] == w or w in C.fset(ct[s + j]) for j, w in enumerate(kt)):
                taken.update(range(s, s + len(kt)))
                lexhits.append(dict(key=key, words=[ct[s + j] for j in range(len(kt))], exp=et))
                xruns.append((100000 + 100 * len(xruns), et))
                xtoks += et
    runs = _runs(dt, cpos) + xruns
    cue = read_move_runs(runs, M, False, False, extra) if (cpos or extra or xruns) else dict(moves=[], tier=None, covered=set(), relief=False)
    covered_pos = {k for k in cue["covered"] if k < n} | consumed
    # words: the ones the page did not understand (after typo repair) are listed apart
    unread, kwords = [], []
    for t in ptoks:
        if t in skip or len(t) < 2:
            continue
        if t not in kwords:
            kwords.append(t)
        if not th.known(t) and t not in unread:
            unread.append(t)
    meaning = any(th.known(t) for t in kwords)
    nact = [c for c in act if c["kind"] == "neg" and not c["idle"]] + rev_hold
    neg_content = any(dt[k] not in skip for k in negpos) or any(dt[c["cue"][0]] == "nothing" or c["solo"] for c in nact if c["kind"] == "neg")
    neg_runs = _runs(dt, sorted(negpos))
    neg_read = read_move_runs(neg_runs, M, False, False) if negpos else dict(moves=[], tier=None, covered=set(), relief=False)
    neg_moves = neg_read["moves"]
    # a negated move in the description is taken out of the Move box ("do not strike" + box "strike")
    mv = list(sets.get("move") or [])
    if mv and neg_moves and (set(mv) - set(neg_moves)):
        mv = [m for m in mv if m not in neg_moves]
        sets["move"] = mv
        fields["move"]["vals"] = mv
    box_neg = fields["move"]["neg"] if "move" in fields else []
    refrain, boxes_context = False, False
    if nact and neg_content and cue["tier"] is None and (not mv or not (set(mv) - set(neg_moves))):
        refrain = True
        boxes_context = any(f in sets for f in F)
    elif box_neg and not mv and cue["tier"] is None and not meaning:
        refrain = True
        boxes_context = any(f in sets for f in F if f != "move")
    conflict = bool(mv) and cue["tier"] is not None and bool(cue["moves"]) and not (set(cue["moves"]) & set(mv))
    # what the viewer said the US would NOT do to: "not nuclear sites" keeps the cases that did not target them
    excl = {}
    if negpos and not neg_moves and not refrain:
        for f in F:
            if f != "move":
                vs = scan_values(dt, sorted(negpos), f, C, br)[0]
                if vs:
                    excl[f] = vs
    negs, last = [], -1
    for c in sorted(nact, key=lambda c: c["cue"][0]):
        if c["cue"][0] < last:
            continue
        negs.append(show_words(dt[c["cue"][0]:c["scope"][1]]))
        last = c["scope"][1]
    covered_words = sorted({dt[k] for k in covered_pos}) if cue["moves"] else []
    return dict(fields=fields, sets=sets, box_text=" ".join(texts), box_words=box_words, desc=dtext, dtoks=dt, ptoks=ptoks, ppos=pos, neg=bool(nact), negs=negs, refrain=refrain,
                boxes_context=boxes_context, pos_content=any(t not in skip for t in ptoks), meaning=meaning, cue=cue, rev=rev, said=any(c["said"] for c in cues), conflict=conflict,
                fixes=fixes, unread=unread, kwords=[] if refrain else kwords, covered_words=covered_words, lex=[[h["key"], " ".join(h["exp"])] for h in lexhits], lexhits=lexhits,
                xtoks=xtoks, excl=excl, typed=bool(texts) or bool(dtext), covered_pos=sorted(covered_pos), relief=bool(cue["relief"]))


# ---------------------------------------------------------------- the cases
class Theater:
    def __init__(self, tid, model, explorer=EXPLORER):
        d = json.load(open(os.path.join(explorer, "data", tid + ".json")))
        self.id = tid
        self.matcher = d["matcher"]
        self.C = comp_of(self.matcher)
        self.neutral = set(self.matcher.get("neutral") or [])
        self.places = set(self.matcher.get("places") or [])
        self.model = model
        if model is not None:
            model.irreg = self.C.irreg
        seen, self.cases, self.holds = set(), [], []
        for o in d["options"]:
            if o.get("is_hold"):    # the hold option's cases are weeks with no logged US move (c.week); the page counts them as option A does
                self.holds = [dict(id=c["id"], date=c["date"], title=c["title"], kind=c.get("kind", ""), okey=o["key"]) for c in o["cases"] if c.get("week")]
            for c in o["cases"]:
                if c.get("week") or "tags" not in c or c["id"] in seen:
                    continue
                seen.add(c["id"])
                self.cases.append(dict(id=c["id"], date=c["date"], title=c["title"], kind=c.get("kind", ""), tags=c["tags"], okey=o["key"]))
        self.by_id = {c["id"]: c for c in self.cases}
        self.by_id.update({w["id"]: w for w in self.holds})
        self._prep = None
        self._fix = {}
        self._df = {}
        self._tools = None

    # ---- word knowledge, typo repair, document frequencies ----
    def tools(self):
        if self._tools:
            return self._tools
        C = self.C
        cf, tw = [], set()
        for c in self.cases:
            ts = tokens(c["title"]) + tokens(c["kind"])
            s = set()
            for t in ts:
                s.update(C.fset(t))
                tw.add(t)
            cf.append(s)
        relief = []
        for c in self.cases:
            ts = tokens(c["title"]) + tokens(c["kind"])
            relief.append(any(t.startswith(C.relief_pre) for t in ts) and not any(t.startswith(C.anti_pre) for t in ts))
        known = set(C.vocab) | C.silent | C.fluff | C.say | self.neutral | tw
        pool = {}

        def put(w, cls, rank):
            if len(w) >= 4 and w.isalpha() and (w not in pool or (cls, rank) < pool[w]):
                pool[w] = (cls, rank)
        for w in C.vocab:
            put(w, 0, 0)
        for w in self.neutral:
            put(w, 0, 0)
        for w in tw:
            put(w, 1, 0)
        if self.model is not None:
            P = self.matcher["params"]
            for i, w in enumerate(self.model.words[:int(P["fix_top"])]):
                if len(w) >= 4 and re.fullmatch("[a-z]+", w):
                    put(w, 2, i)
        by_len = {}
        for w, (cls, rank) in pool.items():
            by_len.setdefault(len(w), []).append((cls, rank, w))
        for v in by_len.values():
            v.sort()
        self._tools = dict(cf=cf, known=known, by_len=by_len, relief=relief)
        return self._tools

    def known(self, t):
        T = self.tools()
        if t in T["known"] or any(x in T["known"] for x in self.C.fset(t)):
            return True
        return self.model is not None and self.model.find(t) is not None

    def fix_word(self, t):
        """The closest known word when t is not known: up to 1 edit (2 for words of 8 letters or more), words under 5 letters are never repaired; prefers the rules' own
        words, then case-title words, then common model words. None when there is none."""
        if t in self._fix:
            return self._fix[t]
        res = None
        L = len(t)
        if L >= 5 and not self.known(t):
            maxd = 2 if L >= 8 else 1
            best = None
            by = self.tools()["by_len"]
            for l in range(L - maxd, L + maxd + 1):
                for cls, rank, w in by.get(l, ()):
                    d = osa(t, w, maxd)
                    if d <= maxd:
                        key = (d, cls, rank, w)
                        if best is None or key < best:
                            best = key
            if best:
                res = best[3]
        self._fix[t] = res
        return res

    def repair(self, toks):
        """-> (tokens with typos repaired, [[typed word, repaired word]])."""
        out, fx = [], []
        for t in toks:
            r = self.fix_word(t)
            if r is not None:
                out.append(r)
                if [t, r] not in fx:
                    fx.append([t, r])
            else:
                out.append(t)
        return out, fx

    def df(self, w):
        if w not in self._df:
            fs = self.C.fset(w)
            self._df[w] = sum(1 for s in self.tools()["cf"] if fs & s)
        return self._df[w]

    def prep(self, P):
        key = (P["kind_weight"], P["tag_weight"])
        if self._prep and self._prep[0] == key:
            return self._prep[1]
        V = self.matcher["vocab"]
        out = []
        for c in self.cases:
            toks, fac = [], []
            for src, fx in ((c["title"], 1.0), (c["kind"], P["kind_weight"]), (V["move"].get(c["tags"]["move"], ""), P["tag_weight"]),
                            (" ".join(V["target"].get(t, "") for t in c["tags"]["target"]), P["tag_weight"])):
                if fx <= 0:
                    continue
                for t in tokens(src):
                    toks.append(t); fac.append(fx)
            vec, words = embed(self.model, toks, self.neutral, fac)
            out.append((vec, np.array([w[0] for w in words], dtype=int)))
        self._prep = (key, out)
        return out


# ---------------------------------------------------------------- finding the cases
def _meets(c, f, sets):
    return any(v in sets[f] for v in c["tags"]["target"]) if f == "target" else c["tags"][f] in sets[f]


def match(spec, th, params=None):
    """spec = {move, target, where, scale, who, open, desc} (typed words). Returns the matched cases, best first:
    {cases: [{id, sim, strength, missed}], kept, dropped, ranked, moves, moves_from, neg, reason}."""
    P = dict(th.matcher["params"])
    P.update(params or {})
    rd = read_spec(spec, th)
    out = _match(rd, th, P)
    out["rd"] = rd
    return out


def _overlap_groups(rd, th, P):
    """The rare words of the description as literal-match groups: [{words, w (weight), df, modelled}]. Words the move cue already covers are left out."""
    C, skip = th.C, th.C.silent | th.C.fluff
    cov = set(rd["covered_pos"])
    lexkeys = set()
    for h in rd["lexhits"]:
        lexkeys.update(h["words"])
    groups, seen = [], set()
    N = len(th.cases)

    def weight(ws):
        best = 0.0
        for w in ws:
            d = th.df(w)
            if d > 0:
                x = math.log(1 + N / d) * (P["place_w"] if w in th.places else 1.0)
                if x > best:
                    best = x
        return best
    for k, t in zip(rd["ppos"], rd["ptoks"]):
        if t in skip or len(t) < 3 or k in cov or t in seen or t in lexkeys:
            continue
        seen.add(t)
        groups.append(dict(words=[t], mod=th.model is not None and th.model.find(t) is not None))
    for h in rd["lexhits"]:
        ws = []
        for t in h["words"] + h["exp"]:
            if t not in skip and len(t) >= 3 and t not in ws:
                ws.append(t)
        if ws:
            groups.append(dict(words=ws, mod=True))
    out = []
    for g in groups:
        w = weight(g["words"])
        if w > 0:
            g["w"] = w
            out.append(g)
        elif not g["mod"]:
            g["w"] = 0.0
    return out


def _match(rd, th, P):
    M, F, model = th.matcher, th.matcher["fields"], th.model
    sets = rd["sets"]
    T = th.tools()
    box = [f for f in F if f in sets and f != "move"]
    mv, mv_from = None, None
    if sets.get("move"):
        mv, mv_from = list(sets["move"]), "box"
    elif rd["cue"]["tier"] is not None:           # a clear cue; tier-0 cues carry no move at all, so nothing can match
        mv, mv_from = list(rd["cue"]["moves"]), "words"
    if mv_from == "words":                          # a kind of move this theater never logged is read as the kind it logs instead (a statement is a "talks" case here)
        mv = [x for m in mv for x in ([m] if any(c["tags"]["move"] == m for c in th.cases) else (M.get("alike") or {}).get(m, [m]))]
        mv = [m for i, m in enumerate(mv) if m not in mv[:i]]
    sib = {}
    if mv_from == "words":
        for m in mv:
            for s in (M.get("siblings") or {}).get(m, []):
                if s not in mv:
                    sib[s] = True
    skip = th.C.silent | th.neutral
    qt, qf = [], []
    for k, t in zip(rd["ppos"], rd["ptoks"]):
        qt.append(t); qf.append(P["place_w"] if t in th.places else P["cue_w"] if k in rd["covered_pos"] else 1.0)
    for t in rd["xtoks"]:
        qt.append(t); qf.append(P["place_w"] if t in th.places else P["lex_w"])
    for t in rd["box_words"]:
        qt.append(t); qf.append(P["place_w"] if t in th.places else 1.0)
    qvec, qwords = (embed(model, qt, skip, qf) if model is not None else (None, []))
    ranked = bool(rd["meaning"])
    ordered = (not ranked) and qvec is not None and bool(sets)      # only the boxes' words: every case that fits the boxes is kept, closest words first
    base = dict(ranked=ranked, ordered=ordered, moves=mv or [], moves_from=mv_from, neg=rd["neg"], hold=False, reason=None)
    if rd["refrain"]:                                  # only a "not": the US would hold back -> the weeks with no new US move
        cs = [dict(id=w["id"], sim=None, strength="loose", missed=[], week=True) for w in sorted(th.holds, key=lambda w: (w["date"], w["id"]))]
        return dict(base, ranked=False, ordered=False, moves=[], moves_from="hold", hold=True, cases=cs, kept=[], dropped=[], reason=None if cs else "nothing")
    if rd["neg"] and not sets and not rd["pos_content"] and mv is None:
        return dict(base, cases=[], kept=[], dropped=[], reason="negation")
    if not sets and not ranked and mv is None:
        return dict(base, cases=[], kept=[], dropped=[], reason="empty")
    if not sets and not ranked:                        # a move read, but no word of the description can be searched
        return dict(base, cases=[], kept=[], dropped=[], reason="empty")
    prep = th.prep(P) if model is not None else None
    mode = "vec" if qvec is not None else "lex"
    groups = _overlap_groups(rd, th, P) if ranked else []
    sc, capped = {}, {}
    if ranked or ordered:
        if qvec is not None:
            qi = np.array([w[0] for w in qwords], dtype=int)
            qwt = np.array([w[1] for w in qwords])
            Q = model.U[qi]
        wsum = sum(g["w"] for g in groups if g["w"] > 0)
        for k, c in enumerate(th.cases):
            sv = None
            if qvec is not None:
                cv, cw = prep[k]
                cos = float(qvec @ cv) if cv is not None else 0.0
                al = float(((Q @ model.U[cw].T).max(axis=1) * qwt).sum() / qwt.sum()) if len(cw) else 0.0
                sv = (1 - P["soft"]) * cos + P["soft"] * al
            ov = None
            cap = False
            if groups:
                got = 0.0
                for g in groups:
                    hit = any(th.C.fset(w) & T["cf"][k] for w in g["words"])
                    if g["w"] > 0:
                        got += g["w"] if hit else 0.0
                    if not g["mod"] and model is not None and not hit and g["w"] > 0:
                        cap = True
                if wsum > 0:
                    ov = got / wsum
            if sv is None:
                s = ov if ov is not None else 0.5
            elif ov is None:
                s = sv
            else:
                s = sv + P["lam"] * ov * (1.0 - sv)
            sc[c["id"]] = s
            capped[c["id"]] = cap
    movef = mv
    rel_ok = {c["id"]: T["relief"][k] for k, c in enumerate(th.cases)}

    def admits(c):
        m = c["tags"]["move"]
        if movef is not None and m not in movef and not (m in sib and c["tags"]["where"] == "adversary"):
            return False
        if rd["relief"] and m in ("sanctions", "legal") and not rel_ok[c["id"]]:
            return False
        return not any(_meets(c, f, rd["excl"]) for f in rd["excl"])

    def pool(kept):
        return [c for c in th.cases if admits(c) and all(_meets(c, f, sets) for f in kept)]

    small = mv_from == "words" and rd["cue"]["tier"] is not None and rd["cue"]["tier"] <= 1
    fl = (P["none_below_move"] if movef else P["none_below"]) if mode == "vec" else P["lex_none"]
    lo0 = (P["min_sim_move"] if movef else P["min_sim"]) if mode == "vec" else P["lex_min"]

    def select(pl):
        if ordered:
            return sorted(pl, key=lambda c: (sum(1 for f in box if not _meets(c, f, sets)), -sc[c["id"]], c["id"])), False
        if not ranked:
            return sorted(pl, key=lambda c: (c["date"], c["id"])), False
        pl = sorted(pl, key=lambda c: (-sc[c["id"]], c["id"]))
        if not pl:
            return [], False
        if small and len(pl) <= P["small_pool"]:      # a precise phrase names a kind of move the log has only a few of: show them all (never better than Loose)
            return pl, False
        best = sc[pl[0]["id"]]
        if best < fl:
            return [], True
        lo = max(lo0, best - P["rel_gap"])
        return [c for c in pl if sc[c["id"]] >= lo][:P["max_cases"]], False

    kept, dropped = list(box), []
    levels = []
    while True:
        cs, weak = select(pool(kept))
        levels.append((len(cs), list(kept), list(dropped), cs, weak))
        if len(cs) >= P["min_pool"]:
            break
        f = next((x for x in M["widen"] if x in kept), None)
        if f is None:
            break
        kept = [x for x in kept if x != f]; dropped = dropped + [f]
    # a level that dropped every box the viewer filled says nothing when there is no move and no word to go by
    inform = [l for l in levels if l[1] or mv is not None or ranked]
    if not inform:
        return dict(base, cases=[], kept=[], dropped=list(box), reason="vague")
    good = [l for l in inform if l[0] >= P["min_pool"]]
    lv = good[0] if good else max(inform, key=lambda l: (l[0], -len(l[2])))
    _, kept, dropped, cs, weak = lv
    move_fit = bool(mv)
    ex_th, cl_th = (P["very_close"], P["close"]) if mode == "vec" else (P["lex_very_close"], P["lex_close"])
    res = []
    for c in cs:
        missed = [f for f in box if not _meets(c, f, sets)]
        s = sc.get(c["id"]) if (ranked or ordered) else None
        if ranked:
            ok = move_fit and not capped[c["id"]] and s >= fl
            st = "exact" if (ok and s >= ex_th and not missed and not dropped) else "close" if (ok and s >= cl_th and len(missed) <= 1 and (not box or len(missed) < len(box))) else "loose"
        else:
            st = "exact" if not missed else "close" if len(missed) == 1 else "loose"
            if not move_fit:
                st = "loose"
            elif dropped and st == "exact":
                st = "close"
        res.append(dict(id=c["id"], sim=s, strength=st, missed=missed))
    return dict(base, cases=res, kept=kept, dropped=dropped, reason="weak" if (weak and not res) else None)


# ---------------------------------------------------------------- relevance (how well the counted cases fit what was typed; never a risk)
def stem_forms(t, irreg=None):
    """A word and its plain base forms (see form_list). Two words match when their forms share one."""
    return set(form_list(t, irreg or {}))


def relevance_headline(strengths):
    """Share of the counted cases rated Very close or Close. strengths = the strength word of each counted case.
    band: 'few' (under 3 cases), 'strong' (75% or more), 'moderate' (50-74%), 'weak' (under 50%). Integer maths only, so Python and JavaScript agree."""
    n = len(strengths)
    close = sum(1 for x in strengths if x in ("exact", "close"))
    if n < 3:
        return dict(n=n, close=close, pct=None, band="few")
    band = "strong" if 4 * close >= 3 * n else "moderate" if 2 * close >= n else "weak"
    return dict(n=n, close=close, pct=(200 * close + n) // (2 * n), band=band)


def key_words(rd, th, dropped=()):
    """The meaningful words the viewer typed, once each, in order -> (words, set of words that count as missing whatever the cases say):
    the description's content words (including the ones the page did not understand), then the words of every box the page had to relax and the box words it
    could not read. Words the viewer said the US would NOT do, small words and the theater's own names are left out; a box word that was read as a setting is
    not a key word (the box is an exact rule, and it is met)."""
    skip = th.C.silent | th.C.fluff | th.neutral
    out, forced = [], set()
    for t in rd["kwords"]:
        if t not in out:
            out.append(t)
    for f, fd in rd["fields"].items():
        if fd["unset"]:
            continue
        for t in (fd["used"] if f in dropped else []) + fd["ignored"]:
            if t in skip or len(t) < 2:
                continue
            if t not in out:
                out.append(t)
            forced.add(t)
    return out, forced


def relevance_words(words, case_token_lists, covered=(), forced=(), irreg=None, expand=None):
    """How many key words show up (after stemming) in at least one counted case's words (or are covered by the move the page read; or are a lexicon word one of
    whose plain words shows up). -> (found count, [missing words])."""
    have = set()
    for toks in case_token_lists:
        for t in toks:
            have |= stem_forms(t, irreg)
    miss = []
    for w in words:
        if w in forced:
            miss.append(w); continue
        if w in covered or (stem_forms(w, irreg) & have):
            continue
        if expand and w in expand and any(stem_forms(x, irreg) & have for x in expand[w]):
            continue
        miss.append(w)
    return len(words) - len(miss), miss


def case_words(th, case_id):
    """The words a counted case offers for the key-word check: its title, its kind line and the plain labels of its tags."""
    c = th.by_id[case_id]
    V = th.matcher["vocab"]
    out = tokens(c["title"]) + tokens(c.get("kind", ""))
    t = c.get("tags")
    if t:
        for f in th.matcher["fields"]:
            for v in (t[f] if f == "target" else [t[f]]):
                out += tokens(V[f].get(v, ""))
    return out


def relevance(rd, th, case_ids, strengths, dropped=()):
    """The whole Relevance figure for the counted cases (ids + strengths): headline numbers and the key-word line. The band is never better than the key
    words allow: with fewer than 3 of 4 key words found it is at most Moderate, with fewer than half at most Weak."""
    h = relevance_headline(strengths)
    words, forced = key_words(rd, th, dropped)
    expand = {}
    for hh in rd["lexhits"]:
        for w in hh["words"]:
            expand[w] = hh["exp"]
    found, miss = relevance_words(words, [case_words(th, i) for i in case_ids], set(rd["covered_words"]), forced, th.C.irreg, expand)
    band = h["band"]
    if band != "few" and words:
        kb = "strong" if 4 * found >= 3 * len(words) else "moderate" if 2 * found >= len(words) else "weak"
        rank = {"weak": 0, "moderate": 1, "strong": 2}
        if rank[kb] < rank[band]:
            band = kb
    return dict(h, band=band, kw_total=len(words), kw_found=found, kw_missing=miss, words=words)


# ---------------------------------------------------------------- bench helpers
THEATERS = ["iran", "houthis", "northkorea", "china", "venezuela"]


def load_all(model=None, explorer=EXPLORER, with_model=True):
    if with_model:
        model = model or Model(os.path.join(explorer, "matcher_vectors.json"))
    return model, {t: Theater(t, model if with_model else None, explorer) for t in THEATERS}
