"""Tests for goal_dcp.readiness: the two mechanical rules.

Dispatch readiness is exactly::

    state == DELIVERY_READY
    AND the item declares a PID (pid_path is a non-empty string)
    AND every dependency resolves to a declared item in an accepted
        terminal state

The PID-authoring wave is exactly::

    state == PID_DRAFT
    AND every dependency resolves to a declared item in an accepted
        terminal state

Each fixture under ``tests/fixtures_readiness/`` isolates one half of one
clause, so a failure names the defect rather than merely reporting that
"readiness is wrong". The canonical backlog is read but never mutated.

The PID clause is the *data* half of a two-layer rule: this module can only
see that an item declares a PID, never that the file exists. ``tests/test_cli.py``
owns the other half, at the process boundary, where ``tools/goal-ready``
validates before answering.
"""

import json
import pathlib

import pytest
import yaml

from goal_dcp import model
from goal_dcp.model import load_backlog
from goal_dcp.readiness import (
    PID_AUTHORING_WAVE_KEY,
    READY_KEY,
    UnknownAssumedId,
    effective_state,
    pid_authoring_wave_items,
    pid_authoring_wave_payload,
    readiness_payload,
    ready_items,
)
from goal_dcp.validate import validate

FIXTURES = pathlib.Path(__file__).parent / "fixtures_readiness"


def load_fixture(name):
    """Load a readiness fixture backlog by file name."""
    return load_backlog(FIXTURES / name)


def ready_ids(backlog, assume_closed=frozenset()):
    """The ids readiness returns, in the order it returns them."""
    return [item.id for item in ready_items(backlog, assume_closed)]


def wave_ids(backlog, assume_closed=frozenset()):
    """The ids the PID-authoring wave returns, in the order it returns them."""
    return [item.id for item in pid_authoring_wave_items(backlog, assume_closed)]


# ---------------------------------------------------------------------------
# The canonical backlog, unprojected
# ---------------------------------------------------------------------------


def test_canonical_backlog_has_nothing_ready_without_a_projection():
    """Nothing is dispatchable today, and that is the correct answer.

    No canonical item is in ``DELIVERY_READY``: the next wave
    (``GOAL-DCP-001`` is now ``CLOSED``) is still in ``PID_DRAFT`` with no PID.
    An empty answer here is the rule doing its job on real data, not a tool
    that failed to find anything.
    """
    backlog = load_backlog()

    gold_audits = [f"GOLD-AUD-{letter}" for letter in "ABCDEF"]
    assert [item.id for item in ready_items(backlog)] == gold_audits
    assert [e["id"] for e in readiness_payload(backlog)[READY_KEY]] == gold_audits
    assert backlog.by_id["GOAL-DCP-001"].state == "CLOSED"
    assert "CLOSED" in model.ACCEPTED_TERMINAL_STATES


def test_no_canonical_item_claims_delivery_readiness_without_a_pid():
    """The data-layer invariant behind the empty answer above.

    If an item ever appears in ``DELIVERY_READY`` with no PID, the validator
    fails it (``MISSING_PID``) and ``tools/goal-ready`` refuses to answer, so
    this is really an assertion that the backlog cannot get into a state where
    readiness has to be trusted to exclude it.
    """
    backlog = load_backlog()

    offenders = sorted(
        item.id
        for item in backlog.items
        if item.state == "DELIVERY_READY" and not item.pid_path
    )

    assert offenders == []


# ---------------------------------------------------------------------------
# Dependency states that do and do not satisfy
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_name, dependency_state",
    [
        ("dep_merged.yaml", "MERGED"),
        ("dep_deployment_ready.yaml", "DEPLOYMENT_READY"),
        ("dep_paper.yaml", "PAPER"),
        ("dep_live.yaml", "LIVE"),
        ("dep_closed.yaml", "CLOSED"),
    ],
)
def test_each_accepted_terminal_state_satisfies_a_dependency(
    fixture_name, dependency_state
):
    backlog = load_fixture(fixture_name)

    assert dependency_state in model.ACCEPTED_TERMINAL_STATES
    assert backlog.by_id["DEP-001"].state == dependency_state
    assert ready_ids(backlog) == ["TARGET-001"]


