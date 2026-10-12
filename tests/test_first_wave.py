"""The PID's headline proof: the first wave is *calculable*, not declared.

``pids/GOAL-DCP-001.md`` requires that the work which becomes dispatchable
after this control plane closes can be computed from
``backlog/backlog.yaml``. These tests prove that end to end, and they are
written to be **non-vacuous**: an empty or universal answer fails them.

Four things are proven here, each of which a wrong implementation could
otherwise pass:

1. **Before** closure the wave is absent - so the "after" assertion is not
   measuring a list that was always present.
2. **After** the projection the ready set is *exactly* the eleven items -
   set equality, so an over-permissive rule fails just as loudly as an
   over-restrictive one.
3. The **state** half of the rule is independently load-bearing
   (``GOAL-DCP-002``).
4. The **dependency** half requires *all* declared dependencies, proven
   against ``LIVE-GATE-001``'s six - the item whose dependency list used to
   be written as the wildcard ``OPS-SAFE-*`` and which Central Architecture
   required be expanded to canonical complete ids.
"""

import ast
import io
import pathlib
import tokenize

import pytest
import yaml

from goal_dcp import docsync, model, readiness
from goal_dcp.model import load_backlog
from goal_dcp.readiness import effective_state, ready_items

#: The id whose closure is projected. This is the *input* to the readiness
#: rule - the work being accepted - not one of its results.
PROJECTION_ID = "GOAL-DCP-001"

#: The first wave this PID documents. Written out here, in the test, on
#: purpose: the test is the specification and the implementation must compute
#: this from the backlog without being told it.
FIRST_WAVE = (
    "ARES-CUR-001",
    "DARWIN-R1",
    "GOAL-CONTRACT-001",
    "HERMES-CUR-001",
    "MT5-GW-001",
    "OPS-CRED-001",
    "OPS-LEGACY-001",
    "OPS-SAFE-001",
    "OPS-SAFE-002",
    "OPS-SAFE-003",
    "TRON-T1",
)

#: Items that must stay out under the projection because a dependency of
#: theirs is still unmet (they depend on first-wave work, not on GOAL-DCP-001).
BLOCKED_BY_DEPENDENCIES = (
    "HERMES-FACT-001",
    "GOAL-CORE-001",
    "PAPER-E2E-001",
    "LIVE-GATE-001",
)


@pytest.fixture
def canonical():
    return load_backlog()


def ready_id_set(backlog, assume_closed=frozenset()):
    return {item.id for item in ready_items(backlog, assume_closed)}


# ---------------------------------------------------------------------------
# Before closure
# ---------------------------------------------------------------------------


def test_first_wave_is_absent_before_closure(canonical):
    """Nothing in the wave is ready while GOAL-DCP-001 is in FORGE_AUDIT.

    This is what makes the "after" assertion meaningful: the eleven items are
    specifically asserted *absent* first, so the projection is demonstrably
    what admits them.
    """
    assert len(FIRST_WAVE) == 11
    assert ready_items(canonical) == ()

    before = ready_id_set(canonical)
    for item_id in FIRST_WAVE:
        assert item_id in canonical.by_id, f"{item_id} is not declared at all"
        assert item_id not in before, f"{item_id} was ready before closure"


def test_the_wave_is_blocked_only_by_the_projected_item(canonical):
    """Each wave item is already DELIVERY_READY and waits on exactly one thing."""
    for item_id in FIRST_WAVE:
        item = canonical.by_id[item_id]
        assert item.state == "DELIVERY_READY"
        assert item.depends_on == (PROJECTION_ID,)


# ---------------------------------------------------------------------------
# After the projected closure
# ---------------------------------------------------------------------------


def test_projected_closure_yields_exactly_the_first_wave(canonical):
    """Set equality: no extras, none missing."""
    after = ready_id_set(canonical, frozenset({PROJECTION_ID}))

    assert after == set(FIRST_WAVE)


def test_first_wave_is_returned_sorted_by_id(canonical):
    items = ready_items(canonical, frozenset({PROJECTION_ID}))

    assert [item.id for item in items] == sorted(FIRST_WAVE)


