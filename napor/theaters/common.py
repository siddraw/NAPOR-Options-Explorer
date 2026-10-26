"""NAPOR theaters: the logic every theater shares, so a theater package is mostly config plus events.

A theater package (theaters/<id>/) holds:
  events*.py   the sourced event log (read-only research files)
  config.py    wording, options, per-option flags, claim-only outlets, who is "the other side", hold-week rules,
               constraint periods, plain-language risk lines, analyst notes
  cases.py / export.py / verify.py / backtest.py   a few lines each that call the classes below

The classes here hold the rules (they are the same for every theater):
  Theater   - joins the event files, scores credibility, builds the past cases behind every option (was houthis/cases.py)
  Export    - builds and writes explorer/data/<id>.json (+ history) and runs the self-checks (was houthis/export.py)
  Backtest  - walk-forward backtest of the page's own numbers (was houthis/backtest.py)
  Recount   - an independent recount of every percentage, written to explorer/verify-<id>.json (was houthis/verify.py);
              it does NOT use Theater, so a mistake in the case builder cannot hide

Rules (same meaning as the Iran engine):
  - an event counts only with credibility >= 0.50 (napor_ids.credibility_of: full-text allowed outlet 0.80, two outlets
    0.96, claim-only outlet 0.30; "Partly verified" x 0.8; a row marked not_confirmed is capped at 0.20)
  - option cases for trigger options are the Trigger Census rows with a counted status (R-strong, R-weak, R-proxy, N)
  - non-trigger options use every counted US move with that letter; hold weeks are Mondays with no logged US move
  - windows: reply = config REPLY_DAYS (default 5), hostile act 7 days, economic ECON days (default 7), talks 14 days

Hooks a config may define (all optional; the defaults are the Houthi rules):
  KIND_OF(event)            kind of an event row (Kinetic, Maritime, Diplomatic, Sanctions, Posture, Other); default: data.act_kind + KIND_OVERRIDE
  ATTACK_KINDS              kinds that count as a hostile act when the other side does them
  MILITARY_REPLY(event)     True when a reply counts for the military corner; default: kind is Kinetic
  HOSTILE_TEST(event, kind) rows that add points to the intensity scale; default: any counted Kinetic or Maritime row
  BASELINE_TEST(event, kind) rows the "no new US move" baseline counts (with BASELINE = "attack"); default: the hostile acts (ATTACK_KINDS)
  ECON                      dict(mode="ships" | "events" | "none", days=7, kinds=(...), extra=set()): how the economic corner is measured
  BASELINE                  "ships" (default) or "attack": what the "no new US move" baseline counts
  REPLY_DAYS, THREAD_PREFIX, SANCTIONS_KEY, HOLD_TITLE, RISK_TEXT, LOOKBACKS, PERIOD_KEYS, period()
"""
import datetime as dt
import json
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import data                      # only for act_kind(), the shared word list that sorts an action type into a kind
import napor_ids as N
import napor_intensity as INT    # only for the shared bands and the "someone died" test
import theaters as TH_REG

REPLY = ("R-strong", "R-weak", "R-proxy")
COUNTED = REPLY + ("N",)
CATS = ["people", "escalation", "military", "economic", "political"]
DAY = dt.timedelta(days=1)
ERA = dt.date(2026, 1, 1)
M = 2


def _cfg(C, name, default):
    return getattr(C, name, default)


def econ_of(C):
    e = dict(mode="ships", days=7)
    e.update(_cfg(C, "ECON", {}))
    return e


def explorer_dir():
    return TH_REG.EXPLORER


def theater_dir(C):
    return os.path.dirname(os.path.abspath(sys.modules[C.__name__].__file__))


def wilson(k, n, z=1.96):
    if not n:
        return None
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return max(0.0, c - h), min(1.0, c + h)


def strength(n):
    if n == 0: return "No data"
    if n <= 3: return "Very thin"
    if n <= 7: return "Thin"
    return "OK"


