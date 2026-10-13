"""Deterministic delivery readiness, and the next PID-authoring wave.

Two questions are answered here, and they are deliberately *different*
questions with different answers and different output keys.

**1. Dispatch readiness** — which work could ROGUE genuinely hand to FORGE
right now? Three clauses, all required::

    state == DELIVERY_READY
    AND the item declares a PID (pid_path is a non-empty string)
    AND every dependency resolves to a declared item in an accepted
        terminal state

**2. The next PID-authoring wave** — which work is waiting on the PO to
author a canonical PID, and nothing else? Two clauses, all required::

    state == PID_DRAFT
    AND every dependency resolves to a declared item in an accepted
        terminal state

There is no PID clause in (2): an item in ``PID_DRAFT`` is by definition
pre-PID, and the wave exists precisely to name the PIDs that need writing.
Items in this wave are **not** FORGE-dispatchable, and must never be
described as such. FORGE dispatch requires an approved canonical PID and then
``DELIVERY_READY``.

The dependency clause is shared by both rules (:func:`_dependencies_satisfied`)
so the two waves cannot drift apart.

Both rules are implemented **once, generically**. There is deliberately no
list of wave ids here, and no per-id special case anywhere: a wave is an
*output* of a rule applied to ``backlog/backlog.yaml``, never an input. A
hard-coded list would make the backlog advisory and the tool authoritative,
which is exactly backwards.

**The PID requirement is two-layered**, the same shape as the two-layer
identifier rule in ``goal_dcp.model``:

1. *Data* — this module requires the item to **declare** a PID. That is a
   pure check on the loaded value, and it is all that can be decided here.
2. *Validation* — ``goal_dcp.validate`` requires the declared PID file to
   exist, to be readable, to be structurally valid as a PID, and for its
   metadata to agree with the backlog (``MISSING_PID``,
   ``PID_FILE_NOT_FOUND``, ``PID_INVALID``, ``BACKLOG_PID_MISMATCH``).

Layer 2 gained ``PID_INVALID`` without this module gaining a clause, and that
is the design holding rather than an omission. Judging whether a declared PID
is a PID means reading the file, which this module must never do; the
validate-before-answer gate in ``tools/goal-ready`` is what joins the two
halves, so it needs no second invariant check for the new code either.

``tools/goal-ready`` validates first and refuses to answer at all from an
invalid backlog, so a *successful* readiness answer can never contain an item
whose PID does not exist. Both layers are required; neither alone is
sufficient — layer 1 alone would accept a declared path pointing at nothing,
and layer 2 alone lives in a different module that readiness must not call,
because calling it would mean reading files from here.

Two properties matter as much as the rules themselves:

* **Fail closed.** A dependency that does not resolve to a declared item
  makes the dependent item *not* ready. Unknown, shorthand, wildcard and
  typo'd dependencies therefore never unblock work by default. This is the
  membership half of the two-layer identifier rule described in
  ``backlog/SCHEMA.md``; the syntax half belongs to the validator.
* **Purity.** Nothing here reads a file, touches the network, prints, or
  mutates its input. The only input is an already-loaded
  :class:`~goal_dcp.model.Backlog`.

``assume_closed`` is a what-if projection for planning: "if these items were
closed, what would each of these two answers become?". It never writes
anything and never changes the backlog; it only changes the answer to that
hypothetical.
"""

from __future__ import annotations

from typing import Iterable

from goal_dcp.model import ACCEPTED_TERMINAL_STATES, Backlog, Item

#: The one state an item itself must be in to be FORGE-dispatchable. It is
#: necessary and not sufficient: the item must also declare a PID (see the
#: module docstring's two-layer rule) and have every dependency satisfied.
DISPATCHABLE_STATE = "DELIVERY_READY"

#: The one state an item itself must be in to belong to the next PID-authoring
#: wave. These items are awaiting PO PID authoring; they are **not**
#: FORGE-dispatchable.
PID_AUTHORING_STATE = "PID_DRAFT"

#: The state an ``assume_closed`` projection pretends an item has reached.
#: ``CLOSED`` is a member of ``ACCEPTED_TERMINAL_STATES``, so projecting an
#: item closed satisfies dependencies on it.
PROJECTED_STATE = "CLOSED"

#: Payload key for the FORGE-dispatchable answer. This is the published,
#: consumed contract; nothing else may be emitted under it.
READY_KEY = "ready"