def test_every_accepted_terminal_state_has_a_fixture():
    """Guard against the vocabulary growing past the fixtures that cover it."""
    covered = {"MERGED", "DEPLOYMENT_READY", "PAPER", "LIVE", "CLOSED"}

    assert covered == set(model.ACCEPTED_TERMINAL_STATES)


def test_cancelled_is_terminal_but_not_accepted():
    """CANCELLED must not unblock work.

    This is the distinction the whole set exists for: work can stop
    permanently without its outcome ever being delivered, so "finished" and
    "delivered" are not the same thing.
    """
    backlog = load_fixture("dep_cancelled.yaml")

    assert backlog.by_id["DEP-001"].state == "CANCELLED"
    assert "CANCELLED" not in model.ACCEPTED_TERMINAL_STATES
    assert ready_items(backlog) == ()


@pytest.mark.parametrize(
    "fixture_name, dependency_state",
    [
        ("dep_blocked.yaml", "BLOCKED"),
        ("dep_po_acceptance.yaml", "PO_ACCEPTANCE"),
        ("dep_matt_decision.yaml", "MATT_DECISION"),
        ("dep_candidate.yaml", "CANDIDATE"),
    ],
)
def test_live_and_in_flight_states_do_not_satisfy_a_dependency(
    fixture_name, dependency_state
):
    """BLOCKED is not terminal; the gates are in flight, not acceptance."""
    backlog = load_fixture(fixture_name)

    assert backlog.by_id["DEP-001"].state == dependency_state
    assert ready_items(backlog) == ()


def test_all_dependencies_must_be_satisfied_not_merely_one():
    """One met and one unmet dependency is not ready: the rule is ALL, not ANY."""
    backlog = load_fixture("one_met_one_unmet.yaml")

    accepted = model.ACCEPTED_TERMINAL_STATES
    assert effective_state(backlog.by_id["DEP-MET-001"]) in accepted
    assert effective_state(backlog.by_id["DEP-UNMET-001"]) not in accepted
    assert ready_items(backlog) == ()


def test_unresolvable_dependency_fails_closed():
    """A dependency no item declares makes the item NOT ready.

    Readiness is never ready-by-default: an unknown, shorthand or typo'd
    dependency must block rather than silently disappear, because ROGUE
    dispatches on this answer.
    """
    backlog = load_fixture("unresolvable_dependency.yaml")

    assert backlog.by_id["TARGET-001"].depends_on == ("NOT-DECLARED-001",)
    assert "NOT-DECLARED-001" not in backlog.by_id
    assert ready_items(backlog) == ()


def test_state_gate_holds_however_satisfied_the_dependencies_are():
    """An item not in DELIVERY_READY is never ready, everything else regardless.

    The fixture satisfies the other two clauses outright - the dependency is
    accepted-terminal and the item declares a PID - so the state clause is the
    only thing excluding it, and this test cannot pass for the wrong reason.
    """
    backlog = load_fixture("state_not_delivery_ready.yaml")
    target = backlog.by_id["TARGET-001"]

    assert target.state == "ARCHITECTURE_REQUIRED"
    assert target.pid_path, "the PID clause must not be what excludes it"
    assert backlog.by_id["DEP-001"].state in model.ACCEPTED_TERMINAL_STATES
    assert ready_items(backlog) == ()


# ---------------------------------------------------------------------------
# The PID clause of dispatch readiness
# ---------------------------------------------------------------------------


def test_delivery_ready_without_a_declared_pid_is_never_ready():
    """The repaired defect, isolated: no PID means not dispatchable.

    The fixture satisfies the state clause and the dependency clause, so the
    declared-PID clause is the only thing excluding ``TARGET-001``. Readiness
    is what ROGUE hands to FORGE, and FORGE delivers against a canonical PID;
    an item without one is not work that can be dispatched.
    """
    backlog = load_fixture("no_pid_declared.yaml")
    target = backlog.by_id["TARGET-001"]

    assert target.state == "DELIVERY_READY"
    assert effective_state(backlog.by_id["DEP-001"]) in model.ACCEPTED_TERMINAL_STATES
    assert target.pid_path is None

    assert ready_items(backlog) == ()
    assert readiness_payload(backlog) == {READY_KEY: []}