# =====================================================================================================================
class Theater:
    """The event table and the past cases behind every option, in the shape the page uses."""

    REPLY = REPLY
    COUNTED = COUNTED
    CATS = CATS
    INT = INT

    def __init__(self, C, mods):
        self.C = C
        mods = list(mods)
        get = lambda name, default, ms=mods: [getattr(m, name, default) for m in ms]
        # ---- the raw tables, event files joined ----
        self.EVENTS = sorted([e for ev in get("EVENTS", []) for e in ev], key=lambda e: (e[1], e[0]))
        self.EV = {e[0]: e for e in self.EVENTS}
        self.SOURCES, self.VERDICT, self.US_OPTION, self.CHAIN_NAMES = {}, {}, {}, {}
        for m in mods:
            self.SOURCES.update(getattr(m, "SOURCES", {})); self.VERDICT.update(getattr(m, "VERDICT", {}))
            self.US_OPTION.update(getattr(m, "US_OPTION", {})); self.CHAIN_NAMES.update(getattr(m, "CHAIN_NAMES", {}))
        self.PARTLY = set().union(*[set(p) for p in get("PARTLY", set())])
        self.CENSUS_RAW = [c for ms in get("CENSUS", []) for c in ms]
        self.PAIRS_RAW = [p for ms in get("PAIRS", []) for p in ms]
        self.WINDOWS = [w for ms in get("WINDOWS", []) for w in ms]
        self.START_ACTS = set().union(*[set(s) for s in get("START_ACTS", set())])
        self.PHASES = sorted([p for ms in get("PHASES", []) for p in ms], key=lambda p: p[1])
        self.CONSTRAINTS = [c for ms in reversed(get("CONSTRAINTS", None)) for c in (ms or [])] + list(_cfg(C, "CONSTRAINTS", []))
        self.LAST = max(e[1] for e in self.EVENTS)
        self.FIRST = min(e[1] for e in self.EVENTS)
        self.FLAGS = C.FLAGS
        self.CATS = CATS
        self.ECON = econ_of(C)
        self.REPLY_DAYS = _cfg(C, "REPLY_DAYS", 5)
        self.KIND = {e[0]: self._kind(e) for e in self.EVENTS}
        self.CRED = {e[0]: N.credibility_of(self.reports_for(e[0]), self.check_of(e[0])) for e in self.EVENTS}
        self.census = [c for c in self.CENSUS_RAW if self.counts(c[0])]
        self.pairs = [p for p in self.PAIRS_RAW if self.counts(p[1]) and self.counts(p[2])]
        self.dropped = dict(census=[c[0] for c in self.CENSUS_RAW if not self.counts(c[0])], pairs=[p[0] for p in self.PAIRS_RAW if p not in self.pairs])
        self.phase_names = [p[0] for p in self.PHASES]
        # ---- chains (back-and-forth) ----
        self.THREADS = []
        prefix = _cfg(C, "THREAD_PREFIX", "H")
        for n, ids in enumerate(self._chains(), start=1):
            sides = [self._side(i) for i in ids if self._side(i)]
            self.THREADS.append(dict(thread_id=f"{prefix}{n:02d}", name=self.CHAIN_NAMES.get(ids[0], "Unnamed chain"), events=ids, start=self.EV[ids[0]][1], end=self.EV[ids[-1]][1],
                                     days=(self.EV[ids[-1]][1] - self.EV[ids[0]][1]).days, n=len(ids), rounds=sum(1 for x, y in zip(sides, sides[1:]) if x != y),
                                     hostile_acts=sum(1 for i in ids if self.KIND[i] in ("Kinetic", "Maritime"))))
        # ---- war intensity (same points and bands as the Iran page) ----
        self.HOSTILE = [e for e in self.EVENTS if self._hostile(e)]

    # ---- kinds, credibility ----
    def _kind(self, e):
        f = getattr(self.C, "KIND_OF", None)
        if f:
            return f(e)
        return self.C.KIND_OVERRIDE.get(e[0], data.act_kind(e[3], e[5]))

    def reports_for(self, eid):
        C, out = self.C, []
        for s in self.SOURCES.get(eid, []):
            out.append(dict(event_id=eid, outlet_raw=s["outlet"], outlet=N.outlet_name(s["outlet"]),
                            kind=N.source_kind(s["outlet"], C.CLAIM_MEDIA, C.CLAIM_LABEL),
                            headline=s.get("headline", ""), published=s.get("published", ""), url=s.get("url", ""), seen=s.get("seen", "")))
        return out

    def check_of(self, eid):
        if self.VERDICT.get(eid) == "not_confirmed":
            return "Not supported"
        return "Partly verified" if eid in self.PARTLY else "Verified"

    def counts(self, eid):
        return self.CRED.get(eid, 0) >= N.INCLUDE_AT

    # ---- who is who and what counts ----
    def usable(self, e):
        return self.counts(e[0])

    def us_side(self, tid):
        return self.C.us_side(self.EV[tid][2])

    def phase_of(self, day):
        for name, a, b, _ in self.PHASES:
            if a <= day <= b:
                return name
        return "Before the record starts"

    def _window(self, f, day, a, b):
        return [e[0] for e in self.EVENTS if f(e) and day + dt.timedelta(days=a) <= e[1] <= day + dt.timedelta(days=b)]

    def _attack(self, e):
        """A hostile act by the other side (config ATTACK_KINDS). A threat or a declaration is not one unless the config says so."""
        return self.usable(e) and self.C.adversary_side(e[2]) and self.KIND[e[0]] in self.C.ATTACK_KINDS

    def _ship(self, e):
        """The theater's baseline act by the other side (Houthis: an attack on shipping)."""
        C = self.C
        if _cfg(C, "BASELINE", "ships") == "attack":
            f = _cfg(C, "BASELINE_TEST", None)
            return self.usable(e) and f(e, self.KIND[e[0]]) if f else self._attack(e)
        return self.usable(e) and C.adversary_side(e[2]) and (self.KIND[e[0]] == "Maritime" or e[0] in _cfg(C, "SHIP_ATTACK_EXTRA", ()))

    def _econ(self, e):
        """A counted row of the economic measure (mode "ships": an attack on shipping; mode "events": e.g. a counter-sanction)."""
        if self.ECON["mode"] == "events":
            return self.usable(e) and self.C.adversary_side(e[2]) and (self.KIND[e[0]] in self.ECON.get("kinds", ()) or e[0] in self.ECON.get("extra", ()))
        return self._ship(e)

    def _talks(self, e):
        """Same rule as the live Iran rule: any diplomatic event (any side, statements included)."""
        return self.usable(e) and self.KIND[e[0]] == "Diplomatic"

    def is_military_reply(self, eid):
        f = _cfg(self.C, "MILITARY_REPLY", None)
        return f(self.EV[eid]) if f else self.KIND[eid] == "Kinetic"

    def econ_window(self, day):
        """(rows before, rows after, days) of the economic measure for a case on `day`."""
        mode, days = self.ECON["mode"], self.ECON["days"]
        if mode == "none":
            return [], [], days
        before = self._window(self._econ, day, -7, -1) if mode == "ships" else []
        return before, self._window(self._econ, day, 1, days), days

    # ---- chains ----
    def _chains(self):
        EV, links = self.EV, set()
        for e in self.EVENTS:
            if e[6] and e[6] in EV and self.counts(e[0]) and self.counts(e[6]):
                links.add((e[6], e[0]))
        for p in self.pairs:
            links.add((p[1], p[2]))
        par = {}
        def find(x):
            par.setdefault(x, x)
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        for a, b in links:
            par[find(a)] = find(b)
        groups = {}
        for a, b in links:
            groups.setdefault(find(a), set()).update({a, b})
        return sorted((sorted(g, key=lambda i: (EV[i][1], i)) for g in groups.values()), key=lambda ids: (EV[ids[0]][1], ids[0]))

    def _side(self, i):
        a = self.EV[i][2]
        return "Houthis" if self.C.adversary_side(a) else "US" if self.C.us_side(a) else None

    def chain_stats(self):
        mil = [t for t in self.THREADS if t["hostile_acts"] >= 1]
        if not mil:
            return {}
        r = [t["rounds"] for t in mil]
        return dict(chains=len(mil), max_rounds=max(r), share_stopped_after_one_reply=round(sum(1 for x in r if x <= 1) / len(r), 2))

    # ---- intensity ----
    def _hostile(self, e):
        if not self.usable(e):
            return False
        f = _cfg(self.C, "HOSTILE_TEST", None)
        return f(e, self.KIND[e[0]]) if f else self.KIND[e[0]] in ("Kinetic", "Maritime")

    def points_for(self, e):
        return (2 if self.KIND[e[0]] == "Kinetic" else 1) + (2 if INT._deadly(e) else 0)

    def intensity_before(self, day, window=INT.WINDOW_DAYS):
        start = day - dt.timedelta(days=window)
        return sum(self.points_for(e) for e in self.HOSTILE if start <= e[1] < day)

    def baseline_hold(self):
        """Baseline acts per week in the current phase (what happens with no new US move)."""
        start = [p for p in self.PHASES if p[0] == self.phase_of(self.LAST)][-1][1]
        acts = [e for e in self.EVENTS if e[1] >= start and self._ship(e)]
        weeks = max(1, ((self.LAST - start).days + 1) / 7)
        return dict(n=len(acts), weeks=round(weeks, 1), per_week=round(len(acts) / weeks, 1), ids=[e[0] for e in acts])

    # ---- hold weeks (option A) ----
    def _in_window(self, day):
        return any(a <= day <= b for a, b in self.WINDOWS)

    def is_us_move(self, e):
        """A logged move by the US itself of kinds C-H (by its option letter, or by its kind of act)."""
        if not (self.usable(e) and self.C.us_side(e[2])):
            return False
        return self.US_OPTION.get(e[0], "B") in "CDEFGH" or self.KIND[e[0]] in self.C.US_MOVE_KINDS

    def weeks(self, last=None):
        """Every Monday from HOLD_START to 7 days before the latest news, with its verdict."""
        C = self.C
        last = last or self.LAST
        m = C.HOLD_START
        out = []
        while m is not None and m <= last - dt.timedelta(days=7):
            a, b = m, m + dt.timedelta(days=7)
            why = None
            for x, y in self.WINDOWS:
                if not (b < x or a > y):
                    why = f"excluded: continuous fighting {x.isoformat()} to {y.isoformat()}"
            moves = [e[0] for e in self.EVENTS if a <= e[1] <= b and self.is_us_move(e)]
            if not why and moves:
                why = "US move logged: " + ", ".join(f"#{i}" for i in moves)
            if not why and m.isoformat() in C.UNCERTAIN:
                why = "uncertain: " + C.UNCERTAIN[m.isoformat()]
            out.append(dict(monday=m, hold=why is None, why=why, logged=[e[0] for e in self.EVENTS if a <= e[1] <= b]))
            m += dt.timedelta(days=7)
        return out

    def hold_mondays(self, last=None):
        return [w["monday"] for w in self.weeks(last) if w["hold"]]

    def hold_hurt_candidates(self, last=None):
        """For each hold week: the hostile acts in the 7 days after, with their logged damage text (to set PEOPLE_HURT by hand)."""
        return {m.isoformat(): [(i, self.EV[i][5][:60], self.EV[i][7]) for i in self._window(self._attack, m, 1, 7)] for m in self.hold_mondays(last)}

    def missing_flags(self, last=None):
        return [m.isoformat() for m in self.hold_mondays(last) if m.isoformat() not in self.C.PEOPLE_HURT and self._window(self._attack, m, 1, 7)]

    # ---- cases ----
    def ev(self, i):
        e = self.EV[i]
        return dict(id=i, date=e[1].isoformat(), actor=e[2], kind=e[3], title=e[5], cred=round(self.CRED[i], 2))

    def _brief(self, ids):
        EV = self.EV
        return [dict(id=j, date=EV[j][1].isoformat(), title=EV[j][5], actor=EV[j][2], dmg=EV[j][7] or "") for j in ids]

    def _hold_mil(self, st):
        """Hold weeks, military corner: any hostile act in the 7 days after (default) or, if the config defines MILITARY_REPLY, only such a reply."""
        if _cfg(self.C, "MILITARY_REPLY", None):
            return any(self.is_military_reply(i) for i in st)
        return bool(st)

    def hold_cases(self, last):
        C, out = self.C, []
        hold_title = _cfg(C, "HOLD_TITLE", "Week of {mon} {day}: no new US sanctions, naval, strike or posture move logged ({n} event{s} logged that week)")
        for w in self.weeks(last):
            if not w["hold"]:
                continue
            m = w["monday"]; iso = m.isoformat()
            st = self._window(self._attack, m, 1, 7)
            talks = self._window(self._talks, m, 1, 14)
            eb, ea, edays = self.econ_window(m)
            flag = C.PEOPLE_HURT.get(iso) or ((False, [], "No hostile act logged.") if not st else None)
            nlog = len(w["logged"])
            out.append(dict(
                id="W" + iso, week=True, date=iso, actor="US (no new move)", kind="Hold", cred=None,
                title=hold_title.format(mon=m.strftime('%b'), day=m.day, n=nlog, s='' if nlog == 1 else 's'),
                cls=None, replied=None, replies=[], note=None, civ=None,
                strike7=bool(st), mil7=self._hold_mil(st),
                hurt7=(flag[0] if flag else None), hurt_ev=self._brief(flag[1]) if flag else self._brief(st), hurt_note=(flag[2] if flag else "Not set by hand yet."),
                talks14=True if talks else (False if (last - m).days >= 14 else None),
                dmg="", strike_ev=self._brief(st), talk_ev=self._brief(talks),
                ship_b_ev=self._brief(eb), ship_a_ev=self._brief(ea),
                ship_b=len(eb), ship_a=(len(ea) if self.ECON["mode"] != "none" and (last - m).days >= edays else None),
                logged=nlog))
        return out

    def option_ids(self, key):
        """Counted US moves with this option letter (non-trigger options: all of them; trigger options: only those that are Trigger Census cases, below)."""
        return [i for i, k in sorted(self.US_OPTION.items(), key=lambda kv: (self.EV[kv[0]][1], kv[0])) if k == key and self.counts(i) and self.us_side(i)]

    def option_cases(self, key, last=None):
        last = last or self.LAST
        C, EV, KIND, FLAGS = self.C, self.EV, self.KIND, self.FLAGS
        cases = []
        if FLAGS[key]["is_hold"]:
            cases = self.hold_cases(last)
            if len(cases) < C.MIN_HOLD_WEEKS:
                cases = []                         # too few weeks: show "too few cases", do not invent weeks
        elif FLAGS[key]["trigger"]:
            for c in [c for c in self.census if self.us_side(c[0]) and self.US_OPTION.get(c[0]) == key]:
                prs = [p for p in self.pairs if p[1] == c[0]]
                counted = c[2] in COUNTED
                cases.append(dict(**self.ev(c[0]), cls=c[2], replied=(c[2] != "N") if counted else None,
                                  replies=[dict(id=p[2], days=(EV[p[2]][1] - EV[p[1]][1]).days, hurt=p[4] == "Y", kinetic=self.is_military_reply(p[2]),
                                                title=EV[p[2]][5], actor=EV[p[2]][2], date=EV[p[2]][1].isoformat(), dmg=EV[p[2]][7] or "") for p in prs],
                                  note=c[3], civ=C.CIVILIAN_HARM.get(c[0])))
            cases = [c for c in cases if c["cls"] in COUNTED]      # unclear / unverified rows are listed in the census, not counted
        else:
            for i in self.option_ids(key):
                if (last - EV[i][1]).days >= 7:
                    cases.append(dict(**self.ev(i), cls=None, replied=None, replies=[], civ=None, note=None))
        for c in cases:
            if not c.get("week"):
                day = EV[c["id"]][1]
                full7 = (last - day).days >= 7
                eb, ea, edays = self.econ_window(day)
                c["strike7"] = bool(self._window(self._attack, day, 1, 7)) if full7 else None
                talks = bool(self._window(self._talks, day, 1, 14))
                c["talks14"] = True if talks else (False if (last - day).days >= 14 else None)
                c["dmg"] = EV[c["id"]][7] or ""
                c["strike_ev"] = self._brief(self._window(self._attack, day, 1, 7))
                c["talk_ev"] = self._brief(self._window(self._talks, day, 1, 14))
                c["ship_b_ev"] = self._brief(eb)
                c["ship_a_ev"] = self._brief(ea)
                c["ship_b"] = len(c["ship_b_ev"])
                c["ship_a"] = len(c["ship_a_ev"]) if (self.ECON["mode"] != "none" and (last - day).days >= edays) else None
                c["civ"] = c["civ"] if c["id"] in C.CIVILIAN_HARM else None
                c["phase"] = self.phase_of(day)
            else:
                day = dt.date.fromisoformat(c["date"])
                c["phase"] = self.phase_of(day)
            c["pts_at"] = self.intensity_before(day)
            c["band_at"] = INT.band(c["pts_at"])
        cases.sort(key=lambda x: x["date"])
        return cases

    def all_cases(self, last=None):
        last = last or self.LAST
        return {o["key"]: self.option_cases(o["key"], last) for o in self.C.OPTIONS}

    def uses(self):
        """Every counted US move of each kind, including those inside long fights (for "what did the US do next" on past dates)."""
        out = {o["key"]: [] for o in self.C.OPTIONS}
        for e in self.EVENTS:
            k = self.US_OPTION.get(e[0])
            if k in out and self.counts(e[0]) and self.us_side(e[0]):
                out[k].append(dict(id=e[0], date=e[1].isoformat(), title=e[5], unsorted=False))
        return out

    # ---- measured signals and the plain-language risk lines (the page's "What the log says") ----
    def wilson(self, k, n, z=1.96):
        return wilson(k, n, z)

    def strength(self, n):
        return strength(n)

    def option_rows(self, cases_by_key):
        """The same per-option numbers as napor_options.option_rows(), as strings."""
        chain = self.chain_stats()
        longer = 1 - chain["share_stopped_after_one_reply"] if chain else None
        none_shipping = self.ECON["mode"] == "none"
        rows = {}
        for o in self.C.OPTIONS:
            k = o["key"]; fl = self.FLAGS[k]; cs = cases_by_key[k]
            row = dict(key=k, n=len(cs))
            if fl["trigger"]:
                counted = [c for c in cs if c["replied"] is not None]
                kk, n = sum(1 for c in counted if c["replied"]), len(counted)
                ci = wilson(kk, n)
                row["reply"] = f"{kk} of {n} ({kk / n:.0%})" if n else "No past cases"
                row["reply_range"] = f"{ci[0]:.0%}-{ci[1]:.0%}" if ci else ""
                reps = [r for c in cs for r in c["replies"]]
                row["fast"] = f"{sum(1 for r in reps if r['days'] <= 2)} of {len(reps)}" if reps else "No past replies to measure"
                row["casualties"] = f"{sum(1 for r in reps if r['hurt'])} of {len(reps)}" if reps else "No past replies to measure"
                row["longer"] = f"~{longer:.0%} (all chains, n={chain['chains']})" if longer is not None and kk else "No past replies"
                row["phase_note"] = ""
            else:
                row.update(reply="Not measured", reply_range="", fast="Not measured", casualties="Not measured", longer="", phase_note="")
            out = [c for c in cs if not c.get("week")]
            if out:
                done = [c for c in out if c['ship_a'] is not None]
                if none_shipping:
                    shipping = "not measured"
                elif self.ECON["mode"] == "events":
                    shipping = f"{sum(1 for c in done if c['ship_a'] > c['ship_b'])} of {len(done)}"
                else:
                    shipping = f"{sum(c['ship_b'] for c in done)} -> {sum(c['ship_a'] for c in done)}"
                row["signals"] = dict(
                    n=len(out),
                    strikes_after=f"{sum(1 for c in out if c['strike7'])} of {sum(1 for c in out if c['strike7'] is not None)}",
                    shipping=shipping,
                    talks=f"{sum(1 for c in out if c['talks14'])} of {sum(1 for c in out if c['talks14'] is not None)}")
            else:
                row["signals"] = dict(n=0)
            rows[k] = row
        return rows

    def risk_lines(self, key, cases_by_key, rows):
        """Five plain-language lines (one per category) plus the evidence strength, from the measured numbers only."""
        C = self.C
        r, fl, cs = rows[key], self.FLAGS[key], cases_by_key[key]
        m = r["signals"]; bl = self.baseline_hold(); T = C.RISK_TEXT
        reps = [x for c in cs for x in c["replies"]]
        hurt = [x for x in reps if x["hurt"]]
        L5 = []
        if fl["trigger"] and cs:
            L5.append(T["people_trigger"].format(hurt=len(hurt), n=len(reps), detail=(": " + "; ".join(f"#{x['id']} {x['dmg'][:70]}" for x in hurt)) if hurt else ""))
        elif fl["is_hold"]:
            L5.append(T["people_hold"].format(per_week=bl["per_week"]))
        elif key == _cfg(C, "SANCTIONS_KEY", "C"):
            L5.append(T["people_sanctions"])
        else:
            L5.append(T["people_other"])
        if fl["trigger"] and cs:
            L5.append(T["esc_trigger"].format(reply=r["reply"], range=r["reply_range"] or "-", fast=r["fast"], longer=r["longer"]))
        elif fl["is_hold"]:
            L5.append(T["esc_hold"])
        elif m.get("n"):
            L5.append(T["esc_timing"].format(strikes=m["strikes_after"]))
        else:
            L5.append(T["no_cases"])
        if fl["military"] == "reply" and cs:
            k_ = sum(1 for c in cs if any(x["kinetic"] for x in c["replies"]))
            L5.append(T["mil_reply"].format(k=k_, n=len(cs)))
        elif fl["military"] == "strike":
            L5.append(T["mil_strike"])
        else:
            L5.append(T["mil_none"])
        if m.get("n"):
            L5.append(T["eco_cases"].format(shipping=m["shipping"]))
        else:
            L5.append(T["eco_baseline"].format(per_week=bl["per_week"]))
        if m.get("n"):
            L5.append(T["pol_cases"].format(talks=m["talks"]))
        else:
            L5.append(T["pol_none"])
        ev_str = strength(r["n"]) if fl["trigger"] else (f"{r['n']} hold weeks" if fl["is_hold"] else (f"{m['n']} past cases (timing only)" if m.get("n") else "No data"))
        return L5, ev_str

    def public(self):
        return {k: getattr(self, k) for k in dir(self) if not k.startswith("__")}


