# Manifest

Every file tracked in this repository. The list below is generated from
`git ls-files` by `./tools/goal-docs`, so it cannot drift from what the
repository actually contains; untracked files are deliberately absent, because
an untracked file is not repository truth. Never hand-edit the generated
region — run `./tools/goal-docs --write` after committing new files.

<!-- BEGIN GENERATED: manifest -->

- `.github/workflows/control-plane.yml`
- `.gitignore`
- `MANIFEST.md`
- `README.md`
- `architecture/DELIVERY-CONTROL-PLANE.md`
- `audits/2026-10-11/mt5/EVIDENCE-HASHES.txt`
- `audits/2026-10-11/mt5/SUMMARY.md`
- `audits/2026-10-12/goal-dcp-001/AUDIT-VERDICT.md`
- `audits/2026-10-12/goal-dcp-001/DELIVERY-EVIDENCE.md`
- `backlog/MASTER-BACKLOG.md`
- `backlog/SCHEMA.md`
- `backlog/backlog.yaml`
- `conftest.py`
- `decisions/ADR-DELIVERY-001-GITHUB-AND-MEMORY-FABRIC.md`
- `decisions/ADR-MT5-001-REUSE-CONTAINER-REPLACE-BRIDGE.md`
- `decisions/ADR-MT5-002-LEGACY-LIVE-FLAGGED-EXECUTOR.md`
- `governance/DELIVERY-STATE-MACHINE.md`
- `operations/HELM-BOOTSTRAP-INSTRUCTIONS.md`
- `operations/HELM-NEXT-ACTIONS.md`
- `operations/ROGUE-DISPATCH-GOAL-DCP-001.md`
- `operations/ROGUE-READINESS.md`
- `pids/GOAL-DCP-001.md`
- `templates/DECISION-BRIEF.md`
- `tests/fixtures/README.md`
- `tests/fixtures/backlog-pid-mismatch.yaml`
- `tests/fixtures/cycle-disjoint.yaml`
- `tests/fixtures/cycle-three-node.yaml`
- `tests/fixtures/cycle-two-node.yaml`
- `tests/fixtures/cycle-via-chain.yaml`
- `tests/fixtures/delivery-ready-pid-key-absent.yaml`
- `tests/fixtures/delivery-ready-pid-wrong-type.yaml`
- `tests/fixtures/duplicate-dependency.yaml`
- `tests/fixtures/duplicate-id.yaml`
- `tests/fixtures/empty-field.yaml`
- `tests/fixtures/invalid-field-type.yaml`
- `tests/fixtures/invalid-lane.yaml`
- `tests/fixtures/invalid-priority.yaml`
- `tests/fixtures/invalid-risk.yaml`
- `tests/fixtures/invalid-state.yaml`
- `tests/fixtures/load-error-items-not-list.yaml`
- `tests/fixtures/malformed-dependency-id.yaml`
- `tests/fixtures/malformed-id.yaml`
- `tests/fixtures/malformed-target-repository.yaml`
- `tests/fixtures/maximally-broken.yaml`
- `tests/fixtures/missing-architecture-ref-file.yaml`
- `tests/fixtures/missing-field.yaml`
- `tests/fixtures/missing-pid.yaml`
- `tests/fixtures/missing-target-repository.yaml`
- `tests/fixtures/pid-file-not-found.yaml`
- `tests/fixtures/pid-fixture-beta.md`
- `tests/fixtures/pid-fixture.md`
- `tests/fixtures/pid-match.yaml`
- `tests/fixtures/pid-path-not-repo-relative.yaml`
- `tests/fixtures/precedence-lane-type.yaml`
- `tests/fixtures/self-dependency.yaml`
- `tests/fixtures/unknown-dependency.yaml`
- `tests/fixtures/valid.yaml`
- `tests/fixtures/wildcard-dependency.yaml`
- `tests/fixtures_readiness/dep_blocked.yaml`
- `tests/fixtures_readiness/dep_cancelled.yaml`
- `tests/fixtures_readiness/dep_candidate.yaml`
- `tests/fixtures_readiness/dep_closed.yaml`
- `tests/fixtures_readiness/dep_deployment_ready.yaml`
- `tests/fixtures_readiness/dep_live.yaml`
- `tests/fixtures_readiness/dep_matt_decision.yaml`
- `tests/fixtures_readiness/dep_merged.yaml`
- `tests/fixtures_readiness/dep_paper.yaml`
- `tests/fixtures_readiness/dep_po_acceptance.yaml`
- `tests/fixtures_readiness/multiple_ready.yaml`
- `tests/fixtures_readiness/no_pid_declared.yaml`
- `tests/fixtures_readiness/one_met_one_unmet.yaml`
- `tests/fixtures_readiness/pid-alpha.md`
- `tests/fixtures_readiness/pid-mike.md`
- `tests/fixtures_readiness/pid-zulu.md`
- `tests/fixtures_readiness/state_not_delivery_ready.yaml`
- `tests/fixtures_readiness/unresolvable_dependency.yaml`
- `tests/test_cli.py`
- `tests/test_docsync.py`
- `tests/test_first_wave.py`
- `tests/test_model.py`
- `tests/test_readiness.py`
- `tests/test_secret_scan.py`
- `tests/test_validate.py`
- `tools/goal-docs`
- `tools/goal-ready`
- `tools/goal-validate`
- `tools/goal_dcp/__init__.py`
- `tools/goal_dcp/docsync.py`
- `tools/goal_dcp/model.py`
- `tools/goal_dcp/readiness.py`
- `tools/goal_dcp/validate.py`
- `tools/secret-scan`

<!-- END GENERATED: manifest -->

Raw forensic evidence is held in a private evidence store (see `audits/2026-10-11/mt5/SUMMARY.md`), not in this repository.
