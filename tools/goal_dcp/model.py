"""Canonical vocabularies, identifier rules and the structural backlog loader.

This module is the single shared foundation for the GOAL delivery control
plane. It owns three things and nothing else:

1. the canonical delivery vocabularies, copied from
   ``governance/DELIVERY-STATE-MACHINE.md``;
2. the identifier patterns for item ids and declared target repositories;
3. a *structural* loader for ``backlog/backlog.yaml``.

``load_backlog`` is a structural loader, not a validator. It deliberately
tolerates semantically invalid data and hands it through intact so that
``goal_dcp.validate`` can report on it. Semantic checks (lane membership,
state membership, dependency resolution, cycles, file existence) belong in
the validator, never here.
"""

from __future__ import annotations

import dataclasses
import pathlib
import re
from typing import Any, Iterable

import yaml

# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------

#: Repository root, derived from this file's location (three parents up:
#: ``<repo>/tools/goal_dcp/model.py``).
REPO_ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parents[2]

#: The canonical machine-readable backlog.
BACKLOG_PATH: pathlib.Path = REPO_ROOT / "backlog" / "backlog.yaml"

# ---------------------------------------------------------------------------
# Canonical vocabularies (from governance/DELIVERY-STATE-MACHINE.md)
# ---------------------------------------------------------------------------

#: Canonical delivery states, in state-machine order.
STATES: tuple[str, ...] = (
    "DISCOVERED", "ARCHITECTURE_REQUIRED", "PID_DRAFT", "PO_REVIEW",
    "BLOCKED", "DELIVERY_READY", "ROGUE_DISPATCHED", "FORGE_BUILD",
    "FORGE_AUDIT", "REPAIR", "PO_ACCEPTANCE", "MATT_DECISION",
    "CANDIDATE", "MERGED", "DEPLOYMENT_READY", "PAPER", "LIVE",
    "CLOSED", "CANCELLED",
)

# A dependency counts as satisfied ONLY in one of these states.
# CANCELLED is terminal but NOT accepted. BLOCKED is not terminal.
# PO_ACCEPTANCE / MATT_DECISION / CANDIDATE are in-flight gates, not acceptance.
ACCEPTED_TERMINAL_STATES: frozenset[str] = frozenset({
    "MERGED", "DEPLOYMENT_READY", "PAPER", "LIVE", "CLOSED",
})

# States that mean FORGE is already engaged, so a canonical PID must exist.
PID_REQUIRED_STATES: frozenset[str] = frozenset({
    "ROGUE_DISPATCHED", "FORGE_BUILD", "FORGE_AUDIT", "REPAIR",
    "PO_ACCEPTANCE", "MATT_DECISION", "CANDIDATE", "MERGED",
    "DEPLOYMENT_READY", "PAPER", "LIVE", "CLOSED",
})

#: Lane values are lowercase to match the ``lane:*`` label vocabulary in
#: ``governance/DELIVERY-STATE-MACHINE.md``.
LANES: frozenset[str] = frozenset({"shared", "research", "trading", "ops"})
PRIORITIES: frozenset[str] = frozenset({"P0", "P1", "P2"})
RISKS: frozenset[str] = frozenset({"low", "medium", "high", "capital"})

# ---------------------------------------------------------------------------
# Identifier rules
# ---------------------------------------------------------------------------
#
# Canonical ids are *complete*: GOAL-DCP-001, OPS-SAFE-001, DARWIN-R1,
# MT5-GW-001, PAPER-E2E-001. Shorthand (DCP-001, CONTRACT-001, CORE-001),
# wildcards (OPS-SAFE-*), lowercase (tron-t1) and comma lists
# (TRON-T2,T3,T4) are not canonical ids.
#
# Rejecting shorthand is deliberately two-layered, because no regex can tell
# DCP-001 (shorthand, invalid) from DARWIN-R1 (canonical, valid):
#
#   1. Syntax   -- ID_PATTERN rejects wildcards, lowercase, commas,
#                  whitespace and empty strings.
#   2. Membership -- a dependency must resolve to a declared item id. This is
#                  what rejects shorthand, aliases and unknown ids, and it is
#                  the validator's job, not this module's.
#
# Both layers are required; neither alone is sufficient.

ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
REPO_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$")

#: The 13 backlog item fields, in canonical order.
ITEM_FIELDS: tuple[str, ...] = (
    "id",
    "title",
    "lane",
    "component",
    "target_repository",
    "priority",
    "risk",
    "state",
    "depends_on",
    "po_gate",
    "matt_gate",
    "pid_path",
    "architecture_refs",
)

#: Fields carried through verbatim, whatever their source type.
_SCALAR_FIELDS: tuple[str, ...] = (
    "id", "title", "lane", "component", "target_repository",
    "priority", "risk", "state", "po_gate", "matt_gate", "pid_path",
)