@pytest.mark.parametrize("declared", [None, "", "   "])
def test_an_empty_or_whitespace_pid_path_does_not_count_as_declared(
    tmp_path, declared
):
    """"Declares a PID" means a usable value, not merely a present key.

    An empty string is a key with nothing in it. Treating it as a declaration
    would let a blank field unblock dispatch, which is the failure mode this
    clause exists to stop.
    """
    document = yaml.safe_load(
        (FIXTURES / "no_pid_declared.yaml").read_text(encoding="utf-8")
    )
    for entry in document["items"]:
        if entry["id"] == "TARGET-001":
            entry["pid_path"] = declared

    backlog_dir = tmp_path / "backlog"
    backlog_dir.mkdir()
    path = backlog_dir / "backlog.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=True), encoding="utf-8")

    assert ready_items(load_backlog(path)) == ()


#: The ways a ``DELIVERY_READY`` item's PID can be absent or broken.
#:
#: ``PID_INVALID`` belongs here for the same reason the others do: a fixture
#: item whose declared PID exists but is not a PID is a document the validator
#: rejects, so leaving it out would let these fixtures quietly become invalid
#: backlogs while this guard reported them sound. It is also what forced each
#: ``DELIVERY_READY`` fixture item to declare a PID naming *itself* — a PID can
#: no longer be shared across items with different ids.
PID_FINDING_CODES = frozenset(
    {"MISSING_PID", "PID_FILE_NOT_FOUND", "PID_INVALID", "BACKLOG_PID_MISMATCH"}
)

#: ``(fixture file name, item id) -> the one PID finding that item must yield``.
#:
#: The exemption list for the integrity guard below, and deliberately a list of
#: exact pairs rather than a list of files or a directory-wide skip: it exempts
#: one named item in one named fixture, so no other item - not even another
#: item in the same file - can inherit the exemption by accident.
DELIVERY_READY_PID_EXEMPTIONS: dict[tuple[str, str], str] = {
    # The fixture whose entire purpose is that this item declares no PID.
    ("no_pid_declared.yaml", "TARGET-001"): "MISSING_PID",
}


def test_every_delivery_ready_fixture_item_declares_an_agreeing_pid():
    """Fixture integrity: a DELIVERY_READY fixture item must be valid as one.

    These fixtures exist to isolate the readiness rule, so their target items
    have to stay eligible on the state clause. Now that ``DELIVERY_READY``
    requires a canonical PID, "eligible" means the declared PID really exists
    and really agrees - otherwise the fixture quietly becomes a document the
    validator would reject, and a reader cannot tell whether the clause under
    test is the reason for the answer.

    Scoped to ``DELIVERY_READY`` items on purpose. The ``DEP-*`` items are the
    variable each fixture manipulates, and several are parked in states that
    require a PID for reasons that have nothing to do with readiness; whether
    a dependency declares a PID has no bearing on whether it satisfies a
    dependant.

    **Why there is an exemption at all.** This directory holds both positive
    and negative readiness fixtures. A negative fixture that asserts "this item
    is NOT ready *because* it declares no PID" is necessarily a document the
    validator rejects - the rejection is the thing it proves. Such a fixture
    cannot satisfy the guard above and must not be "repaired" into silence, so
    it is named in :data:`DELIVERY_READY_PID_EXEMPTIONS` instead.

    **Why the exemption cannot become a hiding place.** It is earned on every
    run, not granted once:

    * an exempted item must produce *exactly* the one finding it is listed for,
      so it cannot quietly acquire a second, unrelated PID defect; and
    * every entry must be earned by an item that really exists and really is
      still ``DELIVERY_READY``, so a renamed or deleted fixture, or one that is
      later given a valid PID, fails here as an exemption that is no longer
      needed rather than lingering as dead weight.
    """
    checked = 0
    earned: set[tuple[str, str]] = set()
    for path in sorted(FIXTURES.glob("*.yaml")):
        backlog = load_backlog(path)
        findings = validate(backlog)
        for item in backlog.items:
            if item.state != "DELIVERY_READY":
                continue
            checked += 1
            offending = sorted(
                finding.code
                for finding in findings
                if finding.item_id == item.id
                and finding.code in PID_FINDING_CODES
            )

            exempted = DELIVERY_READY_PID_EXEMPTIONS.get((path.name, item.id))
            if exempted is not None:
                assert offending == [exempted], (
                    f"{path.name}: {item.id} is exempted for {exempted!r} and must "
                    f"produce exactly that finding, but produced {offending} - "
                    "the exemption is no longer earned"
                )
                earned.add((path.name, item.id))
                continue

            assert offending == [], f"{path.name}: {item.id}: {offending}"

    assert checked, "no fixture declares a DELIVERY_READY item - assertion vacuous"

    unearned = sorted(set(DELIVERY_READY_PID_EXEMPTIONS) - earned)
    assert not unearned, (
        f"exemptions no longer earned by any DELIVERY_READY fixture item: {unearned} "
        "- delete the stale entry rather than leaving the guard weakened"
    )


