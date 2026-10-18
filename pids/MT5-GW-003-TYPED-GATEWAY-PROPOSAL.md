# Engineering package 4: typed MT5 DEMO gateway with a mechanically enforced DEMO-only latch

**Status:** DRAFT PROPOSAL for Central Architecture. Not registered, not approved, not `DELIVERY_READY`. Drafting only: no implementation, no contract freeze, no broker access, no deployment or production mutation is authorised by this document.
**Date:** 2026-10-17. **Author:** ROGUE (Delivery Train Controller), prepared from the published GOLD-AUD-D evidence (lane state `PO_ACCEPTANCE`, not `MERGED`).
**Backlog relationship:** refines the existing items `MT5-GW-003` (typed in-container allow-list service; `ARCHITECTURE_REQUIRED`, no `pid_path`) and the latch part of `MT5-GW-004`. It adds no backlog item and changes no count. If approved it would become the PID text for `MT5-GW-003` through a separate governed change.
**Evidence base:** GOLD-AUD-D (GOAL `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-D/`, findings F-D-10, F-D-11; gap rows G-25 to G-32; increments INC-08 to INC-10, INC-13, INC-15, INC-16; proof classes) and the mt5-gateway mirror note; ADR-MT5-001 (reuse the container, replace the bridge).

## 1. Problem (what the evidence proves)

- **F-D-11 (blocker for any TRON integration):** the typed gateway does not exist. The only control surface is the stock remote-execution bridge, which exposes every attribute without authentication. Programme ruling: TRON must not connect to it.
- **F-D-10 (major):** there is no in-container DEMO latch. The expected-mode setting is carried only as a label; no start script or service reads it at runtime. DEMO-only is enforced by a lint-and-render tool whose refusal is bypassable by anything that starts a container by other means.
- **G-26:** DEMO environment assertion is `partial` (lint and render refusal, tested; no runtime latch).

This package defines what must exist, and how it is proven credential-free, before any TRON adapter may be connected to a gateway.

## 2. Scope

1. **A typed, closed allow-list service** inside the MT5 container, replacing the raw remote-execution bridge for every consumer. The raw bridge is absent from the image, not merely unexposed.
2. **A DEMO-only latch** that is mechanical, fail-closed, sticky and has no override path.
3. **A protected local transport** (Unix-domain socket preferred) with no network-published listener.
4. **A fake backend and a conformance suite** so every behaviour above is provable without any broker session.
5. **A typed error taxonomy** including an explicit unknown-outcome class that forbids blind resubmission.

## 3. Non-goals

- No implementation, image build, container start or deployment under this drafting authority.
- No broker session of any kind (read-only DEMO or write). Real-session proofs are `MT5-GW-004` and are separately Matt-gated.
- No LIVE capability. The gateway must be incapable of acting on a non-DEMO account, not merely configured not to.
- No change to the legacy executors or the existing legacy MT5 services.
- No connection of TRON, or anything else, to the raw bridge at any stage.
- No new strategy, sizing or risk logic (TRON-owned: `TRON-T3A`, `TRON-T3`).
- No credential handling design beyond the custody decision listed in section 9.
- No promotion of any simulated proof to the state `PAPER` (ADR-MT5-001; owner decision R-9).

## 4. Typed API surface (class level)

A closed enumeration of operations. Anything not listed is refused; there is no generic call, no attribute access, no evaluation of caller-supplied code, and no operation that accepts an account, server or login selector.

| Group | Operations (names indicative) | Notes |
|---|---|---|
| Identity and health | `describe` (service version, protocol version, latch state, trade-mode observed), `health` | `describe` reports latch state; it never reports credentials. |
| Reads | `get_account`, `get_symbol_spec`, `get_ticks`, `get_positions`, `get_orders`, `get_deals`, `reconcile_snapshot` | Read operations only observe. Results carry a freshness timestamp. |
| Writes (DEMO latch required) | `place_order` (with broker-side protection on the opening request), `modify_protection`, `cancel_order`, `close_position` | Caller supplies a client order id; replay of an id returns the original outcome and never creates a second order. |
| Errors | Typed taxonomy: validation, refused-by-latch, refused-by-cap, broker-rejected, transport, and `TIMEOUT_UNKNOWN_OUTCOME` | The unknown-outcome class is resolved only by lookup of the client order id, never by resubmission. |