def test_first_wave_payload_carries_each_items_target_repository(canonical):
    payload = readiness.readiness_payload(canonical, frozenset({PROJECTION_ID}))

    assert [entry["id"] for entry in payload["ready"]] == sorted(FIRST_WAVE)
    for entry in payload["ready"]:
        assert entry["target_repository"] == (
            canonical.by_id[entry["id"]].target_repository
        )


def test_the_projected_item_itself_is_not_in_the_wave(canonical):
    """A projected-closed item is closed, not dispatchable."""
    after = ready_id_set(canonical, frozenset({PROJECTION_ID}))

    assert PROJECTION_ID not in after


# ---------------------------------------------------------------------------
# The state half of the rule, independently
# ---------------------------------------------------------------------------


def test_state_gate_is_independently_load_bearing(canonical):
    """GOAL-DCP-002 proves the state clause does real work on its own.

    GOAL-DCP-002 depends only on GOAL-DCP-001, so under the projection its
    dependencies *are* fully satisfied - exactly like every first-wave item.
    The only thing keeping it out is its own state, ARCHITECTURE_REQUIRED.

    That is why this specific case proves the state half: if the
    implementation checked dependencies alone, GOAL-DCP-002 would appear in
    the answer, and ROGUE would dispatch work whose architecture has not been
    settled. No other assertion in this file separates the two clauses, since
    every first-wave item satisfies both.
    """
    assumed = frozenset({PROJECTION_ID})
    item = canonical.by_id["GOAL-DCP-002"]

    # Dependencies satisfied ...
    assert item.depends_on == (PROJECTION_ID,)
    assert effective_state(canonical.by_id[PROJECTION_ID], assumed) == "CLOSED"
    assert "CLOSED" in model.ACCEPTED_TERMINAL_STATES

    # ... own state is not DELIVERY_READY ...
    assert item.state == "ARCHITECTURE_REQUIRED"

    # ... so it stays out.
    assert "GOAL-DCP-002" not in ready_id_set(canonical, assumed)


# ---------------------------------------------------------------------------
# The dependency half of the rule
# ---------------------------------------------------------------------------


def test_items_with_unmet_dependencies_stay_out(canonical):
    after = ready_id_set(canonical, frozenset({PROJECTION_ID}))

    for item_id in BLOCKED_BY_DEPENDENCIES:
        assert item_id in canonical.by_id
        assert item_id not in after, f"{item_id} should still be blocked"


def test_live_gate_declares_six_resolvable_dependencies(canonical):
    """No wildcard survived the migration to canonical complete ids."""
    dependencies = canonical.by_id["LIVE-GATE-001"].depends_on

    assert len(dependencies) == 6
    assert len(set(dependencies)) == 6
    for dependency_id in dependencies:
        assert "*" not in dependency_id and "?" not in dependency_id
        assert dependency_id in canonical.by_id, "dependency must resolve"


def live_gate_dispatchable_copy(tmp_path, canonical):
    """A temp copy of the canonical backlog with LIVE-GATE-001 DELIVERY_READY.

    LIVE-GATE-001 is ``ARCHITECTURE_REQUIRED`` in canonical data, so the
    *state* clause alone would keep it out and the dependency clause could
    never be observed. Flipping only its state, in a temp copy, isolates the
    dependency clause. The canonical file is never mutated.
    """
    document = yaml.safe_load(canonical.source_path.read_text(encoding="utf-8"))
    for entry in document["items"]:
        if entry["id"] == "LIVE-GATE-001":
            entry["state"] = "DELIVERY_READY"

    backlog_dir = tmp_path / "backlog"
    backlog_dir.mkdir(parents=True, exist_ok=True)
    path = backlog_dir / "backlog.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=True), encoding="utf-8")
    return load_backlog(path)


def test_live_gate_needs_all_six_dependencies_closed(tmp_path, canonical):
    """It stays out until the sixth dependency closes - all, never any.

    This is the Central Architecture no-wildcard requirement proven
    mechanically: each of the six capital-safety prerequisites is load-bearing
    on its own, so a readiness rule that accepted "some OPS-SAFE work is
    done" would fail here.
    """
    backlog = live_gate_dispatchable_copy(tmp_path, canonical)
    item = backlog.by_id["LIVE-GATE-001"]
    assert item.state == "DELIVERY_READY"

    dependencies = sorted(item.depends_on)
    assert len(dependencies) == 6

    for count in range(6):
        projection = frozenset(dependencies[:count])
        assert "LIVE-GATE-001" not in ready_id_set(backlog, projection), (
            f"became ready with only {count} of 6 dependencies closed"
        )

    assert "LIVE-GATE-001" in ready_id_set(backlog, frozenset(dependencies))