#: Payload key for the PID-authoring wave. A separate key on purpose: these
#: items are not dispatchable, so putting them under ``READY_KEY`` would hand
#: ROGUE work FORGE cannot build.
PID_AUTHORING_WAVE_KEY = "pid_authoring_wave"


class UnknownAssumedId(Exception):
    """An ``assume_closed`` id is not declared by any backlog item.

    Raised rather than ignored on purpose. A typo'd projection id that was
    silently dropped would produce a confidently wrong answer — most likely an
    empty ready list that reads as "nothing to do" — and ROGUE dispatches on
    this output.
    """


def effective_state(item: Item, assume_closed: frozenset[str] = frozenset()) -> str:
    """Return ``item``'s state under the ``assume_closed`` projection.

    ``PROJECTED_STATE`` when ``item.id`` is in ``assume_closed``, otherwise the
    item's declared state, unconverted.

    The ``isinstance`` guard keeps this total over structurally loaded but
    semantically invalid data: ``load_backlog`` carries a missing or
    wrong-typed ``id`` through as-is, and an unhashable id must not raise here.
    Such an item simply never matches a projection; the validator is what
    reports it.
    """
    if isinstance(item.id, str) and item.id in assume_closed:
        return PROJECTED_STATE
    return item.state


def _assumed(backlog: Backlog, assume_closed: Iterable[str]) -> frozenset[str]:
    """Normalise and check a projection set against declared ids."""
    assumed = frozenset(assume_closed)
    unknown = sorted(i for i in assumed if i not in backlog.by_id)
    if unknown:
        raise UnknownAssumedId(
            "assume_closed contains ids no backlog item declares: "
            + ", ".join(unknown)
        )
    return assumed


def _dependency_satisfied(
    backlog: Backlog, dependency_id: object, assumed: frozenset[str]
) -> bool:
    """True only when ``dependency_id`` resolves and is accepted-terminal.

    Fails closed on anything else: a non-string entry (invalid data), an
    unknown id, shorthand, or a declared item that has not reached an accepted
    terminal state.
    """
    if not isinstance(dependency_id, str):
        return False
    dependency = backlog.by_id.get(dependency_id)
    if dependency is None:
        return False
    return effective_state(dependency, assumed) in ACCEPTED_TERMINAL_STATES


def _dependencies_satisfied(
    backlog: Backlog, item: Item, assumed: frozenset[str]
) -> bool:
    """True when *every* declared dependency of ``item`` is satisfied.

    Shared by both wave rules so they cannot drift apart: a change to what
    "satisfied" means must change both answers or neither. An item with no
    dependencies satisfies this vacuously.
    """
    return all(
        _dependency_satisfied(backlog, dependency_id, assumed)
        for dependency_id in item.depends_on
    )


def _declares_pid(item: Item) -> bool:
    """True when ``item`` declares a PID: a non-empty, non-whitespace string.

    This is the *data* layer of the two-layer PID rule (see the module
    docstring). It deliberately does not ask whether the file exists — that is
    the validator's layer, and asking here would break purity. The
    ``isinstance`` guard keeps this total over structurally loaded but
    semantically invalid data, where ``pid_path`` may hold any type at all.
    """
    return isinstance(item.pid_path, str) and bool(item.pid_path.strip())


def _is_ready(backlog: Backlog, item: Item, assumed: frozenset[str]) -> bool:
    """The whole dispatch-readiness rule, for one item, with no special cases."""
    if effective_state(item, assumed) != DISPATCHABLE_STATE:
        return False
    if not _declares_pid(item):
        return False
    return _dependencies_satisfied(backlog, item, assumed)


def _is_pid_authoring(backlog: Backlog, item: Item, assumed: frozenset[str]) -> bool:
    """The whole PID-authoring-wave rule, for one item, with no special cases.

    No PID clause: the state under test *is* the pre-PID state.
    """
    if effective_state(item, assumed) != PID_AUTHORING_STATE:
        return False
    return _dependencies_satisfied(backlog, item, assumed)


def _id_sort_key(item: Item) -> str:
    """Total, never-raising sort key by id.

    Non-string ids (invalid data only) sort together and keep their relative
    source order, because :func:`sorted` is stable. Output therefore stays
    deterministic even for a backlog the validator would reject.
    """
    return item.id if isinstance(item.id, str) else ""


