"""NAPOR: the "Your own option" matcher, Python reference (numpy). The page (explorer/index.html) has the same
steps in JavaScript; tests and the Playwright parity check make sure both give the same ranked case ids.

What it does, in plain words: a viewer describes a US action. The matcher finds past cases of the SAME KIND:
  1. Hard rules. Boxes the viewer filled are exact filters on the case tags. In the description, clear cue phrases
     ("pull troops out", "sell weapons to", "kill a general") pick the Type of move, and that is a hard filter too.
  2. Word meaning. Every case (title + kind + the plain label of its move and target) and the description become one
     vector (the weighted average of GloVe word vectors). Cases are ranked by closeness (cosine), with a second
     score for how well each word of the description is matched by some word of the case.
  3. A closeness cut-off and a maximum number of cases. If even the best case is not close enough, nothing is returned.
The model only RETRIEVES cases. Every number on the page (five categories, risk index) is still counted from the
matched cases by the page's own code. All tuning numbers live in action_tags.MATCH (exported with the page data).
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
NEG = {"not", "no", "never", "without", "dont", "don", "doesnt", "doesn", "didnt", "wont", "won", "refuse", "refuses", "refrain", "avoid", "instead", "rather", "neither", "nor"}
SILENT = set("the a an of to for by with if did does do would from then than is it that this these those some all as be into u s us on in at near onto over off against up".split())
NOTSET = ["", "n/a", "na", "none", "-", "any"]
GAP = 4


def tokens(text):
    return TOK.findall(str(text if text is not None else "").lower().replace("’", "'").replace("‘", "'"))


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
    best, moves, cov = None, set(), set()
    hits = []
    for tier, mv, phs in cue_rows(matcher, names):
        for terms in phs:
            r = phrase_match(toks, terms)
            if r is not None:
                hits.append((tier, mv, r))
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
    dt = tokens(dtext)
    neg = False
    for k, t in enumerate(dt):
        if t in NEG and not any(x in SAY for x in dt[:k]):
            neg = True
    cue = dict(moves=[], tier=None, covered=set())
    if dt and not neg:
        cue = read_move(dt, matcher)
    return dict(fields=fields, sets=sets, box_text=" ".join(texts), desc=dtext, dtoks=dt, neg=neg, cue=cue)


# ---------------------------------------------------------------- the cases
class Theater:
    def __init__(self, tid, model, explorer=EXPLORER):
        d = json.load(open(os.path.join(explorer, "data", tid + ".json")))
        self.id = tid
        self.matcher = d["matcher"]
        self.neutral = set(self.matcher.get("neutral") or [])
        self.model = model
        seen, self.cases = set(), []
        for o in d["options"]:
            for c in o["cases"]:
                if c.get("week") or "tags" not in c or c["id"] in seen:
                    continue
                seen.add(c["id"])
                self.cases.append(dict(id=c["id"], date=c["date"], title=c["title"], kind=c.get("kind", ""), tags=c["tags"], okey=o["key"]))
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
    qtext = ("" if rd["neg"] else rd["desc"]) + " " + rd["box_text"]
    qvec, qwords = embed(model, tokens(qtext), th.neutral)
    ranked = bool(rd["dtoks"]) and not rd["neg"] and qvec is not None
    ordered = (not ranked) and qvec is not None      # only the boxes' words: every case that fits the boxes is kept, closest words first
    base = dict(ranked=ranked, moves=mv or [], moves_from=mv_from, neg=rd["neg"], reason=None)
    if rd["neg"] and not sets:
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


# ---------------------------------------------------------------- bench helpers
THEATERS = ["iran", "houthis", "northkorea", "china", "venezuela"]


def load_all(model=None, explorer=EXPLORER):
    model = model or Model(os.path.join(explorer, "matcher_vectors.json"))
    return model, {t: Theater(t, model, explorer) for t in THEATERS}
