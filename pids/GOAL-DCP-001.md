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
5. A deterministic readiness command lists dependency-satisfied `DELIVERY_READY` work.
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
- backlog/PID metadata mismatch.

Create readiness output for items where:

```text
state == DELIVERY_READY
AND all dependencies are accepted terminal GREEN states
```

Example:

```json
{"ready":[{"id":"MT5-GW-001","target_repository":"maff0000/mt5-gateway"}]}
```

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
- deterministic readiness output;
- first wave calculable;
- test suite GREEN;
- fresh FORGE Auditor GREEN;
- evidence + exact SHAs + PR;
- documentation shows how ROGUE consumes readiness without Matt.

## Stop conditions

Return to PO if:
- GitHub capability requires a custom external service;
- FORGE doctrine would need modification;
- a new architecture decision is required.

Do not invent around a stop condition.
