# GOLD-AUD-D BASELINE: source inventory and baseline re-confirmation

Deliverable 1. CA evidence items 1 and 2.

## 1. PID/WO identifier and exact audited scope (CA item 1)

- Audit id: `GOLD-AUD-D` (child audit of `GOLD-MVP-001`), PID `pids/GOLD-AUD-D.md` at GOAL `main` `ceaf0291a43d029b1a47b1c192a62ff147f05ac0`. Approved by Central Architecture 15 and 16 October 2026 (PID, Approval section).
- Evidence branch: `wo/GOLD-AUD-D-evidence` (local, unpushed, no PR, in all three repositories).
- The single question (PID, Purpose, quoted): "what is the smallest set of missing capabilities that lets ONE order travel the whole DEMO path: HELIOS trigger in -> TRON claim / risk / size -> MT5 gateway place on DEMO -> reconcile -> evidence".
- The CA directive (PID, quoted verbatim): "Audit TRON D1 and its existing implementation candidates, risk rules, journal and trigger-intake assumptions. Coordinate with the ongoing MT5-GW-001 GitHub consolidation. Identify the smallest missing capabilities for one DEMO execution path. Do not duplicate existing MT5 work or disturb operating broker instances."
- Audited scope: six hops H1..H6 (trigger intake, claim/disposition and journal, risk and sizing, adapter, gateway and broker, reconcile and evidence); validation of the scope of the approved `TRON-T3A`; assessment of reuse candidates. Read-only. No code, no backlog edit, no broker session.

## 2. Source revisions (CA item 2)

Full 40-character SHAs, captured at audit start. Aliases are used in the citations of every other file in this folder.

| Alias | Repository / ref | Full SHA | On GitHub? |
|---|---|---|---|
| GOAL | `maff0000/GOAL` `main` | `ceaf0291a43d029b1a47b1c192a62ff147f05ac0` | yes |
| TRON-main | `maff0000/tron` `main` | `5577039b5db05e70effef72c7e59df14db408419` | yes |
| D1 | `maff0000/tron` `wo/WO-TRON-D1` | `37d5f009a080d25930eea37cf8c627bb0f3a1ff4` | yes (branch only, no PR) |
| GW | `maff0000/mt5-gateway` `main` | `6263d61f4cb0d4d5b16337e67c30f409bc9c5051` | yes |
| Legacy tooling | private repository, source text only | recorded in the private record | yes (private repository) |
| RAT | GOAL-programme branch `wo/GOAL-TRON-D1-RATIFY`, `audits/2026-10-14/tron-d1/RATIFICATION-PACKAGE.md` | `d5f6d32adb4e1cf8b1c19670fd27382dc67e9855` | NO (local branch of the programme repository) |
| H2 | GOAL-programme branch `wo/GOAL-RECON-H2-tradechain`, `audits/2026-10-14/reconciliation/RECON-H2.md` | `2780076e620dcc1f62e95b821b7e483093d21f42` | NO |
| RDY | GOAL-programme branch `wo/GOAL-MT5-READINESS`, `audits/2026-10-15/mt5-readiness/MT5-READINESS.md` | `fe43db38f821d53879585a919f211a16eec0d1b3` | NO |
| TPL | GOAL-programme branch `wo/GOAL-MT5-TEMPLATE`, `audits/2026-10-15/mt5-template/MT5-TEMPLATE-CONTRACT.md` | `6c92a43144a93525b73f4e06e5b7314145a48b72` | NO |
| DEMO | GOAL-programme branch `wo/GOAL-MT5-DEMO-VERIFY`, `audits/2026-10-15/mt5-demo/` | `da2e4ea907f3d966715b1ed39429b17cdc382933` | NO |
| T1C | GOAL-programme branch `wo/GOAL-PID-WAVE1-C-execution`, `pids/TRON-T1.md` | `3f14c5ef3c0c1e6f9e6a4eef34e78a17ad938fe9` | NO |
| TRG | GOAL-programme branch `wo/GOAL-CONTRACT-TRIGGER`, `pids/GOAL-TRIGGER-001.md` | `64c843b901d435a17efa56e3b2a1f925ad58c30b` | NO |