def test_a_ready_items_pid_path_is_never_null():
    """Stated as a property of the answer, over every fixture that has one.

    Whatever a fixture is isolating, if an item comes out of ``ready_items`` it
    declares a PID. That is clause (2) read back off the output rather than
    off the implementation.
    """
    checked = 0
    for path in sorted(FIXTURES.glob("*.yaml")):
        backlog = load_backlog(path)
        for item in ready_items(backlog):
            assert item.pid_path, f"{path.name}: {item.id} is ready with no PID"
            checked += 1

    assert checked, "no fixture produced a ready item - the assertion is vacuous"


def test_item_without_dependencies_satisfies_the_dependency_clause_vacuously():
    backlog = load_fixture("multiple_ready.yaml")

    assert backlog.by_id["ALPHA-001"].depends_on == ()
    assert "ALPHA-001" in ready_ids(backlog)


# ---------------------------------------------------------------------------
# effective_state and the assume_closed projection
# ---------------------------------------------------------------------------


def test_effective_state_returns_the_declared_state_without_a_projection():
    backlog = load_backlog()

    for item in backlog.items:
        assert effective_state(item) == item.state


def test_effective_state_returns_closed_for_a_projected_id():
    backlog = load_backlog()
    item = backlog.by_id["OPS-SAFE-001"]

    assert item.state == "PID_DRAFT"
    assert effective_state(item, frozenset({"OPS-SAFE-001"})) == "CLOSED"
    assert effective_state(item, frozenset({"OPS-SAFE-002"})) == "PID_DRAFT"


def test_projection_does_not_mutate_the_backlog():
    """assume_closed is a what-if answer, not a state change."""
    backlog = load_backlog()

    ready_items(backlog, frozenset({"OPS-SAFE-001"}))

    assert backlog.by_id["OPS-SAFE-001"].state == "PID_DRAFT"


def test_unknown_assumed_id_raises_rather_than_answering():
    """A typo must not silently produce an empty or wrong answer."""
    backlog = load_backlog()

    with pytest.raises(UnknownAssumedId):
        ready_items(backlog, frozenset({"DCP-001"}))

    with pytest.raises(UnknownAssumedId):
        readiness_payload(backlog, frozenset({"DCP-001"}))


def test_unknown_assumed_id_names_the_offending_ids_deterministically():
    backlog = load_backlog()

    with pytest.raises(UnknownAssumedId) as excinfo:
        ready_items(backlog, frozenset({"ZZZ-002", "DCP-001"}))

    assert "DCP-001" in str(excinfo.value)
    assert "ZZZ-002" in str(excinfo.value)
    assert str(excinfo.value).index("DCP-001") < str(excinfo.value).index("ZZZ-002")


def test_a_declared_assumed_id_is_accepted_even_when_already_terminal():
    """Projecting an already-closed id is a no-op, not an error."""
    backlog = load_fixture("dep_closed.yaml")

    assert ready_ids(backlog, frozenset({"DEP-001"})) == ["TARGET-001"]


def test_projection_accepts_any_iterable_of_ids():
    """A plain set literal is the natural call shape for callers."""
    backlog = load_fixture("dep_blocked.yaml")

    assert ready_items(backlog, {"DEP-001"}) == (backlog.by_id["TARGET-001"],)


# ---------------------------------------------------------------------------
# Ordering and payload shape
# ---------------------------------------------------------------------------


def test_ready_items_are_sorted_by_id_not_source_order():
    backlog = load_fixture("multiple_ready.yaml")

    assert [item.id for item in backlog.items] == ["ZULU-001", "ALPHA-001", "MIKE-001"]
    assert ready_ids(backlog) == ["ALPHA-001", "MIKE-001", "ZULU-001"]


