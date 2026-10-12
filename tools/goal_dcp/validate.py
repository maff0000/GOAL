"""Deterministic, offline validation of the machine-readable delivery backlog.

This module answers one question: *is the backlog a sound statement of
delivery truth?* It never mutates anything, never touches the network, and
never raises on semantically broken input — broken input is precisely what it
exists to describe. ``load_backlog`` hands through missing keys as ``None``
and wrong-typed values unconverted (see ``goal_dcp.model``), so every value
read here is treated as untrusted and type-checked before use.

Two public entry points:

* :func:`validate` — every finding for a loaded backlog, in
  ``sort_findings`` order. An empty tuple means the backlog is valid.
* :func:`dependency_cycles` — the dependency graph's elementary cycles, in a
  canonical, byte-stable form.

Design rules this module holds to:

**Offline.** ``target_repository`` is a *declared* target and is checked
against :data:`goal_dcp.model.REPO_PATTERN` only. Several declared targets do
not exist on GitHub yet; that is correct for work that has not started, and
contacting GitHub would make validation non-deterministic and network-bound.

**Repo-relative paths only.** ``pid_path`` and ``architecture_refs`` are
resolved against ``backlog.repo_root`` — never the process working directory,
and never as absolute paths. ``/pids/X.md`` and ``../pids/X.md`` are both
refused by :func:`_resolve_under_root` rather than being allowed to reach a
file outside the backlog's own root, which keeps a fixture's findings a
property of the fixture.

**Shorthand rejection is two-layered.** No regular expression can tell
``DCP-001`` (shorthand, invalid) from ``DARWIN-R1`` (canonical, valid), so
syntax and membership are separate layers:
``MALFORMED_DEPENDENCY_ID``/``WILDCARD_DEPENDENCY`` reject bad *syntax*, and
``UNKNOWN_DEPENDENCY`` rejects anything well-formed that no item declares as
its ``id``. That second layer is what catches shorthand and aliases. Both are
required; neither alone is sufficient.

**Finding precedence — one defect, one finding.** A field is checked
structurally first (present? right Python type?). When a field is absent
(``MISSING_FIELD``) or present with the wrong type (``INVALID_FIELD_TYPE``),
the *downstream* semantic findings for that same field are suppressed: no
enum check (``INVALID_LANE``, ``INVALID_STATE``, ``INVALID_PRIORITY``,
``INVALID_RISK``), no pattern check (``MALFORMED_ID``,
``MALFORMED_TARGET_REPOSITORY``), no emptiness check (``EMPTY_FIELD``), no
file-existence check, no PID comparison, and no dependency analysis. A single
defect must not produce a pile of findings. Two deliberate exceptions, both
required by the contract's finding table:

1. ``target_repository`` has a dedicated presence code, so an absent
   ``target_repository`` reports both ``MISSING_FIELD`` (the generic
   structural rule, which covers all 13 fields) and
   ``MISSING_TARGET_REPOSITORY`` (the field-specific rule, whose stated
   condition is "absent, null or empty"). A *null* or *empty*
   ``target_repository`` reports only ``MISSING_TARGET_REPOSITORY``, not
   ``INVALID_FIELD_TYPE``, because the contract assigns the null case to the
   dedicated code.
2. ``MISSING_PID`` is state-conditional, so it is evaluated only when
   ``state`` itself is a valid state. A broken ``state`` suppresses it.

**Determinism.** Everything emitted is sorted; no set is ever iterated
without sorting; no timestamp, duration, absolute path, hostname or username
appears in any message. Byte-identical input yields byte-identical output.
"""

from __future__ import annotations

import pathlib
import re
from typing import Any, Iterable, Iterator

from goal_dcp import model
from goal_dcp.model import Backlog, Finding, Item, sort_findings

# ---------------------------------------------------------------------------
# Field expectations
# ---------------------------------------------------------------------------

#: The Python type each backlog field must hold.
_EXPECTED_TYPES: dict[str, type] = {
    "id": str,
    "title": str,
    "lane": str,
    "component": str,
    "target_repository": str,
    "priority": str,
    "risk": str,
    "state": str,
    "depends_on": list,
    "po_gate": bool,
    "matt_gate": bool,
    "pid_path": str,
    "architecture_refs": list,
}