Per-request caps (symbol allow-list, maximum quantity, maximum open positions) are configuration owned by the gateway instance; parameter values are not set by this package.

## 5. The DEMO-only latch (mechanism)

The latch is a single, sticky state with one owner inside the gateway process. It is layered so that no single check is the only protection.

1. **Declared mode is mandatory and is read.** The start path refuses to run unless the instance configuration declares the expected trade mode, and the service reads that value (today it is not read). Absent, unreadable or any value other than the DEMO value is a refusal to start.
2. **Observed mode is authoritative.** After the terminal connects and before any listener is opened, the service reads the account trade mode from the terminal itself. Observed mode must equal DEMO. A mismatch, an error, a timeout or a missing value is a refusal to start (fail closed).
3. **Per-request re-verification for every write.** Before each state-changing operation the service re-reads the observed trade mode. Reads may use a short, bounded cache; writes may not.
4. **Trip is sticky.** Any latch failure (mismatch, error, unexpected account identity change) moves the single latch state to TRIPPED, refuses all writes, and persists across process restarts. Reset is an operator action on the host, not an API operation; no remote caller can reset or relax it.
5. **No override.** There is no flag, environment variable, configuration key, header or API field that disables, weakens or bypasses the latch. A repository test enforces this by search and by behaviour (section 7).
6. **Closed surface.** Because no operation accepts an account or server selector, a caller cannot redirect an operation to another account; the service operates only on the account the terminal is logged into, and the latch ties that account to DEMO.
7. **Secondary check (defence in depth, optional decision).** A server-name pattern allow-list in configuration may be added as a second signal; it can only further restrict and never overrides the observed-mode check.

The latch does not replace TRON's own single kill state. The gateway latch refuses by environment; the TRON kill state refuses by risk. They are separate mechanisms with separate owners and are not merged (ownership of the one kill switch stays with `TRON-T3A`).

## 6. Network and exposure constraints

- Protected local transport: a Unix-domain socket with owner-only permissions is preferred. If a socket is not feasible, a loopback-only bind with a per-instance authentication secret is the fallback (owner decision, section 9).
- No published container port, no bind to a non-loopback address, no operator interface exposed beyond the host.
- The raw remote-execution bridge is not installed in the image and no service in the image provides arbitrary attribute or code access. A conformance test asserts the absence.
- TRON's adapter runs outside the MT5 container and reaches the gateway only through the protected transport. How the transport is shared between containers is an owner decision.
- No address, hostname, port or account identifier is recorded in any public repository as part of this package.

## 7. Technical acceptance proofs (all credential-free, class (a))

| Proof | What it demonstrates | Method |
|---|---|---|
| P1 | The closed allow-list: an operation outside the list is refused; no generic call exists | Conformance suite against the fake backend; static scan of the service for dynamic dispatch |
| P2 | Start refusal on missing, unreadable or non-DEMO declared mode | Fake backend and configuration fixtures |
| P3 | Start refusal when observed mode is not DEMO, errors, times out or is absent; no listener is opened | Fault injection on the fake terminal |
| P4 | Zero backend write calls are recorded in every refusal path | Call-recording fake backend asserting an empty write log |
| P5 | Mid-run mode flip to non-DEMO trips the latch on the next write; the write is refused; subsequent writes stay refused | Fault injection between calls |
| P6 | Latch trip persists across a simulated restart and is not clearable through the API | Restart simulation; attempt every operation after restart |
| P7 | No override path exists | Repository test searching for any key, flag or environment variable that could relax the latch, plus behavioural attempts |
| P8 | Replay of a client order id never produces a second order | Fake backend with duplicate submission |
| P9 | `TIMEOUT_UNKNOWN_OUTCOME` is returned on injected timeouts and the service never retries the write itself | Fault injection |
| P10 | The raw bridge is absent from the built artefact definition and no listener is published | Image-definition lint; configuration lint (no real build required for the lint proof) |
| P11 | Reproducibility prerequisite (`MT5-GW-002`): two builds of the same inputs give the same digest | Separate item; listed as a dependency, not proven here |
| P12 | Mutation check: weakening any latch condition makes at least one of P2 to P7 fail | Mutation test run on the latch module |

