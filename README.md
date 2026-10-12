# THE GOAL — Delivery Control Plane

**Date:** 2026-10-11  
**Status:** BOOTSTRAP CANDIDATE

`maff0000/GOAL` is the central architecture and programme-control plane for THE GOAL.

Component repositories own code and implementation evidence. GOAL owns cross-system architecture, decisions, dependencies, canonical PIDs, programme backlog and delivery state.

> **If programme state cannot be reconstructed from GitHub, it is not authoritative.**

```text
Matt
  │ product/capital decisions only
  ▼
ChatGPT — Product Owner / Central Architecture
  │
  ▼
GitHub GOAL control plane
  │
  ▼
ROGUE — delivery train controller
  │
  ├── FORGE PL — project A
  ├── FORGE PL — project B
  └── FORGE PL — project C
          ├── Engineers
          └── independent Auditor
```

> **Architecture before PID. PID before build. Evidence before acceptance.**

> **ROGUE schedules. FORGE delivers. GitHub remembers. The PO adjudicates. Matt decides only what genuinely requires Matt.**

## Current MT5 decision

HELM has proven the Vantage MT5 direction: retain the Docker/Wine/MT5 platform, reconcile its Git history, replace the unrestricted bridge, prove the complete DEMO execution path, then bind TRON through a broker-neutral adapter.

Memory Fabric remains permanent agent memory; GitHub remains architecture/build/delivery truth.
