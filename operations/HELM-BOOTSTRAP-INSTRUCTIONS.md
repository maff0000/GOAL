# HELM — GOAL Repository Bootstrap

**Target:** `dell-debian:/srv/GOAL` → `maff0000/GOAL`

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
