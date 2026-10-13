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
import subprocess
import sys

import pytest
import yaml

from goal_dcp import model
from goal_dcp.model import BacklogLoadError, load_backlog, sort_findings
from goal_dcp.validate import dependency_cycles, validate

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"
REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
GOAL_VALIDATE = REPO_ROOT / "tools" / "goal-validate"

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
    "PID_INVALID",
    "MISSING_ARCHITECTURE_REF_FILE",
    "BACKLOG_PID_MISMATCH",
})

#: The five minimum-PID-validity requirements, as the message names them.
#:
#: Prose is not the assertion surface in this file, with one exception that
#: already has precedent in ``test_backlog_pid_mismatch_reports_one_finding_
#: per_label``: *which* requirement a finding reports is part of the contract,
#: because a PO repairing a PID acts on it. Only these fragments are matched,
#: never whole messages, so the wording around them stays free to improve.
IDENTITY_REASON = "the first heading does not name"
SECTION_REASONS = {
    "purpose": "no 'purpose' section with substantive content",
    "scope": "no 'scope' section with substantive content",
    "acceptance criteria": "no 'acceptance criteria' section with substantive content",
    "approval evidence": "no 'approval evidence' section with substantive content",
}


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


def item_mapping(**overrides):
    """A structurally and semantically clean item mapping, with overrides.

    Clean on purpose: a fixture built from this produces no finding at all, so
    whatever an override provokes is the *complete* finding set and can be
    asserted as such — the same property the committed fixtures have.
    """
    base = {
        "id": "ALPHA-001",
        "title": "Alpha",
        "lane": "shared",
        "component": "GOAL",
        "target_repository": "maff0000/GOAL",
        "priority": "P0",
        "risk": "low",
        "state": "ARCHITECTURE_REQUIRED",
        "depends_on": [],
        "po_gate": True,
        "matt_gate": False,
        "pid_path": None,
        "architecture_refs": [],
    }
    base.update(overrides)
    return base


def unmet(findings, item_id):
    """The requirement fragments one item's ``PID_INVALID`` message names.

    Asserts there is at most one such finding on the way past, because "one
    file, one finding" is itself part of the rule.
    """
    reported = [
        finding for finding in findings
        if finding.code == "PID_INVALID" and finding.item_id == item_id
    ]
    assert len(reported) <= 1, f"{item_id}: {len(reported)} PID_INVALID findings"
    if not reported:
        return set()

    message = reported[0].message
    named = {name for name, reason in SECTION_REASONS.items() if reason in message}
    if IDENTITY_REASON in message:
        named.add("identity")
    return named


def write_pid(tmp_path, text, name="ALPHA-001.md"):
    """Write a PID file under ``<tmp_path>/pids/`` and return its declared path.

    The returned value is repo-relative to the fixture's own ``repo_root``,
    which :func:`write_backlog` makes ``tmp_path``, so nothing written here can
    be resolved against the real repository.
    """
    pids = tmp_path / "pids"
    pids.mkdir(parents=True, exist_ok=True)
    (pids / name).write_text(text, encoding="utf-8")
    return f"pids/{name}"


#: A PID body that satisfies all five requirements for ``ALPHA-001``. Tests
#: below mutate one thing about it, so whatever they provoke is attributable.
VALID_PID = """# ALPHA-001 — a valid fixture PID

## Purpose

State plainly why this work exists at all.

## Scope

Describe what is built and what is not.

## Acceptance

List what GREEN means for this work.

## Approval

Record where the approval evidence actually lives.
"""


