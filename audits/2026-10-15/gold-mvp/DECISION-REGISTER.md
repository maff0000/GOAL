# GOLD MVP decision register

**Work order:** `GOAL-GOLD-PORTFOLIO`. **Baseline:** GOAL `main` @ `1739e742154c77e9e2a96927dc40d4978b9cd798`. **Date:** 2026-10-15.
**Nature:** one de-duplicated, ranked register of every open decision for the PO. It records no decision and no approval. It supersedes the PD list in `PORTFOLIO.md` section 12 (PD ids are kept as references) and consolidates the open decisions of `pids/GOLD-MVP-001.md` and `pids/GOLD-AUD-A.md` to `-F.md` and the pending GOAL PR #5 and #6 items.
**Owners:** PO, Matt (production access, capital, Matt-gated items), CA (contract and numbering authority). Minor findings are not listed; each lane PID keeps its own.
**Closed by the consolidation:** CA's evidence numbering (lane decisions E D-3 and F D8 retired); amend-versus-new is now a confirmation (DR-3), not an open question.
Source key: `A D1` = decision D1 of `GOLD-AUD-A`; `B 1` = decision 1 of `GOLD-AUD-B`; `C D-C1`; `D 1`; `E D-1`; `F D1`; `MVP D-1`; `PD-n` = PORTFOLIO section 12; `T D-n` = `GOAL-TRIGGER-001`.

## 1. Needed to approve the portfolio and dispatch the audits