def ready_items(
    backlog: Backlog, assume_closed: frozenset[str] = frozenset()
) -> tuple[Item, ...]:
    """Return the FORGE-dispatchable items, sorted by id.

    An item is ready **iff** all three hold, with no other condition and no
    special-casing of any id:

    1. ``effective_state(item) == "DELIVERY_READY"``;
    2. the item declares a PID — ``pid_path`` is a non-empty string; and
    3. every entry in ``item.depends_on`` resolves to a declared item whose
       ``effective_state`` is in ``ACCEPTED_TERMINAL_STATES``.

    An item with no dependencies satisfies (3) vacuously. A dependency that
    does not resolve makes the item **not** ready.

    Clause (2) is the data half of the two-layer PID rule: it proves the item
    *claims* a PID, not that the PID exists. ``tools/goal-ready`` validates the
    backlog before answering and refuses to answer from an invalid one, so a
    successful answer cannot contain an item whose declared PID is absent,
    unreadable, not actually a PID, or in disagreement with the backlog.

    Raises :class:`UnknownAssumedId` if ``assume_closed`` names an id no item
    declares.
    """
    assumed = _assumed(backlog, assume_closed)
    ready = [item for item in backlog.items if _is_ready(backlog, item, assumed)]
    return tuple(sorted(ready, key=_id_sort_key))


def pid_authoring_wave_items(
    backlog: Backlog, assume_closed: frozenset[str] = frozenset()
) -> tuple[Item, ...]:
    """Return the next PID-authoring wave, sorted by id.

    An item is in the wave **iff** both hold, with no special-casing of any id:

    1. ``effective_state(item) == "PID_DRAFT"``; and
    2. every entry in ``item.depends_on`` resolves to a declared item whose
       ``effective_state`` is in ``ACCEPTED_TERMINAL_STATES``.

    These are the items whose architecture intent is settled and whose
    prerequisites are met, so the only thing standing between them and
    delivery is an approved canonical PID. They are **not** FORGE-dispatchable
    and must not be reported as if they were: that is why this answer carries
    its own key.

    Raises :class:`UnknownAssumedId` if ``assume_closed`` names an id no item
    declares.
    """
    assumed = _assumed(backlog, assume_closed)
    wave = [item for item in backlog.items if _is_pid_authoring(backlog, item, assumed)]
    return tuple(sorted(wave, key=_id_sort_key))


def _entry(item: Item, with_pid: bool) -> dict:
    """One payload entry for ``item``, shared by both payload shapes.

    The two-key default is the published contract shape; ``with_pid`` adds
    ``pid_path`` and nothing else, identically in either mode.
    """
    entry = {"id": item.id, "target_repository": item.target_repository}
    if with_pid:
        entry["pid_path"] = item.pid_path
    return entry


def readiness_payload(
    backlog: Backlog,
    assume_closed: frozenset[str] = frozenset(),
    with_pid: bool = False,
) -> dict:
    """Return the readiness answer in the shape ``pids/GOAL-DCP-001.md`` documents.

    ``{"ready": [{"id": ..., "target_repository": ...}, ...]}``, entries sorted
    by id. ``with_pid=True`` adds ``"pid_path"`` to each entry.

    A ready item always declares a PID, so ``pid_path`` is never ``null`` in
    this payload; that is clause (2) of :func:`ready_items`, not a coincidence.

    The default shape carries exactly the two keys the PID's example shows and
    nothing else: it is a consumed contract, so extra keys are a breaking
    change, not a convenience.
    """
    return {
        READY_KEY: [
            _entry(item, with_pid) for item in ready_items(backlog, assume_closed)
        ]
    }


def pid_authoring_wave_payload(
    backlog: Backlog,
    assume_closed: frozenset[str] = frozenset(),
    with_pid: bool = False,
) -> dict:
    """Return the PID-authoring wave as a payload, entries sorted by id.

    ``{"pid_authoring_wave": [{"id": ..., "target_repository": ...}, ...]}``,
    with the same entry shape and the same ``with_pid`` behaviour as
    :func:`readiness_payload`.

    It deliberately does **not** reuse :data:`READY_KEY`. ``ready`` is the
    published FORGE-dispatchable contract; an item here has no PID yet, so
    emitting it under that key would tell ROGUE to dispatch work FORGE cannot
    build. ``with_pid`` therefore renders ``null`` for these items, which is
    the honest answer and the reason the wave exists.
    """
    return {
        PID_AUTHORING_WAVE_KEY: [
            _entry(item, with_pid)
            for item in pid_authoring_wave_items(backlog, assume_closed)
        ]
    }
