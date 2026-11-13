"""NAPOR: the "Your own option" matcher, Python reference (numpy). The page (explorer/index.html) has the same
steps in JavaScript; tests and the Playwright parity check make sure both give the same ranked case ids.

What it does, in plain words: a viewer describes a US action. The matcher finds past cases of the SAME KIND:
  0. "Not". Words after a negation cue (not, never, without, avoid, instead of...) are what the US would NOT do: they are left out of every
     step below (rules, not the model). If that is all the viewer wrote, the US holds back: the matched cases are the hold weeks.
  1. Hard rules. Boxes the viewer filled are exact filters on the case tags. In the description, clear cue phrases
     ("pull troops out", "sell weapons to", "kill a general") pick the Type of move, and that is a hard filter too.
  2. Word meaning. Every case (title + kind + the plain label of its move and target) and the description become one
     vector (the weighted average of GloVe word vectors). Cases are ranked by closeness (cosine), with a second
     score for how well each word of the description is matched by some word of the case.
  3. A closeness cut-off and a maximum number of cases. If even the best case is not close enough, nothing is returned.
The model only RETRIEVES cases. Every number on the page (five categories, risk index) is still counted from the
matched cases by the page's own code. All tuning numbers live in action_tags.MATCH (exported with the page data).
Relevance (further down) says how well the counted cases fit what was typed; it is never a risk and changes no number.
"""
import base64
import json
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXPLORER = os.path.join(HERE, "..", "explorer")
TOK = re.compile(r"[a-z]+")
SAY = {"say", "says", "said", "declare", "declares", "state", "states", "announce", "announces", "pledge", "pledges", "promise", "promises", "reaffirm", "affirm", "tell", "tells", "warn", "warns", "reiterate", "clarify", "commit", "vow", "publicly"}   # words after which a "not" is part of what is said
# ---- negation: a rule layer (NOT the word model, which cannot be told "not"). See docs/METHODOLOGY.md section 13. ----
# A negation cue says the words after it (up to the next clause break, at most NEG_SCOPE words) are what the US would NOT do.
NEG_WORDS = {"not", "no", "never", "nothing", "neither", "nor", "dont", "doesnt", "didnt", "wont", "cant", "cannot", "shouldnt", "wouldnt",
             "couldnt", "mustnt"}
NEG_T = {"don", "doesn", "didn", "won", "can", "shouldn", "wouldn", "couldn", "mustn"}   # followed by "t" ("don't" -> don, t)
NEG_VERBS = ("refrain", "refus", "avoid", "declin", "forgo", "forego", "abstain", "shun", "eschew", "forswear", "renounc", "skip")   # word starts that mean "not doing"
NEG_PAIRS = [(("rule|rules|ruled|ruling", "out"), True), (("hold|holds|holding|held", "off|back"), True), (("stay|stays|staying|stayed|keep|keeps|keeping|kept", "out|away"), True),
             (("steer|steers|steering", "clear"), True), (("back|backs|backing|backed", "off"), True), (("stop|stops|stopping|stopped", "short", "of"), True),
             (("instead", "of"), False), (("rather", "than"), False), (("in", "place", "of"), False), (("as", "opposed", "to"), False)]
NEG_ONLY_AFTER = {"only", "just", "merely", "simply"}           # "not only X but Y" is not a negation
NEG_BREAK_WORDS = {"but", "then", "instead", "however", "although", "though", "while", "whereas", "yet"}
NEG_SCOPE = 8
NEG_GAP = 2     # "not (completely) ruling out": two cues this close cancel each other
FLUFF = set("take takes took taking make makes made making keep keeps kept keeping go goes going get gets have has had be been being are was were am will shall should "
            "could can may might must we i you they he she our their its his her my your america american americans washington administration government president trump "
            "united states also just only please now and or but any anything more further new additional another other again ever even still simply really actually so too very much "
            "many there here what which who when while such yet".split())
SILENT = set("the a an of to for by with if did does do would from then than is it that this these those some all as be into u s us on in at near onto over off against up".split())
NOTSET = ["", "n/a", "na", "none", "-", "any"]
GAP = 4


