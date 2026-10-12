"""Deterministic delivery readiness.

Readiness answers one question for ROGUE: *which work is mechanically
dispatchable right now?* The rule is the one declared in
``pids/GOAL-DCP-001.md`` and nothing more::

    state == DELIVERY_READY
    AND every dependency resolves to a declared item in an accepted
        terminal state

It is implemented **once, generically**. There is deliberately no list of
"first wave" ids here, and no per-id special case anywhere: the first wave is
an *output* of this rule applied to ``backlog/backlog.yaml``, not an input. A
hard-coded readiness list would make the backlog advisory and the tool
authoritative, which is exactly backwards.

Two properties matter as much as the rule itself:

* **Fail closed.** A dependency that does not resolve to a declared item
  makes the dependent item *not* ready. Unknown, shorthand, wildcard and
  typo'd dependencies therefore never unblock work by default. This is the
  membership half of the two-layer identifier rule described in
  ``backlog/SCHEMA.md``; the syntax half belongs to the validator.
* **Purity.** Nothing here reads a file, touches the network, prints, or
  mutates its input. The only input is an already-loaded
  :class:`~goal_dcp.model.Backlog`.

``assume_closed`` is a what-if projection for planning: "if these items were
closed, what would become dispatchable?". It never writes anything and never
changes the backlog; it only changes the answer to that hypothetical.
"""

from __future__ import annotations

from typing import Iterable

from goal_dcp.model import ACCEPTED_TERMINAL_STATES, Backlog, Item

#: The one state an item itself must be in to be dispatchable.
DISPATCHABLE_STATE = "DELIVERY_READY"

#: The state an ``assume_closed`` projection pretends an item has reached.
#: ``CLOSED`` is a member of ``ACCEPTED_TERMINAL_STATES``, so projecting an
#: item closed satisfies dependencies on it.
PROJECTED_STATE = "CLOSED"


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


def _is_ready(backlog: Backlog, item: Item, assumed: frozenset[str]) -> bool:
    """The whole readiness rule, applied to one item, with no special cases."""
    if effective_state(item, assumed) != DISPATCHABLE_STATE:
        return False
    return all(
        _dependency_satisfied(backlog, dependency_id, assumed)
        for dependency_id in item.depends_on
    )


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
    """Return the mechanically dispatchable items, sorted by id.

    An item is ready **iff** both hold, with no other condition and no
    special-casing of any id:

    1. ``effective_state(item) == "DELIVERY_READY"``; and
    2. every entry in ``item.depends_on`` resolves to a declared item whose
       ``effective_state`` is in ``ACCEPTED_TERMINAL_STATES``.

    An item with no dependencies satisfies (2) vacuously. A dependency that
    does not resolve makes the item **not** ready.

    Raises :class:`UnknownAssumedId` if ``assume_closed`` names an id no item
    declares.
    """
    assumed = _assumed(backlog, assume_closed)
    ready = [item for item in backlog.items if _is_ready(backlog, item, assumed)]
    return tuple(sorted(ready, key=_id_sort_key))


def readiness_payload(
    backlog: Backlog,
    assume_closed: frozenset[str] = frozenset(),
    with_pid: bool = False,
) -> dict:
    """Return the readiness answer in the shape ``pids/GOAL-DCP-001.md`` documents.

    ``{"ready": [{"id": ..., "target_repository": ...}, ...]}``, entries sorted
    by id. ``with_pid=True`` adds ``"pid_path"`` to each entry, ``None`` (JSON
    ``null``) when the item declares no PID.

    The default shape carries exactly the two keys the PID's example shows and
    nothing else: it is a consumed contract, so extra keys are a breaking
    change, not a convenience.
    """
    entries = []
    for item in ready_items(backlog, assume_closed):
        entry = {"id": item.id, "target_repository": item.target_repository}
        if with_pid:
            entry["pid_path"] = item.pid_path
        entries.append(entry)
    return {"ready": entries}
