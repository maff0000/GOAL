"""The headline proof: the next wave is *calculable*, not declared.

The file name is unchanged because committed delivery evidence cites it. What
it proves has changed, and the change is the point of this round.

The work that becomes independent once this control plane closes is **not**
FORGE-dispatchable work. Those eleven items have no canonical PID, and no PID
means not ``DELIVERY_READY``: they sit in ``PID_DRAFT``, and what they are
waiting on is the Product Owner authoring and approving a PID for each. So
what is computed here is the next **PID-authoring wave**, and the separate
question "what could FORGE be dispatched against?" correctly answers *nothing*
until those PIDs exist.

Both answers are proven, and both are proven **non-vacuous**: an empty or
universal answer fails these tests.

Six things are proven here, each of which a wrong implementation could
otherwise pass:

1. **Before** closure the wave is absent - so the "after" assertion is not
   measuring a list that was always present.
2. **After** the projection the wave is *exactly* the eleven items - set
   equality plus a length assertion, so an over-permissive rule fails just as
   loudly as an over-restrictive one.
3. The **state** clause of the wave rule is independently load-bearing
   (``GOAL-DCP-002``).
4. The **dependency** clause of the wave rule is independently load-bearing -
   canonical data cannot show this, because every ``PID_DRAFT`` item depends
   only on the projected id, so it is shown against a temp copy.
5. The dependency clause requires *all* declared dependencies, proven against
   ``LIVE-GATE-001``'s six - the item whose dependency list used to be written
   as the wildcard ``OPS-SAFE-*`` and which Central Architecture required be
   expanded to canonical complete ids.
6. The **dispatch** answer stays empty throughout, under every projection
   these tests apply, because nothing in the wave declares a PID.
"""

import ast
import io
import pathlib
import tokenize

import pytest
import yaml

from goal_dcp import docsync, model, readiness
from goal_dcp.model import load_backlog
from goal_dcp.readiness import (
    effective_state,
    pid_authoring_wave_items,
    ready_items,
)

#: The id whose closure is projected. This is the *input* to the wave rule -
#: the work being accepted - not one of its results.
PROJECTION_ID = "GOAL-DCP-001"

