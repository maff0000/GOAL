"""Tests for goal_dcp.readiness: the mechanical readiness rule.

The rule under test is exactly::

    state == DELIVERY_READY
    AND every dependency resolves to a declared item in an accepted
        terminal state

Each fixture under ``tests/fixtures_readiness/`` isolates one half of one
clause, so a failure names the defect rather than merely reporting that
"readiness is wrong". The canonical backlog is read but never mutated.
"""

import json
import pathlib

import pytest

from goal_dcp import model
from goal_dcp.model import load_backlog
from goal_dcp.readiness import (
    UnknownAssumedId,
    effective_state,
    readiness_payload,
    ready_items,
)

FIXTURES = pathlib.Path(__file__).parent / "fixtures_readiness"


def load_fixture(name):
    """Load a readiness fixture backlog by file name."""
    return load_backlog(FIXTURES / name)


def ready_ids(backlog, assume_closed=frozenset()):
    """The ids readiness returns, in the order it returns them."""
    return [item.id for item in ready_items(backlog, assume_closed)]


# ---------------------------------------------------------------------------
# The canonical backlog, unprojected
# ---------------------------------------------------------------------------


def test_canonical_backlog_has_nothing_ready_without_a_projection():
    """Nothing is dispatchable today, and that is the correct answer.

    Every ``DELIVERY_READY`` item in canonical data depends on
    ``GOAL-DCP-001``, which is in ``FORGE_AUDIT`` - deliberately *not* an
    accepted terminal state. An empty answer here is the dependency half of
    the rule doing its job on real data.
    """
    backlog = load_backlog()

    assert ready_items(backlog) == ()
    assert readiness_payload(backlog) == {"ready": []}
    assert backlog.by_id["GOAL-DCP-001"].state == "FORGE_AUDIT"
    assert "FORGE_AUDIT" not in model.ACCEPTED_TERMINAL_STATES


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
    """An item not in DELIVERY_READY is never ready, dependencies regardless."""
    backlog = load_fixture("state_not_delivery_ready.yaml")

    assert backlog.by_id["TARGET-001"].state == "ARCHITECTURE_REQUIRED"
    assert backlog.by_id["DEP-001"].state in model.ACCEPTED_TERMINAL_STATES
    assert ready_items(backlog) == ()


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
    item = backlog.by_id["GOAL-DCP-001"]

    assert item.state == "FORGE_AUDIT"
    assert effective_state(item, frozenset({"GOAL-DCP-001"})) == "CLOSED"
    assert effective_state(item, frozenset({"OPS-SAFE-001"})) == "FORGE_AUDIT"


def test_projection_does_not_mutate_the_backlog():
    """assume_closed is a what-if answer, not a state change."""
    backlog = load_backlog()

    ready_items(backlog, frozenset({"GOAL-DCP-001"}))

    assert backlog.by_id["GOAL-DCP-001"].state == "FORGE_AUDIT"


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
        "ready": [
            {"id": "ALPHA-001", "target_repository": "maff0000/alpha"},
            {"id": "MIKE-001", "target_repository": "maff0000/mike"},
            {"id": "ZULU-001", "target_repository": "maff0000/zulu"},
        ]
    }


def test_payload_default_shape_carries_no_other_keys():
    backlog = load_fixture("multiple_ready.yaml")

    payload = readiness_payload(backlog)

    assert set(payload) == {"ready"}
    for entry in payload["ready"]:
        assert set(entry) == {"id", "target_repository"}


def test_with_pid_adds_pid_path_and_renders_absence_as_null():
    backlog = load_fixture("multiple_ready.yaml")

    payload = readiness_payload(backlog, with_pid=True)

    assert payload == {
        "ready": [
            {
                "id": "ALPHA-001",
                "target_repository": "maff0000/alpha",
                "pid_path": "pids/ALPHA-001.md",
            },
            {
                "id": "MIKE-001",
                "target_repository": "maff0000/mike",
                "pid_path": None,
            },
            {
                "id": "ZULU-001",
                "target_repository": "maff0000/zulu",
                "pid_path": None,
            },
        ]
    }


def test_payload_is_json_serialisable_with_sorted_keys():
    backlog = load_fixture("multiple_ready.yaml")

    rendered = json.dumps(readiness_payload(backlog, with_pid=True), sort_keys=True)

    assert rendered.startswith('{"ready": [{"id": "ALPHA-001"')
    assert "null" in rendered


# ``tests/test_first_wave.py`` holds the complementary proof that neither
# ``readiness.py`` nor ``docsync.py`` hard-codes any work-item id.
