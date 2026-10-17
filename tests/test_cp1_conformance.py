"""CP-1 (HERMES Redis -> HELIOS input) offline conformance: GOLD-AUD-C acceptance A-1 to A-4.

Checker B (standard library) always runs. Checker A (jsonschema) runs when jsonschema is
installed; the repository CI installs only pyyaml and pytest, so the A-versus-B equality tests
are skipped there and the skip is reported, not hidden (see the evidence README).
"""

import re

import pytest

from cp_support import cp1_checker_b as B
from cp_support import cp1_reference_adapter as R
from cp_support.cp_common import CP1_DIR, fixture_files, load_json, unnum

FIXTURES = CP1_DIR / "fixtures"
CASES = [p for p in fixture_files(FIXTURES) if "scenarios" not in p.parts and p.name != "REUSE-MANIFEST.json"]
SCENARIOS = sorted((FIXTURES / "scenarios").glob("*.json"))
PACKAGE = (CP1_DIR / "PACKAGE.md").read_text(encoding="utf-8")
MATRIX_CODES = set(re.findall(r"^\| (CP1-[A-Z]\d{2}) \|", PACKAGE, flags=re.M))

#: HELIOS INPUT_REJECTION_RULES (hermes_boundary.py at 7f7193d, tuple order) -> the CP-1 codes that cover each.
HELIOS_RULES = {
    "binary float": {"CP1-F01"},
    "unknown field": {"CP1-F02"},
    "incoherent candle": {"CP1-F03"},
    "negative volume or rsi range": {"CP1-F04", "CP1-F05"},
    "naive or misaligned timestamp": {"CP1-F06", "CP1-F07"},
    "unsupported timeframe": {"CP1-F08"},
    "provenance order": {"CP1-F09"},
    "mixed window": {"CP1-F10"},
    "duplicate or out-of-order": {"CP1-F11", "CP1-F12"},
    "schema version not accepted": {"CP1-F13"},
    "stale": {"CP1-F14"},
    "incomplete bar": {"CP1-F15"},
    "required indicator absent": {"CP1-F16"},
}


def _verdict_code(result):
    return None if result[0] == "ACCEPT" else result[1]


@pytest.mark.parametrize("path", CASES, ids=lambda p: p.name)
def test_checker_b_reproduces_the_declared_verdict(path):
    case = load_json(path)
    result = B.check_case(case)
    assert _verdict_code(result) == case["expected_code"], path.name
    assert (case["kind"] == "valid") == (case["expected_code"] is None)


def test_every_declared_code_is_in_the_rejection_matrix_and_named_by_its_file():
    assert len(MATRIX_CODES) >= 38, sorted(MATRIX_CODES)
    for path in CASES:
        case = load_json(path)
        code = case["expected_code"]
        if code is None:
            assert path.name.startswith("VALID__")
        else:
            assert code in MATRIX_CODES, (path.name, code)
            assert path.name.startswith(code + "__"), path.name
        assert case["rule"] and case["description"], path.name


def test_valid_wire_cases_produce_exactly_their_expected_canonical_frames():
    for path in (FIXTURES / "valid" / "wire").glob("*.json"):
        case = load_json(path)
        verdict, code, frames = B.check_case(case)
        assert verdict == "ACCEPT", (path.name, code)
        assert B.canonical(frames) == B.canonical(unnum_frames(case["expected_frames"])), path.name
        # the adapter output is itself held to the strict provider forms
        assert B.check_frames_list(frames, case["context"], "adapter") is None


def unnum_frames(frames):
    return unnum(frames)


def test_rejection_matrix_completeness_every_code_has_an_invalid_fixture_or_scenario():
    seen = set()
    for path in CASES:
        code = load_json(path)["expected_code"]
        if code:
            seen.add(code)
    for path in SCENARIOS:
        for step in load_json(path)["steps"]:
            c = step["expect"].get("code")
            if c:
                seen.add(c)
    fixture_codes = {c for c in MATRIX_CODES}
    assert fixture_codes - seen == set(), sorted(fixture_codes - seen)
    assert seen - fixture_codes == set(), sorted(seen - fixture_codes)


def test_every_helios_input_rejection_rule_has_an_invalid_fixture():
    seen = {load_json(p)["expected_code"] for p in CASES if load_json(p)["expected_code"]}
    for rule, codes in HELIOS_RULES.items():
        assert seen & codes, f"no invalid fixture for HELIOS rule: {rule}"


def test_the_fifteen_helios_malformed_cases_are_reused_with_their_source_digests():
    entries = load_json(FIXTURES / "REUSE-MANIFEST.json")["entries"]
    malformed = [e for e in entries if "/malformed/" in e["source_path"]]
    assert len(malformed) == 15
    assert len(entries) == 18
    for e in entries:
        assert re.fullmatch(r"[0-9a-f]{64}", e["sha256"])
        assert (FIXTURES / e["file"]).is_file()


def test_the_checker_rejects_a_mutated_valid_case_with_a_code_not_none():
    case = load_json(FIXTURES / "valid" / "wire" / "VALID__h4_three_bars_hermes_only_fields_dropped.json")
    case["wire"]["bars"][1]["candle"]["data"]["open"] = case["wire"]["bars"][1]["candle"]["data"]["open"].__class__("2395.00000001")
    assert B.check_case(case)[0] == "REJECT"


@pytest.mark.parametrize("path", SCENARIOS, ids=lambda p: p.stem)
def test_scenarios_reproduce_their_expected_outcome_tables(path):
    scn = load_json(path)
    records = scn["records"]
    got = R.run_scenario(unnum(scn), scn["context"], records)
    for step, result in zip(unnum(scn)["steps"], got):
        expect = step["expect"]
        assert {k: result.get(k) for k in expect} == expect, (path.name, step, result)


def test_a_wrong_expectation_is_detected_by_the_scenario_runner():
    scn = unnum(load_json(SCENARIOS[0]))
    got = R.run_scenario(scn, scn["context"], load_json(SCENARIOS[0])["records"])
    assert got and {k: got[0].get(k) for k in ("event", "code")} != {"event": "EVALUATE", "code": "NONE"}


# ----------------------------------------------------------------- checker A (jsonschema)
@pytest.fixture(scope="module")
def checker_a():
    pytest.importorskip("jsonschema", reason="checker A needs jsonschema; checker B ran")
    from cp_support import cp1_checker_a

    return cp1_checker_a


@pytest.mark.parametrize("path", CASES, ids=lambda p: p.name)
def test_checker_a_reproduces_the_declared_verdict_and_equals_checker_b(checker_a, path):
    case = load_json(path)
    ra, rb = checker_a.check_case(case), B.check_case(case)
    assert _verdict_code(ra) == case["expected_code"], (path.name, ra)
    assert ra[:2] == rb[:2]
    if ra[2] is not None:
        assert B.canonical(ra[2]) == B.canonical(rb[2])  # byte-identical frames