#: The next PID-authoring wave. Written out here, in the test, on purpose: the
#: test is the specification and the implementation must compute this from the
#: backlog without being told it.
PID_AUTHORING_WAVE = (
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
#: theirs is still unmet (they depend on wave work, not on GOAL-DCP-001).
BLOCKED_BY_DEPENDENCIES = (
    "HERMES-FACT-001",
    "GOAL-CORE-001",
    "PAPER-E2E-001",
    "LIVE-GATE-001",
)

#: An item that depends on a wave item rather than on the projected id, used
#: to prove the wave's dependency clause against a temp copy.
DEPENDS_ON_WAVE_WORK = "HERMES-FACT-001"


@pytest.fixture
def canonical():
    return load_backlog()


def wave_id_set(backlog, assume_closed=frozenset()):
    return {item.id for item in pid_authoring_wave_items(backlog, assume_closed)}


def ready_id_set(backlog, assume_closed=frozenset()):
    return {item.id for item in ready_items(backlog, assume_closed)}


def write_copy(tmp_path, document):
    """Write ``document`` as a backlog under ``tmp_path`` and load it.

    ``repo_root`` is the loaded path's parent-of-parent, so the copy resolves
    ``tmp_path`` as its own root and nothing it declares reaches the real
    repository. The canonical file is read, never written.
    """
    backlog_dir = tmp_path / "backlog"
    backlog_dir.mkdir(parents=True, exist_ok=True)
    path = backlog_dir / "backlog.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=True), encoding="utf-8")
    return load_backlog(path)


# ---------------------------------------------------------------------------
# Before closure
# ---------------------------------------------------------------------------


def test_the_wave_is_absent_before_closure(canonical, tmp_path):
    """Nothing is in the wave while GOAL-DCP-001 is in FORGE_AUDIT.

    The canonical backlog now has GOAL-DCP-001 ``CLOSED``, so the "before"
    state is reconstructed on a throwaway copy with that one state reverted.

    This is what makes the "after" assertion meaningful: the eleven items are
    specifically asserted *absent* first, so the projection is demonstrably
    what admits them.
    """
    assert len(PID_AUTHORING_WAVE) == 11
    document = yaml.safe_load(canonical.source_path.read_text(encoding="utf-8"))
    for entry in document["items"]:
        if entry["id"] == PROJECTION_ID:
            entry["state"] = "FORGE_AUDIT"
    before_backlog = write_copy(tmp_path, document)
    assert pid_authoring_wave_items(before_backlog) == ()
    assert wave_id_set(canonical) == set(PID_AUTHORING_WAVE)

    before = wave_id_set(before_backlog)
    for item_id in PID_AUTHORING_WAVE:
        assert item_id in canonical.by_id, f"{item_id} is not declared at all"
        assert item_id not in before, f"{item_id} was in the wave before closure"


def test_nothing_is_forge_dispatchable_before_or_after_the_projection(canonical):
    """The dispatch answer is empty, and that is the honest answer.

    The eleven have no canonical PID, so closing GOAL-DCP-001 does not make
    them dispatchable - it makes their PIDs the next thing to write. A tool
    that reported them as ``ready`` would be handing ROGUE work FORGE cannot
    build, which is the defect this round repaired.
    """
    assert ready_items(canonical) == ()
    assert ready_items(canonical, frozenset({PROJECTION_ID})) == ()


def test_the_wave_is_blocked_only_by_the_projected_item(canonical):
    """Each wave item is in PID_DRAFT, has no PID, and waits on exactly one thing."""
    for item_id in PID_AUTHORING_WAVE:
        item = canonical.by_id[item_id]
        assert item.state == "PID_DRAFT", item_id
        assert item.pid_path is None, item_id
        assert item.depends_on == (PROJECTION_ID,), item_id


# ---------------------------------------------------------------------------
# After the projected closure
# ---------------------------------------------------------------------------


def test_projected_closure_yields_exactly_the_pid_authoring_wave(canonical):
    """Set equality: no extras, none missing."""
    after = wave_id_set(canonical, frozenset({PROJECTION_ID}))

    assert after == set(PID_AUTHORING_WAVE)
    assert len(after) == 11


def test_the_wave_is_returned_sorted_by_id(canonical):
    items = pid_authoring_wave_items(canonical, frozenset({PROJECTION_ID}))

    assert [item.id for item in items] == sorted(PID_AUTHORING_WAVE)


def test_wave_payload_carries_each_items_target_repository(canonical):
    payload = readiness.pid_authoring_wave_payload(
        canonical, frozenset({PROJECTION_ID})
    )
    entries = payload[readiness.PID_AUTHORING_WAVE_KEY]

    assert [entry["id"] for entry in entries] == sorted(PID_AUTHORING_WAVE)
    for entry in entries:
        assert entry["target_repository"] == (
            canonical.by_id[entry["id"]].target_repository
        )


def test_the_projected_item_itself_is_not_in_the_wave(canonical):
    """A projected-closed item is closed, not awaiting a PID."""
    after = wave_id_set(canonical, frozenset({PROJECTION_ID}))

    assert PROJECTION_ID not in after


# ---------------------------------------------------------------------------
# The state clause of the wave rule, independently
# ---------------------------------------------------------------------------


def test_state_gate_is_independently_load_bearing(canonical):
    """GOAL-DCP-002 proves the state clause does real work on its own.

    GOAL-DCP-002 depends only on GOAL-DCP-001, so under the projection its
    dependencies *are* fully satisfied - exactly like every wave item. The
    only thing keeping it out is its own state, ARCHITECTURE_REQUIRED.

    That is why this specific case proves the state clause: if the
    implementation checked dependencies alone, GOAL-DCP-002 would appear in the
    answer, and the PO would be asked to author a PID for work whose
    architecture has not been settled. No other assertion in this file
    separates the two clauses, since every wave item satisfies both.
    """
    assumed = frozenset({PROJECTION_ID})
    item = canonical.by_id["GOAL-DCP-002"]

    # Dependencies satisfied ...
    assert item.depends_on == (PROJECTION_ID,)
    assert effective_state(canonical.by_id[PROJECTION_ID], assumed) == "CLOSED"
    assert "CLOSED" in model.ACCEPTED_TERMINAL_STATES

    # ... own state is not PID_DRAFT ...
    assert item.state == "ARCHITECTURE_REQUIRED"

    # ... so it stays out of both answers.
    assert "GOAL-DCP-002" not in wave_id_set(canonical, assumed)
    assert "GOAL-DCP-002" not in ready_id_set(canonical, assumed)


# ---------------------------------------------------------------------------
# The dependency clause of the wave rule
# ---------------------------------------------------------------------------


def test_items_with_unmet_dependencies_stay_out(canonical):
    after = wave_id_set(canonical, frozenset({PROJECTION_ID}))

    for item_id in BLOCKED_BY_DEPENDENCIES:
        assert item_id in canonical.by_id
        assert item_id not in after, f"{item_id} should still be blocked"


def pid_draft_with_an_open_dependency(tmp_path, canonical):
    """A temp copy with one extra item flipped to PID_DRAFT, dependency open.

    Canonical data cannot prove the wave's dependency clause: every
    ``PID_DRAFT`` item depends only on ``GOAL-DCP-001``, so under the
    projection the dependency clause is satisfied for all of them and an
    implementation that ignored dependencies entirely would still produce the
    right eleven.

    ``HERMES-FACT-001`` depends on ``HERMES-CUR-001`` - a wave item, which is
    itself in ``PID_DRAFT`` and therefore *not* accepted-terminal even under
    the projection. Flipping only its state isolates the dependency clause.
    The canonical file is never mutated.
    """
    document = yaml.safe_load(canonical.source_path.read_text(encoding="utf-8"))
    for entry in document["items"]:
        if entry["id"] == DEPENDS_ON_WAVE_WORK:
            entry["state"] = "PID_DRAFT"
    return write_copy(tmp_path, document)


def test_a_pid_draft_item_with_an_unmet_dependency_stays_out(tmp_path, canonical):
    """The wave's dependency clause, isolated and independently load-bearing."""
    backlog = pid_draft_with_an_open_dependency(tmp_path, canonical)
    item = backlog.by_id[DEPENDS_ON_WAVE_WORK]
    assumed = frozenset({PROJECTION_ID})

    # State clause satisfied, dependency clause not.
    assert item.state == "PID_DRAFT"
    assert len(item.depends_on) == 1
    blocker = item.depends_on[0]
    assert effective_state(backlog.by_id[blocker], assumed) == "PID_DRAFT"
    assert "PID_DRAFT" not in model.ACCEPTED_TERMINAL_STATES

    assert DEPENDS_ON_WAVE_WORK not in wave_id_set(backlog, assumed)

    # Non-vacuity: the wave is otherwise computed normally in this copy, and
    # the item joins it the moment its one dependency is also projected closed.
    assert wave_id_set(backlog, assumed) == set(PID_AUTHORING_WAVE)
    assert DEPENDS_ON_WAVE_WORK in wave_id_set(
        backlog, frozenset({PROJECTION_ID, blocker})
    )


def test_live_gate_declares_six_resolvable_dependencies(canonical):
    """No wildcard survived the migration to canonical complete ids."""
    dependencies = canonical.by_id["LIVE-GATE-001"].depends_on

    assert len(dependencies) == 6
    assert len(set(dependencies)) == 6
    for dependency_id in dependencies:
        assert "*" not in dependency_id and "?" not in dependency_id
        assert dependency_id in canonical.by_id, "dependency must resolve"


def live_gate_dispatchable_copy(tmp_path, canonical):
    """A temp copy with LIVE-GATE-001 DELIVERY_READY *and* declaring a real PID.

    LIVE-GATE-001 is ``ARCHITECTURE_REQUIRED`` in canonical data, so the state
    clause alone would keep it out and the dependency clause could never be
    observed. Flipping only its state, in a temp copy, isolates the dependency
    clause.

    The PID is written explicitly, as a real file under the copy's own root,
    and the caller asserts it resolves. Without it the *PID clause* would now
    be what excludes the item and this whole proof would silently stop testing
    dependencies at all - it would pass for the wrong reason, which is worse
    than failing. The canonical file is never mutated.
    """
    document = yaml.safe_load(canonical.source_path.read_text(encoding="utf-8"))
    declared = "pids/LIVE-GATE-001.md"
    for entry in document["items"]:
        if entry["id"] == "LIVE-GATE-001":
            entry["state"] = "DELIVERY_READY"
            entry["pid_path"] = declared

    pids_dir = tmp_path / "pids"
    pids_dir.mkdir(parents=True, exist_ok=True)
    (pids_dir / "LIVE-GATE-001.md").write_text(
        "# LIVE-GATE-001 — fixture PID for the dependency-clause proof\n",
        encoding="utf-8",
    )

    backlog = write_copy(tmp_path, document)

    item = backlog.by_id["LIVE-GATE-001"]
    assert item.state == "DELIVERY_READY"
    assert item.pid_path == declared
    assert (backlog.repo_root / item.pid_path).is_file(), (
        "the declared PID must resolve to a real file under the copy's own "
        "root, or the PID clause silently becomes what excludes this item"
    )
    return backlog


def test_live_gate_needs_all_six_dependencies_closed(tmp_path, canonical):
    """It stays out until the sixth dependency closes - all, never any.

    This is the Central Architecture no-wildcard requirement proven
    mechanically: each of the six capital-safety prerequisites is load-bearing
    on its own, so a readiness rule that accepted "some OPS-SAFE work is done"
    would fail here.
    """
    backlog = live_gate_dispatchable_copy(tmp_path, canonical)
    item = backlog.by_id["LIVE-GATE-001"]

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


def test_generated_region_lists_exactly_the_computed_wave(canonical):
    """The human document restates the computation, with no range notation."""
    rendered = docsync.render_pid_authoring_wave(canonical)

    for item_id in PID_AUTHORING_WAVE:
        assert f"`{item_id}`" in rendered
    assert ".." not in rendered, "range notation is not a canonical id"
    assert "*" not in rendered, "a wildcard is not a canonical id"
    assert rendered.count("\n- ") + 1 == len(PID_AUTHORING_WAVE)


def test_the_generated_region_is_named_for_what_it_now_contains():
    """A region called 'first-wave' rendering PID-authoring work would mislead."""
    regions = {
        name for _, names in docsync.GENERATED_FILES for name in names
    }

    assert "pid-authoring-wave" in regions
    assert "first-wave" not in regions


def test_the_empty_case_reads_correctly_for_this_wave(tmp_path, canonical):
    """The empty message must describe *this* wave, not dispatchability.

    The message is reached by emptying the wave in a temp copy - every
    ``PID_DRAFT`` item moved back to ``ARCHITECTURE_REQUIRED`` - so the prose
    under test is the prose a reader would actually see.
    """
    rendered = docsync.render_pid_authoring_wave(canonical)
    assert rendered.startswith("- ")  # non-vacuity: the populated case is a list

    document = yaml.safe_load(canonical.source_path.read_text(encoding="utf-8"))
    for entry in document["items"]:
        if entry["state"] == "PID_DRAFT":
            entry["state"] = "ARCHITECTURE_REQUIRED"

    emptied = docsync.render_pid_authoring_wave(write_copy(tmp_path, document))

    assert emptied.startswith("_") and emptied.endswith("_")
    assert "dispatchable" not in emptied.lower()
    assert "PID authoring" in emptied


# ---------------------------------------------------------------------------
# No hard-coded wave or readiness list anywhere in the implementation
# ---------------------------------------------------------------------------


def code_only_source(path):
    """Return ``path``'s source with comments and docstrings removed.

    Prose may legitimately *mention* a work item - ``readiness.py`` cites the
    PID by path, for instance. Executable code may not. Stripping only
    comments and docstrings keeps every other string literal, which is
    precisely where a hard-coded wave list would hide.
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
    assert "def pid_authoring_wave_items" in source
    assert "ACCEPTED_TERMINAL_STATES" in source
    # Prose really is gone, and really was there to begin with.
    assert "advisory" in raw
    assert "advisory" not in source


def test_the_hard_coded_list_guard_has_teeth(tmp_path):
    """A hard-coded wave list must fail the suite, so prove the guard sees one.

    Without this, the no-hard-coding assertions below could be passing because
    the stripper hides executable code rather than because the code is clean.
    The id is planted in three places prose could not excuse: a list literal,
    a comparison and a dict key.
    """
    planted = PID_AUTHORING_WAVE[0]
    module = tmp_path / "planted.py"
    module.write_text(
        '"""A docstring naming ' + planted + ' is allowed."""\n'
        "# ...and so is a comment naming " + planted + "\n"
        "WAVE = [" + repr(planted) + "]\n"
        "def f(item):\n"
        "    return item.id == " + repr(planted) + "\n"
        "LOOKUP = {" + repr(planted) + ": 1}\n",
        encoding="utf-8",
    )

    source = code_only_source(module)

    assert source.count(planted) == 3, "the guard must see every planted copy"
    assert "item.id ==" in source
    assert "A docstring naming" not in source
    assert "and so is a comment" not in source


def test_no_wave_id_is_hard_coded_in_the_implementation():
    """The wave must fall out of the rule, never be typed into it."""
    for module in (readiness, docsync):
        source = code_only_source(pathlib.Path(module.__file__))
        for item_id in PID_AUTHORING_WAVE:
            assert item_id not in source, (
                f"{module.__name__} hard-codes wave id {item_id}"
            )


def test_readiness_code_names_no_work_item_and_no_id_comparison(canonical):
    """readiness.py may name states; it may never name a work item."""
    source = code_only_source(pathlib.Path(readiness.__file__))

    assert sorted(canonical.by_id)  # non-vacuous
    for item_id in canonical.by_id:
        assert item_id not in source
    assert "item.id ==" not in source

    # Non-vacuity: both rules really are implemented in the source scanned.
    assert "def _is_ready" in source
    assert "def _is_pid_authoring" in source
    assert "def _dependencies_satisfied" in source


def test_docsync_code_names_only_the_projection_input(canonical):
    """docsync.py names GOAL-DCP-001 as the projection input, and nothing else.

    That one id is the question being asked ("once this closes, which items
    are waiting only on a PID?"), not a cached answer: the answer still comes
    from ``pid_authoring_wave_items``.
    """
    source = code_only_source(pathlib.Path(docsync.__file__))

    assert PROJECTION_ID in source
    for item_id in canonical.by_id:
        if item_id == PROJECTION_ID:
            continue
        assert item_id not in source
    assert "item.id ==" not in source

    # Non-vacuity: the renderer scanned is the one that produces the region.
    assert "def render_pid_authoring_wave" in source
    assert "pid_authoring_wave_items" in source