#: Fields normalised to a tuple when the source value is a list.
_SEQUENCE_FIELDS: tuple[str, ...] = ("depends_on", "architecture_refs")


class BacklogLoadError(Exception):
    """The backlog could not be read as a structurally sound document.

    Raised only for the five structural conditions documented on
    :func:`load_backlog`. Semantic problems are findings, not exceptions.
    """


@dataclasses.dataclass(frozen=True)
class Item:
    """One backlog item, loaded structurally.

    Field values are carried through from YAML **unconverted**, so any
    attribute may hold a value of the wrong type, or ``None`` when the key was
    absent. :attr:`raw` holds the original mapping so the validator can tell
    "absent" apart from "present but null" and report type errors.
    """

    id: str
    title: str
    lane: str
    component: str
    target_repository: str
    priority: str
    risk: str
    state: str
    depends_on: tuple[str, ...]
    po_gate: bool
    matt_gate: bool
    pid_path: str | None
    architecture_refs: tuple[str, ...]
    raw: dict


@dataclasses.dataclass(frozen=True)
class Backlog:
    """A loaded backlog document."""

    items: tuple[Item, ...]
    by_id: dict[str, Item]
    duplicate_ids: tuple[str, ...]
    source_path: pathlib.Path
    repo_root: pathlib.Path


@dataclasses.dataclass(frozen=True)
class Finding:
    """A single deterministic validation or drift finding."""

    code: str
    item_id: str | None
    message: str

    def as_line(self) -> str:
        """``'CODE item_id: message'``, or ``'CODE: message'`` when no item."""
        if self.item_id is None:
            return f"{self.code}: {self.message}"
        return f"{self.code} {self.item_id}: {self.message}"


def sort_findings(findings: Iterable[Finding]) -> tuple[Finding, ...]:
    """Return ``findings`` in deterministic ``(code, item_id or '', message)`` order."""
    return tuple(sorted(findings, key=lambda f: (f.code, f.item_id or "", f.message)))


def _as_tuple(value: Any) -> tuple[Any, ...]:
    """Tuple-ise a list value without touching its elements; else empty tuple.

    A missing or wrong-typed sequence field becomes an empty tuple here; the
    original value stays in ``Item.raw`` so the validator can report it.
    """
    if isinstance(value, list):
        return tuple(value)
    return ()


def _build_item(raw: dict) -> Item:
    """Build an :class:`Item` from a source mapping without validating it."""
    fields: dict[str, Any] = {name: raw.get(name) for name in _SCALAR_FIELDS}
    for name in _SEQUENCE_FIELDS:
        fields[name] = _as_tuple(raw.get(name))
    return Item(raw=raw, **fields)


def load_backlog(path: pathlib.Path | None = None) -> Backlog:
    """Load a backlog document structurally, tolerating semantic errors.

    Raises :class:`BacklogLoadError` only when the document is not
    structurally usable, which is exactly one of:

    1. the YAML does not parse;
    2. the top level is not a mapping;
    3. the top-level ``items`` key is missing;
    4. ``items`` is not a list;
    5. an ``items`` entry is not a mapping.

    Nothing else raises. Unreadable or absent files surface as the underlying
    :class:`OSError` rather than being folded into a sixth condition.

    ``repo_root`` is ``path.parent.parent``, so a fixture backlog in a
    temporary directory resolves its own root; for :data:`BACKLOG_PATH` this
    yields :data:`REPO_ROOT`.
    """
    source_path = BACKLOG_PATH if path is None else pathlib.Path(path)
    text = source_path.read_text(encoding="utf-8")

    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise BacklogLoadError(f"backlog YAML does not parse: {exc}") from exc

    if not isinstance(document, dict):
        raise BacklogLoadError("backlog top level must be a mapping with an 'items' key")
    if "items" not in document:
        raise BacklogLoadError("backlog top level is missing the required 'items' key")

    entries = document["items"]
    if not isinstance(entries, list):
        raise BacklogLoadError("backlog 'items' must be a list")

    items: list[Item] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise BacklogLoadError(f"backlog items[{index}] must be a mapping")
        items.append(_build_item(entry))

    # Only string ids participate in identity bookkeeping. An absent or
    # wrong-typed id is a validator finding (MISSING_FIELD /
    # INVALID_FIELD_TYPE), and keeping non-strings out of by_id keeps
    # duplicate_ids totally orderable.
    counts: dict[str, int] = {}
    by_id: dict[str, Item] = {}
    for item in items:
        if not isinstance(item.id, str):
            continue
        counts[item.id] = counts.get(item.id, 0) + 1
        if item.id not in by_id:
            by_id[item.id] = item  # first occurrence wins

    duplicate_ids = tuple(sorted(i for i, count in counts.items() if count > 1))

    return Backlog(
        items=tuple(items),
        by_id=by_id,
        duplicate_ids=duplicate_ids,
        source_path=source_path,
        repo_root=source_path.parent.parent,
    )
