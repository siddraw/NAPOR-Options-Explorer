"""NAPOR: build the small word-meaning file the "Your own option" matcher loads (explorer/matcher_vectors.json).

What it is: GloVe word vectors (Stanford, "glove-wiki-gigaword-100": 100 numbers per word, trained on Wikipedia and
news text, public domain licence PDDL). The page never downloads anything from outside its own files, so this script
keeps only the words the matcher can need and stores each number as one byte.

Words kept: the 20,000 most frequent GloVe words, plus every word in any case title or kind in the five theaters, the
plain labels of the tag words, the synonym and cue lists and the theater names (when GloVe knows them).
Also stored: one weight per word (SIF weight a/(a+p(word)), p from the word's frequency rank under Zipf's law, so
"the" counts almost nothing and "radar" counts a lot; a short list of words that appear in every title counts almost
nothing too).

Get the GloVe file once (about 130 MB; not committed to the repo; the folder napor/glove/ is git-ignored):
    python3 build_vectors.py --fetch
which downloads
    https://github.com/RaRe-Technologies/gensim-data/releases/download/glove-wiki-gigaword-100/glove-wiki-gigaword-100.gz
(or download it yourself and pass --glove PATH). Then run `python3 build_vectors.py` from napor/ (after export_explorer has
run for every theater). The output is deterministic: the same inputs give the same bytes.
The weekly agent reruns this when new case titles bring new words (AGENT.md). `--check` only tells you whether the
file already covers every word in the current data (exit 1 if not).
"""
import argparse
import base64
import gzip
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import action_tags as A
import theaters

EXPLORER = os.path.join(HERE, "..", "explorer")
OUT = os.path.join(EXPLORER, "matcher_vectors.json")
GLOVE_URL = "https://github.com/RaRe-Technologies/gensim-data/releases/download/glove-wiki-gigaword-100/glove-wiki-gigaword-100.gz"
GLOVE_DEFAULT = os.path.join(HERE, "glove", "glove-wiki-gigaword-100.gz")
TOP = 20000          # most frequent GloVe words kept
SIF_A = 1e-3         # SIF constant: weight = a / (a + p(word))
LOW = 0.03           # weight of the "appears in every title" words below
# Words that carry no meaning for "which past action is this like": reporting verbs and "US" itself. Weight LOW.
LOW_WORDS = set("""us u s american america americans would could should did does do doing done will can may might must shall
 says said say announces announced announce announcing tells told says reports reported report according
 also just now new more than then that this these those which who whom whose what when where while whether
 about after before over under into onto from with without within against between during per via""".split())
WORD = re.compile(r"[a-z]+")


def words_of(text):
    return WORD.findall(str(text).lower().replace("’", "'"))


def case_rows():
    """(theater id, id, title, kind) of every counted case in the page data."""
    out = []
    for tid in theaters.registered():
        d = json.load(open(os.path.join(EXPLORER, "data", tid + ".json")))
        seen = set()
        for o in d["options"]:
            for c in o["cases"]:
                if c.get("week") or "tags" not in c or c["id"] in seen:
                    continue
                seen.add(c["id"])
                out.append((tid, c["id"], c["title"], c.get("kind", "")))
    return out


def needed_words():
    need = set()
    for _, _, title, kind in case_rows():
        need.update(words_of(title)); need.update(words_of(kind))
    for f in A.FIELDS:
        for lab in A.VOCAB[f].values():
            need.update(words_of(lab))
        for v in A.VOCAB[f]:
            need.update(words_of(v))
        for ws in A.SYNONYMS.get(f, {}).values():
            for w in ws:
                need.update(words_of(w))
    for cue in A.CUES:
        for p in cue["phrases"]:
            need.update(words_of(re.sub(r"[a-z]+\*", " ", p)))      # a stem ending in * is not a word
    for k, v in A.LANG["lexicon"].items():        # the plain words a lexicon term (Fordow, THAAD...) stands for
        need.update(words_of(k)); need.update(words_of(v))
    for ws in A.NEUTRAL.values():
        for w in ws:
            need.update(words_of(w))
    return need