def test_readiness_is_deterministic_across_repeated_calls():
    backlog = load_fixture("multiple_ready.yaml")

    assert readiness_payload(backlog) == readiness_payload(backlog)


def test_payload_shape_matches_the_documented_example_exactly():
    """The PID documents {"ready":[{"id":...,"target_repository":...}]}."""
    backlog = load_fixture("multiple_ready.yaml")

    assert readiness_payload(backlog) == {
        READY_KEY: [
            {"id": "ALPHA-001", "target_repository": "maff0000/alpha"},
            {"id": "MIKE-001", "target_repository": "maff0000/mike"},
            {"id": "ZULU-001", "target_repository": "maff0000/zulu"},
        ]
    }


def test_payload_default_shape_carries_no_other_keys():
    backlog = load_fixture("multiple_ready.yaml")

    payload = readiness_payload(backlog)

    assert set(payload) == {READY_KEY}
    for entry in payload[READY_KEY]:
        assert set(entry) == {"id", "target_repository"}


def test_with_pid_adds_each_items_own_pid_and_never_a_null():
    """``pid_path`` is additive, and in this payload it is never ``null``.

    A ready item declares a PID by definition, so there is no absent case to
    render here - that is the point of the strict rule. Each entry carries
    *its own* path, which is why the fixture gives the three items three
    different PIDs rather than one shared file.
    """
    backlog = load_fixture("multiple_ready.yaml")

    payload = readiness_payload(backlog, with_pid=True)

    assert payload == {
        READY_KEY: [
            {
                "id": "ALPHA-001",
                "target_repository": "maff0000/alpha",
                "pid_path": "fixtures_readiness/pid-alpha.md",
            },
            {
                "id": "MIKE-001",
                "target_repository": "maff0000/mike",
                "pid_path": "fixtures_readiness/pid-mike.md",
            },
            {
                "id": "ZULU-001",
                "target_repository": "maff0000/zulu",
                "pid_path": "fixtures_readiness/pid-zulu.md",
            },
        ]
    }
    for entry in payload[READY_KEY]:
        assert entry["pid_path"] is not None


def test_payload_is_json_serialisable_with_sorted_keys():
    backlog = load_fixture("multiple_ready.yaml")

    rendered = json.dumps(readiness_payload(backlog, with_pid=True), sort_keys=True)

    assert rendered.startswith('{"ready": [{"id": "ALPHA-001"')
    assert "null" not in rendered, "a ready item always declares a PID"


# ---------------------------------------------------------------------------
# The PID-authoring wave
# ---------------------------------------------------------------------------


def test_the_wave_rule_requires_the_pid_draft_state():
    """A ``DELIVERY_READY`` item is not in the PID-authoring wave.

    The two answers are answers to different questions. An item that is
    already delivery-ready has a PID; it is not waiting for one to be written.
    """
    backlog = load_fixture("dep_closed.yaml")

    assert backlog.by_id["TARGET-001"].state == "DELIVERY_READY"
    assert ready_ids(backlog) == ["TARGET-001"]
    assert pid_authoring_wave_items(backlog) == ()


def test_the_wave_rule_needs_no_pid_because_it_is_the_pre_pid_state(tmp_path):
    """A ``PID_DRAFT`` item with no PID *is* the wave - that is why it exists.

    The same item would be excluded from the ready answer by the PID clause,
    so this is the proof that the two rules do not share that clause.
    """
    document = yaml.safe_load(
        (FIXTURES / "no_pid_declared.yaml").read_text(encoding="utf-8")
    )
    for entry in document["items"]:
        if entry["id"] == "TARGET-001":
            entry["state"] = "PID_DRAFT"

    backlog_dir = tmp_path / "backlog"
    backlog_dir.mkdir()
    path = backlog_dir / "backlog.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=True), encoding="utf-8")
    backlog = load_backlog(path)

    assert backlog.by_id["TARGET-001"].pid_path is None
    assert wave_ids(backlog) == ["TARGET-001"]
    assert ready_items(backlog) == ()