Limit on verifiability (UNVERIFIED for an outside reader): the RAT, H2, RDY, TPL, DEMO, T1C and TRG documents are on local branches of the programme repository that are not on GitHub (`git ls-remote` of GOAL lists only `main`, the DCP, backup-plan, portfolio, register and RECON-PR branches). They were read with `git show <branch>:<path>` from the programme repository without checking anything out or altering it. A reviewer without that local access can verify the SHAs only from the maintainers' record. All other citations resolve on GitHub.

Movement during the audit: `mt5-gateway` `main` was `6263d61f4cb0d4d5b16337e67c30f409bc9c5051` at start and when the evidence was finished (re-read with `git ls-remote`). `tron` `main` and D1 did not move.

## 3. Re-confirmation commands and results

Only facts that decide a gap-matrix cell are re-confirmed. Every command is read-only. Test runs were made from scratch copies outside every repository (`git archive` for D1; a scratch clone for the gateway, because three of its tests call `git ls-files`).

| # | Fact | Command (paths relative to the repository root) | Result |
|---|---|---|---|
| B1 | GOAL base and control-plane tools | `git rev-parse HEAD`; `./tools/goal-validate`; `./tools/secret-scan` | `ceaf0291...`; `backlog OK: 49 items`, exit 0; working tree and history CLEAN, exit 0 |
| B2 | Backlog has no `TRON-T3A` | `grep -c T3A backlog/backlog.yaml` | `0` |
| B3 | Backlog states of the path items | parse `state:` of each id | `MT5-GW-001` PID_DRAFT; `MT5-GW-002..004` ARCHITECTURE_REQUIRED; `TRON-D1-RATIFY` PID_DRAFT; `TRON-T1` PID_DRAFT; `TRON-T2..T4` ARCHITECTURE_REQUIRED; `HELIOS-T3`, `GOAL-TRIGGER-001`, `PAPER-E2E-001` ARCHITECTURE_REQUIRED; `GOLD-AUD-A..F` DELIVERY_READY |
| B4 | TRON `main` content | `git ls-tree -r --name-only origin/main` | 4 files: `.gitignore`, `.gitleaks.toml`, `PID.md`, `scripts/hooks/pre-commit`. No runtime code |
| B5 | D1 tip and distance | `git rev-parse origin/wo/WO-TRON-D1`; `git rev-list --count origin/main..origin/wo/WO-TRON-D1`; `--no-merges` variant | `37d5f009...`; 20; 11 |
| B6 | D1 size | `git diff --stat origin/main origin/wo/WO-TRON-D1 \| tail -1`; `git ls-tree -r --name-only origin/wo/WO-TRON-D1 \| wc -l` | 60 files changed, 5044 insertions, 0 deletions; 64 files in the tree |
| B7 | `wi-a..wi-i` | `git merge-base --is-ancestor origin/wo/WO-TRON-D1-wi-<x> origin/wo/WO-TRON-D1` for nine branches | all nine are ancestors of D1 (tips `b884fd4`, `c4b605a`, `4c2e907`, `b18c338`, `45ddefc`, `0458277`, `87e9453`, `8186127`, `32f4f54`) |
| B8 | Only one Python file; no executable, no deployment artefact | `git ls-tree -r --name-only origin/wo/WO-TRON-D1 \| grep -E '\.py$\|\.sh$\|Dockerfile\|compose\|\.sql'`; `grep -E 'rpyc\|MetaTrader\|socket\|urllib\|subprocess\|hmac\|ed25519\|requests' tests/test_docs_baseline.py` | one file, `tests/test_docs_baseline.py` (plus the pre-commit hook script inherited from `main`); the test module imports only `json`, `re`, `pathlib`, `pytest`, `yaml`, `jsonschema`; the grep returns nothing |
| B9 | D1 gate | `python3 -m pytest -q -p no:cacheprovider tests` in a scratch copy of D1 | `148 passed` |
| B10 | No pull request for D1; repository visibility | `gh pr list -R maff0000/tron --state all`; `gh api repos/maff0000/tron --jq .visibility` | one PR (#1, merged, gitleaks rules); `public` |
| B11 | Secret-scan count anomaly in D1's own evidence | `git rev-list --count 9b1bf70`; same at `37d5f00`; D1 `docs/evidence/WO-TRON-D1.md:44` | 23 and 24 reachable commits; the evidence file says "14 commits scanned" (anomaly confirmed, RAT section 2.5) |
| B12 | Gateway `main` | `git ls-remote origin refs/heads/main`; `git rev-list --count origin/main` | `6263d61f...`; 46 commits |
| B13 | Gateway tests and CI | `python3 -m pytest -q -p no:cacheprovider tests` in a scratch clone at `6263d61`; `gh run list -R maff0000/mt5-gateway -L 5` | `105 passed, 3 xfailed` (the three strict expected failures encode known hazards H1 to H3); workflow `validate` conclusion `success` for `6263d61` |
| B14 | No typed gateway in the source | `grep -rn -i 'client_order_id\|reconcile\|TIMEOUT_UNKNOWN\|place_order\|describe'` over `*.py`, `tools/mt5ctl`, `*.sh`, `Dockerfile`, `*.yml`, `*.json` | no match; `bridge/rpyc_server.py` (9 lines) is the stock all-attributes remote-execution service with no authentication |
| B15 | No in-container DEMO latch | `grep -n -i 'EXPECTED_TRADE_MODE\|trade_mode' start.sh Dockerfile deploy/compose.instance.yml` | no match (the environment value only appears as a compose label); `docs/KNOWN-LIMITATIONS.md:27` says the same |
| B16 | Gateway repository visibility; hardening issue | `gh api repos/maff0000/mt5-gateway --jq .visibility`; `gh issue view 10` | `public`; issue #10 OPEN ("Gate A follow-up: secrets ownership, symlink handling and audit notices") |
| B17 | Trigger contract status | `git ls-remote origin` of GOAL; backlog entry | no trigger branch on GitHub; `GOAL-TRIGGER-001` is in the backlog (ARCHITECTURE_REQUIRED, `pid_path` null); PID candidate only on the local branch TRG |
| B18 | Legacy sources (read as text only) | source inspection of legacy tooling and one legacy archive; nothing run, imported or connected to | see `CANDIDATES.md`; command detail is held in the private record |
| B19 | Graph check on current GOAL main | fetch `origin/main` (`e80fcda25a50140dc24793f2dd2770b1da2db517`, 50 backlog items); add `TRON-T3A` (`depends_on` `TRON-T1`) and add `TRON-T3A` to `TRON-T3.depends_on`; depth-first cycle check | acyclic; dependants of `TRON-T3`: `TRON-T5`, `PAPER-E2E-001`, `GOLD-MVP-001` |

## 4. What this audit did not read or do

- No broker call, gateway or bridge connection, container probe, Graylog, Redis, database or service access. No instance directory, secrets directory or credential file was opened.
- The source of the legacy live-flagged executor named in ADR-MT5-002 was not located among the sources this audit was permitted to read: UNVERIFIED.
- The legacy simulated-broker service was considered by role only (its README), not read further, to respect an internal isolation rule.
- `tron` PID section text beyond what RAT and the D1 documents quote was not re-read end to end; D1 documents 01, 02, 07, 08, 09 and 12 were searched, not read in full.
- HELIOS and FALCON repositories were not read (lane B and lane E); their claims are cited from H2 and TRG and marked as such.
