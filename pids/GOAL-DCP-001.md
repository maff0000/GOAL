# GOAL-DCP-001 — GitHub Delivery Control Plane Foundation

**Lane:** Shared  
**Target repository:** `maff0000/GOAL`  
**Priority:** P0  
**Risk:** Medium  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE

## Purpose

Establish the minimum GitHub-native delivery control plane so THE GOAL can move from Matt-mediated coordination to a reconstructable, dependency-aware ROGUE/FORGE programme.

## Target outcome

At closure:

1. GOAL is the authoritative architecture/programme repository.
2. Backlog items have machine-readable metadata.
3. Delivery states and dependencies are explicit.
4. A deterministic validator catches malformed backlog/PIDs.
5. A deterministic readiness command lists dependency-satisfied `DELIVERY_READY` work for which a valid, canonical, PO-approved PID exists.
6. ROGUE can consume that list without asking Matt what comes next.
7. No automated engineering launch or auto-merge is introduced yet.

## Scope

Create canonical machine-readable `backlog/backlog.yaml`.

Minimum fields:

```text
id
title
lane
component
target_repository
priority
risk
state
depends_on[]
po_gate
matt_gate
pid_path
architecture_refs[]
```

Create a deterministic validator that fails on:
- duplicate IDs;
- unknown dependencies;
- dependency cycles;
- invalid lane/state;
- missing target repo;
- missing PID;
- a PID that exists but is empty or effectively content-free;
- backlog/PID metadata mismatch.

Create readiness output for items where:

```text
state == DELIVERY_READY
AND all dependencies are accepted terminal GREEN states
AND a valid, canonical, PO-approved PID exists for the item
```

Example:

```json
{"ready":[{"id":"EXAMPLE-ID-001","target_repository":"owner/name"}]}
```

The example illustrates the **shape** of the answer and nothing else. It names
no declared backlog item on purpose — `EXAMPLE-ID-001` and `owner/name` are
deliberately not the id or the target repository of anything in
`backlog/backlog.yaml` — and it must never be read as a dispatch
authorisation.

Document linkage:

```text
GOAL backlog
 ↕
GOAL issue
 ↕
canonical PID
 ↕
component PR
 ↕
implementation evidence
```

Add unit tests covering valid and deliberately invalid fixtures.

## Non-goals

Do not:
- build trading software;
- build a custom web dashboard;
- create a daemon;
- use Redis;
- invent a workflow DSL;
- automatically invoke FORGE;
- auto-merge;
- modify component repos.

## Acceptance

GREEN requires:
- coherent repo layout;
- machine-readable backlog;
- validator GREEN on canonical data;
- invalid fixtures prove every failure mode;
- cycle detection proven;
- minimum PID validity proven: a PID that is missing, empty or effectively
  content-free does not satisfy delivery readiness;
- deterministic readiness output;
- first wave calculable;
- test suite GREEN;
- fresh FORGE Auditor GREEN;
- evidence + exact SHAs + PR;
- documentation shows how ROGUE consumes readiness without Matt.

## Approval

Approved for delivery by the Product Owner / Central Architecture. The PO gate
declared in this PID's header is satisfied for *PID approval* — the authority
that permitted this item to leave `PID_DRAFT` and reach `DELIVERY_READY`.

The approval record lives in GitHub and in this repository, not in this
paragraph:

- `maff0000/GOAL` issue #1 — the delivery tracking issue opened by the Product
  Owner. It names `pids/GOAL-DCP-001.md` as the canonical PID for this item,
  records the PO gate as YES and the Matt gate as NO, pins the base SHA
  `acc3f48ea3379843719741b56e30267845af78bd`, and states that merge is not
  authorised: delivery stops at the governed PR candidate.
- `operations/ROGUE-DISPATCH-GOAL-DCP-001.md` — ROGUE's record of being
  instructed to deliver this PID through the existing FORGE process.
- `backlog/backlog.yaml` — declares `po_gate: true` for `GOAL-DCP-001` and
  carries the item's current delivery state.
- `maff0000/GOAL` pull request #2, on branch `wo/GOAL-DCP-001`, with the
  evidence trail committed under `audits/`.

This section records approval **of this PID**, and nothing more. It is not a
record of delivery acceptance: acceptance of the delivered work is a separate,
later gate (`PO_ACCEPTANCE`) held by the Product Owner, and the item's current
delivery state is whatever `backlog/backlog.yaml` says it is — not whatever
this document might imply.

## Stop conditions

Return to PO if:
- GitHub capability requires a custom external service;
- FORGE doctrine would need modification;
- a new architecture decision is required.

Do not invent around a stop condition.