# =====================================================================================================================
class Backtest:
    """Walk-forward backtest of the page's own numbers (same method and decision rules as backtest_risk.py)."""

    def __init__(self, C, K):
        import backtest_risk as BR
        self.C, self.K, self.BR = C, K, BR
        self.JSON_FILE = os.path.join(theater_dir(C), "backtest_risk.json")

    def _robustness(self):
        """Escalation (reply) rate per trigger option under rule variants, from the theater census (same variants as Iran)."""
        K, C = self.K, self.C
        rd = K.REPLY_DAYS
        variants = [
            (f"As published (R-strong, R-weak, R-proxy count; ~{rd} days)", lambda st, lags: st in K.REPLY),
            ("Proxy replies do not count", lambda st, lags: st in ("R-strong", "R-weak")),
            ("Weak replies do not count", lambda st, lags: st in ("R-strong", "R-proxy")),
            ("Only strong replies count", lambda st, lags: st == "R-strong"),
            ("Reply within 3 days (logged reply dates)", lambda st, lags: st in K.REPLY and any(x <= 3 for x in lags)),
        ]
        out = []
        for o in C.OPTIONS:
            k = o["key"]
            if not C.FLAGS[k]["trigger"]:
                continue
            rows = [c for c in K.census if K.us_side(c[0]) and K.US_OPTION.get(c[0]) == k and c[2] in K.COUNTED]
            res = dict(key=k, name=o["name"], cells=[])
            for label, f in variants:
                kk = n = 0
                for tid, _, st, _ in rows:
                    lags = [(K.EV[p[2]][1] - K.EV[tid][1]).days for p in K.pairs if p[1] == tid]
                    if "3 days" in label and st in K.REPLY and not lags:
                        continue
                    n += 1
                    kk += 1 if f(st, lags) else 0
                res["cells"].append(dict(variant=label, k=kk, n=n))
            out.append(res)
        return dict(variants=[v[0] for v in variants], short=["As published", "No proxy", "No weak", "Strong only", "Within 3 days"], rows=out)

    def _talk_dates(self, words):
        K = self.K
        return [e[1] for e in K.EVENTS if K._talks(e) and (words is None or any(w in e[3].lower() for w in words))]

    def context(self):
        K, C = self.K, self.C
        return types.SimpleNamespace(flags=C.FLAGS, last=K.LAST, talk_dates=self._talk_dates, robustness=self._robustness,
                                     periods=(C.PERIOD_KEYS, C.period), oos_cut=C.OOS_CUT, oos_label=C.OOS_LABEL)

    def run(self, cb=None):
        cb = cb or self.K.all_cases()
        return self.BR.run(cb, self.context()), cb

    def run_and_report(self, report):
        res, cb = self.run()
        json.dump(res, open(self.JSON_FILE, "w"), indent=1, default=str)
        report(res, cb, self.C.FLAGS)
        return res

    def weighting_in_force(self):
        try:
            d = json.load(open(self.JSON_FILE))["weighting"]["decision"]
            return d["scheme"], d["param"]
        except Exception:                                  # noqa: BLE001
            return "none", None