| id | question | options | recommended outcome | owner | blocks | source |
|---|---|---|---|---|---|---|
| DR-1 | `GOLD-MVP-001` versus `PAPER-E2E-001` | (a) supersede; (b) keep both, `PAPER-E2E-001` depends on `GOLD-MVP-001`; (c) independent | (b) | PO | approval of `GOLD-MVP-001`; patch part 2 | PD-1, MVP D-1 |
| DR-2 | Header gates of `GOLD-MVP-001` | risk `capital` + Matt gate; or `high` with Matt gate only at PAPER | `capital`, Matt gate true | PO, Matt informed | approval of `GOLD-MVP-001` | PD-2, MVP D-2 |
| DR-3 | Confirm each lane is a new bounded item (all six drafters concluded new) rather than an amendment | new for all six (fallbacks in `PORTFOLIO.md` section 3), or amend per lane | new for all six | PO / CA | approval of each lane PID | PD-3, A D6, B 1, C D-C2, D 1, E D-1, F D1 |
| DR-4 | Read-only production Redis access for lane A (via which operator and read path) | allow under the 6.2 / S1-S9 protocol; require the Matt gate; repo-only audit | allow under the protocol; `GOLD-AUD-A` `matt_gate` stays true until Matt waives it in one line | PO records, Matt confirms | start of A's runtime half; A approval | PD-5, A D1 |
| DR-5 | Which Redis instance and logical DB is "PROD" for lane A (fabric sources disagree by about 250 times on key count) | operator identifies by build-info environment match and records evidence; stop if ambiguous | as stated | PO | A approval | A D2 |
| DR-6 | Run A before or after the pending PROD recreate (config on disk is ahead of the running container) | now, flag the skew; after | now; a short delta later is a separate increment | PO | A approval | A D5 |
| DR-7 | Freeze owner of CP-1 (HERMES Redis to HELIOS input contract) | a `HERMES-FACT-001` PID with C's package as input; a small GOAL item; a section of `GOAL-CONTRACT-001` (C rejects: it excludes fact payloads) | `HERMES-FACT-001` PID | PO / CA | C approval; CP-1 freeze | C D-C1 |
| DR-8 | Authority of the trigger contract and the Matt gate of `GOAL-TRIGGER-001` (its blockers D-1..D-4, D-12 and Matt gate D-3 are open; the PID text is on a branch, the backlog item arrives with PR #5) | CA confirms D-12; Matt decides D-3 | decide D-12 and D-3 before CP-2 draft-freeze, `HELIOS-T3`, `TRON-T4` | CA, Matt | CP-2 freeze; trigger path (long pole) | C (carried D-12, D-1..D-6, D-8, S-1, S-2, O-2, O-4), D 5, T D-3 |
| DR-9 | Order of applying backlog changes and GOAL PR #5 / #6 | #5 merges first (40 to 43 items); then patch part 1 (49); then part 2 after DR-1 (50); #6 is documentation only, `MANIFEST.md` collision resolved by `goal-docs --write` | #5, part 1, part 2 serially, never concurrent writers | PO | patch application | PD-10, `PORTFOLIO.md` 11.1 |
| DR-10 | Dispatch all six audits concurrently | all six in wave 0; stagger C last | all six (collision-free by design; C finalises last) | PO | ROGUE scheduling | PD-6 |
| DR-11 | Where sanitised evidence samples live | public repo excerpts + private full captures; GOAL pointer-only | sanitised excerpts public, full captures private by identifier | PO | A, B approval | A D4, B 3, E D-9 |
| DR-12 | Confirm FALCON is evidence-only and never gates an entry (reverses falcon Decision 16 coupling) | confirm; keep coupling | confirm | PO (CA) | E approval | E D-2 |
| DR-13 | Priority and risk values of the audit items (patch draft: all P0; lane PIDs: E and F say P1; C and D say risk medium) | P0 for all; P1 for E, F | P0 for all six (E and F feed acceptance); risk as the lane PIDs | PO | patch content | PORTFOLIO 2, E header, F header |
| DR-14 | Lane B form and scope: pre-increment of `HELIOS-T2` (implied fallback: fold into the T2 PID); and is `HELIOS-T2` in scope for ARES (RECON-H2 contradiction) | new vs fold-in; T2 ARES scope | new; the ARES question blocks the T2 PID, not B | PO | B approval; T2 PID | B 1, B 2 |
| DR-15 | Evidence PR location and spread for D and F (lane PIDs: GOAL record plus mirrors in tron / mt5-gateway, and CER / HSA / DARWIN / neo; first draft: tron primary, CER primary) and the PR into private `maff0000/neo` | primary plus companion notes; one PR per repository | GOAL record plus bounded mirror PRs; `neo` PR only with PO approval | PO | D, F approval; `neo` PR | PD-12, D deliverables, F D10 |

## 2. Needed before the audit runs

| id | question | options | recommended outcome | owner | blocks | source |
|---|---|---|---|---|---|---|
| DR-16 | Sampling duration for lane A | M15 + H1 boundary; include an H4 boundary and a session close | M15 + H1 now; H4 only if it falls in the window | PO | A run | A D3 |
| DR-17 | May D use an in-memory journal port for the credential-free first path ahead of the Postgres decision (R-4 stays undecided) | yes; wait for R-4 | yes, classification only | PO | D run | D 2 |
| DR-18 | May D and F read NEO's practice bridge and legacy executors as source text only (no run, no import) and how NEO executor wording is handled | text only; none | text only; disposition not decided here | PO | D, F run; `neo` PR scope | D 4, F D5 |
| DR-19 | Does D's trigger-assumption area wait for `GOAL-TRIGGER-001` or proceed with an assumption register | wait; proceed | proceed, refresh when the contract exists | PO | D area 4 | D 5 |
| DR-20 | Authenticated read-only Graylog access for E (or a HELM-run export) | grant; accept UNVERIFIED rows | HELM-run read-only export; E may close with UNVERIFIED | Matt (credentials) / HELM | E UNVERIFIED rows | E D-4 |
| DR-21 | Licence posture for GPL / AGPL libraries (backtrader fork, backtesting.py) | compatible with repository visibility; not | PO ruling before any reuse recommendation is acted on | PO | acting on F reuse advice | F D9 |
| DR-22 | Matt-owned inputs D needs only to classify: DEMO account entitlement and instance choice, simulated lane versus state `PAPER` (R-9), TRON ratification R-1, R-2, R-4..R-8 | by id in `TRON-D1-RATIFY` and DEMO-verify | Matt answers in the ratification flow, not in this audit | Matt | D classification; later TRON items | D 3, D 6, D 7, R-12 |
| DR-23 | First GOLD strategy and qualification threshold (B ranks, F qualifies; lane F says it blocks approval, portfolio says acceptance) | simplest single-timeframe package the PROD publication satisfies; `gold_context_breakout` (chained H4 + M5, SMA vs EMA naming) | simplest single-timeframe package; threshold fixed by PO before the run | PO (Matt if capital choice) | F approval or acceptance (contradiction) | PD-8, MVP D-5, B 5, F D2 |

## 3. Later

| id | question | options | recommended outcome | owner | blocks | source |
|---|---|---|---|---|---|---|
| DR-24 | Add the missing MVP items: fixed-size sizing (TRON-owned), minimum FALCON publication work, FALCON-T2/T3 to the backlog | add after D and E report; fold into TRON-T3 / FALCON-T3; wait for TRON-T5 | add bounded items after D and E; do not wait for TRON-T5 / CER-R1 | PO | MVP acceptance | PD-4, MVP D-3, D-4, E D-7 |
| DR-25 | Composition vehicle: `GOLD-STRATEGY-RUNTIME` and deferred `PLATFORM-RT-001` | adopt; adapt; per-component | decide after B; do not rebuild a delivered runtime | PO | acceptance | PD-7, MVP D-7 |
| DR-26 | Price basis for the MVP (feed versus futures truth versus CFD) | plumbing proof only; require HMT-3H first | plumbing proof, no performance claim | PO | acceptance | PD-9, MVP D-6 |
| DR-27 | CP-1 mechanics: who maps `v1` to the HELIOS fact schema string (and fixes HELIOS's two version strings), reader placement outside the pure engine, numeric form on the wire | HERMES republishes; adapter; HELIOS accepts `v1` | reader adapter outside the engine, exact-decimal conversion, transport mapping only | CA / PO | CP-1 freeze; `HELIOS-T2` | C D-C3, D-C4, D-C5 |
| DR-28 | Spelling canon at the HERMES boundary (`XAU_USD` / `H4` versus `XAUUSD` / `4H`) | one canon in the fact grammar | ruling by `HERMES-FACT-001` / `GOAL-CONTRACT-001`; audits report only | PO | T2 mapping | B 4 |
| DR-29 | FALCON follow-ups: durable backfill after an outage, where trigger evidence is emitted, retire `tron.discovery_service` | accept loss or gap-fill from journals; publisher vs HELIOS; retire / rename | gap-fill from publisher and TRON journals; publisher after outbox commit; retire | PO / falcon architect | FALCON-T2/T3, `HELIOS-T3` PID | E D-5, D-6, D-8 |
| DR-30 | Strategy-chain terms: representation authority, `EdgeProfileVersion`, strategy-health authority, meaning of `LEAN-P1` / `DARWIN-R2` | per RECON-G and RECON-H1 | rule only if the MVP needs them (audit F reports); defer otherwise | PO | CER-R1, TRON-T5, hop 2 / 9 conclusions | F D3, D4, D6, D7 |
| DR-31 | Does A's comparison table become the HERMES contract registry | audit records only; becomes the registry | audit records only; the registry belongs to `HERMES-FACT-001` | PO | none | A D7 |
| DR-32 | Visibility of `maff0000/mt5-gateway` (public per MT5-READINESS, an earlier record says private) | owner confirms | owner decision outside this portfolio; evidence treated as public-level meanwhile | owner / PO | none (flagged) | PD-11 |
