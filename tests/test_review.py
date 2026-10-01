"""Regression tests for vi-inspector review rules.

Each rule test pins behavior verified against genuine LabVIEW-rendered
ground truth (precision audit, 2026-10-01). If a rule change breaks one of
these, the precision assumption behind it needs re-verification — do not
just update the expectation.
"""
import json
import os

import pytest

from vi_inspector.review import review_vi, review_many, SEVERITY_ORDER

FIX = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def vi(*parts):
    return os.path.join(FIX, *parts)


def findings_for(path, rule=None, severity=None):
    r = review_vi(path)
    assert r.parse_ok, f"parse failed for {path}: {r.parse_error}"
    out = r.findings
    if rule:
        out = [f for f in out if f.rule_id == rule]
    if severity:
        out = [f for f in out if f.severity == severity]
    return out


# --- ERR-1: unwired error terminals -------------------------------------------

def test_err1_high_unwired_error_out():
    # Core.vi: the SIM node genuinely bypasses the error wire (ground truth).
    hits = findings_for(vi("vessel", "MB Slave Simulator Base", "Core.vi"),
                        "ERR-1", "high")
    assert any("Simulation.vi" in f.title and "error out" in f.title
               for f in hits)


def test_err1_medium_unwired_error_in_wired_error_out():
    # To JSON Text.vim: error-in unwired, chain otherwise intact -> medium.
    hits = findings_for(vi("vessel", "Launcher", "Config Flatten.vi"),
                        "ERR-1", "medium")
    assert any("To JSON Text.vim" in f.title and "error in" in f.title
               for f in hits)


def test_err1_exempts_error_handlers():
    # Simple Error Handler.vi terminates chains by design: never flagged.
    hits = findings_for(vi("vessel", "Launcher", "Interface.vi"), "ERR-1")
    assert not [f for f in hits
                if "error handler" in (f.node_name or "").lower()]


# --- ERR-1b: broken error chains ----------------------------------------------

def test_err1b_names_invoke_node_method():
    hits = findings_for(vi("vessel", "Launcher", "Interface.vi"),
                        "ERR-1b", "medium")
    assert any("FP.Close" in f.title for f in hits), \
        [f.title for f in hits]


def test_err1b_names_property():
    hits = findings_for(
        vi("vessel", "Launcher", "Dialogs", "Dialog_EditFormulas.vi"),
        "ERR-1b", "medium")
    assert any("Property Node" in f.title and "Value" in f.title
               for f in hits), [f.title for f in hits]


# --- RACE-1 -------------------------------------------------------------------

def test_race1_local_variables():
    hits = findings_for(vi("vessel", "Sim DiscreteIO", "Interface.vi"),
                        "RACE-1", "medium")
    assert hits and "15 local variable(s)" in hits[0].title


# --- dedup --------------------------------------------------------------------

def test_identical_findings_deduped_with_count():
    hits = findings_for(
        vi("vessel", "Launcher", "Dialogs", "Dialog_EditFormulas.vi"), "ERR-1")
    assert any("(×2)" in f.title for f in hits), [f.title for f in hits]


# --- removed rules --------------------------------------------------------------

def test_no_wire1_findings():
    import glob as _glob
    paths = _glob.glob(os.path.join(FIX, "vessel", "**", "*.vi"),
                       recursive=True)
    assert paths, "fixture VIs missing"
    reviews = review_many(paths)
    bad = [f for r in reviews for f in r.findings if f.rule_id == "WIRE-1"]
    assert not bad, f"WIRE-1 was removed: {[f.title for f in bad][:3]}"


# --- invariants -----------------------------------------------------------------

def test_findings_sorted_by_severity():
    r = review_vi(vi("vessel", "Launcher", "Dialogs", "Dialog_EditFormulas.vi"))
    orders = [SEVERITY_ORDER[f.severity] for f in r.findings]
    assert orders == sorted(orders)


def test_active_rule_ids():
    import glob as _glob
    paths = _glob.glob(os.path.join(FIX, "vessel", "**", "*.vi"),
                       recursive=True)
    reviews = review_many(paths)
    seen = {f.rule_id for r in reviews for f in r.findings}
    assert seen <= {"ERR-1", "ERR-1b", "ERR-2", "RACE-1", "CPLX-1"}, seen


# --- CLI: exit codes and baselines -----------------------------------------------

def _main(*argv):
    from vi_inspector.cli import main
    return main(list(argv))


def test_cli_exit_1_on_high(tmp_path):
    rc = _main("review", vi("vessel", "Launcher"), "--fail-on", "high")
    assert rc == 1


def test_cli_exit_0_fail_on_never():
    rc = _main("review", vi("vessel", "Launcher"), "--fail-on", "never")
    assert rc == 0


def test_cli_baseline_roundtrip(tmp_path):
    bl = str(tmp_path / "baseline.json")
    rc = _main("review", vi("vessel", "Launcher"),
               "--update-baseline", bl, "--fail-on", "never")
    assert rc == 0
    data = json.loads(open(bl).read())
    assert data["version"] == 1 and len(data["findings"]) > 0
    # nothing new -> exit 0 even with fail-on high
    rc = _main("review", vi("vessel", "Launcher"),
               "--baseline", bl, "--fail-on", "high")
    assert rc == 0
    # without the baseline the same code fails
    rc = _main("review", vi("vessel", "Launcher"), "--fail-on", "high")
    assert rc == 1


def test_cli_sarif_output(tmp_path):
    sarif = str(tmp_path / "r.sarif")
    rc = _main("review", vi("vessel", "Launcher"), "--sarif", sarif,
               "--fail-on", "never")
    assert rc == 0
    data = json.loads(open(sarif).read())
    assert data["version"] == "2.1.0"
    assert data["runs"][0]["tool"]["driver"]["name"] == "vi-inspector"
    assert len(data["runs"][0]["results"]) > 0
