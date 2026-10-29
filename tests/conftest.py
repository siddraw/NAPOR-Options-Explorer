"""pytest setup: the NAPOR code lives in napor/ and imports its own modules by plain name, so put that folder on sys.path."""
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAPOR = os.path.join(REPO, "napor")
EXPLORER = os.path.join(REPO, "explorer")
if NAPOR not in sys.path:
    sys.path.insert(0, NAPOR)

import theaters  # noqa: E402  (needs napor/ on sys.path)

THEATER_IDS = theaters.registered()          # ids in explorer/theaters.json, in tab order


@pytest.fixture(scope="session")
def repo():
    return REPO


def load_export(tid):
    """The exported page data for one theater (explorer/data/<id>.json), as the page reads it."""
    with open(os.path.join(EXPLORER, "data", tid + ".json")) as f:
        return json.load(f)