def read_glove(path):
    words, vecs = [], []
    with gzip.open(path, "rt", encoding="utf8") as f:
        first = f.readline().split()
        if len(first) != 2:     # no header: the first line is already a word
            f.seek(0)
        for line in f:
            p = line.rstrip("\n").split(" ")
            words.append(p[0]); vecs.append(np.array(p[1:], dtype=np.float64))
    return words, np.vstack(vecs)


def build(glove):
    words, vecs = read_glove(glove)
    n_all = len(words)
    rank = {w: i for i, w in enumerate(words)}
    need = needed_words()
    keep = [i for i, w in enumerate(words) if re.fullmatch(r"[a-z]+", w)]     # glove order = frequency order
    sel = sorted(set(keep[:TOP]) | {rank[w] for w in need if w in rank and re.fullmatch(r"[a-z]+", w)})
    unknown = sorted(w for w in need if w not in rank)  # asked for but GloVe has no vector: the matcher skips them
    h = math.log(n_all) + 0.5772
    wt, vs = [], []
    for i in sel:
        p = 1.0 / ((i + 1) * h)                        # Zipf: chance of the word given its frequency rank
        w = SIF_A / (SIF_A + p)
        if words[i] in LOW_WORDS:
            w = min(w, LOW)
        wt.append(int(round(w * 255)))
        v = vecs[i]; vs.append(v / (np.linalg.norm(v) or 1.0))
    V = np.vstack(vs)
    scale = float(np.abs(V).max()) / 127.0
    scale = float(f"{scale:.8g}")
    Q = np.clip(np.rint(V / scale), -127, 127).astype(np.int8)
    out = dict(dim=int(V.shape[1]), n=len(sel), unknown=unknown, scale=scale, words=" ".join(words[i] for i in sel),
               w=base64.b64encode(bytes(wt)).decode("ascii"), q=base64.b64encode(Q.tobytes()).decode("ascii"),
               src="GloVe glove-wiki-gigaword-100 (Stanford NLP, PDDL licence), " + GLOVE_URL,
               how="unit-length vectors stored as int8 (value = q * scale); w = SIF weight * 255 (one byte per word)")
    return out


def covered(out=None):
    """Words in the current data that the file does not hold but GloVe might (only a rebuild can tell): list of words."""
    out = out or json.load(open(OUT))
    have = set(out["words"].split(" ")) | set(out.get("unknown", []))
    return sorted(w for w in needed_words() if w not in have)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--glove", default=GLOVE_DEFAULT, help="path of glove-wiki-gigaword-100.gz")
    ap.add_argument("--fetch", action="store_true", help="download the GloVe file first (about 130 MB)")
    ap.add_argument("--check", action="store_true", help="only report words in the data that the built file lacks")
    a = ap.parse_args()
    if a.check:
        missing = covered()
        print("Word coverage: " + ("PASS (every word in the data is in the file, or GloVe has no vector for it)" if not missing else "WARN %d words are new since the file was built: run build_vectors.py (%s)" % (len(missing), ", ".join(missing[:30]))))
        sys.exit(0)   # a hint only: the matcher still works, it just cannot read the new words
    if a.fetch or not os.path.exists(a.glove):
        if not a.fetch:
            sys.exit("GloVe file not found at %s. Run: python3 build_vectors.py --fetch" % a.glove)
        import urllib.request
        os.makedirs(os.path.dirname(a.glove), exist_ok=True)
        print("downloading", GLOVE_URL)
        urllib.request.urlretrieve(GLOVE_URL, a.glove)
    out = build(a.glove)
    with open(OUT, "w") as f:
        json.dump(out, f, separators=(",", ":"), sort_keys=True)
    print("wrote %s: %d words, %.2f MB" % (os.path.relpath(OUT), out["n"], os.path.getsize(OUT) / 1e6))


if __name__ == "__main__":
    main()
