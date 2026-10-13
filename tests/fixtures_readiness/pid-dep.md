# DEP-001 — fixture PID

**Lane:** Shared
**Target repository:** `maff0000/GOAL`
**Priority:** P0
**Matt gate:** No
**PO gate:** Yes

A test fixture, not a real Product Initiation Document. Only
`no_pid_declared.yaml` declares it, and only because that fixture's `DEP-001`
is `CLOSED` — a PID-required state — so without a PID of its own the document
yields a second finding that has nothing to do with the clause under test. See
that fixture's header comment for the full reasoning.

The other `dep_*.yaml` fixtures leave `DEP-001` without a PID on purpose:
readiness does not care whether a *dependency* declares one, and their
incidental `MISSING_PID` does not collide with the code they prove.

## Purpose

Exist as the PID that `no_pid_declared.yaml`'s `DEP-001` declares, so
`TARGET-001`'s `MISSING_PID` stays the only finding that document yields.

## Scope

Nothing is delivered from this file. It carries the labels above and the
minimum sections, and claims no authority of any kind beyond that.

## Acceptance

GREEN when `no_pid_declared.yaml` yields exactly one finding, against
`TARGET-001`.

## Approval

No real approval exists and none is claimed. This stands in for the
approval-evidence section, which the validator requires to be present and
non-trivial but deliberately never reads for meaning.
