# ALPHA-001 — fixture PID for the MERGED agreement case

**Lane:** Shared
**Target repository:** `maff0000/GOAL`
**Priority:** P0
**Matt gate:** No
**PO gate:** Yes
**Delivery:** ROGUE → FORGE

This is a test fixture, not a real Product Initiation Document. It exists so
`tests/fixtures/valid.yaml` can hold a `MERGED` item whose PID is valid as a
PID, which minimum PID validity now requires of every item from
`DELIVERY_READY` onwards.

It is a separate file from `pid-fixture.md` for one reason: **identity**. A PID
must name the item that declares it in its first heading, and `pid-fixture.md`
is headed `PIDFIX-001` because that is the id the agreement fixtures declare.
`ALPHA-001` therefore needs its own file rather than a share of that one — a
fixture PID is no longer reusable across items with different ids.

Its label set is deliberately the same shape as `pid-fixture.md`'s, including
the omitted `Risk` label, so the "a label the PID omits is not a mismatch"
property is exercised on this item too.

## Purpose

Exist as the PID that `ALPHA-001` declares, so the valid fixture's `MERGED`
item is genuinely valid rather than merely tolerated.

## Scope

Nothing is delivered from this file. It carries the labels above and the
minimum sections, and claims no authority of any kind beyond that.

## Acceptance

GREEN when `tests/fixtures/valid.yaml` yields no finding whatsoever, at both
ends of the PID-required range.

## Approval

No real approval exists and none is claimed. This stands in for the
approval-evidence section, which the validator requires to be present and
non-trivial but deliberately never reads for meaning.
