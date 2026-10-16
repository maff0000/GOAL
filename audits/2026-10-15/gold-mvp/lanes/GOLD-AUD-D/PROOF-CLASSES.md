# GOLD-AUD-D PROOF-CLASSES: what can be proven how

Deliverable 6. CA evidence item 9 (safety and deployment constraints).

Three classes, in order of rising authority needed:

- (a) `credential-free`: simulated adapter, fake backend conformance suite, deterministic risk code, in-memory journal, schema and lint checks. Needs no session of any kind.
- (b) `DEMO read-only`: one read-only DEMO session (identity, entitlement to trade, symbols, ticks, positions, orders, deals). Needs the approvals named below. Writes nothing.
- (c) `write-approval`: only with the DEMO write-test approval (order lifecycle, restart with a live position).

References: `DEMO@da2e4ea` section 5 (owner decisions 1 to 4 of the DEMO verification), its read-only work order and lifecycle test plan (both "for approval", not approved), `RDY@fe43db3` section D (owner decisions D-1..D-7), `H2@2780076` decision D-8 (account custody and approval of write calls), `TPL@6c92a43` section 12.

## 1. Every increment in exactly one class

| Increment | Class | Needs (approval or owner decision) |
|---|---|---|
| INC-01 Ratify D1 and amendments | (a) credential-free | Matt decisions R-1..R-10 (a design decision, not a session) |
| INC-02 Freeze trigger contract | (a) credential-free | Matt gate on the contract |
| INC-03 Execution journal | (a) credential-free | R-4 for the durable store; lane decision 2 for the in-memory port |
| INC-04 Adapter interface, simulated adapter, conformance suite | (a) credential-free | PO choice between `TRON-T1` scope and a candidate `TRON-T2A` |
| INC-05 `GAP-TRON-FIXED-SIZE-DEMO-RISK` incl. the single kill state | (a) credential-free | PO decision on the proposed item shape; parameter values are Matt-gated capital-adjacent configuration; R-8 for the promoted minimum checks |
| INC-06 Extended hard risk limits (`TRON-T3` extends INC-05) | (a) credential-free | R-8 (promotion of the remaining risk checks) |
| INC-07 Inbox intake against signed fixtures | (a) credential-free | `GOAL-TRIGGER-001` frozen (INC-02) |
| INC-08 Follow-up notices (issue #10) | (a) credential-free | none beyond normal review |
| INC-09 Digest-pinned image build | (a) credential-free | none beyond normal review |
| INC-10 Typed service with fake backend | (a) credential-free | `MT5-GW-003` PID approval; template owner decisions 1 and 6 |
| INC-11 Vantage adapter against fake backend | (a) credential-free | `TRON-T2` PID approval |
| INC-12 One-path simulated rehearsal | (a) credential-free | R-9: it never carries the state PAPER unless Matt rules otherwise |
| INC-13 First DEMO instance, read-only proof | (b) DEMO read-only | `DEMO@da2e4ea` section 5: decision 1 (entitlement and permitted automated use), 2 (reuse the existing instance for read-only steps only, or a fresh DEMO login), 3 (approve one read-only session), 4 (accept or fix the exposure of the existing instance for the read-only phase); `RDY@fe43db3` D-3 (credential custody), D-4 (host and instance), per-run authorisation to start an instance |
| INC-14 Adapter reads through the gateway on DEMO | (b) DEMO read-only | Same approval as INC-13; the typed gateway must exist and be approved (INC-10) |
| INC-15 Order lifecycle proof | (c) write-approval | `RDY@fe43db3` D-5 and `H2@2780076` D-8: approval of the test plan and of each write call, per-run start approval; a fresh DEMO login is recommended by `DEMO@da2e4ea` section 4 for write tests |
| INC-16 Restart and recovery proof with a live position | (c) write-approval | Same approval as INC-15, plus the recovery test plan |
| INC-17 One order end to end | (c) write-approval | Matt gate on `PAPER-E2E-001` (capital-risk item), DEMO write approval, independent auditor |

## 2. What can be proven credential-free (class a)

- Contract and schema validity of intake, intent, check report, event (D1 gate, already green, B9).
- Signature, validity-window, duplicate and conflict handling on signed fixtures with synthetic test keys (INC-07).
- Journal-before-submit, idempotent identity, claim and disposition, reconcile diff and simulated restart on the in-memory port and on a throwaway durable store (INC-03, INC-12).
- All six elements of `GAP-TRON-FIXED-SIZE-DEMO-RISK`, with zero submit calls recorded in every refusal (INC-05).
- The single-kill-switch property: engaging the one kill state refuses a new OPEN, and a repository test finds exactly one writer (INC-05).
- Gateway protocol behaviour against a fake backend: allow-list, caps, replay of `client_order_id`, error taxonomy including `TIMEOUT_UNKNOWN_OUTCOME` by fault injection, refusal of a faked non-DEMO mode before any backend call (INC-10).
- Instance configuration lint, render, and image digest checks (INC-08, INC-09).

Limit, stated once: a simulated lane proves pipeline logic, not broker behaviour. It cannot satisfy the ADR-MT5-001 required proofs and cannot carry the state PAPER (R-9 is Matt's).

## 3. What needs a DEMO read-only session (class b)

- The environment latch on a real session (mode reported by the terminal, entitlement to trade).
- Real symbol specifications, quantity limits and steps for the instrument (needed to replace the placeholder values the credential-free proofs use).
- Tick age and freshness, real position, order and deal reads, and the reconcile snapshot shape.
- First container run of the new template, and the `verify` command output.

## 4. What only the write-test approval can prove (class c)

- Market and pending order placement, cancel, SL/TP place and modify, full and partial close.
- Whether the broker keeps the client order id in the order comment through partial closes and fills (open proof item of `TPL@6c92a43` section 8.4).
- Broker-side protection present and read back after a fill.
- Restart and recovery with a live position; idempotent retry; resolution of `TIMEOUT_UNKNOWN_OUTCOME` by lookup.
- The end-to-end single order.

## 5. Safety statement for this audit

No increment above was performed. No session of class (b) or (c) was opened, and none was needed to produce this analysis.
