# GOLD-AUD-D FINDINGS: findings, contradictions and the TRON-T3A scope validation

Deliverable 8. CA evidence items 6, 9 and (for unresolved items) 10.

Findings are reported only. No backlog entry, PID, ADR, decision or repository was edited, and nothing here applies a change. Class vocabulary (PID): PROVEN, INFERRED, UNPROVEN. Label vocabulary (programme brief): PROVEN, PARTIAL, UNVERIFIED, MISSING. Severity (portfolio 7.1 item 6): BLOCKER, MAJOR, MINOR. Aliases are in `BASELINE.md` section 2.

## 1. Signed statement (CA evidence item 9, PID checklist)

The author of this evidence, acting as the FORGE PL for GOLD-AUD-D, states that during this audit:

- no broker was contacted and no broker session of any kind was opened;
- no connection was made to the existing unrestricted bridge, to any gateway or MT5 service, to any container, Redis, Graylog or database;
- no legacy executor was run, imported, modified, stopped or connected to; legacy executor sources were read as text only (`CANDIDATES.md`);
- no instance directory, secrets directory or credential file was opened;
- nothing was pushed, no pull request was opened, no GitHub comment was made, and no existing checkout or worktree was edited.

Reads were made by `git` (clone, log, show, archive, ls-tree, ls-remote), `gh` read calls, file reads, and test runs from scratch copies outside every repository.

## 2. TRON-T3A scope validation (PID audit area 2; DR-36 condition)

Subject: the approved-as-proposed `TRON-T3A` of `PORTFOLIO.md` 11.4 (read at GOAL@ceaf029), validated against the PID's six elements, `TRON-T1`, `TRON-T3`, and the single-kill-switch rule, **under the Central Architecture arrangement of 16 October 2026**: `TRON-T3A` depends on `TRON-T1` and OWNS the minimum credential-free DEMO sizing and risk baseline including ONE enforceable kill switch; `TRON-T3` EXTENDS that implementation. This supersedes the 15 October wording ("`TRON-T3A` must reuse or extend `TRON-T3`"), which an earlier draft of this section followed. Lane D validates the dependency arrangement. Reported as findings only: `backlog/backlog.yaml` is untouched (B2). Graph checks (B19) use GOAL `main` `e80fcda25a50140dc24793f2dd2770b1da2db517`.

### 2.1 Does its content match the six elements?

| # | Required element (PID audit area 2; `PORTFOLIO.md` 3b) | In the `TRON-T3A` title and 11.4 text | Match |
|---|---|---|---|
| 1 | fixed DEMO base quantity from configuration | "fixed base quantity from config" | yes |
| 2 | one-position-per-instrument rule | "one position per instrument" | yes |
| 3 | maximum open positions | "max open positions" | yes |
| 4 | maximum daily loss and trade-count guard | "daily loss and trade-count guard" | yes |
| 5 | kill switch with a setter | "kill switch with setter" | yes (owned by `TRON-T3A`, see 2.4) |
| 6 | hard gates before submit, fail-closed | "hard gates before submit" (fail-closed is in 3b, not in the title) | yes |

Result: the title and text carry all six elements. PROVEN (F-D-02).

### 2.2 Does it need a broker credential?

No. Every element is deterministic code over configuration, a journal and an adapter's read results; each has a smallest credential-free proof with the simulated adapter and an in-memory journal port (`INCREMENTS.md`, `GAP-TRON-FIXED-SIZE-DEMO-RISK` row). Two qualifications, neither a credential need: (a) the inputs for open positions and daily profit and loss come from broker truth at run time, so at DEMO they come through the adapter's reads (a class (b) fact, not a T3A dependency); (b) placeholder values for the proof are not the real broker limits, which only a DEMO read-only session gives (G-24). PROVEN for the logic, INFERRED for the input path.

### 2.3 Relation to TRON-T1