def write_backlog(tmp_path, items):
    """Write ``items`` as a backlog at ``<tmp_path>/backlog/backlog.yaml``.

    The ``backlog/`` subdirectory matters: ``repo_root`` is the loaded path's
    parent-of-parent, so the fixture resolves ``tmp_path`` as its own root and
    nothing it declares can reach the real repository.
    """
    backlog_dir = tmp_path / "backlog"
    backlog_dir.mkdir(parents=True, exist_ok=True)
    path = backlog_dir / "backlog.yaml"
    path.write_text(yaml.safe_dump({"items": items}, sort_keys=True), encoding="utf-8")
    return path


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

    At least one canonical item is in a PID-required state, and every such
    item declares a PID. Without this, ``MISSING_PID`` could be silently
    unreachable in practice.
    """
    backlog = load_backlog()
    engaged = [
        item for item in backlog.items
        if item.state in model.PID_REQUIRED_STATES
    ]
    assert engaged
    assert all(item.pid_path for item in engaged)


def test_no_canonical_item_in_a_pid_required_state_has_a_null_pid_path():
    """The canonical-data invariant, stated as the rule rather than as a count.

    ``DELIVERY_READY`` is a PID-required state, so this also asserts that no
    canonical item claims to be delivery-ready without a PID. Reported per id,
    so a failure names the offending items rather than just failing.
    """
    backlog = load_backlog()

    offenders = sorted(
        item.id
        for item in backlog.items
        if item.state in model.PID_REQUIRED_STATES and not item.pid_path
    )

    assert offenders == []


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


def test_missing_pid_is_state_conditional_and_delivery_ready_requires_one():
    """DELIVERY_READY requires a PID; a pre-delivery state does not.

    The fixture holds all three cases at once:

    * ``ALPHA-001`` is ``FORGE_AUDIT`` — FORGE is engaged, PID required;
    * ``BETA-001`` is ``DELIVERY_READY`` with ``pid_path: null`` — **this is
      the repaired defect**. No PID means not delivery-ready, so it is RED;
    * ``GAMMA-001`` is ``PID_DRAFT`` with ``pid_path: null`` — correct, and
      must produce no finding at all. That is the non-vacuity half: a rule
      that demanded a PID unconditionally would also "pass" the two
      assertions above.
    """
    findings = fixture_findings("missing-pid.yaml")

    assert pairs(findings) == [
        ("MISSING_PID", "ALPHA-001"),
        ("MISSING_PID", "BETA-001"),
    ]
    assert not [f for f in findings if f.item_id == "GAMMA-001"]


@pytest.mark.parametrize("state", sorted(model.PID_REQUIRED_STATES))
def test_every_pid_required_state_requires_a_pid(tmp_path, state):
    """Parametrised over the set itself, so no state can be left unproven.

    Listing states by hand here would let a state be added to
    ``PID_REQUIRED_STATES`` without anything proving the validator honours it
    for that state. Driving the parametrisation off the set closes that gap by
    construction.

    A temp fixture rather than a committed one: the point is coverage of the
    whole set, and 13 near-identical committed files would be worse than the
    rule they encode.
    """
    path = write_backlog(tmp_path, [item_mapping(state=state, pid_path=None)])

    assert pairs(validate(load_backlog(path))) == [("MISSING_PID", "ALPHA-001")]


@pytest.mark.parametrize("state", [
    "DISCOVERED", "ARCHITECTURE_REQUIRED", "PID_DRAFT", "PO_REVIEW", "BLOCKED",
])
def test_no_pre_delivery_state_requires_a_pid(tmp_path, state):
    """The other side of the boundary: a null pid_path is correct here."""
    assert state not in model.PID_REQUIRED_STATES

    path = write_backlog(tmp_path, [item_mapping(state=state, pid_path=None)])

    assert validate(load_backlog(path)) == ()


def test_delivery_ready_with_an_absent_pid_key_is_one_structural_finding():
    """Absent key -> MISSING_FIELD only. Precedence: one defect, one finding."""
    findings = fixture_findings("delivery-ready-pid-key-absent.yaml")

    assert pairs(findings) == [("MISSING_FIELD", "ALPHA-001")]
    assert "MISSING_PID" not in codes(findings)


def test_delivery_ready_with_a_wrong_typed_pid_is_one_structural_finding():
    """Wrong type -> INVALID_FIELD_TYPE only, with no downstream pile-on."""
    findings = fixture_findings("delivery-ready-pid-wrong-type.yaml")

    assert pairs(findings) == [("INVALID_FIELD_TYPE", "ALPHA-001")]
    assert "MISSING_PID" not in codes(findings)
    assert "PID_FILE_NOT_FOUND" not in codes(findings)


def test_pid_file_not_found_is_the_separate_broken_pointer_case():
    """A DELIVERY_READY item whose declared PID file does not exist is RED.

    And RED exactly once: ``pid_path`` is a non-null string, so ``MISSING_PID``
    must not also fire — the item did declare a PID, it just named nothing.
    """
    findings = fixture_findings("pid-file-not-found.yaml")

    assert pairs(findings) == [("PID_FILE_NOT_FOUND", "ALPHA-001")]
    assert "MISSING_PID" not in codes(findings)


def test_delivery_ready_with_an_unreadable_pid_file_is_reported(tmp_path):
    """A PID file that exists but is not UTF-8 text is a broken pointer.

    Built in a temp directory rather than committed: a deliberately
    undecodable file is not something to carry in the repository, where it
    would be a binary blob in the manifest and a trap for every tool that
    reads the tree as text. The fixture is still a file, and the canonical
    backlog is still untouched.
    """
    (tmp_path / "pids").mkdir()
    (tmp_path / "pids" / "ALPHA-001.md").write_bytes(b"\xff\xfe**Lane:** Shared\n")
    path = write_backlog(
        tmp_path,
        [item_mapping(state="DELIVERY_READY", pid_path="pids/ALPHA-001.md")],
    )

    findings = validate(load_backlog(path))

    assert pairs(findings) == [("PID_FILE_NOT_FOUND", "ALPHA-001")]
    assert "MISSING_PID" not in codes(findings)


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
    """Two labels disagree, so there are exactly two findings.

    The item is ``DELIVERY_READY``, so this is also the proof that declaring a
    PID that exists is not sufficient: its metadata must agree with the
    backlog. ``MISSING_PID`` must not fire — the PID is there; what it says is
    wrong.
    """
    findings = fixture_findings("backlog-pid-mismatch.yaml")
    assert pairs(findings) == [
        ("BACKLOG_PID_MISMATCH", "PIDFIX-001"),
        ("BACKLOG_PID_MISMATCH", "PIDFIX-001"),
    ]
    assert "MISSING_PID" not in codes(findings)
    # The label each finding is about is part of the contract, so the set of
    # labels is asserted even though prose is not.
    labelled = sorted(
        finding.message.split(":", 1)[0] for finding in findings
    )
    assert labelled == ["Lane", "Matt gate"]


# ---------------------------------------------------------------------------
# Minimum PID validity — PID_INVALID
# ---------------------------------------------------------------------------


def test_a_pid_that_merely_exists_is_not_a_pid():
    """The whole gap this rule closes, on one committed fixture.

    Eight items, eight ways of declaring a readable file that is not a PID,
    and ``PID_INVALID`` is the only code the document yields — one finding per
    item, never one per missing section.
    """
    findings = fixture_findings("pid-invalid.yaml")

    assert codes(findings) == {"PID_INVALID"}
    assert pairs(findings) == [
        ("PID_INVALID", "BLANK-001"),
        ("PID_INVALID", "EMPTY-001"),
        ("PID_INVALID", "HOLLOW-001"),
        ("PID_INVALID", "IDENTITY-001"),
        ("PID_INVALID", "NOACCEPT-001"),
        ("PID_INVALID", "NOAPPROVAL-001"),
        ("PID_INVALID", "PADDED-001"),
        ("PID_INVALID", "PROSE-001"),
    ]


@pytest.mark.parametrize("item_id, expected", [
    # A zero-byte and a whitespace-only file have no heading and no section,
    # so all five requirements are unmet. This is the `touch` case.
    ("EMPTY-001", {"identity", "purpose", "scope",
                   "acceptance criteria", "approval evidence"}),
    ("BLANK-001", {"identity", "purpose", "scope",
                   "acceptance criteria", "approval evidence"}),
    # Headings present, bodies empty: identity holds, the four sections do not.
    ("HOLLOW-001", {"purpose", "scope",
                    "acceptance criteria", "approval evidence"}),
    # Complete and substantive, but headed with a different id.
    ("IDENTITY-001", {"identity"}),
    # Four of five. The message must name the one that is missing.
    ("NOAPPROVAL-001", {"approval evidence"}),
    ("NOACCEPT-001", {"acceptance criteria"}),
    # The words without the structure: no ATX heading at all.
    ("PROSE-001", {"identity", "purpose", "scope",
                   "acceptance criteria", "approval evidence"}),
    # Padding is not content, so this fails exactly as the empty bodies do.
    ("PADDED-001", {"purpose", "scope",
                    "acceptance criteria", "approval evidence"}),
])
def test_the_message_names_every_unmet_requirement_and_no_other(item_id, expected):
    """A PO repairing a PID is told which sections to write, not merely that it failed."""
    assert unmet(fixture_findings("pid-invalid.yaml"), item_id) == expected


def test_a_genuinely_valid_minimal_pid_passes():
    """The reachable GREEN, and the state-scoping control, in one document.

    Without this, every assertion above would be satisfied by a rule that
    failed every PID it was shown. ``DRAFT-001`` declares a genuinely
    incomplete draft and is in ``PID_DRAFT``, so it must produce nothing.
    """
    assert fixture_findings("pid-valid-minimal.yaml") == ()


@pytest.mark.parametrize("state", sorted(model.PID_REQUIRED_STATES))
def test_every_pid_required_state_requires_a_valid_pid(tmp_path, state):
    """Parametrised over the set itself, so no state can be left unproven.

    The same incomplete draft that ``pid-valid-minimal.yaml`` proves is silent
    in ``PID_DRAFT`` is copied here and declared in each PID-required state in
    turn. One file, two opposite correct answers, decided only by the state.
    """
    draft = (FIXTURES / "pid-invalid-draft.md").read_text(encoding="utf-8")
    declared = write_pid(tmp_path, draft)
    path = write_backlog(
        tmp_path, [item_mapping(id="DRAFT-001", state=state, pid_path=declared)]
    )

    assert pairs(validate(load_backlog(path))) == [("PID_INVALID", "DRAFT-001")]


@pytest.mark.parametrize("state", [
    "DISCOVERED", "ARCHITECTURE_REQUIRED", "PID_DRAFT", "PO_REVIEW", "BLOCKED",
])
def test_no_pre_delivery_state_requires_a_valid_pid(tmp_path, state):
    """The other side of the boundary: a half-written draft is correct here.

    ``PID_DRAFT`` is where the PO authors a PID. A rule that failed a draft
    there would demand the finished document before the state that exists to
    produce it.
    """
    assert state not in model.PID_REQUIRED_STATES

    draft = (FIXTURES / "pid-invalid-draft.md").read_text(encoding="utf-8")
    declared = write_pid(tmp_path, draft)
    path = write_backlog(
        tmp_path, [item_mapping(id="DRAFT-001", state=state, pid_path=declared)]
    )

    assert validate(load_backlog(path)) == ()


def test_the_valid_pid_template_these_tests_mutate_is_itself_valid(tmp_path):
    """Non-vacuity guard for every mutation test below.

    Each of those changes exactly one thing about ``VALID_PID``. If the
    unmutated template were already failing, they would all "pass" while
    proving nothing.
    """
    declared = write_pid(tmp_path, VALID_PID)
    path = write_backlog(
        tmp_path, [item_mapping(state="DELIVERY_READY", pid_path=declared)]
    )

    assert validate(load_backlog(path)) == ()


@pytest.mark.parametrize("heading, satisfied", [
    ("# ALPHA-001 — fine", True),
    ("###### ALPHA-001", True),                 # any ATX level names the id
    ("# PID: ALPHA-001 (rev 2)", True),         # punctuation is not a token char
    ("# ALPHA-0011 — a different item", False),  # trailing digit: not a token
    ("# XALPHA-001", False),                    # leading letter: not a token
    ("# ALPHA-001-B", False),                   # trailing hyphen: not a token
    ("# ALPHA-001_2", False),                   # trailing underscore
    ("# alpha-001", False),                     # canonical ids are uppercase
    ("#ALPHA-001", False),                      # not an ATX heading: no space
    ("ALPHA-001", False),                       # not a heading at all
])
def test_identity_requires_the_id_as_a_whole_token(tmp_path, heading, satisfied):
    """The near-miss cases, which a substring search would all accept.

    ``ALPHA-001`` is a substring of ``ALPHA-0011``, ``XALPHA-001``,
    ``ALPHA-001-B`` and ``ALPHA-001_2``. None of them names it.
    """
    declared = write_pid(
        tmp_path, VALID_PID.replace("# ALPHA-001 — a valid fixture PID", heading, 1)
    )
    path = write_backlog(
        tmp_path, [item_mapping(state="DELIVERY_READY", pid_path=declared)]
    )
    findings = validate(load_backlog(path))

    assert ("identity" not in unmet(findings, "ALPHA-001")) is satisfied


def test_identity_reads_the_first_heading_and_not_a_later_one(tmp_path):
    """A correct id further down the document does not establish identity.

    Otherwise a PID for one item could be made to vouch for another by
    mentioning its id in any later heading — which is how a shared template
    would quietly serve two items.
    """
    declared = write_pid(
        tmp_path,
        VALID_PID.replace("# ALPHA-001 — a valid fixture PID", "# BETA-001", 1)
        + "\n## Related: ALPHA-001\n\nA later heading naming the other item.\n",
    )
    path = write_backlog(
        tmp_path, [item_mapping(state="DELIVERY_READY", pid_path=declared)]
    )

    assert unmet(validate(load_backlog(path)), "ALPHA-001") == {"identity"}


@pytest.mark.parametrize("spelling", [
    "## Purpose", "## PURPOSE", "## purpose", "## Purpose:", "##   Purpose   ",
    "## Objective",
])
def test_every_accepted_purpose_spelling_satisfies_the_requirement(
    tmp_path, spelling
):
    """Normalisation is case, whitespace and trailing colon, and nothing else."""
    declared = write_pid(tmp_path, VALID_PID.replace("## Purpose", spelling, 1))
    path = write_backlog(
        tmp_path, [item_mapping(state="DELIVERY_READY", pid_path=declared)]
    )

    assert validate(load_backlog(path)) == ()


@pytest.mark.parametrize("original, spelling", [
    ("## Acceptance", "## Acceptance criteria"),
    ("## Acceptance", "## ACCEPTANCE CRITERIA"),
    ("## Approval", "## Approval evidence"),
    ("## Approval", "## PO approval"),
    ("## Approval", "## PO Approval:"),
])
def test_every_accepted_alternative_spelling_satisfies_its_requirement(
    tmp_path, original, spelling
):
    assert original in VALID_PID

    declared = write_pid(tmp_path, VALID_PID.replace(original, spelling, 1))
    path = write_backlog(
        tmp_path, [item_mapping(state="DELIVERY_READY", pid_path=declared)]
    )

    assert validate(load_backlog(path)) == ()


@pytest.mark.parametrize("heading, requirement", [
    ("## Out of scope", "scope"),
    ("## Non-goals (scope)", "scope"),
    ("## Scope and approach", "scope"),
    ("## Purpose and background", "purpose"),
    ("## Acceptance criteria and evidence", "acceptance criteria"),
    ("## Approval evidence trail", "approval evidence"),
    ("## Pre-approval", "approval evidence"),
])
def test_heading_spellings_are_matched_exactly_not_by_substring(
    tmp_path, heading, requirement
):
    """``## Out of scope`` is not a scope statement, and must not pass as one.

    Every heading here contains an accepted spelling as a substring. A
    substring match is the obvious implementation and it is wrong: these are
    the headings a real PID has *alongside* its scope section, not instead of
    it.
    """
    original = "## " + ("Acceptance" if requirement == "acceptance criteria"
                        else "Approval" if requirement == "approval evidence"
                        else requirement.capitalize())
    assert original in VALID_PID

    declared = write_pid(tmp_path, VALID_PID.replace(original, heading, 1))
    path = write_backlog(
        tmp_path, [item_mapping(state="DELIVERY_READY", pid_path=declared)]
    )

    assert unmet(validate(load_backlog(path)), "ALPHA-001") == {requirement}


@pytest.mark.parametrize("body, substantive", [
    ("", False),
    ("   \n\t\n", False),
    ("one two three four five", False),            # five distinct words
    ("one two three four five six", True),         # exactly the floor
    ("xxxxx xxxxx xxxxx xxxxx xxxxx xxxxx", False),  # one distinct word
    ("One ONE one oNe onE one two three four five", False),  # case-folded: two
    ("a b c d e f g h i j k l", False),            # single characters: no words
    ("- one\n- two\n- three\n- four\n- five\n- six", True),  # a list is prose
])
def test_the_substantive_floor_is_six_distinct_case_folded_words(
    tmp_path, body, substantive
):
    """The number, and every way of trying to reach it without writing anything.

    A character, byte, line or total-word count would accept the padding case.
    Counting distinct words is what makes repetition worthless.
    """
    declared = write_pid(
        tmp_path,
        VALID_PID.replace("State plainly why this work exists at all.", body, 1),
    )
    path = write_backlog(
        tmp_path, [item_mapping(state="DELIVERY_READY", pid_path=declared)]
    )
    findings = validate(load_backlog(path))

    assert ("purpose" not in unmet(findings, "ALPHA-001")) is substantive


@pytest.mark.parametrize("section", ["Purpose", "Scope", "Acceptance", "Approval"])
def test_the_minimal_valid_fixture_sits_exactly_on_the_floor(tmp_path, section):
    """``pid-valid-minimal.md`` clears the floor by nothing at all.

    Proven behaviourally rather than by recounting words here: dropping the
    final word from any one of its four sections must make that section
    insubstantial. So the committed fixture cannot drift above the boundary and
    silently stop pinning it.
    """
    lines = (FIXTURES / "pid-valid-minimal.md").read_text(
        encoding="utf-8"
    ).splitlines()

    index = lines.index(f"## {section}") + 2
    shortened = " ".join(lines[index].split()[:-1])
    assert shortened and shortened != lines[index]
    lines[index] = shortened

    declared = write_pid(tmp_path, "\n".join(lines) + "\n", name="MINIMAL-001.md")
    path = write_backlog(
        tmp_path,
        [item_mapping(id="MINIMAL-001", state="DELIVERY_READY", pid_path=declared)],
    )

    assert pairs(validate(load_backlog(path))) == [("PID_INVALID", "MINIMAL-001")]


def test_two_thin_sections_with_the_same_heading_do_not_add_up(tmp_path):
    """Each heading occurrence is its own section; bodies are never merged.

    Three distinct words plus three more would clear the floor if the bodies of
    repeated headings were pooled. Neither section states the scope, so neither
    may satisfy the requirement.
    """
    declared = write_pid(
        tmp_path,
        VALID_PID.replace(
            "## Scope\n\nDescribe what is built and what is not.\n",
            "## Scope\n\nalpha beta gamma\n\n## Scope\n\ndelta epsilon zeta\n",
            1,
        ),
    )
    path = write_backlog(
        tmp_path, [item_mapping(state="DELIVERY_READY", pid_path=declared)]
    )

    assert unmet(validate(load_backlog(path)), "ALPHA-001") == {"scope"}


def test_one_substantive_section_satisfies_a_requirement_a_thin_twin_does_not(
    tmp_path,
):
    """The other half of the previous test: a repeated heading is not fatal.

    A PID may legitimately repeat a heading. What matters is that *some*
    section with that heading says something.
    """
    declared = write_pid(
        tmp_path,
        VALID_PID.replace(
            "## Scope\n\nDescribe what is built and what is not.\n",
            "## Scope\n\nalpha\n\n## Scope\n\nDescribe what is built and what is "
            "not.\n",
            1,
        ),
    )
    path = write_backlog(
        tmp_path, [item_mapping(state="DELIVERY_READY", pid_path=declared)]
    )

    assert validate(load_backlog(path)) == ()


def test_pid_invalid_and_backlog_pid_mismatch_are_independent(tmp_path):
    """Both fire together, because they are different defects.

    A structurally hollow document whose one declared label also contradicts
    the backlog is wrong twice, and a reader repairing it needs to be told
    twice. This is not a precedence violation: the precedence rule collapses
    findings that share one cause, and these do not.
    """
    declared = write_pid(tmp_path, "# ALPHA-001\n\n**Lane:** Ops\n")
    path = write_backlog(
        tmp_path,
        [item_mapping(state="DELIVERY_READY", lane="shared", pid_path=declared)],
    )

    assert pairs(validate(load_backlog(path))) == [
        ("BACKLOG_PID_MISMATCH", "ALPHA-001"),
        ("PID_INVALID", "ALPHA-001"),
    ]


def test_an_unresolvable_or_unreadable_pid_is_not_also_reported_invalid(tmp_path):
    """Precedence: a pointer that never resolved cannot be judged as a document.

    ``PID_FILE_NOT_FOUND`` is the one defect, and ``PID_INVALID`` must not pile
    on — there is no document to be invalid.
    """
    absent = fixture_findings("pid-file-not-found.yaml")
    assert pairs(absent) == [("PID_FILE_NOT_FOUND", "ALPHA-001")]

    (tmp_path / "pids").mkdir()
    (tmp_path / "pids" / "ALPHA-001.md").write_bytes(b"\xff\xfe# ALPHA-001\n")
    path = write_backlog(
        tmp_path,
        [item_mapping(state="DELIVERY_READY", pid_path="pids/ALPHA-001.md")],
    )

    assert pairs(validate(load_backlog(path))) == [
        ("PID_FILE_NOT_FOUND", "ALPHA-001"),
    ]


def test_a_null_pid_path_is_missing_not_invalid():
    """``MISSING_PID`` and ``PID_INVALID`` cannot both describe one item.

    Nothing was declared, so there is no document to judge. The committed
    fixture that proves ``MISSING_PID`` must not acquire a second code.
    """
    assert codes(fixture_findings("missing-pid.yaml")) == {"MISSING_PID"}


def test_pid_invalid_output_is_byte_stable():
    """Reasons are sorted, so the same document always produces the same bytes."""
    backlog = load_backlog(FIXTURES / "pid-invalid.yaml")

    first = [finding.as_line() for finding in validate(backlog)]
    assert first == [finding.as_line() for finding in validate(backlog)]
    assert first == sorted(first), "messages must be emitted in sorted order"


def test_pid_invalid_messages_carry_no_environment_detail():
    """No absolute path, hostname or username reaches a finding message."""
    findings = fixture_findings("pid-invalid.yaml")

    assert findings
    for finding in findings:
        assert str(REPO_ROOT) not in finding.message
        assert str(FIXTURES) not in finding.message
        assert not finding.message.startswith("/")


def test_the_canonical_pid_is_a_valid_pid():
    """The rule is live on canonical data, not only on fixtures.

    ``GOAL-DCP-001`` is itself in a PID-required state, so it is subject to the
    rule it implements. That is deliberately not circular: the requirement is
    that an approval-evidence *section* exists, which records approval of the
    PID — the authority that let the item reach ``DELIVERY_READY`` — and never
    acceptance of the delivered work, which is a later gate the item has not
    reached.
    """
    backlog = load_backlog()

    engaged = [
        item for item in backlog.items if item.state in model.PID_REQUIRED_STATES
    ]
    assert engaged

    findings = validate(backlog)
    assert [f for f in findings if f.code == "PID_INVALID"] == []
    assert findings == ()


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
    # An extensionless command name is part of the CLI contract.
    assert GOAL_VALIDATE.suffix == ""

    # The executable bit is asserted against the **git index**, not against
    # ``GOAL_VALIDATE.stat()``. git applies the checking-out process's umask
    # when it materialises a file, so a committed 100755 lands on disk as 0775
    # under the common umask 0002 and as 0755 only under umask 0022. Asserting
    # the on-disk bits therefore tests the umask of whoever ran ``git
    # checkout`` -- not anything about this repository -- and fails in any
    # ordinary group-writable checkout, CI included. The committed mode is the
    # durable fact, so read it from the index. Do not "simplify" this back to
    # comparing ``stat()`` bits against 0o755.
    recorded = subprocess.run(
        ["git", "ls-files", "-s", "--", "tools/goal-validate"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    assert recorded.stdout.split()[0] == "100755"

    # ...and that the bit survived into this particular checkout.
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