def tokens(text):
    return TOK.findall(str(text if text is not None else "").lower().replace("’", "'").replace("‘", "'"))


PIECE = re.compile(r"[a-z]+|[,;:.!?()\u2014\u2013]")


def tokens_br(text):
    """-> (tokens, breaks): the same words as tokens(), plus the set of word positions that have a punctuation break (comma, ;, :, ., !, ?, brackets, dashes) just before them."""
    toks, breaks = [], set()
    for m in PIECE.findall(str(text if text is not None else "").lower().replace("\u2019", "'").replace("\u2018", "'")):
        if m[0].isalpha():
            toks.append(m)
        else:
            breaks.add(len(toks))
    return toks, breaks


def said_before(toks, i):
    """True when a say/declare/announce word comes before word i (then a "not" there is part of what is said). "United States" is not a say word."""
    return any(x in SAY and not (x == "states" and k > 0 and toks[k - 1] == "united") for k, x in enumerate(toks[:i]))


def _alt(tok, alts):
    return tok in alts.split("|")


def _cue_at(toks, i):
    """The negation cue that starts at word i: (end, can_cancel) or None. can_cancel = it may cancel a "not" right before it."""
    n, t = len(toks), toks[i]
    for pair, can in NEG_PAIRS:
        if i + len(pair) <= n and all(_alt(toks[i + j], pair[j]) for j in range(len(pair))):
            return i + len(pair), can
    if t in NEG_T and i + 1 < n and toks[i + 1] == "t":
        return i + 2, False
    if t == "not" and i + 1 < n and toks[i + 1] in NEG_ONLY_AFTER:
        return None
    if t in NEG_WORDS:
        return i + 1, False
    if t == "without" or t.startswith(NEG_VERBS):
        return i + 1, True
    return None


def find_negations(toks, breaks):
    """Negation cues and what they cover: a list of {cue: (start, end), scope: (start, end), can_cancel, cancelled} in text order (positions are word
    positions, end exclusive). The scope is the words after the cue up to the next clause break (comma, ; : . ! ? bracket, dash, "but", "then",
    "instead", "however"...) and at most NEG_SCOPE words. A cue after a say/declare word is part of what is said, not a negation here. "not only/just"
    is not a negation. A second cue right after a first one ("not ruling out", "won't refuse") cancels both: a double negative is positive."""
    cues, i, n = [], 0, len(toks)
    while i < n:
        h = _cue_at(toks, i)
        if h is None:
            i += 1
            continue
        end, can = h
        if said_before(toks, i):
            i = end
            continue
        e = end
        while e < n and e - end < NEG_SCOPE and e not in breaks and toks[e] not in NEG_BREAK_WORDS:
            e += 1
        cues.append(dict(cue=(i, end), scope=(end, e), can_cancel=can, cancelled=False))
        i = end
    live = None
    for c in cues:
        if live is not None and c["can_cancel"] and live["scope"][0] <= c["cue"][0] < live["scope"][1] and c["cue"][0] - live["cue"][1] <= NEG_GAP:
            live["cancelled"] = c["cancelled"] = True
            live = None
            continue
        live = c
    return cues


def split_negation(toks, breaks):
    """-> (positive positions [sorted], negated positions {cue words and what they cover}, cue-word positions, active negations)."""
    cues = find_negations(toks, breaks)
    neg, cuew = set(), set()
    for c in cues:
        cuew.update(range(*c["cue"]))
        if not c["cancelled"]:
            neg.update(range(*c["scope"]))
    pos = [k for k in range(len(toks)) if k not in neg and k not in cuew]
    return pos, neg, cuew, [c for c in cues if not c["cancelled"]]


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

    def find(self, t):
        """Index of a word, or of its plain stem (-s, -es, -ies, -ed, -ing), or None."""
        if t in self.idx:
            return self.idx[t]
        c = []
        if t.endswith("ies"): c.append(t[:-3] + "y")
        if t.endswith("es"): c.append(t[:-2])
        if t.endswith("s") and not t.endswith("ss"): c.append(t[:-1])
        if t.endswith("ed"): c += [t[:-2], t[:-1]]
        if t.endswith("ing"): c += [t[:-3], t[:-3] + "e"]
        for x in c:
            if len(x) >= 3 and x in self.idx:
                return self.idx[x]
        return None