#: Fields whose value is legitimately ``null``.
_NULLABLE_FIELDS = frozenset({"pid_path"})

#: Fields whose absent/null case has a dedicated finding code, so the generic
#: "present but null" type finding is not also emitted for them.
_DEDICATED_PRESENCE_FIELDS = frozenset({"target_repository"})

#: Fields that must not be empty or whitespace-only (``EMPTY_FIELD``).
_NON_EMPTY_TEXT_FIELDS: tuple[str, ...] = ("title", "component")

#: ``field -> (finding code, allowed values)`` for the enum checks.
_ENUM_FIELDS: tuple[tuple[str, str, Iterable[str]], ...] = (
    ("lane", "INVALID_LANE", model.LANES),
    ("state", "INVALID_STATE", model.STATES),
    ("priority", "INVALID_PRIORITY", model.PRIORITIES),
    ("risk", "INVALID_RISK", model.RISKS),
)

#: Characters that make a dependency entry a pattern rather than an id.
_WILDCARD_CHARACTERS = ("*", "?")

# Structural status of one field, used to apply the precedence rule above.
_OK = "ok"
_MISSING = "missing"
_NULL = "null"
_BAD_TYPE = "bad-type"

# ---------------------------------------------------------------------------
# PID metadata comparison
# ---------------------------------------------------------------------------

#: Bold label lines in a canonical PID, e.g. ``**Target repository:** `a/b` ``.
_PID_LABEL_PATTERN = re.compile(r"^\*\*(?P<label>[^*]+):\*\*\s*(?P<value>.+?)\s*$")

#: ``case-folded PID label -> backlog field``. Labels the PID does not declare
#: are not compared at all; only a label the PID actually states can disagree.
_PID_LABEL_FIELDS: dict[str, str] = {
    "lane": "lane",
    "target repository": "target_repository",
    "priority": "priority",
    "risk": "risk",
    "matt gate": "matt_gate",
    "po gate": "po_gate",
}

#: Canonical PID spellings of the labels above, for message text.
_PID_LABEL_NAMES: dict[str, str] = {
    "lane": "Lane",
    "target_repository": "Target repository",
    "priority": "Priority",
    "risk": "Risk",
    "matt_gate": "Matt gate",
    "po_gate": "PO gate",
}

