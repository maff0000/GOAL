"""Tests for goal_dcp.model: vocabularies, identifier rules, structural loading.

These tests exercise the canonical backlog and hermetic temp-file fixtures.
They never mutate the canonical backlog in place.
"""

import pathlib

import pytest
import yaml

from goal_dcp import model
from goal_dcp.model import BacklogLoadError, Finding, load_backlog

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def item_mapping(**overrides):
    """A minimal structurally sound item mapping, with overrides applied."""
    base = {
        "id": "ALPHA-001",
        "title": "Alpha",
        "lane": "shared",
        "component": "GOAL",
        "target_repository": "maff0000/GOAL",
        "priority": "P0",
        "risk": "low",
        "state": "DELIVERY_READY",
        "depends_on": [],
        "po_gate": True,
        "matt_gate": False,
        "pid_path": None,
        "architecture_refs": [],
    }
    base.update(overrides)
    return base


def write_items(tmp_path, items):
    """Write ``items`` as a backlog fixture at ``<tmp_path>/backlog/backlog.yaml``.

    The ``backlog/`` subdirectory matters: ``repo_root`` is the loaded path's
    parent-of-parent, so the fixture resolves ``tmp_path`` as its own root.
    """
    return write_text(tmp_path, yaml.safe_dump({"items": items}, sort_keys=True))


def write_text(tmp_path, text):
    """Write raw ``text`` as a backlog fixture and return its path."""
    backlog_dir = tmp_path / "backlog"
    backlog_dir.mkdir(exist_ok=True)
    path = backlog_dir / "backlog.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def only_item(tmp_path, **overrides):
    """Load a single-item fixture and return the loaded Item."""
    backlog = load_backlog(write_items(tmp_path, [item_mapping(**overrides)]))
    assert len(backlog.items) == 1
    return backlog.items[0]


# ---------------------------------------------------------------------------
# Canonical backlog
# ---------------------------------------------------------------------------


def test_canonical_backlog_loads_and_every_item_exposes_all_thirteen_fields():
    backlog = load_backlog()

    assert len(model.ITEM_FIELDS) == 13
    assert backlog.source_path == model.BACKLOG_PATH

    for item in backlog.items:
        for field in model.ITEM_FIELDS:
            assert hasattr(item, field), f"{item.id} missing attribute {field}"
            assert field in item.raw, f"{item.id} omits key {field}"
        assert isinstance(item.raw, dict)


def test_canonical_backlog_has_exactly_fifty_one_items_with_unique_ids():
    backlog = load_backlog()

    assert len(backlog.items) == 51
    ids = [item.id for item in backlog.items]
    assert len(set(ids)) == 51
    assert backlog.duplicate_ids == ()
    assert len(backlog.by_id) == 51


def test_canonical_backlog_repo_root_is_the_repository_root():
    backlog = load_backlog()

    assert backlog.repo_root == model.REPO_ROOT
    assert (backlog.repo_root / "backlog" / "backlog.yaml").is_file()


def test_canonical_declared_paths_resolve_under_repo_root():
    backlog = load_backlog()

    for item in backlog.items:
        if item.pid_path is not None:
            assert (backlog.repo_root / item.pid_path).is_file(), item.id
        for ref in item.architecture_refs:
            assert (backlog.repo_root / ref).is_file(), f"{item.id}: {ref}"


# ---------------------------------------------------------------------------
# Duplicate identity bookkeeping
# ---------------------------------------------------------------------------


def test_duplicate_ids_are_reported_and_by_id_keeps_the_first_occurrence(tmp_path):
    backlog = load_backlog(write_items(tmp_path, [
        item_mapping(id="ALPHA-001", title="first"),
        item_mapping(id="BETA-002", title="unique"),
        item_mapping(id="ALPHA-001", title="second"),
    ]))

    assert backlog.duplicate_ids == ("ALPHA-001",)
    assert backlog.by_id["ALPHA-001"].title == "first"
    assert backlog.by_id["BETA-002"].title == "unique"
    # Both occurrences are retained in source order for the validator to see.
    assert [item.title for item in backlog.items] == ["first", "unique", "second"]


# ---------------------------------------------------------------------------
# Structural tolerance (one test per contract bullet)
# ---------------------------------------------------------------------------


def test_missing_field_becomes_none(tmp_path):
    mapping = item_mapping()
    del mapping["risk"]

    item = load_backlog(write_items(tmp_path, [mapping])).items[0]

    assert item.risk is None
    # raw lets the validator tell "absent" apart from "present but null".
    assert "risk" not in item.raw


