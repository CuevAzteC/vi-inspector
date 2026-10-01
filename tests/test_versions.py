"""Version-compatibility smoke test: every fixture VI must review cleanly,
except the documented known limitations (see docs/COMPATIBILITY.md).

To expand the matrix: drop real .vi files saved in a new LabVIEW version
into fixtures/ and update docs/COMPATIBILITY.md with the results.
"""
import glob
import os

import pytest

from vi_inspector.vi import inspect_vi
from vi_inspector.review import review_vi

FIX = os.path.join(os.path.dirname(__file__), "..", "fixtures")

# (relative path, reason) — reviewed as known limitations, not failures.
KNOWN_LIMITATIONS = {
    "clLabview_init.vi": "LV 8.6: block-diagram extraction unsupported",
}


def _all_vis():
    return sorted(
        glob.glob(os.path.join(FIX, "**", "*.vi"), recursive=True))


def test_every_fixture_vi_reviews_or_is_a_known_limitation():
    failures = []
    for fp in _all_vis():
        rel = os.path.relpath(fp, FIX)
        if rel in KNOWN_LIMITATIONS:
            continue
        r = review_vi(fp)
        if not r.parse_ok:
            failures.append(f"{rel}: {r.parse_error}")
    assert not failures, "unexpected review failures:\n" + "\n".join(failures)


def test_known_limitations_still_limited():
    # If one of these starts working, promote it: remove from the dict
    # and update docs/COMPATIBILITY.md.
    for rel in KNOWN_LIMITATIONS:
        r = review_vi(os.path.join(FIX, rel))
        assert not r.parse_ok, f"{rel} now parses — promote it out of known limitations"


def test_version_detection_across_fixtures():
    seen = set()
    for fp in _all_vis():
        v = inspect_vi(fp).get("labview_version", {}).get("display", "?")
        seen.add(v)
    assert seen >= {"21.0", "14.0", "8.6"}, seen