`TRON-T3A` as drafted: `depends_on: [TRON-T1]`. That is correct and necessary: trade-count, daily loss and one-position state need the journal and the adapter interface that `TRON-T1` carries (`T1C@3f14c5e pids/TRON-T1.md` scope 2 to 5). `TRON-T1` explicitly leaves "limits and kill state" to `TRON-T3` (`T1C@3f14c5e` scope 4: "Enforcement of limits and kill state is TRON-T3"). PROVEN.

### 2.4 The CA arrangement: is it sound?

Yes, with the corrections in 2.5. Reasons:

- It matches how the pieces already divide. `TRON-T1` leaves "limits and kill state" to a later item (`T1C@3f14c5e` scope 4). The six elements are the smallest set a DEMO order needs, and element (5) cannot exist without a state store, setter and clearer, so the item that needs the kill switch first should create it once. `TRON-T3` (hard risk limits beyond the minimum) then extends it, rather than the reverse.
- It removes the structural conflict of the 15 October text. With T3A creating the switch and T3 extending it, there is one owner of the creation and a clear order.
- Graph check (B19, GOAL `main` `e80fcda`, 50 items, no `TRON-T3A` yet): adding `TRON-T3A` (`depends_on: [TRON-T1]`) and adding `TRON-T3A` to `TRON-T3.depends_on` leaves the dependency graph acyclic. The dependants of `TRON-T3` are `TRON-T5`, `PAPER-E2E-001` and `GOLD-MVP-001`; none depends on anything that would depend on `TRON-T3A` except through `TRON-T3`, so no cycle is introduced.

What the arrangement still leaves open (F-D-01):

- As drafted, `TRON-T3` has `depends_on: [TRON-T1]` and `TRON-T3A` has `depends_on: [TRON-T1]`: siblings. "T3 extends T3A" is stated in prose but not expressed. If `TRON-T3` were built first it would have to create a kill state of its own.
- The minimum DEMO path then no longer waits for `TRON-T3` in full (exposure, drawdown, consecutive-loss and risk-lock automation, event-risk additions) and therefore not for `TRON-T5`, which depends on `TRON-T3`. It waits for `TRON-T3A`. Formally, however, `PAPER-E2E-001` and `GOLD-MVP-001` list `TRON-T3` as a direct dependency; unless the PO relaxes those edges, the item graph keeps `TRON-T3` on the path even though the minimum path does not technically need it.

Scope that would still create a second kill switch: (i) `TRON-T3` defining a state store, setter or command of its own; (ii) any check or configuration key in either item that blocks new risk through a store other than the one kill state; (iii) an operator command that is not the `TRON-T3A` setter; (iv) `TRON-T3` delivered before `TRON-T3A`.

Related definitional risk already present in the design (INFERRED, F-D-14): the stage-0 check set has two separate stores, CHK-074 "manual kill switch" (operator flag) and CHK-064 "active risk lock" (internal risk-lock state, BL-RISK-08), each with its own "state store unreachable" error (D1@37d5f00 `docs/06-CHECKS-CATALOGUE.md:80-81`); the `system.halted` event names a third state (`docs/09-EVENTS-AND-GRAYLOG.md:67`); the reconciliation-integrity "no new risk" signal is a fourth input (`T1C@3f14c5e` scope 4); the gateway template has its own REFUSE_ALL state and caps (`TPL@6c92a43` sections 8.3 and 10.1, M1 and M6); `GOAL-TRIGGER-001` adds publisher-heartbeat loss as another "block new entries" cause (TRG@64c843b "Recovery"). None is wrong as an input; each becomes a competing switch if it is a separate store with its own setter.

### 2.5 Validation result and recommended corrections (findings, not applied)

`TRON-T3A` is valid as a credential-free, high-risk, P0 item whose content matches the six elements, and the CA arrangement is sound. Corrections for CA/PO to consider before the backlog change (the audit decides nothing):

