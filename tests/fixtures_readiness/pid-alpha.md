# ALPHA-001 — fixture PID

**Lane:** Shared
**Target repository:** `maff0000/alpha`
**Priority:** P0
**Matt gate:** No
**PO gate:** Yes

A test fixture, not a real Product Initiation Document. It exists so
`multiple_ready.yaml`'s ALPHA-001 can be genuinely dispatch-ready: readiness
requires the item to declare a PID, and this file is the PID it declares.

One fixture PID per item, rather than one shared file, so the payload has to
carry *each item's own* `pid_path` — a payload that reused one value for all
three entries would pass a single-file version of this fixture.

The four sections below are not decoration. A readiness fixture item in
`DELIVERY_READY` must declare a PID the validator accepts, so each fixture PID
here carries identity plus the minimum sections; without them the document
yields `PID_INVALID` and stops isolating the readiness clause under test.

## Purpose

Exist as the PID that `ALPHA-001` declares, so the readiness answer can report
a genuinely dispatch-ready item.

## Scope

Nothing is delivered from this file. It carries the labels above and the
minimum sections, and claims no authority of any kind beyond that.

## Acceptance

GREEN when `multiple_ready.yaml` validates clean and readiness reports this
item with its own declared path.

## Approval

No real approval exists and none is claimed. This stands in for the
approval-evidence section, which the validator requires to be present and
non-trivial but deliberately never reads for meaning.
