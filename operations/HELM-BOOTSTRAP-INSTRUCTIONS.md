# HELM — GOAL Repository Bootstrap

> ## HISTORICAL — COMPLETED. NOT LIVE INSTRUCTIONS.
>
> The bootstrap described below has completed. It landed as commit `acc3f48`
> (`GOAL-000: establish public delivery control plane authority`), the root
> commit of `main`, pushed to `maff0000/GOAL`. This file is retained as the
> record of what was instructed. It is not a task list, and it must not be
> re-run — step 2 below requires an empty remote, which `maff0000/GOAL` no
> longer is.
>
> **Recorded discrepancy, not corrected:** step 6 below specified the commit
> message `GOAL-000: bootstrap delivery control plane authority`, and
> `HELM-NEXT-ACTIONS.md` specified `GOAL-000: bootstrap delivery control plane
> and audit authority`. The commit actually on `main` is
> `GOAL-000: establish public delivery control plane authority`. History is not
> rewritten to match the instruction and the instruction is left exactly as it
> was issued; the divergence is recorded here instead.
>
> **Superseded by:** `README.md` for the repository's current state, and
> `operations/ROGUE-READINESS.md` for how delivery work is now selected.

**Target:** the HELM-managed local working copy on the operations host → `maff0000/GOAL`

Central Architecture's GitHub connector can read the repository but its App cannot write it (`403 Resource not accessible by integration`).

HELM is authorised for the minimal bootstrap only.

1. Verify `/srv/GOAL` remote is exactly `maff0000/GOAL`.
2. Verify the remote repository is still empty, or stop and report drift.
3. Copy this pack's **contents** into `/srv/GOAL` so `README.md`, `architecture/`, etc. are at repo root.
4. Secret-scan before commit.
5. Because an empty GitHub repo has no base ref, create one initial commit on `main`.
6. Commit message: `GOAL-000: bootstrap delivery control plane authority`
7. Push.
8. No further direct-to-main work after this bootstrap exception.
9. Return exact pre-state, changed paths, secret-scan result, commit SHA, remote main SHA and clean-tree proof.
10. Do not implement GOAL-DCP-001.

Stop.