def embed(model, toks, neutral, factors=None):
    """-> (unit sentence vector or None, [(word index, weight)] unique words) for a list of tokens."""
    acc = {}
    for k, t in enumerate(toks):
        if t in neutral:
            continue
        i = model.find(t)
        if i is None:
            continue
        acc[i] = acc.get(i, 0.0) + model.w[i] * (factors[k] if factors else 1.0)
    if not acc:
        return None, []
    s = np.zeros(model.dim)
    tot = 0.0
    for i, w in acc.items():
        s += w * model.U[i]; tot += w
    n = np.sqrt((s * s).sum())
    return (s / n if n > 0 else None), sorted(acc.items())


# ---------------------------------------------------------------- reading words: cue phrases and boxes
def _terms(phrase):
    """'pull ... out|back' -> [(alts, max_gap_before)]; an alt ending in * matches any ending."""
    out, gap = [], 0
    for part in phrase.split(" "):
        if part == "...":
            gap = GAP
            continue
        alts = [(a[:-1], True) if a.endswith("*") else (a, False) for a in part.split("|") if a]
        out.append((alts, gap)); gap = 0
    return out


def _hit(tok, alts):
    return any((tok.startswith(a) if pre else tok == a) for a, pre in alts)


def phrase_match(toks, terms):
    """First place where the terms occur in order (each within its gap of the one before): list of token positions, or None."""
    def rec(k, pos):
        if k == len(terms):
            return []
        alts, gap = terms[k]
        hi = len(toks) - 1 if k == 0 else min(pos + gap, len(toks) - 1)
        for p in range(pos, hi + 1):
            if _hit(toks[p], alts):
                r = rec(k + 1, p + 1)
                if r is not None:
                    return [p] + r
        return None
    return rec(0, 0)


def cue_rows(matcher, names=False):
    """Every cue row as (tier, moves, [terms...]), including one tier-3 row per move from SYNONYMS (and the move names for a box)."""
    rows = [(c["p"], c["moves"], [_terms(p) for p in c["phrases"]]) for c in matcher["cues"]]
    for v in matcher["vocab"]["move"]:
        words = list((matcher["synonyms"].get("move") or {}).get(v, []))
        if names and v != "other":
            words.append(v)
        if names and v == "other":
            words.append("other")
        # word list -> consecutive-word phrases; the stem form of a word is matched too (strikes/striking via trailing *)
        ph = []
        for w in words:
            t = re.findall(r"[a-z]+\*?", w.lower())
            if t:
                ph.append([([(x[:-1], True) if x.endswith("*") else (x, False)], 0) for x in t])
        rows.append((3, [v], ph))
    return rows


def read_move(toks, matcher, names=False):
    """The Type of move a text points to: {moves: [values in VOCAB order], tier, covered: set of token positions}."""
    return read_move_runs([(0, toks)], matcher, names)


def read_move_runs(runs, matcher, names=False):
    """The same, for several separate runs of words [(offset, tokens)]: a cue phrase never reaches across the gap between two runs
    (the gap is a stretch of words the viewer said the US would NOT do)."""
    moves, cov = set(), set()
    hits = []
    for tier, mv, phs in cue_rows(matcher, names):
        for terms in phs:
            for off, toks in runs:
                r = phrase_match(toks, terms)
                if r is not None:
                    hits.append((tier, mv, [off + x for x in r]))
    if not hits:
        return dict(moves=[], tier=None, covered=set())
    best = min(h[0] for h in hits)
    for tier, mv, r in hits:
        cov.update(r)
        if tier == best:
            moves.update(mv)
    order = list(matcher["vocab"]["move"])
    return dict(moves=[m for m in order if m in moves], tier=best, covered=cov)


