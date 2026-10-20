"""Independent recount of every percentage the Options Explorer shows.

Recomputes each option's five risk-category rates straight from data.py (census, pairs, events),
without using export_explorer.py, and writes them to explorer/verify.json. The page test compares
these with what the page computes in the browser. Run: python3 verify_explorer.py
"""
import json, os, datetime as dt
import data, napor_options as O

HERE = os.path.dirname(os.path.abspath(__file__))
EV = {e[0]: e for e in data.events}
LAST = max(e[1] for e in data.events)
REPLY = ("R-strong", "R-weak", "R-proxy"); COUNTED = REPLY + ("N",)


def within(day, a, b, test):
    return any(test(e) for e in data.events if day + dt.timedelta(days=a) <= e[1] <= day + dt.timedelta(days=b))


def recount():
  out = {}
  for o in O.OPTIONS:
      k = o["key"]
      if o["match"]:
          rows = [c for c in data.census if O.us_side(c[0]) and o["match"](c[0])]
      elif k in ("B", "H"):
          rows = [(i, None, None, None) for i in O.option_cases(k)]
      else:
          rows = []
      ppl = esc = mil = eco = pol = [0, 0]
      ppl, esc, mil, eco, pol = [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]
      for tid, _, st, _ in rows:
          day = EV[tid][1]; full7 = (LAST - day).days >= 7
          prs = [p for p in data.pairs if p[1] == tid]
          if full7:
              ppl[1] += 1; ppl[0] += (tid in O.CIVILIAN_HARM) or any(p[4] == "Y" for p in prs)
          if o["match"] and k in ("C", "D", "E", "F", "G"):
              if st in COUNTED:
                  esc[1] += 1; esc[0] += st in REPLY
                  if k in ("D", "E", "F", "G"):
                      mil[1] += 1; mil[0] += any(data.event_kind[p[2]] == "Kinetic" for p in prs)
          elif full7:
              esc[1] += 1; esc[0] += within(day, 1, 7, O._irstrike)
          if full7:
              b = sum(1 for e in data.events if O._ship(e) and day - dt.timedelta(days=7) <= e[1] <= day - dt.timedelta(days=1))
              a = sum(1 for e in data.events if O._ship(e) and day + dt.timedelta(days=1) <= e[1] <= day + dt.timedelta(days=7))
              eco[1] += 1; eco[0] += a > b
          talks = within(day, 1, 14, O._talks)
          if talks or (LAST - day).days >= 14:
              pol[1] += 1; pol[0] += not talks
      out[k] = dict(people=ppl, escalation=esc, military=mil, economic=eco, political=pol, n=len(rows))
  return out


if __name__ == "__main__":
    out = recount()
    json.dump(out, open(os.path.join(HERE, "..", "explorer", "verify.json"), "w"), indent=1)
    for k, v in out.items():
        print(k, v)