def test_wrong_typed_field_is_carried_through_unconverted(tmp_path):
    item = only_item(tmp_path, po_gate="yes")

    assert item.po_gate == "yes"
    assert isinstance(item.po_gate, str)
    assert item.raw["po_gate"] == "yes"


def test_non_list_sequence_field_yields_empty_tuple_but_raw_keeps_original(tmp_path):
    item = only_item(
        tmp_path,
        depends_on="GOAL-DCP-001",
        architecture_refs={"path": "architecture/DELIVERY-CONTROL-PLANE.md"},
    )

    assert item.depends_on == ()
    assert item.architecture_refs == ()
    assert item.raw["depends_on"] == "GOAL-DCP-001"
    assert item.raw["architecture_refs"] == {"path": "architecture/DELIVERY-CONTROL-PLANE.md"}


def test_list_elements_are_not_converted(tmp_path):
    item = only_item(tmp_path, depends_on=[123, "tron-t1", None])

    assert item.depends_on == (123, "tron-t1", None)


# ---------------------------------------------------------------------------
# The five structural load errors, and nothing else
# ---------------------------------------------------------------------------


def test_load_error_when_yaml_does_not_parse(tmp_path):
    with pytest.raises(BacklogLoadError):
        load_backlog(write_text(tmp_path, "items: [GOAL-DCP-001, \n"))


@pytest.mark.parametrize("text", [
    "- GOAL-DCP-001\n",   # top level is a list
    "null\n",             # top level is null
    "just a string\n",    # top level is a scalar
    "",                   # empty document
])
def test_load_error_when_top_level_is_not_a_mapping(tmp_path, text):
    with pytest.raises(BacklogLoadError):
        load_backlog(write_text(tmp_path, text))


def test_load_error_when_items_key_is_missing(tmp_path):
    with pytest.raises(BacklogLoadError):
        load_backlog(write_text(tmp_path, "backlog_version: 1\n"))


@pytest.mark.parametrize("text", [
    "items: {}\n",
    "items: GOAL-DCP-001\n",
    "items: null\n",
])
def test_load_error_when_items_is_not_a_list(tmp_path, text):
    with pytest.raises(BacklogLoadError):
        load_backlog(write_text(tmp_path, text))


def test_load_error_when_an_items_entry_is_not_a_mapping(tmp_path):
    with pytest.raises(BacklogLoadError):
        load_backlog(write_text(tmp_path, "items:\n  - GOAL-DCP-001\n"))


def test_no_load_error_for_semantically_invalid_but_structurally_sound_data(tmp_path):
    """The loader is structural; semantic breakage must survive to the validator."""
    backlog = load_backlog(write_items(tmp_path, [
        item_mapping(
            id="OPS-SAFE-*",                   # malformed id
            title="   ",                       # empty-ish title
            lane="SHARED",                     # wrong case for LANES
            state="NOT_A_STATE",               # unknown state
            priority="P9",                     # unknown priority
            risk="nuclear",                    # unknown risk
            target_repository="",              # missing target repository
            depends_on=["DCP-001", "OPS-SAFE-*", "OPS-SAFE-*"],  # shorthand, wildcard, dupe
            pid_path="pids/DOES-NOT-EXIST.md",
            architecture_refs=["architecture/DOES-NOT-EXIST.md"],
        ),
        item_mapping(id="CYCLE-001", depends_on=["CYCLE-002"]),
        item_mapping(id="CYCLE-002", depends_on=["CYCLE-001"]),
        item_mapping(id="SELF-001", depends_on=["SELF-001"]),
        item_mapping(id="LATE-001", state="FORGE_AUDIT", pid_path=None),  # MISSING_PID
    ]))

    assert len(backlog.items) == 5
    broken = backlog.items[0]
    assert broken.id == "OPS-SAFE-*"
    assert broken.lane == "SHARED"
    assert broken.state == "NOT_A_STATE"
    assert broken.priority == "P9"
    assert broken.risk == "nuclear"
    assert broken.target_repository == ""
    assert broken.depends_on == ("DCP-001", "OPS-SAFE-*", "OPS-SAFE-*")
    assert backlog.by_id["LATE-001"].pid_path is None


# ---------------------------------------------------------------------------
# repo_root resolution
# ---------------------------------------------------------------------------


def test_repo_root_is_parent_of_parent_for_a_temp_fixture(tmp_path):
    path = write_items(tmp_path, [item_mapping()])

    backlog = load_backlog(path)

    assert backlog.source_path == path
    assert backlog.repo_root == path.parent.parent
    assert backlog.repo_root == tmp_path