def test_live_gate_stays_out_when_any_single_dependency_is_missing(
    tmp_path, canonical
):
    """Leave exactly one of the six open, six times over."""
    backlog = live_gate_dispatchable_copy(tmp_path, canonical)
    dependencies = sorted(backlog.by_id["LIVE-GATE-001"].depends_on)

    for held_open in dependencies:
        projection = frozenset(d for d in dependencies if d != held_open)
        assert "LIVE-GATE-001" not in ready_id_set(backlog, projection), (
            f"became ready while {held_open} was still open"
        )


# ---------------------------------------------------------------------------
# The documented wave is the computed wave
# ---------------------------------------------------------------------------


def test_generated_first_wave_region_lists_exactly_the_computed_wave(canonical):
    """The human document restates the computation, with no range notation."""
    rendered = docsync.render_first_wave(canonical)

    for item_id in FIRST_WAVE:
        assert f"`{item_id}`" in rendered
    assert ".." not in rendered, "range notation is not a canonical id"
    assert "*" not in rendered, "a wildcard is not a canonical id"
    assert rendered.count("\n- ") + 1 == len(FIRST_WAVE)


# ---------------------------------------------------------------------------
# No hard-coded readiness anywhere in the implementation
# ---------------------------------------------------------------------------


def code_only_source(path):
    """Return ``path``'s source with comments and docstrings removed.

    Prose may legitimately *mention* a work item - ``readiness.py`` cites the
    PID by path, for instance. Executable code may not. Stripping only
    comments and docstrings keeps every other string literal, which is
    precisely where a hard-coded readiness list would hide.
    """
    text = path.read_text(encoding="utf-8")

    docstring_lines = set()
    for node in ast.walk(ast.parse(text)):
        if not isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            continue
        if not node.body:
            continue
        first = node.body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            docstring_lines.update(range(first.lineno, first.end_lineno + 1))

    comment_cut = {}
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type == tokenize.COMMENT:
            row, column = token.start
            comment_cut[row] = min(column, comment_cut.get(row, column))

    kept = []
    for number, line in enumerate(text.splitlines(), start=1):
        if number in docstring_lines:
            continue
        kept.append(line[: comment_cut[number]] if number in comment_cut else line)
    return "\n".join(kept)


def test_code_only_source_actually_strips_prose():
    """Guard the guard: a stripper that returned "" would pass everything."""
    source = code_only_source(pathlib.Path(readiness.__file__))

    raw = pathlib.Path(readiness.__file__).read_text(encoding="utf-8")

    assert "def ready_items" in source
    assert "ACCEPTED_TERMINAL_STATES" in source
    # Prose really is gone, and really was there to begin with.
    assert "advisory" in raw
    assert "advisory" not in source


def test_no_first_wave_id_is_hard_coded_in_the_implementation():
    """The wave must fall out of the rule, never be typed into it."""
    for module in (readiness, docsync):
        source = code_only_source(pathlib.Path(module.__file__))
        for item_id in FIRST_WAVE:
            assert item_id not in source, (
                f"{module.__name__} hard-codes first-wave id {item_id}"
            )


def test_readiness_code_names_no_work_item_and_no_id_comparison(canonical):
    """readiness.py may name states; it may never name a work item."""
    source = code_only_source(pathlib.Path(readiness.__file__))

    assert sorted(canonical.by_id)  # non-vacuous
    for item_id in canonical.by_id:
        assert item_id not in source
    assert "item.id ==" not in source


def test_docsync_code_names_only_the_projection_input(canonical):
    """docsync.py names GOAL-DCP-001 as the projection input, and nothing else.

    That one id is the question being asked ("once this closes, what is
    dispatchable?"), not a cached answer: the answer still comes from
    ``ready_items``.
    """
    source = code_only_source(pathlib.Path(docsync.__file__))

    assert PROJECTION_ID in source
    for item_id in canonical.by_id:
        if item_id == PROJECTION_ID:
            continue
        assert item_id not in source
    assert "item.id ==" not in source