# =====================================================================================================================
class Export:
    """Build and write everything the page needs for one theater tab, and run the self-checks.

    Writes explorer/data/<id>.json, explorer/data/<id>-history.json and this theater's entry in explorer/theaters.json."""

    def __init__(self, C, K, BT):
        import export_explorer as X          # shared helpers: risk_index, pooled_rates, check, wilson (no Iran data is read here)
        import backtest_risk as BR
        self.C, self.K, self.BT, self.X, self.BR = C, K, BT, X, BR
        self.EXPLORER = TH_REG.EXPLORER
        self.DATA_FILE = os.path.join(self.EXPLORER, "data", C.THEATER_ID + ".json")
        self.HISTORY_FILE = os.path.join(self.EXPLORER, "data", C.THEATER_ID + "-history.json")
        self.HERE = theater_dir(C)

    def sources_for(self, ids):
        """Outlet links and credibility for every event the page mentions (claim-only media marked as claims)."""
        K, out = self.K, {}
        for i in sorted(ids):
            if i not in K.EV:
                continue
            seen, links = set(), []
            for r in K.reports_for(i):
                if not r["url"] or r["outlet"] in seen:
                    continue
                seen.add(r["outlet"])
                links.append(dict(o=r["outlet"], u=r["url"], claim=r["kind"].endswith("(claim only)")))
            out[str(i)] = dict(cred=K.CRED[i], links=links)
        return out

    def context_periods(self):
        """Constraint periods from the research file / config, in the shape the page reads (notes per option letter)."""
        K, C, out = self.K, self.C, []
        for n, (a, b, text, ids) in enumerate(sorted(K.CONSTRAINTS, key=lambda c: c[0])):
            label = text.split(":")[0][:70]
            notes = getattr(C, "CONSTRAINT_NOTES", {}).get(a.isoformat()) or {k: text for k in C.CONSTRAINT_OPTIONS}
            out.append(dict(key=f"c{n}", label=label, start=a.isoformat(), start_event=ids[0] if ids else None,
                            end=(b.isoformat() if b < K.LAST else None), end_event=None, notes=notes))
        return out

    def build(self):
        K, C, BT, BR, X = self.K, self.C, self.BT, self.BR, self.X
        cb = K.all_cases()
        rows = K.option_rows(cb)
        uses = K.uses()
        chain = K.chain_stats() or {}
        series, d = [], K.FIRST
        while d <= K.LAST:
            series.append([d.isoformat(), K.intensity_before(d + dt.timedelta(days=1))])
            d += dt.timedelta(days=1)
        cur = series[-1][1]
        peak = max(p for _, p in series)
        from napor_intensity import BANDS, band
        out = dict(
            theater=C.THEATER, asof=K.LAST.isoformat(), generated=dt.date.today().isoformat(), phase=K.phase_of(K.LAST),
            intensity=dict(pts=cur, band=band(cur), bands=[[lo, nm] for lo, nm in BANDS], peak=peak,
                           share_days_below=round(sum(1 for _, p in series if p < cur) / len(series), 3), window_days=14),
            series=series,
            hostile=[dict(id=e[0], date=e[1].isoformat(), actor=e[2], kind=K.KIND[e[0]], pts=K.points_for(e), deadly=bool(K.INT._deadly(e)), title=e[5]) for e in K.HOSTILE],
            phases=[dict(name=p[0], start=p[1].isoformat(), end=min(p[2], K.LAST).isoformat()) for p in K.PHASES if p[1] <= K.LAST],
            baseline=K.baseline_hold(), n_events=len([e for e in K.EVENTS if K.counts(e[0])]),
            chain=dict(n=chain.get("chains"), longer=round(1 - chain["share_stopped_after_one_reply"], 3) if chain else None),
            options=[])
        out["week_events"] = [K.ev(e[0]) | dict(actor=e[2]) for e in K.EVENTS if (K.LAST - e[1]).days <= 6 and K.counts(e[0])]
        now_file = os.path.join(self.HERE, C.NOW_FILE)
        out["now"] = json.load(open(now_file)) if os.path.exists(now_file) else None
        for o in C.OPTIONS:
            k = o["key"]; r = rows[k]; fl = C.FLAGS[k]; m = r["signals"]
            lines, evid = K.risk_lines(k, cb, rows)
            cases = cb[k]
            opt = dict(
                key=k, name=o["name"], what=o["what"], evidence=evid, **fl,
                official=dict(reply=r["reply"], fast=r["fast"], casualties=r["casualties"], strikes=m.get("strikes_after"), talks=m.get("talks"), shipping=m.get("shipping")),
                cases=cases, risks=lines, pros=C.PROS[k], harms=C.HARMS[k], unknown=C.UNKNOWNS[k], forecasts=[], uses=uses[k])
            if C.MIN_CASES:
                opt["too_few"] = len(cases) < C.MIN_CASES        # the page shows "too few cases" instead of a risk index
            opt["last_used"] = max([c["date"] for c in cases if not c.get("week")] + [u["date"] for u in uses[k]], default=None)
            out["options"].append(opt)
        out["context"] = self.context_periods()
        bt, _ = BT.run(cb)
        json.dump(bt, open(BT.JSON_FILE, "w"), indent=1, default=str)
        out["report_card"] = dict(forecasts=[], backtest=bt, political_proposal=bt["political_proposal"])
        dw = bt["weighting"]["decision"]
        out["estimate"] = dict(shrink=bt["decision"]["adopt"], m=BR.M_MAIN,
                               weighting=dict(scheme=dw["scheme"], param=dw["param"], name=dw["name"], adopt=dw["adopt"], best_candidate=dw["best_candidate"],
                                              gain=dw["gain"], worse_by_cat=dw["worse_by_cat"], rule=dw["rule"]))
        ids = set()
        for o in out["options"]:
            for c in o["cases"]:
                if not c.get("week"):
                    ids.add(c["id"])
                for key in ("replies", "strike_ev", "talk_ev", "ship_a_ev", "ship_b_ev", "hurt_ev"):
                    ids.update(x["id"] for x in c.get(key) or [])
            ids.update(u["id"] for u in o["uses"])
        ids.update(e["id"] for e in out["week_events"])
        out["sources"] = self.sources_for(ids)
        out["history"] = self.update_history(out)
        return out

    def update_history(self, out):
        X = self.X
        hist = json.load(open(self.HISTORY_FILE)) if os.path.exists(self.HISTORY_FILE) else []
        W, T = X.weighting_of(out), dt.date.fromisoformat(out["asof"])
        pool = X.pooled_rates(out["options"], W, T)
        snap = dict(asof=out["asof"], intensity=out["intensity"]["pts"], band=out["intensity"]["band"], events=out["n_events"],
                    options={o["key"]: dict(n=len(o["cases"]), index=X.risk_index(o, o["cases"]),
                                            estimate=X.risk_index(o, o["cases"], pool=pool, weighting=W, T=T) if out["estimate"]["shrink"] else None) for o in out["options"]},
                    status={k: dict(status=v["status"], label=v["label"]) for k, v in ((out.get("now") or {}).get("options") or {}).items()},
                    status_as_of=(out.get("now") or {}).get("as_of"))
        hist = [h for h in hist if h["asof"] != snap["asof"]] + [snap]
        hist.sort(key=lambda h: h["asof"])
        return hist[-60:]

    def write(self, out):
        C = self.C
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
        with open(self.DATA_FILE, "w") as f:
            f.write(json.dumps(out, separators=(",", ":"), default=str))
        with open(self.HISTORY_FILE, "w") as f:
            json.dump(out["history"], f, indent=1)
        TH_REG.register(dict(id=C.THEATER_ID, name=C.THEATER["name"], status=C.THEATER["status"], data="data/" + C.THEATER_ID + ".json", asof=out["asof"]), out["generated"])

    def recount_diff(self, out, recount):
        """Compare [k, n, sum_wy, sum_w] per option and category with the independent recount (tolerance 1e-9)."""
        X = self.X
        W, T = X.weighting_of(out), dt.date.fromisoformat(out["asof"])
        ver, diff = recount(weighting=W, asof=T), []
        for o in out["options"]:
            if not o["cases"]:
                continue
            sc = X.category_scores(o, o["cases"], W, T)
            for c in X.CATS:
                if sc[c].get("assumed"):
                    continue
                mine = [sc[c]["k"], sc[c]["n"], sc[c]["swy"], sc[c]["sw"]]
                theirs = ver[o["key"]][c]
                if any(abs(a - b) > 1e-9 for a, b in zip(mine, theirs)):
                    diff.append((o["key"], c, mine, theirs))
        return diff

    def run(self, recount):
        """Build, write and self-check the theater. Returns the list of problems (empty = PASS)."""
        X, C, K = self.X, self.C, self.K
        out = self.build()
        bad = [b for b in X.check(out) if b[2] != (0, 0)]       # an option with no counted cases says "No past cases", which has no x of n to compare
        self.write(out)
        print("wrote", os.path.normpath(self.DATA_FILE), "(+ history, theaters.json) | asof", out["asof"], "| intensity", out["intensity"]["pts"], out["intensity"]["band"])
        print("MISMATCH vs workbook counts:" if bad else "page counts match the log's own counts", bad or "")
        diff = self.recount_diff(out, recount)
        print("MISMATCH vs independent recount:" if diff else "risk rates match the independent recount", diff or "")
        print("cases per option:", {o["key"]: len(o["cases"]) for o in out["options"]}, "| too few cases:", [o["key"] for o in out["options"] if o.get("too_few")])
        return bad + diff