1. `TRON-T3.depends_on` gains `TRON-T3A` (acyclic, 2.4). `TRON-T3A.depends_on` stays `[TRON-T1]`.
2. `TRON-T3A` delivers the single kill state record, its setter and clearer, and the reason codes, and its acceptance includes a one-writer test: a repository test asserts exactly one module writes the kill state and that every refusal reason maps to that state or to a gate result. `TRON-T3` extends it (more sources and checks) and must pass the same test.
3. One-state rule (kept): the risk lock, the reconciliation-integrity signal, hard-limit breach and publisher-heartbeat loss either engage the single kill state with a recorded reason or are "block new risk" gate results that are not a switch; the gateway's REFUSE_ALL state and caps are a separate layer that TRON reads and never substitutes for its own kill state.
4. Because T3A now carries the minimum gate set (Annex B of `GAP-MATRIX.md`), it needs an enforcing gate for the one-position rule (F-D-05) and a configuration home for the trade-count key (F-D-06); `TRON-T3` carries the remainder of the promoted checks.
5. Decide whether protection-distance policy (stop and take-profit derivation, F-D-07) is a seventh element of `TRON-T3A` or is owned by `TRON-T4`; without it a DEMO order cannot satisfy HR-01 from a trigger that carries no stop or target.
6. `TRON-T3`'s title and description should say it extends the T3A kill state (the title proposed in `H2@2780076` P2, "Hard risk limits and kill switch", would otherwise suggest it creates the switch).
7. `matt_gate` as drafted unless the PO reduces it: base quantity and loss limits are capital-adjacent parameters.
8. PO to decide whether `PAPER-E2E-001` and `GOLD-MVP-001` keep a direct `TRON-T3` edge once T3A is on the path.

## 3. Findings register