def _phrases(matcher, f):
    M = matcher
    mp = {}
    def add(v, p):
        t = " ".join(tokens(p))
        if t:
            mp.setdefault(t, [])
            if v not in mp[t]:
                mp[t].append(v)
    for v in M["vocab"][f]:
        if v != "none":
            add(v, v)
    for v, ws in (M["synonyms"].get(f) or {}).items():
        for w in ws:
            add(v, w)
    if f == "target":
        add("none", "no target")
    if f == "where":
        add("none", "no place"); add("none", "no location")
    lst = sorted(((t.split(" "), vs) for t, vs in mp.items()), key=lambda x: -len(x[0]))
    labs = sorted(((v, str(l).lower()) for v, l in M["vocab"][f].items()), key=lambda x: -len(x[1]))
    return lst, labs


def scan_box(text, f, matcher, neutral=()):
    """What one box's typed words mean: (values in VOCAB order, ignored words). The move box also reads cue phrases."""
    s = str(text if text is not None else "").lower().replace("’", "'")
    hits, ignored = [], []
    if f == "move":
        toks = tokens(s)
        r = read_move(toks, matcher, names=True)
        hits = list(r["moves"])
        for k, t in enumerate(toks):
            if k not in r["covered"] and t not in SILENT and t not in neutral and t not in ignored:
                ignored.append(t)
    else:
        lst, labs = _phrases(matcher, f)
        for v, lab in labs:
            m = re.search(r"(^|[^a-z0-9])" + re.escape(lab) + r"(?![a-z0-9])", s)
            if m:
                if v not in hits: hits.append(v)
                s = s[:m.start()] + m.group(1) + " , " + s[m.end():]
        for piece in re.split(r"\s*(?:,|;|/|\band\b|\bor\b)\s*", s):
            t = tokens(piece)
            i = 0
            while i < len(t):
                m = next((p for p in lst if all(i + j < len(t) and t[i + j] == w for j, w in enumerate(p[0]))), None)
                if m:
                    for v in m[1]:
                        if v not in hits: hits.append(v)
                    i += len(m[0])
                else:
                    if t[i] not in SILENT and t[i] not in neutral and t[i] not in ignored:
                        ignored.append(t[i])
                    i += 1
    order = list(matcher["vocab"][f])
    return [v for v in order if v in hits], ignored


def read_spec(spec, matcher, neutral=()):
    """What the page understood from the boxes and the description."""
    F = matcher["fields"]
    sets, texts, fields = {}, [], {}
    for f in F:
        typed = " ".join(str(spec.get(f, "") or "").split())[:200]
        unset = typed.lower() in NOTSET
        vals, ign = ([], []) if unset else scan_box(typed, f, matcher, neutral)
        fields[f] = dict(typed=typed, unset=unset, vals=vals, ignored=ign)
        if vals:
            sets[f] = vals
        if not unset:
            texts.append(typed)
    dtext = " ".join(str(spec.get("desc", "") or "").split())[:400]
    dt, br = tokens_br(dtext)
    pos, negpos, cuew, act = split_negation(dt, br)
    ptoks = [dt[k] for k in pos]
    cue = dict(moves=[], tier=None, covered=set())
    runs = []
    for k in pos:                       # runs of neighbouring positive words: a cue phrase never reaches across negated words
        if runs and k == runs[-1][0] + len(runs[-1][1]):
            runs[-1][1].append(dt[k])
        else:
            runs.append([k, [dt[k]]])
    runs = [(r[0], r[1]) for r in runs]
    if ptoks:
        cue = read_move_runs(runs, matcher)
    skip = SILENT | FLUFF | set(neutral)
    neg_content = any(dt[k] not in skip for k in negpos) or any(dt[c["cue"][0]] == "nothing" for c in act)
    pos_content = [t for t in ptoks if t not in skip]
    negs = [" ".join(dt[c["cue"][0]:c["scope"][1]]) for c in act]
    refrain = bool(act) and neg_content and cue["tier"] is None and not pos_content and not sets
    return dict(fields=fields, sets=sets, box_text=" ".join(texts), desc=dtext, dtoks=dt, ptoks=ptoks, neg=bool(act), negs=negs, refrain=refrain, pos_content=bool(pos_content), cue=cue)