#: How a PID spells a boolean gate.
_PID_BOOLEANS: dict[str, bool] = {"yes": True, "no": False}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _render(value: Any) -> str:
    """Render ``value`` for a finding message, deterministically.

    Booleans render as YAML spells them, so a message quotes the backlog the
    reader is looking at rather than Python.
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return repr(value)
    return repr(value)


def _type_name(value: Any) -> str:
    """The Python type name of ``value``, for ``INVALID_FIELD_TYPE`` messages."""
    return type(value).__name__


def _item_label(item: Item, index: int) -> str:
    """A stable identifier for ``item`` in finding output.

    The declared ``id`` when it is a usable string, otherwise the item's
    source position, so a finding about an item with a missing or wrong-typed
    ``id`` can still be located. Source position is deterministic because
    ``load_backlog`` preserves source order.
    """
    if isinstance(item.id, str) and item.id.strip():
        return item.id
    return f"items[{index}]"


def _field_status(item: Item, field: str) -> str:
    """Classify ``field`` structurally: present, absent, null, or wrong type.

    Uses :attr:`Item.raw` because that is the only way to tell "key absent"
    from "key present with a null value" — the dataclass attribute is ``None``
    for both.
    """
    raw = item.raw
    if not isinstance(raw, dict) or field not in raw:
        return _MISSING
    value = raw[field]
    if value is None:
        return _NULL
    if not isinstance(value, _EXPECTED_TYPES[field]):
        return _BAD_TYPE
    return _OK


def _resolve_under_root(repo_root: pathlib.Path, declared: Any) -> pathlib.Path | None:
    """Resolve ``declared`` as a repo-relative POSIX path under ``repo_root``.

    Returns ``None`` when ``declared`` is not a usable repo-relative path, so
    the caller reports a broken pointer rather than reading a file the backlog
    did not actually name. Refused: non-strings, empty/whitespace strings,
    absolute paths (``pathlib`` would otherwise discard ``repo_root``
    entirely) and any path containing ``..`` (which could otherwise escape the
    root and resolve against a *different* repository's contents).
    """
    if not isinstance(declared, str) or not declared.strip():
        return None
    pure = pathlib.PurePosixPath(declared)
    if pure.is_absolute() or ".." in pure.parts:
        return None
    return repo_root / pure


def _duplicates(values: Iterable[Any]) -> tuple[str, ...]:
    """Sorted string values that appear more than once in ``values``."""
    counts: dict[str, int] = {}
    for value in values:
        if isinstance(value, str):
            counts[value] = counts.get(value, 0) + 1
    return tuple(sorted(value for value, count in counts.items() if count > 1))


# ---------------------------------------------------------------------------
# Dependency graph and cycles
# ---------------------------------------------------------------------------


def _dependency_graph(backlog: Backlog) -> dict[str, tuple[str, ...]]:
    """The resolvable dependency graph: ``id -> sorted dependency ids``.

    Only membership-resolvable edges are included. A dependency that is not a
    string, or that no item declares as its ``id``, is reported as
    ``UNKNOWN_DEPENDENCY`` / ``MALFORMED_DEPENDENCY_ID`` and contributes no
    edge — an unresolvable name cannot take part in a cycle. Nodes come from
    ``backlog.by_id``, so a duplicated id appears once (first occurrence
    wins, matching the loader's documented behaviour).
    """
    graph: dict[str, tuple[str, ...]] = {}
    for item_id, item in backlog.by_id.items():
        edges = {
            dependency
            for dependency in item.depends_on
            if isinstance(dependency, str) and dependency in backlog.by_id
        }
        graph[item_id] = tuple(sorted(edges))
    return graph


def dependency_cycles(backlog: Backlog) -> tuple[tuple[str, ...], ...]:
    """Every elementary cycle in the dependency graph, canonically ordered.

    Each cycle is a tuple of ids rotated so the lexicographically smallest id
    comes first; the outer tuple is sorted. Output is therefore byte-stable
    across runs and across source reordering of the backlog. Only
    membership-resolvable edges are followed (see :func:`_dependency_graph`).

    Every elementary cycle is enumerated exactly once by rooting the search at
    the cycle's smallest member: the walk from a root never steps onto a node
    that sorts before that root. This finds self-loops, two-node cycles,
    longer cycles, several disjoint cycles in one document, and a cycle
    reachable only through a chain — a cycle is found from its own smallest
    member regardless of what else points into it.

    A self-loop is returned as a one-element cycle. :func:`validate` reports it
    as ``SELF_DEPENDENCY`` rather than ``DEPENDENCY_CYCLE``, because
    ``DEPENDENCY_CYCLE`` is defined for cycles of length >= 2; this function
    still reports it so callers asking "what cycles exist?" get the whole
    truth.
    """
    graph = _dependency_graph(backlog)
    cycles: set[tuple[str, ...]] = set()

    for root in sorted(graph):
        path: list[str] = [root]
        on_path = {root}

        def walk(node: str, root: str = root) -> None:
            for nxt in graph.get(node, ()):
                if nxt == root:
                    cycles.add(tuple(path))
                elif nxt > root and nxt not in on_path:
                    path.append(nxt)
                    on_path.add(nxt)
                    walk(nxt)
                    path.pop()
                    on_path.discard(nxt)

        walk(root)

    return tuple(sorted(cycles))


def _cycle_findings(backlog: Backlog) -> Iterator[Finding]:
    """One ``DEPENDENCY_CYCLE`` finding per cycle of length >= 2."""
    for cycle in dependency_cycles(backlog):
        if len(cycle) < 2:
            continue  # a self-loop is SELF_DEPENDENCY, not DEPENDENCY_CYCLE
        route = " -> ".join(cycle + (cycle[0],))
        yield Finding(
            code="DEPENDENCY_CYCLE",
            item_id=cycle[0],
            message=f"dependency cycle: {route}",
        )


# ---------------------------------------------------------------------------
# Per-item checks
# ---------------------------------------------------------------------------


def _structural_findings(item: Item, label: str, status: dict[str, str]) -> Iterator[Finding]:
    """``MISSING_FIELD`` / ``INVALID_FIELD_TYPE`` for the 13 declared fields."""
    for field in model.ITEM_FIELDS:
        state = status[field]
        if state == _MISSING:
            yield Finding(
                code="MISSING_FIELD",
                item_id=label,
                message=f"required field {field!r} is absent",
            )
        elif state == _NULL:
            if field in _NULLABLE_FIELDS or field in _DEDICATED_PRESENCE_FIELDS:
                continue
            yield Finding(
                code="INVALID_FIELD_TYPE",
                item_id=label,
                message=(
                    f"field {field!r} is null; expected "
                    f"{_EXPECTED_TYPES[field].__name__}"
                ),
            )
        elif state == _BAD_TYPE:
            value = item.raw[field]
            yield Finding(
                code="INVALID_FIELD_TYPE",
                item_id=label,
                message=(
                    f"field {field!r} expected {_EXPECTED_TYPES[field].__name__}, "
                    f"got {_type_name(value)}"
                ),
            )


def _identity_findings(item: Item, label: str, status: dict[str, str]) -> Iterator[Finding]:
    """``MALFORMED_ID`` and ``EMPTY_FIELD``, guarded by structural status."""
    if status["id"] == _OK and not model.ID_PATTERN.fullmatch(item.id):
        yield Finding(
            code="MALFORMED_ID",
            item_id=label,
            message=(
                f"id {item.id!r} is not a canonical complete id "
                f"(pattern {model.ID_PATTERN.pattern})"
            ),
        )

    for field in _NON_EMPTY_TEXT_FIELDS:
        if status[field] == _OK and not item.raw[field].strip():
            yield Finding(
                code="EMPTY_FIELD",
                item_id=label,
                message=f"field {field!r} must not be empty",
            )


def _enum_findings(item: Item, label: str, status: dict[str, str]) -> Iterator[Finding]:
    """The four vocabulary-membership checks, guarded by structural status."""
    for field, code, allowed in _ENUM_FIELDS:
        if status[field] != _OK:
            continue
        value = item.raw[field]
        if value in allowed:
            continue
        yield Finding(
            code=code,
            item_id=label,
            message=(
                f"field {field!r} value {value!r} is not one of: "
                f"{', '.join(sorted(allowed))}"
            ),
        )


def _target_repository_findings(
    item: Item, label: str, status: dict[str, str]
) -> Iterator[Finding]:
    """Presence and shape of the *declared* target repository.

    Never checked against GitHub: a declared target that does not exist yet is
    correct for work that has not started.
    """
    state = status["target_repository"]
    if state == _BAD_TYPE:
        return  # INVALID_FIELD_TYPE already reported; shape is unknowable

    value = item.raw.get("target_repository") if isinstance(item.raw, dict) else None
    if state in (_MISSING, _NULL) or not value.strip():
        yield Finding(
            code="MISSING_TARGET_REPOSITORY",
            item_id=label,
            message="target_repository is required and must name a declared owner/name",
        )
        return

    if not model.REPO_PATTERN.fullmatch(value):
        yield Finding(
            code="MALFORMED_TARGET_REPOSITORY",
            item_id=label,
            message=(
                f"target_repository {value!r} is not owner/name "
                f"(pattern {model.REPO_PATTERN.pattern})"
            ),
        )


def _dependency_findings(
    backlog: Backlog, item: Item, label: str, status: dict[str, str]
) -> Iterator[Finding]:
    """Per-entry dependency checks: syntax, membership, self and duplicates."""
    if status["depends_on"] != _OK:
        return  # MISSING_FIELD / INVALID_FIELD_TYPE already reported

    own_id = item.id if status["id"] == _OK else None

    for index, dependency in enumerate(item.depends_on):
        if not isinstance(dependency, str):
            yield Finding(
                code="INVALID_FIELD_TYPE",
                item_id=label,
                message=(
                    f"depends_on[{index}] expected str, got {_type_name(dependency)}"
                ),
            )
            continue

        if any(character in dependency for character in _WILDCARD_CHARACTERS):
            yield Finding(
                code="WILDCARD_DEPENDENCY",
                item_id=label,
                message=(
                    f"depends_on[{index}] {dependency!r} is a pattern; dependencies "
                    "must be canonical complete ids"
                ),
            )
            continue

        if not model.ID_PATTERN.fullmatch(dependency):
            yield Finding(
                code="MALFORMED_DEPENDENCY_ID",
                item_id=label,
                message=(
                    f"depends_on[{index}] {dependency!r} is not a canonical complete "
                    f"id (pattern {model.ID_PATTERN.pattern})"
                ),
            )
            continue

        if own_id is not None and dependency == own_id:
            yield Finding(
                code="SELF_DEPENDENCY",
                item_id=label,
                message=f"depends_on[{index}] {dependency!r} is the item's own id",
            )
            continue

        # Membership is the layer that rejects shorthand such as 'DCP-001'
        # and aliases: well-formed, but no item declares it.
        if dependency not in backlog.by_id:
            yield Finding(
                code="UNKNOWN_DEPENDENCY",
                item_id=label,
                message=(
                    f"depends_on[{index}] {dependency!r} is not declared as the id of "
                    "any backlog item"
                ),
            )

    for repeated in _duplicates(item.depends_on):
        yield Finding(
            code="DUPLICATE_DEPENDENCY",
            item_id=label,
            message=f"depends_on lists {repeated!r} more than once",
        )


def _architecture_ref_findings(
    backlog: Backlog, item: Item, label: str, status: dict[str, str]
) -> Iterator[Finding]:
    """Each ``architecture_refs`` entry must name a file under ``repo_root``."""
    if status["architecture_refs"] != _OK:
        return

    for index, reference in enumerate(item.architecture_refs):
        if not isinstance(reference, str):
            yield Finding(
                code="INVALID_FIELD_TYPE",
                item_id=label,
                message=(
                    f"architecture_refs[{index}] expected str, "
                    f"got {_type_name(reference)}"
                ),
            )
            continue

        target = _resolve_under_root(backlog.repo_root, reference)
        if target is None or not target.is_file():
            yield Finding(
                code="MISSING_ARCHITECTURE_REF_FILE",
                item_id=label,
                message=(
                    f"architecture_refs[{index}] {reference!r} does not name a file "
                    "under the repository root"
                ),
            )


def _read_pid_labels(path: pathlib.Path) -> dict[str, str] | None:
    """Parse bold label lines from a PID markdown file.

    Returns ``label -> value`` keyed by the case-folded label, values stripped
    of whitespace and surrounding backticks. The first occurrence of a label
    wins, so a repeated label cannot make the result order-dependent. Returns
    ``None`` when the file cannot be read as text, so the caller reports a
    broken pointer rather than raising.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    labels: dict[str, str] = {}
    for line in text.splitlines():
        match = _PID_LABEL_PATTERN.match(line)
        if match is None:
            continue
        key = match.group("label").strip().casefold()
        if key in labels:
            continue
        labels[key] = match.group("value").strip().strip("`").strip()
    return labels


def _pid_mismatch_findings(
    item: Item, label: str, status: dict[str, str], pid_labels: dict[str, str]
) -> Iterator[Finding]:
    """One ``BACKLOG_PID_MISMATCH`` per label the PID and the backlog disagree on.

    Only labels the PID actually declares are compared — a label the PID omits
    is not a mismatch. Strings compare case-insensitively (a PID writes
    ``Shared``, the backlog ``shared``); gates compare as booleans via
    ``yes``/``no``. A field the backlog itself got structurally wrong is
    skipped: that defect is already reported, and comparing it would pile a
    second finding onto one cause.
    """
    for pid_label, field in sorted(_PID_LABEL_FIELDS.items()):
        if pid_label not in pid_labels:
            continue
        if status[field] != _OK:
            continue

        pid_value = pid_labels[pid_label]
        backlog_value = item.raw[field]

        if _EXPECTED_TYPES[field] is bool:
            agrees = _PID_BOOLEANS.get(pid_value.casefold()) is backlog_value
        else:
            agrees = backlog_value.casefold() == pid_value.casefold()

        if agrees:
            continue

        yield Finding(
            code="BACKLOG_PID_MISMATCH",
            item_id=label,
            message=(
                f"{_PID_LABEL_NAMES[field]}: backlog has {_render(backlog_value)}, "
                f"PID declares {_render(pid_value)}"
            ),
        )


def _pid_findings(
    backlog: Backlog, item: Item, label: str, status: dict[str, str]
) -> Iterator[Finding]:
    """``MISSING_PID``, ``PID_FILE_NOT_FOUND`` and PID metadata agreement.

    ``MISSING_PID`` is deliberately state-conditional: it fires only when the
    item's state means FORGE is already engaged. Most items legitimately have
    no PID yet, and ``DELIVERY_READY`` does not require one — authoring the
    PID is part of the dispatch that follows. An unconditional rule would make
    canonical data permanently invalid, which is a defect rather than a check.
    It is evaluated only when ``state`` is itself valid, because a broken
    state cannot be tested for membership meaningfully.
    """
    pid_state = status["pid_path"]
    state_usable = status["state"] == _OK and item.raw["state"] in model.STATES
    pid_required = state_usable and item.raw["state"] in model.PID_REQUIRED_STATES

    if pid_state == _MISSING or pid_state == _BAD_TYPE:
        return  # MISSING_FIELD / INVALID_FIELD_TYPE already reported

    if pid_state == _NULL:
        if pid_required:
            yield Finding(
                code="MISSING_PID",
                item_id=label,
                message=(
                    f"state {item.raw['state']!r} requires a canonical PID but "
                    "pid_path is null"
                ),
            )
        return

    declared = item.raw["pid_path"]
    target = _resolve_under_root(backlog.repo_root, declared)
    if target is None or not target.is_file():
        yield Finding(
            code="PID_FILE_NOT_FOUND",
            item_id=label,
            message=(
                f"pid_path {declared!r} does not name a file under the repository root"
            ),
        )
        return

    pid_labels = _read_pid_labels(target)
    if pid_labels is None:
        yield Finding(
            code="PID_FILE_NOT_FOUND",
            item_id=label,
            message=f"pid_path {declared!r} could not be read as UTF-8 text",
        )
        return

    yield from _pid_mismatch_findings(item, label, status, pid_labels)


def _item_findings(backlog: Backlog, item: Item, index: int) -> Iterator[Finding]:
    """Every finding for one item, structural checks first (see precedence)."""
    label = _item_label(item, index)
    status = {field: _field_status(item, field) for field in model.ITEM_FIELDS}

    yield from _structural_findings(item, label, status)
    yield from _identity_findings(item, label, status)
    yield from _enum_findings(item, label, status)
    yield from _target_repository_findings(item, label, status)
    yield from _dependency_findings(backlog, item, label, status)
    yield from _architecture_ref_findings(backlog, item, label, status)
    yield from _pid_findings(backlog, item, label, status)


def _duplicate_id_findings(backlog: Backlog) -> Iterator[Finding]:
    """One ``DUPLICATE_ID`` finding per id more than one item declares."""
    for duplicate in backlog.duplicate_ids:
        count = sum(1 for item in backlog.items if item.id == duplicate)
        yield Finding(
            code="DUPLICATE_ID",
            item_id=duplicate,
            message=f"id is declared by {count} items; ids must be unique",
        )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def validate(backlog: Backlog) -> tuple[Finding, ...]:
    """Every finding for ``backlog``, in ``sort_findings`` order.

    An empty tuple means the backlog is valid. This function never raises on
    semantically broken data — reporting that data is its purpose — so every
    value is type-checked before use.

    Identical findings are collapsed, because two items declaring the same
    duplicated id produce output lines that are indistinguishable; the
    ``DUPLICATE_ID`` finding is what states that there is more than one item.
    Collapsing cannot lose a distinguishable finding: findings are compared on
    all three of their fields, which is exactly what ``sort_findings`` orders
    by.
    """
    findings: list[Finding] = list(_duplicate_id_findings(backlog))
    for index, item in enumerate(backlog.items):
        findings.extend(_item_findings(backlog, item, index))
    findings.extend(_cycle_findings(backlog))
    return sort_findings(dict.fromkeys(findings))
