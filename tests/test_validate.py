"""Tests for goal_dcp.validate and the ./tools/goal-validate shim.

Two things are proven here:

1. the canonical backlog validates clean, with no finding at all;
2. every finding code the validator claims to implement is provoked by a
   minimal fixture under ``tests/fixtures/``, each isolating exactly the one
   failure mode it exists to prove.

Assertions are on finding **codes** and the ids they attach to, never on
message prose, so improving a message does not break the suite. Fixtures are
files, never in-place mutations of the canonical backlog.
"""

import os
import pathlib
import stat
import subprocess
import sys

import pytest

from goal_dcp import model
from goal_dcp.model import BacklogLoadError, load_backlog, sort_findings
from goal_dcp.validate import dependency_cycles, validate

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"
GOAL_VALIDATE = pathlib.Path(__file__).resolve().parents[1] / "tools" / "goal-validate"

#: Every finding code the validator is required to implement.
EXPECTED_CODES = frozenset({
    "MISSING_FIELD",
    "INVALID_FIELD_TYPE",
    "MALFORMED_ID",
    "DUPLICATE_ID",
    "EMPTY_FIELD",
    "INVALID_LANE",
    "INVALID_STATE",
    "INVALID_PRIORITY",
    "INVALID_RISK",
    "MISSING_TARGET_REPOSITORY",
    "MALFORMED_TARGET_REPOSITORY",
    "WILDCARD_DEPENDENCY",
    "MALFORMED_DEPENDENCY_ID",
    "UNKNOWN_DEPENDENCY",
    "DUPLICATE_DEPENDENCY",
    "SELF_DEPENDENCY",
    "DEPENDENCY_CYCLE",
    "MISSING_PID",
    "PID_FILE_NOT_FOUND",
    "MISSING_ARCHITECTURE_REF_FILE",
    "BACKLOG_PID_MISMATCH",
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fixture_findings(name):
    """Validate the named fixture and return its findings."""
    return validate(load_backlog(FIXTURES / name))


def pairs(findings):
    """``(code, item_id)`` for each finding, sorted — the assertion surface."""
    return sorted((finding.code, finding.item_id) for finding in findings)


def codes(findings):
    """The set of codes present in ``findings``."""
    return {finding.code for finding in findings}


# ---------------------------------------------------------------------------
# The canonical backlog
# ---------------------------------------------------------------------------


def test_canonical_backlog_validates_clean():
    """The canonical backlog must produce no findings whatsoever.

    If this ever fails, the canonical data or the validator is wrong — the
    answer is never to loosen a check so the data passes.
    """
    assert validate(load_backlog()) == ()


def test_canonical_backlog_has_no_dependency_cycles():
    assert dependency_cycles(load_backlog()) == ()


def test_canonical_backlog_exercises_the_missing_pid_rule():
    """The state-conditional PID rule is live on canonical data, not dormant.

    At least one canonical item is in a state that means FORGE is engaged, and
    every such item declares a PID. Without this, ``MISSING_PID`` could be
    silently unreachable in practice.
    """
    backlog = load_backlog()
    engaged = [
        item for item in backlog.items
        if item.state in model.PID_REQUIRED_STATES
    ]
    assert engaged
    assert all(item.pid_path for item in engaged)


def test_canonical_backlog_declares_no_shorthand_dependency():
    """Every canonical dependency resolves to a declared id."""
    backlog = load_backlog()
    unresolved = sorted(
        (item.id, dependency)
        for item in backlog.items
        for dependency in item.depends_on
        if dependency not in backlog.by_id
    )
    assert unresolved == []


# ---------------------------------------------------------------------------
# Coverage of the finding vocabulary
# ---------------------------------------------------------------------------


def test_every_finding_code_is_provoked_by_a_fixture():
    """No check may be quietly skipped, and none may be invented.

    The union of codes across every loadable fixture must be exactly the
    required vocabulary: a missing code means a check is unimplemented or
    unproven, an extra code means the validator emits something undeclared.
    """
    seen = set()
    for path in sorted(FIXTURES.glob("*.yaml")):
        try:
            backlog = load_backlog(path)
        except BacklogLoadError:
            continue
        seen.update(codes(validate(backlog)))
    assert seen == EXPECTED_CODES


def test_valid_fixture_produces_no_findings():
    assert fixture_findings("valid.yaml") == ()


# ---------------------------------------------------------------------------
# Structural findings
# ---------------------------------------------------------------------------


def test_missing_field():
    assert pairs(fixture_findings("missing-field.yaml")) == [
        ("MISSING_FIELD", "ALPHA-001"),
    ]


def test_invalid_field_type():
    """A wrong-typed value and a null non-nullable value are both type errors."""
    assert pairs(fixture_findings("invalid-field-type.yaml")) == [
        ("INVALID_FIELD_TYPE", "ALPHA-001"),
        ("INVALID_FIELD_TYPE", "BETA-001"),
    ]


def test_malformed_id():
    """An item with a lowercase id is located by that id, malformed as it is."""
    assert pairs(fixture_findings("malformed-id.yaml")) == [
        ("MALFORMED_ID", "tron-t1"),
    ]


def test_duplicate_id():
    assert pairs(fixture_findings("duplicate-id.yaml")) == [
        ("DUPLICATE_ID", "ALPHA-001"),
    ]


def test_empty_field():
    assert pairs(fixture_findings("empty-field.yaml")) == [
        ("EMPTY_FIELD", "ALPHA-001"),
        ("EMPTY_FIELD", "BETA-001"),
    ]


# ---------------------------------------------------------------------------
# Vocabulary findings
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_name, code",
    [
        ("invalid-lane.yaml", "INVALID_LANE"),
        ("invalid-state.yaml", "INVALID_STATE"),
        ("invalid-priority.yaml", "INVALID_PRIORITY"),
        ("invalid-risk.yaml", "INVALID_RISK"),
    ],
)
def test_invalid_vocabulary_value(fixture_name, code):
    assert pairs(fixture_findings(fixture_name)) == [(code, "ALPHA-001")]


# ---------------------------------------------------------------------------
# target_repository
# ---------------------------------------------------------------------------


def test_missing_target_repository():
    """Null and whitespace both count as absent."""
    assert pairs(fixture_findings("missing-target-repository.yaml")) == [
        ("MISSING_TARGET_REPOSITORY", "ALPHA-001"),
        ("MISSING_TARGET_REPOSITORY", "BETA-001"),
    ]


def test_malformed_target_repository():
    assert pairs(fixture_findings("malformed-target-repository.yaml")) == [
        ("MALFORMED_TARGET_REPOSITORY", "ALPHA-001"),
    ]


def test_declared_target_repository_is_never_resolved_against_github():
    """A declared target that does not exist yet is valid.

    Canonical data declares targets for repositories that have not been
    created. The validator is offline, so those must produce no finding.
    """
    backlog = load_backlog()
    declared = {item.target_repository for item in backlog.items}
    assert len(declared) > 1
    assert validate(backlog) == ()


# ---------------------------------------------------------------------------
# Dependency syntax and membership — the two layers
# ---------------------------------------------------------------------------


def test_wildcard_dependency():
    assert pairs(fixture_findings("wildcard-dependency.yaml")) == [
        ("WILDCARD_DEPENDENCY", "ALPHA-001"),
    ]


def test_malformed_dependency_id():
    """Lowercase and comma-list entries are rejected by the syntax layer."""
    assert pairs(fixture_findings("malformed-dependency-id.yaml")) == [
        ("MALFORMED_DEPENDENCY_ID", "ALPHA-001"),
        ("MALFORMED_DEPENDENCY_ID", "ALPHA-001"),
    ]


def test_shorthand_dependency_is_rejected_by_the_membership_layer():
    """'DCP-001' is well-formed, so only membership can reject it.

    This is the Central Architecture requirement that shorthand is not a
    usable identifier: the syntax layer cannot tell 'DCP-001' from
    'DARWIN-R1', so the validator resolves every dependency against the
    declared item ids.
    """
    findings = fixture_findings("unknown-dependency.yaml")
    assert pairs(findings) == [("UNKNOWN_DEPENDENCY", "BETA-001")]


def test_shorthand_is_syntactically_well_formed():
    """Guards the reason the membership layer has to exist."""
    assert model.ID_PATTERN.fullmatch("DCP-001")
    assert model.ID_PATTERN.fullmatch("DARWIN-R1")
    assert not model.ID_PATTERN.fullmatch("OPS-SAFE-*")
    assert not model.ID_PATTERN.fullmatch("tron-t1")
    assert not model.ID_PATTERN.fullmatch("TRON-T2,T3,T4")


def test_duplicate_dependency():
    assert pairs(fixture_findings("duplicate-dependency.yaml")) == [
        ("DUPLICATE_DEPENDENCY", "BETA-001"),
    ]


# ---------------------------------------------------------------------------
# Cycles
# ---------------------------------------------------------------------------


def test_self_loop_is_a_self_dependency_not_a_cycle_finding():
    """A self-loop is reported once, as SELF_DEPENDENCY.

    ``DEPENDENCY_CYCLE`` is defined for cycles of length >= 2, so a one-node
    loop must not also appear as a cycle finding. ``dependency_cycles`` still
    reports it, because the question "what cycles exist?" has a one-element
    answer here.
    """
    backlog = load_backlog(FIXTURES / "self-dependency.yaml")
    assert pairs(validate(backlog)) == [("SELF_DEPENDENCY", "ALPHA-001")]
    assert dependency_cycles(backlog) == (("ALPHA-001",),)


def test_two_node_cycle():
    backlog = load_backlog(FIXTURES / "cycle-two-node.yaml")
    assert dependency_cycles(backlog) == (("CYCLE-001", "CYCLE-002"),)
    assert pairs(validate(backlog)) == [("DEPENDENCY_CYCLE", "CYCLE-001")]


def test_three_node_cycle_is_canonically_rotated():
    """Smallest id first, regardless of the order items are declared in."""
    backlog = load_backlog(FIXTURES / "cycle-three-node.yaml")
    assert [item.id for item in backlog.items] == [
        "CYCLE-003", "CYCLE-001", "CYCLE-002",
    ]
    assert dependency_cycles(backlog) == (
        ("CYCLE-001", "CYCLE-002", "CYCLE-003"),
    )
    assert pairs(validate(backlog)) == [("DEPENDENCY_CYCLE", "CYCLE-001")]


def test_two_disjoint_cycles_in_one_document():
    """Both cycles are reported, and the outer tuple is sorted."""
    backlog = load_backlog(FIXTURES / "cycle-disjoint.yaml")
    assert dependency_cycles(backlog) == (
        ("CYCLE-A1", "CYCLE-A2"),
        ("CYCLE-B1", "CYCLE-B2", "CYCLE-B3"),
    )
    assert pairs(validate(backlog)) == [
        ("DEPENDENCY_CYCLE", "CYCLE-A1"),
        ("DEPENDENCY_CYCLE", "CYCLE-B1"),
    ]


def test_cycle_reachable_only_through_a_chain():
    """The cycle is found even though the chain into it is acyclic."""
    backlog = load_backlog(FIXTURES / "cycle-via-chain.yaml")
    assert dependency_cycles(backlog) == (("RING-001", "RING-002"),)
    assert pairs(validate(backlog)) == [("DEPENDENCY_CYCLE", "RING-001")]


def test_cycles_follow_only_membership_resolvable_edges():
    """An unresolvable dependency cannot take part in a cycle."""
    assert dependency_cycles(load_backlog(FIXTURES / "unknown-dependency.yaml")) == ()
    assert dependency_cycles(load_backlog(FIXTURES / "wildcard-dependency.yaml")) == ()


def test_cycle_output_is_byte_stable():
    backlog = load_backlog(FIXTURES / "cycle-disjoint.yaml")
    assert dependency_cycles(backlog) == dependency_cycles(backlog)


# ---------------------------------------------------------------------------
# PID linkage
# ---------------------------------------------------------------------------


def test_missing_pid_is_state_conditional():
    """FORGE-engaged states require a PID; DELIVERY_READY does not.

    The fixture holds both cases, and only the FORGE_AUDIT item is reported.
    """
    assert pairs(fixture_findings("missing-pid.yaml")) == [
        ("MISSING_PID", "ALPHA-001"),
    ]


def test_pid_file_not_found_is_the_separate_broken_pointer_case():
    assert pairs(fixture_findings("pid-file-not-found.yaml")) == [
        ("PID_FILE_NOT_FOUND", "ALPHA-001"),
    ]


def test_pid_path_is_resolved_only_under_the_backlogs_own_root():
    """Absolute paths and '..' escapes are broken pointers, not shortcuts.

    ``../pids/GOAL-DCP-001.md`` would resolve to a real file if the guard were
    missing, because this fixture's ``repo_root`` is ``tests/``. Both items
    must be reported.
    """
    assert pairs(fixture_findings("pid-path-not-repo-relative.yaml")) == [
        ("PID_FILE_NOT_FOUND", "ABS-001"),
        ("PID_FILE_NOT_FOUND", "ESCAPE-001"),
    ]


def test_backlog_pid_agreement_produces_no_finding():
    """Case and backticks do not count as disagreement, nor does an omitted label."""
    assert fixture_findings("pid-match.yaml") == ()


def test_backlog_pid_mismatch_reports_one_finding_per_label():
    """Two labels disagree, so there are exactly two findings."""
    findings = fixture_findings("backlog-pid-mismatch.yaml")
    assert pairs(findings) == [
        ("BACKLOG_PID_MISMATCH", "PIDFIX-001"),
        ("BACKLOG_PID_MISMATCH", "PIDFIX-001"),
    ]
    # The label each finding is about is part of the contract, so the set of
    # labels is asserted even though prose is not.
    labelled = sorted(
        finding.message.split(":", 1)[0] for finding in findings
    )
    assert labelled == ["Lane", "Matt gate"]


def test_missing_architecture_ref_file():
    """The resolvable ref is silent; only the broken one is reported."""
    assert pairs(fixture_findings("missing-architecture-ref-file.yaml")) == [
        ("MISSING_ARCHITECTURE_REF_FILE", "ALPHA-001"),
    ]


# ---------------------------------------------------------------------------
# Robustness and precedence
# ---------------------------------------------------------------------------


def test_validate_does_not_raise_on_maximally_broken_data():
    """Deliberately broken input is reported, never raised on."""
    findings = fixture_findings("maximally-broken.yaml")
    assert findings
    assert codes(findings) <= EXPECTED_CODES
    assert {
        "INVALID_FIELD_TYPE",
        "MISSING_FIELD",
        "MISSING_TARGET_REPOSITORY",
        "WILDCARD_DEPENDENCY",
    } <= codes(findings)


def test_broken_item_findings_are_located_by_source_position():
    """An item whose own id is unusable is still locatable."""
    findings = fixture_findings("maximally-broken.yaml")
    assert any(finding.item_id == "items[0]" for finding in findings)


def test_type_error_suppresses_the_downstream_enum_finding():
    """One defect, one finding: a wrong-typed lane is not also an invalid lane."""
    findings = fixture_findings("precedence-lane-type.yaml")
    assert pairs(findings) == [("INVALID_FIELD_TYPE", "ALPHA-001")]
    assert "INVALID_LANE" not in codes(findings)


def test_findings_are_returned_in_sort_findings_order():
    findings = fixture_findings("maximally-broken.yaml")
    assert findings == sort_findings(findings)


def test_validate_is_deterministic():
    backlog = load_backlog(FIXTURES / "maximally-broken.yaml")
    assert validate(backlog) == validate(backlog)


def test_validate_never_mutates_the_backlog():
    backlog = load_backlog(FIXTURES / "maximally-broken.yaml")
    before = [dict(item.raw) for item in backlog.items]
    validate(backlog)
    assert [dict(item.raw) for item in backlog.items] == before


# ---------------------------------------------------------------------------
# The ./tools/goal-validate shim
# ---------------------------------------------------------------------------


def run_cli(*arguments, cwd=None):
    """Run the shim out of process, so exit codes are the real thing."""
    return subprocess.run(
        [sys.executable, str(GOAL_VALIDATE), *arguments],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_is_an_executable_without_a_py_extension():
    assert GOAL_VALIDATE.suffix == ""
    mode = stat.S_IMODE(GOAL_VALIDATE.stat().st_mode)
    assert mode == 0o755
    assert os.access(GOAL_VALIDATE, os.X_OK)
    first_line = GOAL_VALIDATE.read_text(encoding="utf-8").splitlines()[0]
    assert first_line == "#!/usr/bin/env python3"


def test_cli_exit_zero_on_the_canonical_backlog(tmp_path):
    """Run from an unrelated directory: the shim bootstraps its own sys.path."""
    expected = len(load_backlog().items)
    result = run_cli(cwd=tmp_path)
    assert result.returncode == 0
    assert result.stdout == f"backlog OK: {expected} items\n"
    assert result.stderr == ""


def test_cli_exit_zero_on_a_valid_fixture(tmp_path):
    result = run_cli(str(FIXTURES / "valid.yaml"), cwd=tmp_path)
    assert result.returncode == 0
    assert result.stdout == "backlog OK: 2 items\n"


def test_cli_exit_one_and_writes_findings_to_stderr(tmp_path):
    path = FIXTURES / "cycle-disjoint.yaml"
    result = run_cli(str(path), cwd=tmp_path)
    assert result.returncode == 1
    assert result.stdout == ""
    expected = [finding.as_line() for finding in validate(load_backlog(path))]
    assert result.stderr.splitlines() == expected


def test_cli_exit_two_on_a_structurally_unloadable_backlog(tmp_path):
    result = run_cli(str(FIXTURES / "load-error-items-not-list.yaml"), cwd=tmp_path)
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip()


def test_cli_exit_two_on_an_unreadable_path(tmp_path):
    result = run_cli(str(tmp_path / "absent.yaml"), cwd=tmp_path)
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip()


def test_cli_help_is_available(tmp_path):
    result = run_cli("--help", cwd=tmp_path)
    assert result.returncode == 0
    assert "goal-validate" in result.stdout
