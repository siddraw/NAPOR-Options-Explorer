"""NAPOR theaters: one package per conflict (theaters/<id>/), listed in explorer/theaters.json.

Every theater package has the same thin entry points, which the top-level scripts loop over:
  config.py    - wording, option set, per-option flags, claim-only outlets, adversary test, hold-week rules, constraint periods
  cases.py     - the past cases behind every option (the shape the page uses)
  export.py    - run(): build + write explorer/data/<id>.json (+ history) and run the self-checks; returns a list of problems
  verify.py    - run(): independent recount written to the theater's verify file
  backtest.py  - run_and_report(report): walk-forward backtest, no-hindsight check
`iran` wraps the original modules (data.py, napor_cases.py, ...); `houthis` is built on the shared engine in theaters/engine.py.
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
EXPLORER = os.path.join(HERE, "..", "..", "explorer")
REGISTRY = os.path.join(EXPLORER, "theaters.json")


def build_id():
    """Short git hash of the code the data was built from ("unknown" if git is not available)."""
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=HERE, capture_output=True, text=True, timeout=10, check=True).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def registered():
    """Theater ids in explorer/theaters.json, in tab order."""
    return [t["id"] for t in json.load(open(REGISTRY))["theaters"]]


def register(entry, generated, default="iran"):
    """Add or update one theater's entry in explorer/theaters.json (other entries and fields are kept)."""
    reg = json.load(open(REGISTRY)) if os.path.exists(REGISTRY) else dict(default=default, theaters=[])
    reg["generated"] = generated
    reg.setdefault("default", default)
    for t in reg["theaters"]:
        if t["id"] == entry["id"]:
            t.update(entry)
            break
    else:
        reg["theaters"].append(entry)
    with open(REGISTRY, "w") as f:
        json.dump(reg, f, indent=1)