def test_fixture_repo_root_resolves_declared_paths_against_the_fixture_tree(tmp_path):
    (tmp_path / "pids").mkdir()
    (tmp_path / "pids" / "ALPHA-001.md").write_text("# Alpha\n", encoding="utf-8")
    path = write_items(tmp_path, [item_mapping(pid_path="pids/ALPHA-001.md")])

    backlog = load_backlog(path)
    item = backlog.items[0]

    assert (backlog.repo_root / item.pid_path).is_file()
    assert not (backlog.repo_root / "pids" / "MISSING.md").exists()


def test_load_backlog_accepts_a_string_path(tmp_path):
    path = write_items(tmp_path, [item_mapping()])

    backlog = load_backlog(str(path))

    assert backlog.source_path == pathlib.Path(path)
    assert backlog.repo_root == tmp_path


# ---------------------------------------------------------------------------
# Finding / sort_findings
# ---------------------------------------------------------------------------


def test_finding_as_line_with_item_id():
    finding = Finding("MISSING_FIELD", "GOAL-DCP-001", "risk is absent")

    assert finding.as_line() == "MISSING_FIELD GOAL-DCP-001: risk is absent"


def test_finding_as_line_without_item_id():
    finding = Finding("GENERATED_REGION_DRIFT", None, "backlog-table is stale")

    assert finding.as_line() == "GENERATED_REGION_DRIFT: backlog-table is stale"


def test_sort_findings_is_deterministic_and_order_independent():
    whole_file = Finding("ZEBRA_CODE", None, "whole-file finding")
    a_beta = Finding("ALPHA_CODE", "BETA-002", "beta message")
    a_alpha_1 = Finding("ALPHA_CODE", "ALPHA-001", "first message")
    a_alpha_2 = Finding("ALPHA_CODE", "ALPHA-001", "second message")
    expected = (a_alpha_1, a_alpha_2, a_beta, whole_file)

    shuffled = [a_beta, whole_file, a_alpha_2, a_alpha_1]

    assert model.sort_findings(shuffled) == expected
    assert model.sort_findings(reversed(shuffled)) == expected
    assert model.sort_findings(expected) == expected          # idempotent
    assert model.sort_findings(iter(shuffled)) == expected    # accepts any iterable


def test_sort_findings_orders_whole_file_findings_before_item_findings_of_same_code():
    whole_file = Finding("SAME_CODE", None, "whole file")
    item_level = Finding("SAME_CODE", "ALPHA-001", "item level")

    assert model.sort_findings([item_level, whole_file]) == (whole_file, item_level)


# ---------------------------------------------------------------------------
# Identifier rule regression guards
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("value", [
    "GOAL-DCP-001",
    "DARWIN-R1",
    "MT5-GW-001",
    "PAPER-E2E-001",
    "GOAL-CONTRACT-001",
    "OPS-SAFE-001",
])
def test_id_pattern_matches_canonical_ids(value):
    assert model.ID_PATTERN.match(value), value


@pytest.mark.parametrize("value", [
    "OPS-SAFE-*",        # wildcard
    "GOAL-*",            # wildcard
    "tron-t1",           # lowercase
    "TRON-T2,T3,T4",     # comma list
    "",                  # empty
    "GOAL-DCP-001 ",     # trailing whitespace
    " GOAL-DCP-001",     # leading whitespace
    "GOAL",              # no hyphenated segment
    "GOAL_DCP_001",      # underscores, not hyphens
    "1GOAL-001",         # must start with a letter
])
def test_id_pattern_rejects_non_canonical_ids(value):
    assert not model.ID_PATTERN.match(value), value


def test_shorthand_ids_are_syntactically_valid_and_must_be_caught_by_membership():
    """Why rejection is two-layered: no regex separates shorthand from canonical."""
    backlog = load_backlog()

    for shorthand in ("DCP-001", "CONTRACT-001", "CORE-001"):
        assert model.ID_PATTERN.match(shorthand), shorthand   # syntax layer passes
        assert shorthand not in backlog.by_id                 # membership layer rejects


@pytest.mark.parametrize("value", [
    "maff0000/GOAL",
    "maff0000/hermes",
    "maff0000/mt5-gateway",
    "maff0000/tron",
])
def test_repo_pattern_matches_declared_targets(value):
    assert model.REPO_PATTERN.match(value), value


