# THE GOAL — Delivery Control Plane

**Status:** BOOTSTRAPPED — authoritative.

The bootstrap is complete. This repository was established by commit
`acc3f48` (`GOAL-000: establish public delivery control plane authority`), the
root commit of `main`, pushed to `maff0000/GOAL`, from the delivery-control-plane
bootstrap pack dated 2026-10-11. `maff0000/GOAL` is now the live control plane
of record rather than a candidate for one. The bootstrap instructions that
produced it are retained under `operations/`, marked historical.

`Status` above describes this repository, not a work item. Per-item delivery
state belongs to `backlog/backlog.yaml` and the vocabulary in
`governance/DELIVERY-STATE-MACHINE.md`; it is deliberately not restated here,
because a delivery state copied into prose goes stale and then lies.

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

## Delivery control plane

`backlog/backlog.yaml` is the **machine-readable authority** for programme
delivery state — one entry per work item carrying its lane, component, target
repository, priority, risk, delivery state, dependencies, PO/Matt gates,
canonical PID path and architecture references. `backlog/SCHEMA.md` is the
field reference for it.

`backlog/MASTER-BACKLOG.md` is the **human view generated from that YAML**. Its
generated regions are rendered from the authority and are never hand-edited.
When the two disagree, the YAML is correct and the markdown has drifted.

Four commands operate the plane. All of them are deterministic and offline:
they read repository state and report. None of them mutates the backlog,
dispatches work, or merges anything.

| command | what it does | exit codes |
|---|---|---|
| `./tools/goal-validate` | Validates `backlog/backlog.yaml` — duplicate ids, unknown or wildcard dependencies, dependency cycles, invalid lane/state/priority/risk, missing or malformed target repository, state-conditional missing PID, and backlog/PID metadata mismatch. Prints `backlog OK: N items` when clean, otherwise one finding per line to stderr. | `0` valid, `1` findings, `2` load error |
| `./tools/goal-ready` | Answers "what work is ready next?" as a single line of JSON. Validates first and refuses to answer from an invalid backlog. Options: `--assume-closed ID[,ID...]` for a planning projection, `--with-pid` to include each item's canonical PID path. | `0` ok, `1` invalid backlog, `2` load or usage error |
| `./tools/goal-docs --check` | Reports drift between the generated regions of `backlog/MASTER-BACKLOG.md` and `MANIFEST.md` and actual repository truth. `--write` rewrites the drifted regions in place. | `0` in sync, `1` drift found, `2` error |
| `./tools/secret-scan` | Scans the working tree and the full git history with gitleaks. This repository is public and stays public; this is the repeatable proof that no secret has entered it. | `0` clean, `1` findings, `2` gitleaks unavailable |

The acceptance test command for the control plane, run from the repository
root:

```bash
python3 -m pytest tests/ -q
```

`.github/workflows/control-plane.yml` runs the validator, the generated-document
drift check, the secret scan and the test suite on every push to `main` and
every pull request, so the plane enforces itself. That workflow only validates:
it does not merge, deploy, mutate issues or launch FORGE.

See **`operations/ROGUE-READINESS.md`** for how ROGUE consumes
`./tools/goal-ready` to decide what to dispatch next without asking Matt.

## Current MT5 decision

HELM has proven the Vantage MT5 direction: retain the Docker/Wine/MT5 platform, reconcile its Git history, replace the unrestricted bridge, prove the complete DEMO execution path, then bind TRON through a broker-neutral adapter.

Memory Fabric remains permanent agent memory; GitHub remains architecture/build/delivery truth.
