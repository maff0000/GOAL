# GOAL Delivery Control Plane Architecture

## Problem

THE GOAL is now too large for Matt to act as the message courier between HELM, Central Architecture, ROGUE and FORGE.

The control plane externalises programme state into GitHub and makes delivery dependency-aware.

## Authority

### Matt
Owns product intent, capital activation and genuine owner decisions. Not routine implementation.

### Product Owner / Central Architecture
Owns architecture, priority, backlog, PIDs, dependencies, reuse decisions and PO acceptance.

### ROGUE
Owns readiness checks, parallel scheduling and FORGE dispatch. ROGUE cannot change architecture.

### FORGE
Existing PID → PL → Engineer(s) → independent Auditor → repair → PR loop remains the implementation engine.

### HELM
Default read-only discovery/audit. Mutations require an explicit operations work order.

## Durable surfaces

- GOAL repo: architecture, ADRs, backlog, dependency graph, canonical PIDs.
- Component repo: source, tests, implementation evidence, PR/release.
- GitHub Issues/Project: live delivery state.
- GitHub PRs: proposed changes and review history.

No chat, Redis, Fabric, local scratchpad or agent process is authoritative delivery state.

## Delivery loop

```text
ARCHITECTURE
   ↓
BACKLOG
   ↓
PID_DRAFT
   ↓
PO_REVIEW
   ↓
DELIVERY_READY
   ↓
ROGUE
   ↓
FORGE PL
   ↓
parallel bounded Engineers
   ↓
PL tests/reconciliation
   ↓
fresh Auditor
   ├── RED → repair → audit
   └── GREEN
          ↓
PO_ACCEPTANCE
          ↓
MATT_GATE only when declared
          ↓
MERGE / RELEASE / DEPLOY
```

## Parallelism

ROGUE may launch independent FORGE PLs in parallel when:
- dependencies are GREEN;
- contract versions are frozen for the increment;
- repositories/workspaces do not collide;
- no ungoverned shared mutable environment is involved.

## Automation maturity

1. **DCP-1 GitHub authority** — backlog/PID/state/validation.
2. **DCP-2 ROGUE dispatcher** — compute delivery-ready work and launch independent PLs.
3. **DCP-3 automated launch** — GitHub event starts sandboxed FORGE sessions.
4. **DCP-4 selective auto-merge** — only for explicitly low-risk PIDs with deterministic gates and Auditor GREEN. Never capital-gated work.