# ---------------------------------------------------------------- the cases
class Theater:
    def __init__(self, tid, model, explorer=EXPLORER):
        d = json.load(open(os.path.join(explorer, "data", tid + ".json")))
        self.id = tid
        self.matcher = d["matcher"]
        self.neutral = set(self.matcher.get("neutral") or [])
        self.model = model
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

    def prep(self):
        P = self.matcher["params"]
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
    M = th.matcher
    P = dict(M["params"]); P.update(params or {})
    th.matcher = dict(M, params=P)
    rd = read_spec(spec, M, th.neutral)
    out = _match(rd, th, P)
    out["rd"] = rd
    return out


def _match(rd, th, P):
    M, F, model = th.matcher, th.matcher["fields"], th.model
    sets = rd["sets"]
    box = [f for f in F if f in sets and f != "move"]
    mv, mv_from = None, None
    if sets.get("move"):
        mv, mv_from = list(sets["move"]), "box"
    elif rd["cue"]["tier"] is not None:           # a clear cue; tier-0 cues carry no move at all, so nothing can match
        mv, mv_from = list(rd["cue"]["moves"]), "words"
    qtext = " ".join(rd["ptoks"]) + " " + rd["box_text"]      # the words the viewer said the US would NOT do are never searched
    qvec, qwords = embed(model, tokens(qtext), th.neutral)
    ranked = bool(rd["ptoks"]) and qvec is not None
    ordered = (not ranked) and qvec is not None      # only the boxes' words: every case that fits the boxes is kept, closest words first
    base = dict(ranked=ranked, moves=mv or [], moves_from=mv_from, neg=rd["neg"], hold=False, reason=None)
    if rd["refrain"]:                                  # only a "not": the US would hold back -> the weeks with no new US move
        cs = [dict(id=w["id"], sim=None, strength="loose", missed=[], week=True) for w in sorted(th.holds, key=lambda w: (w["date"], w["id"]))]
        return dict(base, ranked=False, moves=[], moves_from="hold", hold=True, cases=cs, kept=[], dropped=[], reason=None if cs else "nothing")
    if rd["neg"] and not sets and not rd["pos_content"] and mv is None:
        return dict(base, cases=[], kept=[], dropped=[], reason="negation")
    if not sets and not ranked:
        return dict(base, cases=[], kept=[], dropped=[], reason="empty")
    prep = th.prep()
    sc = {}
    if ranked or ordered:
        qi = np.array([w[0] for w in qwords], dtype=int)
        qw = np.array([w[1] for w in qwords])
        qwt = np.array([model.w[i] for i in qi])
        Q = model.U[qi]
        for k, c in enumerate(th.cases):
            cv, cw = prep[k]
            cos = float(qvec @ cv) if cv is not None else 0.0
            if len(cw):
                al = float(((Q @ model.U[cw].T).max(axis=1) * qwt).sum() / qwt.sum())
            else:
                al = 0.0
            sc[c["id"]] = (1 - P["soft"]) * cos + P["soft"] * al
    movef = mv

    def pool(kept):
        return [c for c in th.cases if (movef is None or c["tags"]["move"] in movef) and all(_meets(c, f, sets) for f in kept)]

    def select(pl):
        if ordered:
            return sorted(pl, key=lambda c: (sum(1 for f in box if not _meets(c, f, sets)), -sc[c["id"]], c["id"])), False
        if not ranked:
            return sorted(pl, key=lambda c: (c["date"], c["id"])), False
        pl = sorted(pl, key=lambda c: (-sc[c["id"]], c["id"]))
        if not pl:
            return [], False
        best = sc[pl[0]["id"]]
        floor = P["none_below_move"] if movef else P["none_below"]
        if best < floor:
            return [], True
        lo = max(P["min_sim_move"] if movef else P["min_sim"], best - P["rel_gap"])
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
    lv = levels[-1] if levels[-1][0] >= P["min_pool"] else max(levels, key=lambda l: (l[0], -len(l[2])))
    _, kept, dropped, cs, weak = lv
    res = []
    for c in cs:
        missed = [f for f in box if not _meets(c, f, sets)]
        s = sc.get(c["id"]) if (ranked or ordered) else None
        if ranked:
            st = "exact" if (s >= P["very_close"] and not missed) else "close" if (s >= P["close"] and len(missed) <= 1) else "loose"
        else:
            st = "exact" if not missed else "close" if len(missed) == 1 else "loose"
        res.append(dict(id=c["id"], sim=s, strength=st, missed=missed))
    return dict(base, cases=res, kept=kept, dropped=dropped, reason="weak" if (weak and not res) else None)