| Id | Severity | Class | Label | Finding | Evidence | Needed observation if UNPROVEN |
|---|---|---|---|---|---|---|
| F-D-01 | MAJOR | PROVEN | PARTIAL | Under the CA arrangement of 16 Oct 2026 (`TRON-T3A` owns the single kill state; `TRON-T3` extends it) the backlog does not yet express the extension: drafted `TRON-T3A` and `TRON-T3` both depend only on `TRON-T1`. Adding `TRON-T3A` to `TRON-T3.depends_on` is acyclic on GOAL `main` `e80fcda`. The minimum path then no longer needs `TRON-T3` in full, but `PAPER-E2E-001` and `GOLD-MVP-001` still list it directly | `PORTFOLIO.md` 11.4 yaml and DR-36 (GOAL@ceaf029); `TRON-T3` and `PAPER-E2E-001` entries in `backlog/backlog.yaml`; B19; section 2.4 | none |
| F-D-02 | MINOR | PROVEN | PROVEN | `TRON-T3A` title and text carry all six required elements and need no broker credential | section 2.1 and 2.2 | none |
| F-D-03 | MAJOR | PROVEN | PARTIAL | D1 is unmerged, has no pull request, no recorded auditor verdict and no recorded Matt acceptance in the repository; stale intake, "ledger" and "local journal" wording stands in it; ratification precedes any build | B5, B6, B10; RAT@d5f6d32 sections 2.2, 2.3, 2.5, 5 (this audit re-confirms, does not redo) | whether acceptance or an auditor verdict exists outside the repository (UNVERIFIED) |
| F-D-04 | MAJOR | PROVEN | PROVEN | D1's 44 MVP checks contain no exposure, position-count, order-size, daily-loss, drawdown, consecutive-loss or risk-lock gate; all 38 BACKLOG checks are disabled in the example; CHK-074 is MVP and enabled while its setter BL-OPS-01 is BACKLOG | script over D1@37d5f00 `config.example/checks.yaml` (82 checks: 44 MVP enabled, 38 BACKLOG disabled; CHK-037..048 and CHK-064 BACKLOG disabled; CHK-074 MVP enabled); `docs/10-CAPABILITIES.md:175`. Agrees with RAT@d5f6d32 N-5 | none |
| F-D-05 | MAJOR | PROVEN | MISSING | The amendment A7 promotion list (CHK-037, 038, 039, 040, 044, 045, 047, 048, 064) is not self-sufficient: CHK-044 needs CHK-041 and CHK-042, CHK-045 needs CHK-043, and the composite CHK-048 needs CHK-046, none of which A7 promotes; and nothing in the list enforces the one-position-per-instrument policy (CHK-022 only observes) | RAT@d5f6d32 section 10 (A7) against D1@37d5f00 `docs/06-CHECKS-CATALOGUE.md:120,161-168` (required inputs columns) | none. Does not change a binding ruling; it is an internal inconsistency of a proposal, reported for the ratification record |
| F-D-06 | MINOR | PROVEN | PARTIAL | The trade-count guard key `max_trades_per_day` exists only as a parameter of CHK-047 in `checks.yaml`; `schemas/config/limits.schema.json` and `config.example/limits.yaml` have no key for it, so "limits" has no home for the guard that `TRON-T3A` element (4) requires | D1@37d5f00 `config.example/checks.yaml:403-411`; `schemas/config/limits.schema.json` (grep for trade-count keys returns none) | none |
| F-D-07 | MAJOR | PROVEN (absence) / INFERRED (need) | MISSING | No D1 configuration schema holds a stop-distance or take-profit-distance policy. The trigger candidate carries neither (execution-blind) and offers an opaque `execution_policy_ref`; HR-01 requires protection on every OPEN. No backlog item states who owns the derivation (`RAT@d5f6d32` calls it "a trigger-contract and T4 matter" but `TRON-T4` is titled intake and idempotency) and `TRON-T3A`'s six elements omit it | D1@37d5f00 `schemas/config/*.schema.json` (grep for stop, distance, protection returns none relevant); TRG@64c843b contradiction T-2; RAT@d5f6d32 HR-01 row, A6 | PO/CA assignment of owner; the minimum path cannot place a protected order without one |
| F-D-08 | MINOR | INFERRED | PARTIAL | Negotiation (symbol mapping and canonical-to-broker quantity, CAP-03, lifecycle step 10) has configuration and check entries but no backlog item that names it | D1@37d5f00 `config.example/mapping.falcon.yaml`, `docs/04-TRADE-LIFECYCLE.md`; no match in the TRON backlog titles (GOAL@ceaf029) | owner decision; nearest item `TRON-T2` |
| F-D-09 | MINOR | PROVEN | PARTIAL | Backlog drift: the merged gateway `main` already carries the template skeleton, instance schema, lint, tests and CI (PR #9) that the template contract assigns to increment 1 and part of `MT5-GW-002`, but at base `MT5-GW-001` is PID_DRAFT, `MT5-GW-002..004` are ARCHITECTURE_REQUIRED, and neither PR #9's work order nor issue #10 has a backlog id | B3, B12, B13, B16; TPL@6c92a43 section 11.3 | none. Backlog reconciliation is a governed change outside this audit |
| F-D-10 | MAJOR | PROVEN | MISSING | The gateway has no in-container DEMO latch. The earlier contract record said it was UNVERIFIED whether the expected-mode key is asserted at runtime; it is not: the start script and image do not read it, only a label carries the value. DEMO-only is enforced by the lint and render tool, which refuses unless the code constant `LIVE_PROVISIONING_ENABLED` is set, and is bypassable by anything that starts a container by other means | B15; GW@6263d61 `docs/KNOWN-LIMITATIONS.md:27`; TPL@6c92a43 section 11.1 (row "Expected-trade-mode config key") | none |
| F-D-11 | BLOCKER (for any TRON integration) | PROVEN | MISSING | The typed gateway does not exist. The only control surface is the stock remote-execution bridge with every attribute exposed and no authentication; strict expected-failure tests encode it as a known hazard. TRON must not connect (programme ruling; ADR-MT5-001) | GW@6263d61 `bridge/rpyc_server.py:1-9`; `docs/KNOWN-LIMITATIONS.md:19,25`; B14 | none |
| F-D-12 | MAJOR | PROVEN | MISSING | D1 has no signature, signing or key-trust concept anywhere (docs, schemas, configuration, PID); the signed-trigger rule and the trust store are wholly the candidate contract's | D1@37d5f00 recursive search for signature, signed, signing, hmac, ed25519 over `docs`, `schemas`, `config.example`, `PID.md`: only unrelated hits ("signed notional", "secrets" prose) | none |
| F-D-13 | MINOR | PROVEN | PROVEN | The secret-scan evidence of D1 records 14 commits scanned; 23 commits are reachable at the commit it names and 24 at the tip. The discrepancy is unexplained, so that scan is not re-proven. A secret in public history cannot be fixed by later commits | B11; RAT@d5f6d32 section 2.5, P2 | re-run a full-history scan over D1 and reconcile the count (a ratification precondition, not performed here) |
| F-D-14 | MAJOR | INFERRED | PARTIAL | Multiple stop-like states already exist or are proposed: CHK-074 kill switch, CHK-064 risk lock (both stage 0, separate stores), the `system.halted` event, the reconciliation "no new risk" signal, the gateway REFUSE_ALL state and caps, and the trigger contract's publisher-heartbeat rule. Without a rule that they feed one kill state, they become competing switches. The gateway caps (volume, open positions, rate) also duplicate TRON limits and need an ownership rule: TRON owns policy values, the gateway enforces a wider safety envelope | section 2.4 above; D1@37d5f00 `docs/06-CHECKS-CATALOGUE.md:80-81`, `docs/09-EVENTS-AND-GRAYLOG.md:67`; TPL@6c92a43 sections 8.3, 10.1; TRG@64c843b "Recovery" | a design decision in `TRON-T3A` (recommended in 2.5 item 3) |
| F-D-15 | MAJOR (stop condition) | PROVEN | PROVEN | A stop-condition item was found in a legacy archive among the sources read; handled in the private record (location and value not reproduced); nothing read further, no use made of it | private record (referenced from `EVIDENCE-HASHES.txt` by hash and generic description only) | PO decision whether the archive needs a hygiene work order (outside this audit) |
| F-D-16 | MINOR | PROVEN | PROVEN | The legacy practice-account tooling was assessed as lessons only; reuse as code is rejected (authority model and engineering differences; detail in the private record) | `CANDIDATES.md` C-09 | none |
| F-D-17 | MAJOR | UNPROVEN | UNVERIFIED | `HELIOS-T3` has no PID: its assumptions (who signs, key custody, vocabulary exemption) are not stated by the holder; the register can record only what the trigger candidate and RECON-H2 say | `TRIGGER-ASSUMPTIONS.md` TA-19; GOAL@ceaf029 backlog entry (`pid_path` null) | the signer-owner and custody decisions (candidate D-2, T-11) and the HELIOS-T3 PID |
| F-D-18 | MINOR | PROVEN | PROVEN | Several statements in cited documents are stale against current facts, none binding: the ratification package says the trigger item does not exist and its branch is empty; RECON-H2 and the readiness assessment say the gateway repository is private and eight stacked pull requests are open; the readiness blockers B-1 (visibility) and B-2 (merge) are superseded. The PID already records the supersession | RAT@d5f6d32 N-3; H2@2780076 F-10; RDY@fe43db3 headline 1; GOAL@ceaf029 `pids/GOLD-AUD-D.md` Current state | none |
| F-D-19 | MINOR | PROVEN | PARTIAL | D1's example sizing and limits are for a different instrument and are placeholders; the gold instrument has a disabled mapping entry and no sizing entry, so the path's instrument is unconfigured by design | D1@37d5f00 `config.example/sizing.yaml:10-14`, `config.example/mapping.falcon.yaml` | none; values are the PO's and Matt's |
| F-D-20 | MINOR | UNPROVEN | UNVERIFIED | The source of the legacy live-flagged executor named in ADR-MT5-002 was not located among the sources this audit may read; no statement is made about its gates | `CANDIDATES.md` C-11 | PO-authorised source location, or the operations work order that ADR-MT5-002 requires |
| F-D-21 | MINOR | PROVEN | UNVERIFIED | Seven cited documents exist only on local branches that are not on GitHub; a reviewer without that access cannot reproduce those citations | `BASELINE.md` section 2 (column "On GitHub?") | publication of those branches or an accepted equivalent, a PO decision |
| F-D-22 | MINOR | UNPROVEN | UNVERIFIED | Exposure statements in KNOWN-LIMITATIONS were not re-verified (no probe permitted) | GW@6263d61 `docs/KNOWN-LIMITATIONS.md` | a PO-authorised probe |

## 4. Contradictions against cited documents (stop-and-report test)

PID rule: any claim that contradicts a cited document is reported, not silently corrected; a contradiction that changes a binding ruling, an ADR or an HR is a stop condition.

| Cited document | Claim | Current fact | Changes a binding ruling, ADR or HR? |
|---|---|---|---|
| RAT@d5f6d32 N-3 | `GOAL-TRIGGER-001` does not exist; its branch holds nothing | backlog item on `main`; PID candidate on a local branch (B17) | no (the PID already supersedes it) |
| RAT@d5f6d32 A7 | promoting nine checks completes the PAPER risk set | the list lacks the inputs of CHK-044, 045, 048 and any one-position gate (F-D-05) | no: a proposal's internal gap |
| TPL@6c92a43 section 11.1 | mode assertion UNVERIFIED | confirmed absent (F-D-10) | no |
| RDY@fe43db3, H2@2780076 | gateway private; stack open | public; merged; Gate A closed (B12, B16) | no (PID supersedes) |
| `PORTFOLIO.md` 11.4 and DR-36 (15 Oct text "`TRON-T3A` reuses/extends `TRON-T3`") | superseded by the CA arrangement of 16 Oct 2026 (T3A owns the kill state, T3 extends); the dependency is not yet expressed (F-D-01) | no: clarification needed before application |

Result: no contradiction changes a binding ruling, an ADR or an HR. No stop-and-return on that ground.

## 5. PID stop-condition check

| Stop condition (PID) | Status |
|---|---|
| Contradiction changes a binding ruling, ADR or HR | none (section 4) |
| Reading would need a broker session, bridge connection, container probe or legacy-executor interaction | none; items needing them are recorded as "needs approval" in `PROOF-CLASSES.md` and left unperformed |
| `GOAL-TRIGGER-001` authored in parallel with contradicting content | not observed; the candidate was read at TRG@64c843b and not seen to move. Refresh needed when the contract exists |
| `mt5-gateway` `main` moves so the recorded SHA no longer represents main | no movement; re-read at the end of the audit equal to GW@6263d61 |
| A secret, account identifier or address is found in any source being read | YES, one: F-D-15 (a stop-condition item in a legacy archive, handled in the private record). None other. Return to PO flagged; the audit continued only on material independent of that file |
| The increment list would need a decision that is Matt's | The list refers to R-1, R-2, R-4, R-5, R-6, R-7, R-8, R-9, R-10 and the DEMO owner decisions by id and decides none |

## 6. Status notes

- CA evidence item 10 (independent audit verdict) and acceptance item 12: pending independent audit by ROGUE; this audit does not self-certify.
- Adding this folder makes the generated `MANIFEST.md` drift (`goal-docs --check` reports it). Regeneration of `MANIFEST.md` is required at integration and is ROGUE's step; `goal-docs --write` was not run here.
- The base moved to `e80fcda25a50140dc24793f2dd2770b1da2db517` after the audit started (read only for the graph check B19); the evidence branch is based on `ceaf0291a43d029b1a47b1c192a62ff147f05ac0`.
