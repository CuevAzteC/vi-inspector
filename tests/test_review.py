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


# --- WIRE-1: unwired REQUIRED inputs (precision rebuild) ----------------------
# The 2026-10-01 audit removed WIRE-1 (0/6 samples actionable). The rebuilt
# rule only fires on REQUIRED connector-pane inputs, resolved cross-VI.

from types import SimpleNamespace

from vi_inspector.review import (
    ReviewContext,
    _rule_unwired_required_inputs,
    VIReview,
)


def _wire1_pvi(wired_uids=(), term_index=5, is_output=False,
               node_type="iUse", node_name="Callee.vi"):
    node = SimpleNamespace(uid="n1", node_type=node_type, name=node_name,
                           label=None)
    term = SimpleNamespace(uid="t1", parent_uid="n1", index=term_index,
                           is_output=is_output)
    wires = [SimpleNamespace(from_term=u, to_term="x") for u in wired_uids]
    bd = SimpleNamespace(nodes=[node], terminal_info={"t1": term},
                         wires=wires)
    return SimpleNamespace(block_diagram=bd)


def _wire1_ctx(rules=None, labels=None):
    ctx = SimpleNamespace()
    ctx.callee_interface = lambda caller, name: (
        ("/some/Callee.vi", rules if rules is not None else {5: 1},
         labels if labels is not None else {5: "my input"})
    )
    return ctx


def _run_wire1(pvi, ctx):
    review = VIReview(vi_path="/some/Caller.vi", vi_name="Caller.vi")
    _rule_unwired_required_inputs(pvi, review, ctx)
    return [f for f in review.findings if f.rule_id == "WIRE-1"]


def test_wire1_fires_on_unwired_required_input():
    hits = _run_wire1(_wire1_pvi(), _wire1_ctx())
    assert len(hits) == 1
    assert hits[0].severity == "high"
    assert "my input" in hits[0].title and "Callee.vi" in hits[0].title


def test_wire1_ignores_wired_required_input():
    hits = _run_wire1(_wire1_pvi(wired_uids=("t1",)), _wire1_ctx())
    assert hits == []


def test_wire1_ignores_recommended_and_optional():
    pvi = _wire1_pvi()
    hits = _run_wire1(pvi, _wire1_ctx(rules={5: 2}, labels={5: "rec"}))
    assert hits == []
    hits = _run_wire1(pvi, _wire1_ctx(rules={5: 3}, labels={5: "opt"}))
    assert hits == []


def test_wire1_ignores_outputs():
    # Required on an output is meaningless in LabVIEW (can't compel caller).
    hits = _run_wire1(_wire1_pvi(is_output=True), _wire1_ctx())
    assert hits == []


def test_wire1_ignores_unknown_rule_and_missing_slot():
    pvi = _wire1_pvi()
    assert _run_wire1(pvi, _wire1_ctx(rules={5: 0})) == []
    assert _run_wire1(pvi, _wire1_ctx(rules={})) == []


def test_wire1_skips_method_calls_and_unresolvable():
    pvi = _wire1_pvi(node_type="dynIUse")
    assert _run_wire1(pvi, _wire1_ctx()) == []  # phantom-terminal family
    ctx = SimpleNamespace()
    ctx.callee_interface = lambda caller, name: None
    assert _run_wire1(_wire1_pvi(), ctx) == []
    assert _run_wire1(_wire1_pvi(), None) == []  # no context: skip


def test_wire1_no_false_positives_on_fixtures():
    # Vessel Simulator is committed, working code: a precise WIRE-1 must
    # stay silent (the audit's 0%-precision failure must not regress).
    import glob as _glob
    paths = sorted(_glob.glob(vi("vessel", "**", "*.vi"), recursive=True))
    reviews = review_many(paths)
    assert all(r.parse_ok for r in reviews)
    hits = [f for r in reviews for f in r.findings if f.rule_id == "WIRE-1"]
    assert hits == [], [f.title for f in hits]


def test_review_context_indexes_vim_and_prefers_same_dir(tmp_path):
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    d1.mkdir()
    d2.mkdir()
    (d1 / "Helper.vi").touch()
    (d2 / "Helper.vi").touch()
    (d1 / "Tool.vim").touch()
    caller = d1 / "Caller.vi"
    caller.touch()
    ctx = ReviewContext([str(caller), str(d1 / "Helper.vi")])
    got = ctx._resolve_callee(str(caller), "Helper.vi")
    assert got == str(d1 / "Helper.vi")  # same dir wins
    got = ctx._resolve_callee(str(caller), "Tool.vim")
    assert got == str(d1 / "Tool.vim")  # .vim indexed
    assert ctx._resolve_callee(str(caller), "Nope.vi") is None
    # library-qualified names resolve on the leaf
    got = ctx._resolve_callee(str(caller), "myLib.lvlib:Helper.vi")
    assert got == str(d1 / "Helper.vi")
