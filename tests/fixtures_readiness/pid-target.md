# TARGET-001 — fixture PID

**Lane:** Shared
**Target repository:** `maff0000/GOAL`
**Priority:** P0
**Matt gate:** No
**PO gate:** Yes

A test fixture, not a real Product Initiation Document. It is the PID that
`TARGET-001` declares in every readiness fixture whose target item sits in a
PID-required state.

It exists as its own file because a PID must name the item that declares it:
these fixtures previously shared `fixtures/pid-fixture.md`, which is headed
`PIDFIX-001` and so cannot establish identity for `TARGET-001`. One fixture PID
per declared id is now a constraint, not a style choice.

`state_not_delivery_ready.yaml` deliberately still points at
`fixtures/pid-fixture.md`. Its `TARGET-001` is `ARCHITECTURE_REQUIRED`, which
is not a PID-required state, so minimum PID validity does not apply there —
and leaving it is a live proof that the rule really is state-scoped.

## Purpose

Exist as the PID that `TARGET-001` declares, so each readiness fixture isolates
its own clause and nothing else.

## Scope

Nothing is delivered from this file. It carries the labels above and the
minimum sections, and claims no authority of any kind beyond that.

## Acceptance

GREEN when every `DELIVERY_READY` fixture item yields no PID finding except the
one its fixture is exempted for.

## Approval

No real approval exists and none is claimed. This stands in for the
approval-evidence section, which the validator requires to be present and
non-trivial but deliberately never reads for meaning.
