# Your own option: how accurate is the matcher?

Checked 2026-11-11 against the hand-written answer key `tests/matcher_bench.json` (65 things a viewer might type, each with the
past cases that really are the same kind of US action; written from the case titles, not from the tags).
The key has a **dev** half (used to set the tuning numbers) and a **test** half (never used for tuning). Six queries are
admittedly loose (the key itself says the log has no exact match) and are listed apart.

**v1** is the old key-word reader. **v2** is the word-meaning model plus hard rules (see `docs/METHODOLOGY.md` section 13).

| Queries | Matcher | n | precision@5 | recall@10 | F1 | none-correct |
|---|---|---|---|---|---|---|
| Dev (used for tuning) | v1 key words | 27 | 0.33 | 0.52 | 0.40 | 0.50 |
| Dev (used for tuning) | v2 word meaning | 27 | 0.67 | 0.72 | 0.65 | 1.00 |
| Test (never tuned on) | v1 key words | 29 | 0.32 | 0.48 | 0.41 | 1.00 |
| Test (never tuned on) | v2 word meaning | 29 | 0.66 | 0.66 | 0.58 | 1.00 |
| Loose queries (reported only) | v1 key words | 6 | 0.44 | 0.51 | 0.42 | - |
| Loose queries (reported only) | v2 word meaning | 6 | 0.58 | 0.56 | 0.48 | - |

What the columns mean (all averages over queries; none-correct is only for the queries where the key says the log has
nothing like it: dev 2, test 1):

- **precision@5**: of the first 5 cases returned, the share the key lists. v1 lists cases by date, v2 best-first.
- **recall@10**: the share of the key's cases that are in the first 10 returned.
- **F1**: precision and recall of the whole returned set (v2 returns at most 12 cases; v1 returns every case whose tags fit).
- **none-correct**: the share of "nothing like this in the log" queries where the page returned nothing.

Honest limits: the key lists only 1 to 11 cases per query (most 2 to 4), so the numbers move a lot when a single case is
added or removed. The test half was scored after the tuning numbers were frozen; later edits did not change its score. The model understands words, not whole situations. The key is a person's judgement; a few of its
choices are debatable. Each theater's log is small (27 to 98 cases).

Re-run: `cd napor && python3 bench_matcher.py` (v2 only needs numpy). `python3 bench_matcher.py --v1` re-runs the old matcher in a
headless browser (needs node and playwright) and refreshes `tests/matcher_v1_baseline.json`. The weekly build runs
`python3 bench_matcher.py --check`, which fails if the test half falls below `tests/matcher_floor.json`.
