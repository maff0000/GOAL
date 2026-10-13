# PIDFIX-001 — fixture PID for backlog/PID agreement tests

**Lane:** Shared
**Target repository:** `maff0000/GOAL`
**Priority:** P0
**Matt gate:** No
**PO gate:** Yes
**Delivery:** ROGUE → FORGE

This is a test fixture, not a real Product Initiation Document. It exists to
give `BACKLOG_PID_MISMATCH` something to compare against.

Three properties are deliberate:

1. Labels are spelled and cased as a canonical PID spells them (`Shared`, not
   `shared`), so the comparison must be case-insensitive.
2. `Target repository` is wrapped in backticks, so the value must be stripped
   of them before comparison.
3. There is **no** `Risk` label, and `Delivery` is a label the comparison does
   not know. A label the PID omits is not a mismatch, and a label outside the
   compared set is ignored — a PID is prose, and only the metadata it actually
   declares can disagree with the backlog.

Four sections follow, and a fourth property is deliberate with them: minimum
PID validity requires identity plus purpose, scope, acceptance criteria and
approval evidence, so a fixture PID declared by an item in a PID-required
state must carry them or it yields an incidental `PID_INVALID` that is an
artefact of the fixture rather than the failure mode under test.

## Purpose

Exist as a readable document the backlog can point at, so the metadata
agreement checks have something real to compare against.

## Scope

Nothing is delivered from this file. It carries the labels above and the
minimum sections, and claims no authority of any kind beyond that.

## Acceptance

GREEN when each declaring fixture yields exactly the one finding code it
exists to prove, with no incidental PID validity finding beside it.

## Approval

No real approval exists and none is claimed. This stands in for the
approval-evidence section, which the validator requires to be present and
non-trivial but deliberately never reads for meaning.