Out of this package and separately gated: the latch assertion on a real DEMO session (class (b), `INC-13`), and order placement, protection read-back, restart-with-position and unknown-outcome resolution on DEMO (class (c), `INC-15`, `INC-16`). None of these is performed, scheduled or authorised here. The GOLD-AUD-D amendment (GOAL #30) keeps acceptance criterion 7 open: a bounded repository policy test that enforces the typed-gateway ordering obligations (typed gateway before accepted TRON integration; typed gateway before any PAPER claim) is assigned to FORGE and is not provided or claimed by this package.

## 8. Dependency graph

```
GOAL-DCP-001 (CLOSED)
  -> MT5-GW-001 reconcile stacked WO branches (PID_DRAFT)
      -> MT5-GW-002 reproducible image/build provenance, pinning, environment guard, health, CI
          -> MT5-GW-003 typed allow-list service + latch   <== this proposal (ARCHITECTURE_REQUIRED)
              -> MT5-GW-004 DEMO read-only and write proofs (Matt-gated sessions)
                  -> TRON-T2 Vantage DEMO broker-neutral adapter  (also needs TRON-T1)
                      -> GOLD-MVP-001 (also needs TRON-T3A, GOAL-TRIGGER-001/GOAL-CONTRACT-001 decisions, ...)
TRON-T1 (journal, reconciliation, adapter interface, simulated adapter) -> TRON-T2, TRON-T3A
```

`INC-08` (clear the open follow-up notices in the gateway configuration tooling) precedes `INC-10` in the lane D ordering. The credential-free half of `TRON-T2` (adapter against the gateway's fake backend, `INC-11`) needs this package's fake backend and conformance suite, not a live session.

## 9. Unresolved owner decisions

1. **Transport:** Unix-domain socket versus loopback-only with a per-instance secret; how the socket is shared with TRON's container.
2. **mt5-gateway repository visibility:** the owner decision on moving the repository to PRIVATE. This package's design and test names are generic and publishable, but the detailed instance configuration and any future real-session evidence should not be in a public repository; the timing of the transition affects where the implementation PRs and evidence live.
3. **Credential custody** for the later DEMO sessions (who holds the login, where, rotation) and whether a fresh DEMO login is used for write tests.
4. **Accepted observed trade-mode values:** DEMO only (recommended), with an explicit decision that contest, real and any unknown value are all refusals.
5. **Latch reset authority:** which operator role may reset a tripped latch and what record is required.
6. **Optional secondary signal:** whether the server-name allow-list in section 5 item 7 is adopted.
7. **Separate read-only build or tag:** whether a read-only image or mode that omits the write operations entirely is delivered first.
8. **Runtime and language** of the in-container service, constrained by what runs reliably in the existing container's compatibility layer.
9. **R-9:** whether a simulated lane may ever carry the state `PAPER` (current ruling: it cannot).
10. **Authority split with TRON:** confirmation that the gateway latch and TRON's single kill state remain separate and that the gateway has no risk logic.

## 10. Effort (planning estimate, unverified)

Credential-free scope only (service, fake backend, conformance suite, latch, mutation tests, documentation): roughly 12 to 18 engineer-days, excluding `MT5-GW-001`, `MT5-GW-002` and `INC-08`. Real-session proofs (`MT5-GW-004`) are additional, depend on owner approvals and are not estimated here. This is an order-of-magnitude figure for planning, not a commitment, and has not been reviewed by the gateway owner.

## 11. Risks

| Risk | Treatment |
|---|---|
| The terminal's reported trade mode is misreported or unavailable | Fail closed on any error; secondary server-name signal; real-session assertion proven separately in `INC-13` |
| Latch implemented only at start, drifting later | Per-request re-verification for every write and sticky trip (P5, P6) |
| An override creeps in during maintenance | Repository search test (P7) and mutation test (P12) in CI |
| Fake backend diverges from the real terminal | Fake limited to protocol and fault behaviour; real behaviour proven only by the gated class (b)/(c) proofs; divergences recorded as findings |
| A consumer connects to the raw bridge before the typed service exists | Programme ruling stands; absence of the bridge from the image is asserted by P10 |
| Public exposure of operational detail | Generic wording here; instance configuration and real-session evidence follow the repository-visibility decision |
| A simulated pass is read as broker proof | Section 3 non-goal and the proof-class labels; no `PAPER` from simulation |

## 12. Approval

PENDING. This document is a drafting product. Approval, registration as the `MT5-GW-003` PID, and any readiness transition are separate governed steps. No implementation, contract freeze or broker access is authorised through it.
