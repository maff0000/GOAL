# HELM — Preserve MT5 Audit and Bootstrap GOAL

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