@pytest.mark.parametrize("value", [
    "",
    "maff0000",
    "/GOAL",
    "maff0000/",
    "maff0000/GOAL/extra",
    "-maff0000/GOAL",
])
def test_repo_pattern_rejects_malformed_targets(value):
    assert not model.REPO_PATTERN.match(value), value


# ---------------------------------------------------------------------------
# Vocabularies
# ---------------------------------------------------------------------------


def test_vocabularies_match_the_delivery_state_machine():
    assert len(model.STATES) == 19
    assert len(set(model.STATES)) == 19
    assert model.STATES[0] == "DISCOVERED"
    assert model.STATES[-1] == "CANCELLED"
    assert model.LANES == {"shared", "research", "trading", "ops"}
    assert model.PRIORITIES == {"P0", "P1", "P2"}
    assert model.RISKS == {"low", "medium", "high", "capital"}
    assert model.ACCEPTED_TERMINAL_STATES <= set(model.STATES)
    assert model.PID_REQUIRED_STATES <= set(model.STATES)


def test_cancelled_is_terminal_but_not_accepted():
    assert "CANCELLED" in model.STATES
    assert "CANCELLED" not in model.ACCEPTED_TERMINAL_STATES


def test_in_flight_gates_are_not_accepted_terminal_states():
    for state in ("BLOCKED", "PO_ACCEPTANCE", "MATT_DECISION", "CANDIDATE"):
        assert state not in model.ACCEPTED_TERMINAL_STATES, state


def test_delivery_ready_requires_a_pid():
    """No PID = not DELIVERY_READY. This is the semantic the repair installed."""
    assert "DELIVERY_READY" in model.PID_REQUIRED_STATES
    assert "FORGE_AUDIT" in model.PID_REQUIRED_STATES


def test_every_delivery_state_from_delivery_ready_onward_requires_a_pid():
    """Asserted mechanically off STATES, not by listing states by hand.

    ``STATES`` is in state-machine order, so "DELIVERY_READY and every later
    delivery state" is exactly the run from ``DELIVERY_READY`` up to (not
    including) ``CANCELLED``. Comparing against that slice means a new
    delivery state added to the vocabulary cannot be quietly left out of
    ``PID_REQUIRED_STATES`` — this test fails until it is handled on purpose.
    """
    start = model.STATES.index("DELIVERY_READY")
    cancelled = model.STATES.index("CANCELLED")

    assert start < cancelled
    assert model.PID_REQUIRED_STATES == frozenset(model.STATES[start:cancelled])

    # Non-vacuity: the slice really is the whole delivery tail, not one state.
    assert len(model.PID_REQUIRED_STATES) == 13
    for state in ("ROGUE_DISPATCHED", "FORGE_BUILD", "REPAIR", "MERGED", "CLOSED"):
        assert state in model.PID_REQUIRED_STATES, state


def test_pre_delivery_states_do_not_require_a_pid():
    """An item legitimately has no PID before it is delivery-ready.

    ``PID_DRAFT`` is the state in which the PO authors the PID, so requiring
    one there would make the state unreachable in practice.
    """
    for state in (
        "DISCOVERED", "ARCHITECTURE_REQUIRED", "PID_DRAFT", "PO_REVIEW", "BLOCKED",
    ):
        assert state in model.STATES, state
        assert state not in model.PID_REQUIRED_STATES, state


def test_cancelled_does_not_require_a_pid():
    """Work can be abandoned from any state, including before a PID existed."""
    assert "CANCELLED" in model.STATES
    assert "CANCELLED" not in model.PID_REQUIRED_STATES


def test_the_canonical_sequence_is_declared_in_order():
    """ARCHITECTURE_REQUIRED -> PID_DRAFT -> PO_REVIEW -> DELIVERY_READY -> ...

    The ratified sequence, asserted as *order* within ``STATES`` rather than as
    prose: the PID-required boundary is defined by a slice of this tuple, so
    the order is load-bearing, not decorative.
    """
    sequence = (
        "ARCHITECTURE_REQUIRED", "PID_DRAFT", "PO_REVIEW", "DELIVERY_READY",
        "ROGUE_DISPATCHED", "FORGE_BUILD",
    )
    positions = [model.STATES.index(state) for state in sequence]

    assert positions == sorted(positions)


def test_item_fields_are_the_thirteen_canonical_fields_in_order():
    assert model.ITEM_FIELDS == (
        "id", "title", "lane", "component", "target_repository", "priority",
        "risk", "state", "depends_on", "po_gate", "matt_gate", "pid_path",
        "architecture_refs",
    )
