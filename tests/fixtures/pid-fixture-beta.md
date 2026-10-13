# BETA-001 — fixture PID for the DELIVERY_READY agreement case

**Lane:** Ops
**Target repository:** `maff0000/GOAL`
**Priority:** P2
**Risk:** Capital
**Matt gate:** Yes
**PO gate:** Yes
**Delivery:** ROGUE → FORGE

This is a test fixture, not a real Product Initiation Document. It exists so
`tests/fixtures/valid.yaml` can hold a `DELIVERY_READY` item that is genuinely
delivery-ready: `DELIVERY_READY` requires a canonical PID, so an item in that
state with `pid_path: null` is `MISSING_PID`, not a valid document.

It deliberately differs from `pid-fixture.md` in every compared label it
shares, and declares a `Risk` label that `pid-fixture.md` omits. Agreement is
therefore being proven against a second, distinct label set — including a
`Risk` comparison and a `Matt gate` of `Yes` — rather than against one set of
values that might happen to match for the wrong reason.

The four sections below are required of any fixture PID whose declaring item
sits in a PID-required state: without them the document yields an incidental
`PID_INVALID` that has nothing to do with the agreement case it exists for.

## Purpose

Exist as the second readable fixture PID, so backlog/PID agreement is proven
against a distinct label set rather than one lucky set of values.

## Scope

Nothing is delivered from this file. It carries the labels above and the
minimum sections, and claims no authority of any kind beyond that.

## Acceptance

GREEN when `tests/fixtures/valid.yaml` yields no finding whatsoever, with this
`DELIVERY_READY` item genuinely valid rather than merely tolerated.

## Approval

No real approval exists and none is claimed. This stands in for the
approval-evidence section, which the validator requires to be present and
non-trivial but deliberately never reads for meaning.
