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

State names are the canonical vocabulary of
`governance/DELIVERY-STATE-MACHINE.md`; the annotations say who acts and what
gates the step.

```text
ARCHITECTURE_REQUIRED          architecture owned, no PID yet
   ↓
PID_DRAFT                      PO authors the canonical PID
   ↓
PO_REVIEW                      PO gate on the PID
   ↓
DELIVERY_READY                 requires an approved canonical PID
   ↓
ROGUE_DISPATCHED               ROGUE starts a FORGE PL
   ↓
FORGE_BUILD                    PL → parallel bounded Engineers
   ↓                           → PL tests/reconciliation
FORGE_AUDIT                    fresh independent Auditor
   ├── RED → REPAIR → FORGE_AUDIT
   └── GREEN
          ↓
PO_ACCEPTANCE
          ↓
MATT_DECISION                  only when declared
          ↓
CANDIDATE → MERGED → DEPLOYMENT_READY → PAPER → LIVE
```

`ARCHITECTURE_REQUIRED` is entered from the backlog, and `DISCOVERED` precedes
it. `BLOCKED` can suspend any point in the loop and `CANCELLED` can end it.
Per-item state is in `backlog/backlog.yaml`, never in this diagram.

**Architecture before PID. PID before build.** The arrow into
`DELIVERY_READY` is gated on an approved canonical PID that exists and agrees
with the backlog: no PID means the item stays pre-delivery, and ROGUE never
sees it as dispatchable. `governance/DELIVERY-STATE-MACHINE.md` is the
authority for that rule.

## Parallelism

ROGUE may launch independent FORGE PLs in parallel when:
- dependencies are GREEN;
- contract versions are frozen for the increment;
- repositories/workspaces do not collide;
- no ungoverned shared mutable environment is involved.

## Automation maturity

The rungs are the `GOAL-DCP-*` work items, in increasing order of how much the
control plane does on its own. The ordering is not a single chain: rungs 3 and
4 both build on rung 2 and are independent of each other.

1. **`GOAL-DCP-001` — GitHub control-plane authority.** Machine-readable
   backlog, deterministic validation, dependency graph, strict delivery
   readiness, generated human views, CI enforcement. GitHub becomes the
   authoritative programme surface.
2. **`GOAL-DCP-002` — ROGUE dispatcher: deterministic consumption and
   multi-project dispatch control.** ROGUE consumes canonical GOAL state and
   safely dispatches independent FORGE PLs across projects without Matt
   mediating work selection. Dispatch remains something ROGUE performs, not
   something a GitHub event triggers.
3. **`GOAL-DCP-003` — automated GitHub-triggered sandboxed delivery launch.**
   A GitHub event starts a sandboxed FORGE session. Attempted only after
   DCP-002's dispatcher behaviour is proven in real multi-project use.
4. **`GOAL-DCP-004` — automated PO/ROGUE status and stale/blocked brief.**
   Deterministic reporting on programme state: what is moving, what is stale,
   what is blocked and on what.

`backlog/backlog.yaml` is the authority for the risk, state and dependencies
of each of these; they are deliberately not restated here.

### The maturity boundary

The line between rungs 2 and 3 is the one that matters, because it is easy to
blur and expensive to blur:

- **DCP-002 is deterministic consumption and dispatch control.** ROGUE reads
  canonical state and decides what to dispatch. It is not GitHub-triggered
  execution, and nothing runs because a commit or an issue event happened.
- **DCP-003 is GitHub-triggered automated launch**, and only after DCP-002 is
  proven. Automating the trigger before the dispatch decision itself is
  trustworthy would mean automating an unproven judgement.
- **No rung introduces auto-merge.** Not at rung 4, not for low-risk PIDs with
  deterministic gates, not ever. Merging is a human-authorised act on reviewed
  evidence; an Auditor GREEN is an input to that decision, not a substitute
  for it. Nothing in this control plane merges, releases or deploys on its own
  at any maturity level.
