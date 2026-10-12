# ADR-DELIVERY-001 — GitHub and Memory Fabric Have Distinct Authorities

**Status:** ACCEPTED  
**Date:** 2026-10-12

## GitHub

GitHub is durable architecture/build/delivery truth: architecture, PIDs, source, backlog/dependencies, PRs, build/audit evidence and release state.

## Memory Fabric

Memory Fabric is permanent agent memory: durable agent context, learned findings, continuity across sessions, and concise conclusions/pointers to authoritative GitHub evidence.

Memory Fabric is not a build gate and GitHub does not replace agent memory.

Agents may backfill concise semantic memories about the MT5 audit, referencing canonical GitHub evidence once committed. A Fabric write is not required to close a build PID unless an explicit agent-memory requirement says so.