# ---------------------------------------------------------------- relevance (how well the counted cases fit what was typed; never a risk)
def stem_forms(t):
    """A word and its plain stems (-s, -es, -ies, -ed, -ing; the same simple stemming as Model.find). Two words match when their forms share one."""
    c = {t}
    if t.endswith("ies"): c.add(t[:-3] + "y")
    if t.endswith("es"): c.add(t[:-2])
    if t.endswith("s") and not t.endswith("ss"): c.add(t[:-1])
    if t.endswith("ed"): c.update([t[:-2], t[:-1]])
    if t.endswith("ing"): c.update([t[:-3], t[:-3] + "e"])
    return {x for x in c if x == t or len(x) >= 3}


def relevance_headline(strengths):
    """Share of the counted cases rated Very close or Close. strengths = the strength word of each counted case.
    band: 'few' (under 3 cases), 'strong' (75% or more), 'moderate' (50-74%), 'weak' (under 50%). Integer maths only, so Python and JavaScript agree."""
    n = len(strengths)
    close = sum(1 for x in strengths if x in ("exact", "close"))
    if n < 3:
        return dict(n=n, close=close, pct=None, band="few")
    band = "strong" if 4 * close >= 3 * n else "moderate" if 2 * close >= n else "weak"
    return dict(n=n, close=close, pct=(200 * close + n) // (2 * n), band=band)


def key_words(rd, neutral, known):
    """The meaningful words the viewer typed (description + boxes), once each, in order: not a small word, not one of the theater's own names, not a word
    the viewer said the US would NOT do, and (description) known to the word model / (box) understood by the page. known(t) -> bool for description words."""
    skip = SILENT | FLUFF | set(neutral)
    out = []
    for t in rd["ptoks"]:
        if t not in skip and known(t) and t not in out:
            out.append(t)
    for f, fd in rd["fields"].items():
        if fd["unset"]:
            continue
        for t in tokens(fd["typed"]):
            if t not in skip and t not in fd["ignored"] and t not in out:
                out.append(t)
    return out


def relevance_words(words, case_token_lists):
    """How many key words show up (after stemming) in at least one counted case's words. -> (found count, [missing words])."""
    have = set()
    for toks in case_token_lists:
        for t in toks:
            have |= stem_forms(t)
    miss = [w for w in words if not (stem_forms(w) & have)]
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


def relevance(rd, th, case_ids, strengths):
    """The whole Relevance figure for the counted cases (ids + strengths): headline numbers and the key-word line."""
    h = relevance_headline(strengths)
    words = key_words(rd, th.neutral, lambda t: th.model.find(t) is not None)
    found, miss = relevance_words(words, [case_words(th, i) for i in case_ids])
    return dict(h, kw_total=len(words), kw_found=found, kw_missing=miss, words=words)


# ---------------------------------------------------------------- bench helpers
THEATERS = ["iran", "houthis", "northkorea", "china", "venezuela"]


def load_all(model=None, explorer=EXPLORER):
    model = model or Model(os.path.join(explorer, "matcher_vectors.json"))
    return model, {t: Theater(t, model, explorer) for t in THEATERS}
