# HELM — Preserve MT5 Audit and Bootstrap GOAL

> ## HISTORICAL — COMPLETED. NOT LIVE INSTRUCTIONS.
>
> Both parts below have completed. The bootstrap landed as commit `acc3f48`
> (`GOAL-000: establish public delivery control plane authority`), the root
> commit of `main`, pushed to `maff0000/GOAL`; the preserved MT5 audit is in
> the repository under `audits/2026-10-11/mt5/`. This file is retained as the
> record of what was instructed. It is not a task list, and it must not be
> re-run — step 1 below requires `maff0000/GOAL` to have no refs, which is no
> longer true.
>
> **Recorded discrepancy, not corrected:** step 6 below specified the commit
> message `GOAL-000: bootstrap delivery control plane and audit authority`, and
> `HELM-BOOTSTRAP-INSTRUCTIONS.md` specified `GOAL-000: bootstrap delivery
> control plane authority`. The commit actually on `main` is
> `GOAL-000: establish public delivery control plane authority`. History is not
> rewritten to match the instruction and the instruction is left exactly as it
> was issued; the divergence is recorded here instead.
>
> **Superseded by:** `README.md` for the repository's current state, and
> `operations/ROGUE-READINESS.md` for how delivery work is now selected.

## Part A — already complete

The MT5 audit is preserved under:

`/tmp/goal-mt5-audit-2026-10-11/`

with SHA-256 checksums.

## Part B — bootstrap

Use this exact pack:

`GOAL-DELIVERY-CONTROL-PLANE-BOOTSTRAP-V2-2026-10-11.zip`

1. Re-check that `maff0000/GOAL` still has no refs.
2. Initialise `/srv/GOAL` with that remote.
3. Extract the pack contents into the repository root.
4. Copy the preserved MT5 audit unchanged into `audits/2026-10-11/mt5/`.
5. Secret-scan.
6. Make the single authorised bootstrap commit on `main`:
   `GOAL-000: bootstrap delivery control plane and audit authority`
7. Push.
8. Return exact SHA, remote SHA, changed paths, scan result and clean-tree proof.
9. Stop. Do not implement GOAL-DCP-001 yet.

After this bootstrap exception, no further direct-to-main work is authorised.