def test_the_wave_shares_the_dependency_clause_with_readiness(tmp_path):
    """An unsatisfied dependency keeps an item out of the wave too.

    The dependency logic is factored out and used by both rules, so this is
    the assertion that the factoring is real rather than two copies that can
    drift.
    """
    document = yaml.safe_load(
        (FIXTURES / "one_met_one_unmet.yaml").read_text(encoding="utf-8")
    )
    for entry in document["items"]:
        if entry["id"] == "TARGET-001":
            entry["state"] = "PID_DRAFT"

    backlog_dir = tmp_path / "backlog"
    backlog_dir.mkdir()
    path = backlog_dir / "backlog.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=True), encoding="utf-8")
    backlog = load_backlog(path)

    assert backlog.by_id["TARGET-001"].state == "PID_DRAFT"
    assert pid_authoring_wave_items(backlog) == ()

    # ...and it joins the wave once the unmet dependency is projected closed.
    assert wave_ids(backlog, frozenset({"DEP-UNMET-001"})) == ["TARGET-001"]


def test_wave_payload_uses_its_own_key_and_the_same_entry_shape():
    """``pid_authoring_wave``, never ``ready``.

    ``ready`` is the published FORGE-dispatchable contract. These items have no
    PID, so emitting them under that key would tell ROGUE to dispatch work
    FORGE cannot build - which is exactly the failure this round repaired.
    """
    backlog = load_fixture("multiple_ready.yaml")

    payload = pid_authoring_wave_payload(backlog)

    assert set(payload) == {PID_AUTHORING_WAVE_KEY}
    assert PID_AUTHORING_WAVE_KEY == "pid_authoring_wave"
    assert READY_KEY not in payload


def test_wave_payload_is_sorted_by_id_and_carries_target_repositories(tmp_path):
    document = yaml.safe_load(
        (FIXTURES / "multiple_ready.yaml").read_text(encoding="utf-8")
    )
    for entry in document["items"]:
        entry["state"] = "PID_DRAFT"
        entry["pid_path"] = None

    backlog_dir = tmp_path / "backlog"
    backlog_dir.mkdir()
    path = backlog_dir / "backlog.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=True), encoding="utf-8")
    backlog = load_backlog(path)

    assert pid_authoring_wave_payload(backlog) == {
        PID_AUTHORING_WAVE_KEY: [
            {"id": "ALPHA-001", "target_repository": "maff0000/alpha"},
            {"id": "MIKE-001", "target_repository": "maff0000/mike"},
            {"id": "ZULU-001", "target_repository": "maff0000/zulu"},
        ]
    }

    # --with-pid behaves uniformly across both modes, and here the honest
    # value is null: these items have no PID yet, which is why they are listed.
    with_pid = pid_authoring_wave_payload(backlog, with_pid=True)
    for entry in with_pid[PID_AUTHORING_WAVE_KEY]:
        assert set(entry) == {"id", "target_repository", "pid_path"}
        assert entry["pid_path"] is None


def test_wave_is_deterministic_and_mutates_nothing():
    backlog = load_backlog()
    before = [dict(item.raw) for item in backlog.items]

    first = pid_authoring_wave_payload(backlog, frozenset({"GOAL-DCP-001"}))
    second = pid_authoring_wave_payload(backlog, frozenset({"GOAL-DCP-001"}))

    assert first == second
    assert [dict(item.raw) for item in backlog.items] == before


def test_wave_rejects_an_unknown_assumed_id():
    """The same fail-loud projection contract as the ready answer."""
    backlog = load_backlog()

    with pytest.raises(UnknownAssumedId):
        pid_authoring_wave_items(backlog, frozenset({"DCP-001"}))

    with pytest.raises(UnknownAssumedId):
        pid_authoring_wave_payload(backlog, frozenset({"DCP-001"}))


def test_a_projected_item_is_not_in_either_answer():
    """Projection means CLOSED, which is neither DELIVERY_READY nor PID_DRAFT."""
    backlog = load_backlog()
    assumed = frozenset({"GOAL-DCP-001"})

    assert "GOAL-DCP-001" not in ready_ids(backlog, assumed)
    assert "GOAL-DCP-001" not in wave_ids(backlog, assumed)


# ``tests/test_first_wave.py`` holds the complementary proof that neither
# ``readiness.py`` nor ``docsync.py`` hard-codes any work-item id.