# =====================================================================================================================
class Recount:
    """Independent recount of every percentage the page shows for one theater tab.

    Recomputes each option's five risk-category numbers straight from the research files and config WITHOUT using Theater,
    Export or Backtest (so a mistake in the case builder cannot hide). Writes explorer/verify-<id>.json; the Node page test
    compares it with what the page computes in the browser, at the as-of date and at look-back dates.

    Per option and category it records [k, n, sum_wy, sum_w]: k of n are the plain counts; sum_w is the sum of the recency
    weights of the counted cases and sum_wy the same sum over the cases that count as risk (weights as in verify_explorer.py).
    Estimate = (sum_wy + 2 x pooled) / (sum_w + 2) when the written decision rule adopted it, else the plain k / n."""

    def __init__(self, C, mods):
        self.C = C
        mods = list(mods)
        self.OUT = os.path.join(explorer_dir(), "verify-" + C.THEATER_ID + ".json")
        self.BT_JSON = os.path.join(theater_dir(C), "backtest_risk.json")
        self.EVL = sorted([e for m in mods for e in m.EVENTS], key=lambda e: (e[1], e[0]))
        self.EV = {e[0]: e for e in self.EVL}
        self.SRC, self.VERD, self.OPT = {}, {}, {}
        for m in mods:
            self.SRC.update(getattr(m, "SOURCES", {})); self.VERD.update(getattr(m, "VERDICT", {})); self.OPT.update(getattr(m, "US_OPTION", {}))
        self.PARTLY = set().union(*[set(getattr(m, "PARTLY", set())) for m in mods])
        self.WINDOWS = [w for m in mods for w in getattr(m, "WINDOWS", [])]
        self.LAST = max(e[1] for e in self.EVL)
        self.ECON = econ_of(C)
        self.RD = _cfg(C, "REPLY_DAYS", 5)
        self.GOOD = {e[0] for e in self.EVL if self.cred(e[0]) >= 0.5}
        self.CENSUS = [c for m in mods for c in getattr(m, "CENSUS", []) if c[0] in self.GOOD and self.EV[c[0]][2].lower().startswith("us")]
        self.PAIRS = [p for m in mods for p in getattr(m, "PAIRS", []) if p[1] in self.GOOD and p[2] in self.GOOD]

    def kind(self, i):
        f = _cfg(self.C, "KIND_OF", None)
        if f:
            return f(self.EV[i])
        return self.C.KIND_OVERRIDE.get(i) or data.act_kind(self.EV[i][3], self.EV[i][5])

    def cred(self, i):
        C = self.C
        reps = [dict(outlet=N.outlet_name(s["outlet"]), kind=N.source_kind(s["outlet"], C.CLAIM_MEDIA, C.CLAIM_LABEL), seen=s.get("seen", "")) for s in self.SRC.get(i, [])]
        chk = "Not supported" if self.VERD.get(i) == "not_confirmed" else ("Partly verified" if i in self.PARTLY else "Verified")
        return N.credibility_of(reps, chk)

    def weighting_in_force(self):
        try:
            d = json.load(open(self.BT_JSON))
            return (d["weighting"]["decision"]["scheme"], d["weighting"]["decision"]["param"]), bool(d["decision"]["adopt"])
        except Exception:                                  # noqa: BLE001
            return ("none", None), False

    @staticmethod
    def weight(scheme, param, asof, day):
        if scheme == "none":
            return 1.0
        if scheme == "era":
            return float(param) if day < ERA else 1.0
        if scheme == "halflife":
            return 0.5 ** ((asof - day).days / param)
        raise ValueError(scheme)

    @staticmethod
    def add(acc, w, risk):
        acc[1] += 1; acc[3] += w
        if risk:
            acc[0] += 1; acc[2] += w

    def hold_mondays(self):
        """Mondays from HOLD_START whose week (Monday to the next Monday) is outside the fighting windows and has no US move of kinds C-H."""
        C, EV, EVL, GOOD, OPT = self.C, self.EV, self.EVL, self.GOOD, self.OPT
        out, m = [], C.HOLD_START
        while m is not None and m <= self.LAST - 7 * DAY:
            a, b = m, m + 7 * DAY
            skip = any(not (b < x or a > y) for x, y in self.WINDOWS) or m.isoformat() in C.UNCERTAIN
            skip = skip or any(a <= e[1] <= b and e[0] in GOOD and EV[e[0]][2].lower().startswith("us")
                               and (OPT.get(e[0], "B") in "CDEFGH" or self.kind(e[0]) in C.US_MOVE_KINDS) for e in EVL)
            if not skip:
                out.append(m)
            m += 7 * DAY
        return out

    def recount(self, weighting=None, asof=None):
        """Numbers as they looked on `asof` (default: the latest news): only cases dated on or before it, only events logged by it.
        A window that has not finished by then counts only once the answer is already "yes" (a reply, an attack, talks), as the page does."""
        C, EV, EVL, GOOD, OPT, LAST = self.C, self.EV, self.EVL, self.GOOD, self.OPT, self.LAST
        (scheme, param) = weighting or self.weighting_in_force()[0]
        T = dt.date.fromisoformat(asof) if isinstance(asof, str) else (asof or LAST)
        known = [e for e in EVL if e[1] <= T and e[0] in GOOD]
        usd = lambda i: EV[i][2].lower().startswith("us")
        hou = lambda i: C.adversary_side(EV[i][2])
        def win(day, a, b, test):
            return [e for e in known if day + a * DAY <= e[1] <= day + b * DAY and test(e[0])]
        attack = lambda i: hou(i) and self.kind(i) in C.ATTACK_KINDS
        ship = lambda i: hou(i) and (self.kind(i) == "Maritime" or i in _cfg(C, "SHIP_ATTACK_EXTRA", ()))
        econ_events = lambda i: hou(i) and (self.kind(i) in self.ECON.get("kinds", ()) or i in self.ECON.get("extra", ()))
        talk = lambda i: self.kind(i) == "Diplomatic"
        mil = _cfg(C, "MILITARY_REPLY", None)
        is_mil = (lambda i: bool(mil(EV[i]))) if mil else (lambda i: self.kind(i) == "Kinetic")
        done = lambda day, n: day + n * DAY <= T
        strike7 = lambda day: True if win(day, 1, 7, attack) else (False if done(day, 7) else None)
        talks14 = lambda day: True if win(day, 1, 14, talk) else (False if done(day, 14) else None)
        mode, edays = self.ECON["mode"], self.ECON["days"]
        new = lambda: [[0, 0, 0.0, 0.0] for _ in range(5)]
        out = {}
        for o in C.OPTIONS:
            k = o["key"]; fl = C.FLAGS[k]
            ppl, esc, mil_, eco, pol = new()
            if fl["is_hold"]:
                rows = [("W", m) for m in self.hold_mondays() if m <= T]
            elif fl["trigger"]:
                rows = [(c[0], EV[c[0]][1]) for c in self.CENSUS if OPT.get(c[0]) == k and c[2] in COUNTED]
            else:
                rows = [(i, EV[i][1]) for i in sorted(GOOD) if OPT.get(i) == k and usd(i) and (LAST - EV[i][1]).days >= 7]
            rows = [(i, day) for i, day in rows if day <= T]
            for tid, day in rows:
                w = self.weight(scheme, param, T, day)
                s7 = strike7(day)
                if fl["is_hold"]:
                    if s7 is not None:
                        self.add(esc, w, s7)
                        hm = s7 if not mil else (True if win(day, 1, 7, lambda i: attack(i) and is_mil(i)) else (False if done(day, 7) else None))
                        self.add(mil_, w, hm)
                    flag = C.PEOPLE_HURT.get(day.isoformat()) or ((False, [], "") if not [e for e in EVL if e[0] in GOOD and day + DAY <= e[1] <= day + 7 * DAY and attack(e[0])] else None)
                    if done(day, 7) and flag is not None:
                        self.add(ppl, w, bool(flag[0]))
                else:
                    prs = [p for p in self.PAIRS if p[1] == tid and EV[p[2]][1] <= T]
                    if s7 is not None:
                        self.add(ppl, w, (tid in _cfg(C, "CIVILIAN_HARM", {})) or any(p[4] == "Y" for p in prs))
                    if fl["trigger"]:
                        st = [c[2] for c in self.CENSUS if c[0] == tid][0]
                        rep = (st in REPLY) if done(day, self.RD) else (True if prs else None)
                        if rep is not None:
                            self.add(esc, w, rep)
                            if fl["military"] == "reply":
                                self.add(mil_, w, any(is_mil(p[2]) for p in prs))
                    elif s7 is not None:
                        self.add(esc, w, s7)
                if mode == "ships":
                    if done(day, edays):
                        self.add(eco, w, len(win(day, 1, edays, ship)) > len(win(day, -7, -1, ship)))
                elif mode == "events":
                    if done(day, edays):
                        self.add(eco, w, len(win(day, 1, edays, econ_events)) > 0)
                t14 = talks14(day)
                if t14 is not None:
                    self.add(pol, w, t14 is False)
            out[k] = dict(people=ppl, escalation=esc, military=mil_, economic=eco, political=pol, n=len(rows))
        return out

    def estimates(self, out, shrink):
        C = self.C
        opts = list(out)
        assumed = lambda k, c: c == "military" and C.FLAGS[k]["military"] == "none"
        pool = {}
        for c in CATS:
            swy = sum(out[k][c][2] for k in opts if not assumed(k, c))
            sw = sum(out[k][c][3] for k in opts if not assumed(k, c))
            pool[c] = swy / sw if sw else None
        est = {}
        for k in opts:
            est[k] = {}
            for c in CATS:
                a = out[k][c]
                if assumed(k, c):
                    est[k][c] = 0.0
                elif not a[1]:
                    est[k][c] = None
                else:
                    est[k][c] = (a[2] + M * pool[c]) / (a[3] + M) if (shrink and pool[c] is not None) else a[0] / a[1]
        return est, pool

    def run(self):
        C = self.C
        (scheme, param), shrink = self.weighting_in_force()
        rc = self.recount((scheme, param), self.LAST)
        est, pool = self.estimates(rc, shrink)
        for k in rc:
            rc[k]["estimate"] = est[k]
        lbs = {}
        for iso in C.LOOKBACKS:
            r = self.recount((scheme, param), iso)
            e, pl = self.estimates(r, shrink)
            for k in r:
                r[k]["estimate"] = e[k]
            lbs[iso] = dict(asof=iso, pooled=pl, options=r)
        out = dict(asof=self.LAST.isoformat(), weighting=dict(scheme=scheme, param=param), shrink=shrink, m=M, pooled=pool, options=rc, lookbacks=lbs)
        json.dump(out, open(self.OUT, "w"), indent=1)
        print(f"as of {self.LAST} | recency weighting: {scheme} {param if param is not None else ''} | estimate shrunk: {shrink}".rstrip())
        for k, v in rc.items():
            print(k, {c: [v[c][0], v[c][1], round(v[c][2], 4), round(v[c][3], 4)] for c in CATS}, "n", v["n"])
        return []
