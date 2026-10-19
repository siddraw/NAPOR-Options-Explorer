"""Walk-forward backtest (no peeking at the future).

For every event in time order, the model is only allowed to use events that came BEFORE it.
  Test 1 - Will there be a reply within ~5 days?  (Trigger Census rows)
  Test 2 - If a reply comes, will it come within 2 days?  (Action-reaction pairs)
Each prediction is scored with the Brier score: (prediction - outcome)^2, averaged.
0 = perfect, 0.25 = what you get by always saying 50%. Lower is better.
We compare against simple baselines so we know whether the model adds anything.
"""
from data import events, pairs, census
import napor_ids as NAPOR
import napor_threads as THREADS
pairs, _ = NAPOR.filter_pairs(pairs)      # same credibility rule as the workbook
census, _ = NAPOR.filter_census(census)
ev_date = {e[0]: e[1] for e in events}

def brier(preds): return sum((p - y) ** 2 for p, y in preds) / len(preds) if preds else float("nan")

def walk_forward_phase(rows):
    """rows: (date, category, outcome, phase). Model = rate within the same war phase, past only."""
    out = []
    for i, (d, cat, y, ph) in enumerate(rows):
        same = [r[2] for r in rows[:i] if r[0] < d and r[3] == ph]
        out.append(((sum(same) + 1) / (len(same) + 2), y))
    return out

def walk_forward(rows, prior_a=1, prior_b=1):
    """rows: list of (date, category, outcome 0/1) sorted by date.
    Model = category rate from earlier rows only, smoothed with a weak 50/50 prior
    (Laplace: (hits+1)/(n+2)) so the first guesses are not 0% or 100%."""
    model, base_all, base_half, log = [], [], [], []
    for i, (d, cat, y) in enumerate(rows):
        past = [r for r in rows[:i] if r[0] < d]                 # strictly earlier dates only
        same = [r[2] for r in past if r[1] == cat]
        p_cat = (sum(same) + prior_a) / (len(same) + prior_a + prior_b)
        p_all = (sum(r[2] for r in past) + 1) / (len(past) + 2)   # baseline: overall rate, ignores category
        model.append((p_cat, y)); base_all.append((p_all, y)); base_half.append((0.5, y))
        log.append((d, cat, len(same), round(p_cat, 2), y))
    return model, base_all, base_half, log

# ---- Test 1: reply or not (counted census rows only; R-weak counted as a reply = 'BEST' scenario)
c_rows = []
for tid, cat, status, note in census:
    if status in ("R-strong", "R-weak", "N"):
        c_rows.append((ev_date[tid], cat, 1 if status != "N" else 0))
c_rows.sort()
m1, a1, h1, log1 = walk_forward(c_rows)
_ph1 = sorted((d, cat, y, THREADS.phase_of(d)) for d, cat, y in c_rows)
p1 = walk_forward_phase(_ph1)

# ---- Test 2: fast (<=2 days) given a reply (pairs; lag from event dates)
p_rows = []
for pid, trig, resp, cat, *_ in pairs:
    lag = (ev_date[resp] - ev_date[trig]).days
    p_rows.append((ev_date[trig], cat, 1 if lag <= 2 else 0))
p_rows.sort()
m2, a2, h2, log2 = walk_forward(p_rows)
_ph2 = sorted((d, cat, y, THREADS.phase_of(d)) for d, cat, y in p_rows)
p2 = walk_forward_phase(_ph2)

def report(name, m, a, h, log, ph=None):
    n = len(m)
    print(f"\n{name}: {n} predictions")
    if ph: print(f"  Phase model (rate in the same war phase, past only): Brier {brier(ph):.3f}   last 6: {brier(ph[-6:]):.3f}")
    print(f"  Our model (rate for that type of act, past only): Brier {brier(m):.3f}   last 6: {brier(m[-6:]):.3f}")
    print(f"  Baseline A (overall rate, ignores type of act):   Brier {brier(a):.3f}   last 6: {brier(a[-6:]):.3f}")
    print(f"  Baseline B (always say 50%):                      Brier {brier(h):.3f}")
    # second half only: once the model has some history
    k = n // 2
    print(f"  Second half only (model has history): model {brier(m[k:]):.3f} vs overall-rate {brier(a[k:]):.3f} vs 50% {brier(h[k:]):.3f}")
    # calibration buckets
    hi = [(p, y) for p, y in m if p >= 0.7]; lo = [(p, y) for p, y in m if p < 0.7]
    if hi: print(f"  When the model said 70%+ ({len(hi)} times): average forecast {sum(p for p,_ in hi)/len(hi):.0%}, actually happened {sum(y for _,y in hi)/len(hi):.0%}")
    if lo: print(f"  When the model said under 70% ({len(lo)} times): average forecast {sum(p for p,_ in lo)/len(lo):.0%}, actually happened {sum(y for _,y in lo)/len(lo):.0%}")
    return log

if __name__ == "__main__":
    l1 = report("TEST 1 - Will a reply come within ~5 days?", m1, a1, h1, log1, p1)
    l2 = report("TEST 2 - If a reply comes, is it within 2 days?", m2, a2, h2, log2, p2)
    print("\nTest 1 detail (date, type, past cases of that type, forecast, outcome):")
    for r in l1: print("  ", r[0], r[1][:18].ljust(18), r[2], r[3], r[4])
