# CP-2: HELIOS signed trigger to durable outbox to TRON inbox

**Package version:** `cp-2/0.1.0`  
**Status:** PROPOSED. Nothing in this package is frozen, approved or authoritative.  
**Produced by:** GOLD-AUD-C (read-only audit); GOAL base `ceaf0291a43d029b1a47b1c192a62ff147f05ac0`.  
**Normative authority:** `GOAL-TRIGGER-001` alone (CA guidance 2026-10-15, item 2), and through it `GOAL-CONTRACT-001`. This package is a **conformance and reconciliation package over that contract**. It introduces no envelope, identity, signing, outbox or inbox rule of its own: every rule below cites the candidate text it executes, every value the candidate does not state is listed as an assumption in section 9, and every disagreement is a change request to the owning PID (section 10), never a decision made here.  
**Status of the authority:** the PID candidates for `GOAL-CONTRACT-001` and `GOAL-TRIGGER-001` exist only as commit `64c843b` on a local branch `wo/GOAL-CONTRACT-TRIGGER` of the delivery host; they are not on GitHub `main` and `GOAL-TRIGGER-001` has no `pid_path` (AC-26). The text read is therefore UNPUBLISHED; its SHA-256 is recorded in `SOURCES.tsv`. Decision D-12 (that the trigger contract is the TradingTriggerInbox specification of record) is not decided; until it is, CP-2 is a proposal against no authority and cannot be frozen.

## 1. Purpose and boundary

Provider: the HELIOS-side trigger publisher (outbox). Consumer: the TRON TradingTriggerInbox. The package defines what each can be tested on offline: the door verdict on one envelope, the inbox row lifecycle, and the publisher and inbox behaviour under duplicate, replay, expiry, skew, crash, partial publication and poison input.

Out of scope: HELIOS evaluation, signing implementation, key custody (`KEY-CUSTODY` of the candidate), broker execution, sizing, risk, protection, and FALCON (an asynchronous evidence consumer that is never on a decision path). No component code is changed; no runtime is contacted.

## 2. Sources audited

| Source | Revision | Files |
|---|---|---|
| `GOAL-TRIGGER-001`, `GOAL-CONTRACT-001`, ADR-CONTRACT-001 candidates | `64c843b` (local branch, unpublished) | `pids/GOAL-TRIGGER-001.md`, `pids/GOAL-CONTRACT-001.md`, `decisions/ADR-CONTRACT-001-STRATEGY-SEMANTICS.md` |
| HELIOS `main` | `7f7193d55475e40583892b94dd461b1b64d6f1ef` | whole tree searched for trigger, signing and outbox code (negative result, commands in `RECONCILIATION.md`); `helios/publish/sink.py`, `helios/publish/negotiation.py`, `docs/INTEGRATION.md` section 1, `helios/contracts/serialisation.py` |
| FALCON `main` | `8f218ec1b85b932285b042a7b1ae64dbd11eebee` | `schemas/payloads/helios/strategy_trigger.v1.schema.json`, `docs/security/FALCON-HELIOS-TRIGGER-SIGNING.md`, `registry/event_family_registry.v1.json` |
| TRON `main` and branch `wo/WO-TRON-D1` | `5577039b5db05e70effef72c7e59df14db408419`; `37d5f009a080d25930eea37cf8c627bb0f3a1ff4` | `PID.md`; on the branch `docs/04-TRADE-LIFECYCLE.md`, `docs/05-CONTRACTS.md`, `schemas/falcon.trade_action.v1.json` |

TRON `main` contains only `PID.md` and tooling; the schemas and lifecycle documents exist only on the D1 branch. Lane D (TRON intake facts) and Lane E (FALCON registry facts) run in parallel and were not waited for; the TRON and FALCON facts above were read directly from the repositories at the revisions shown, and rows that depend on Lane D or E conclusions are marked so in section 11.

## 3. Versioning and compatibility rules

* Package version `cp-2/MAJOR.MINOR.PATCH`. The wire schema version is the string `goal.strategy-trigger/v1`, owned by the trigger PID. The envelope is a **closed world**: an unknown field, token or schema marker is refused (`REJECTED_SCHEMA`), so any additive change forces a deliberate version.
* Additive (minor): a new `reference_levels` role token, a new `signal_class` or timeframe token, a new outcome name, once the owning PID has added it. Breaking (major): a change to the occurrence key, the signed field set, the canonical form, the signature domain, or the meaning of an outcome.
* Pairs are judged by the matrix rows in section 11 with the same status words as `cp-1/0.1.0`: no row is `COMPATIBLE` while no implementation of either side exists or has been run against these fixtures.

## 4. The envelope under test (mechanical snapshot of the candidate)

The signed-field table of `GOAL-TRIGGER-001` (section "Proposed design") is encoded as `schema/trigger.envelope.schema.json` so fixtures can run. The schema is a **snapshot of a proposal**, not an alternative contract; where the candidate leaves a value domain open the choice is an assumption (section 9) and is the first thing to re-base when the PID changes.

Signed fields (all required unless stated): `schema`, `trigger_id`, `strategy_id`, `strategy_version`, `strategy_fingerprint`, `binding_id`, `execution_policy_ref`, `instrument_id`, `timeframe`, `signal_class`, `output_direction`, `state_from`, `state_to`, `setup_origin_bar_utc`, `bar_close_utc`, `valid_from_utc`, `valid_until_utc`, `evaluation_id`, `input_snapshot_id`, `input_snapshot_hash`, `reference_levels` (optional), `signing_key_id`. Plus `signature`, which covers the domain string `goal.strategy-trigger/v1` followed by a newline and the canonical bytes of every other field.

Excluded by the candidate and therefore refused by the closed world: quantity, size, risk, stop-loss, take-profit, order type, broker symbol, account, generic confidence, production time, publisher host.

## 5. Conformance rules (the door and the inbox)

Each rule executes a statement of the candidate. The door verdict is the **first failing rule in this order** (section 6 gives the outcome names).

| Rule | Check | Candidate source | Outcome |
|---|---|---|---|
| CP2-R01 | The object has `schema` equal to `goal.strategy-trigger/v1` | Proposed design, signed fields | REJECTED_SCHEMA |
| CP2-R06 | `signature` and `signing_key_id` are present (AS-1) | Terminal outcomes; T-A3 "unsigned copy" | REJECTED_SIGNATURE |
| CP2-R02 | No field outside the signed set; no execution vocabulary | Excluded on purpose; T-A6 forbidden content | REJECTED_SCHEMA |
| CP2-R03 | Token sets, patterns and forms of section 4 and `schema/`: decimal strings only, fixed-width microsecond `Z` instants, `SETUP_ACTIVE` carries `LONG` or `SHORT`, no `FLAT`, no `EXIT/ADJUST`, no `M30/W1` | T-2, T-4, T-5, T-6; D-5, D-6 | REJECTED_SCHEMA |
| CP2-R04 | `trigger_id` equals `trg1_` plus the lowercase hex SHA-256 of the canonical bytes of the occurrence key | Occurrence key; T-7 | REJECTED_SCHEMA |
| CP2-R05 | `valid_from_utc` equals `bar_close_utc` | Signed fields table | REJECTED_SCHEMA |
| CP2-R07 | The signing key is in the trust store, not revoked, valid at receipt, and tagged for the receiver's environment | Signature and trust | REJECTED_KEY |
| CP2-R08 | The Ed25519 signature verifies over the domain string and canonical bytes under the claimed key | Signature and trust | REJECTED_SIGNATURE |
| CP2-R09 | `strategy_fingerprint` is in the receiver's pinned set | Signed fields ("TRON refuses a fingerprint outside its pinned set") | REJECTED_STRATEGY |
| CP2-R10 | `valid_until_utc` is after `valid_from_utc`; `valid_from_utc` is not later than receipt plus the skew tolerance; the window is not longer than the maximum (tolerance and maximum are receiver configuration, D-7) | Validity | REJECTED_CLOCK |
| CP2-R11 | Receipt time is before `valid_until_utc`; at or after it the trigger is expired | Validity | EXPIRED |
| CP2-R12 | Same `trigger_id` and same content digest again: one row, same receipt, event DUPLICATE_DELIVERY; same id, different digest: CONFLICT, quarantined, never claimed (AS-3) | Idempotency layers (inbox) | CONFLICT |
| CP2-R13 | A `SETUP_ACTIVE` trigger whose setup already has an invalidation is SUPERSEDED (AS-2) | Terminal outcomes | SUPERSEDED |
| CP2-R14 | A row is `RECEIVED`, then `CLAIMED`, then exactly one terminal outcome; after a crash a `CLAIMED` row goes to RECONCILE and nothing is re-submitted while broker state is uncertain; one client order reference per trigger | Inbox lifecycle; Recovery | ABANDONED_UNRESOLVED at window end if unresolved |
| CP2-R15 | The publisher writes the signed envelope to a durable outbox before acknowledging upstream, delivers on the same `trigger_id`, marks delivered only on the inbox's durable receipt | Durable publication | n/a |
| CP2-R16 | Bounded retry then quarantine for an entry repeatedly rejected, with no head-of-line block (AS-9) | CA scope item 6 | n/a |
| CP2-R17 | Neither side reads FALCON to decide anything; dispositions are identical with the evidence sink up or down | FALCON; T-A7 | n/a |

Canonical form, identifier and digest rules are those of `goal-canon/1` as proposed in ADR-CONTRACT-001 section 4 (sorted keys, no whitespace, un-escaped non-ASCII, decimals as normalised strings, `null` preserved, digest `sha256:<hex>`). CP-2 does not define them; `tests/cp_support/cp2_canon.py` is a test reference implementing that proposed text so fixtures can be checked, and is itself subject to the two-implementation reproduction rule (T-A2) that belongs to the trigger PID.

## 6. Outcomes and rejection matrix

Closed outcome vocabulary of the candidate, plus the two non-outcome events. Pre-authentication rejections are journaled by content digest and never consume a `trigger_id` (AS-6, AC-22).

| Outcome | Side | Effect |
|---|---|---|
| REJECTED_SCHEMA | inbox door | refuse, journal by digest, no row; publisher counts an attempt |
| REJECTED_SIGNATURE | inbox door | refuse, journal by digest, no row; publisher counts an attempt |
| REJECTED_KEY | inbox door | refuse, journal by digest, alert; publisher counts an attempt |
| REJECTED_CLOCK | inbox door | authenticated: row recorded with this terminal outcome; entry delivered; alert |
| REJECTED_STRATEGY | inbox door | authenticated: row recorded with this terminal outcome; entry delivered; alert |
| EXPIRED | inbox door or claim | authenticated: row terminal EXPIRED; never claimed, never executed |
| CONFLICT | inbox | incoming envelope quarantined and alerted; original row unaffected (AS-3) |
| DUPLICATE_DELIVERY | inbox | event, not an outcome; original receipt returned; original disposition stands |
| SUPERSEDED | inbox | row terminal SUPERSEDED; cannot be claimed |
| REFUSED | TRON core | terminal after claim (eligibility, admission, serviceability or check failure); reason codes are TRON's |
| EXECUTED | TRON core | terminal after claim; the broker has exactly one order for the client reference |
| EXECUTION_REJECTED | TRON core | terminal after claim; not exercised by CP-2 fixtures (broker behaviour is outside this audit) |
| ABANDONED_UNRESOLVED | TRON core | window ended with unresolved broker state after reconciliation; alerted; never retried |

Mapping to TRON D1 terminals (`REJECTED`, `EXPIRED`, `DUPLICATE`, `NEGOTIATED`) is that of the candidate and is final only when TRON-T4 names its states (AC-18): the D1 terminal set has no `CONFLICT`, `SUPERSEDED` or `ABANDONED_UNRESOLVED`.

## 7. Failure and recovery scenarios

Fixtures under `fixtures/scenarios/`; reproduced by `tests/cp_support/cp2_reference_model.py` (test-only). Each step states its expected status, state or table.

| Scenario | Required observable outcome |
|---|---|
| `duplicate_delivery` | One row; second and third delivery return the original receipt; event DUPLICATE_DELIVERY twice; original disposition unchanged |
| `occurrence_key_replay` | Upstream replay after a publisher restart regenerates the same id; one outbox entry; one row |
| `expired_trigger` and `claim_after_window` | EXPIRED at receipt or at claim; no submission |
| `clock_skew` | Within tolerance: received. Beyond tolerance: terminal REJECTED_CLOCK |
| `publisher_outbox_crash_restart` | After a crash between the outbox write and delivery the entry is delivered once after restart |
| `inbox_down` | Entries stay PENDING, no attempt is charged, nothing is lost or quarantined; delivery resumes in order |
| `partial_publication_receipt_lost` | Inbox committed, receipt lost: redelivery returns the original receipt; execution happens once |
| `poison_message_no_head_of_line_block` | The rejected entry is retried up to the bound then QUARANTINED and alerted; the entry behind it is delivered on the first pass |
| `falcon_sink_up` / `falcon_sink_down` | Identical dispositions, row counts and submissions with the sink disabled (counters and timestamps excluded) |
| `crash_after_submit_no_double_execution` | Crash between broker submission and the journaled outcome: RECONCILE finds the order; redelivery and re-claim cannot submit again; total submissions 1 |
| `uncertain_broker_state_never_retried` | UNCERTAIN stays RECONCILE with no new submission; at window end ABANDONED_UNRESOLVED |
| `id_collision_different_digest` | CONFLICT; one row; original still RECEIVED |
| `invalidation_first_supersedes` | Later active trigger SUPERSEDED; no submission |
| `forged_copy_cannot_poison_id` | A forged copy with a real `trigger_id` is rejected before authentication and journaled by digest; the genuine envelope is still accepted |

Not covered, by decision: the publisher heartbeat (D-8 undecided), claim-time re-verification of the key (AC-25), the final TRON-T4 state names.

## 8. Reconciliation of competing shapes to the contract

These tables record each competing shape as a conflict **to be reconciled to** `goal.strategy-trigger/v1`, never as a second authority. Source is the competing field; target is the contract field. `UNSUPPORTED` means the contract has no equivalent: a provider carrying it is refused with the stated outcome.

### 8.1 FALCON `helios.strategy_trigger` v1 (`8f218ec`)

<!-- mapping-table falcon -->
| Source field | Target field | Disposition | Rule and fail-closed behaviour |
|---|---|---|---|
| `trigger_id` (free string) | `trigger_id` | DERIVED | Replaced by the deterministic `trg1_` identifier of CP2-R04; a free string is `REJECTED_SCHEMA`. |
| `evaluation_id` | `evaluation_id` | MAPPED | Opaque token pattern (AS-5). |
| `strategy_id` | `strategy_id` | MAPPED | Pattern of the shared identity (AS-5). |
| `strategy_version` (free string) | `strategy_version` | DERIVED | Must be strict semantic version; otherwise `REJECTED_SCHEMA`. |
| `semantic_fingerprint` | `strategy_fingerprint` | DERIVED | Renamed, and written `sha256:` plus 64 lowercase hex; the algorithm is that of `GOAL-CONTRACT-001`, not FALCON's free string. |
| `parameter_set_id` | `binding_id` | DERIVED | Renamed; opaque token pattern (AS-5). |
| `chain_id` | none | UNSUPPORTED | No chain identity in the v1 trigger; `REJECTED_SCHEMA`. |
| `instrument_id` | `instrument_id` | MAPPED | Canonical instrument id. |
| `direction` | `output_direction` | DERIVED | `LONG` and `SHORT` map; `FLAT` has no v1 token and is `REJECTED_SCHEMA`. |
| `action_type` | `signal_class` | DERIVED | `ENTRY` maps to `SETUP_ACTIVE`; `EXIT` and `ADJUST` are execution policy and are `REJECTED_SCHEMA` (T-6). |
| `timeframe` | `timeframe` | MAPPED | Six HELIOS tokens; `M30` and `W1` are `REJECTED_SCHEMA`. |
| `trigger_at_utc` | none | UNSUPPORTED | Production time is excluded from the signed body (unsigned transport metadata only); `REJECTED_SCHEMA` if carried. |
| `valid_from_utc` | `valid_from_utc` | DERIVED | Fixed-width microsecond `Z`, equal to `bar_close_utc`; variable precision and `+00:00` are `REJECTED_SCHEMA`. |
| `valid_until_utc` | `valid_until_utc` | DERIVED | Fixed-width microsecond `Z`; same refusal as `valid_from_utc`. |
| `input_snapshot_id` | `input_snapshot_id` | MAPPED | Opaque token pattern (AS-5). |
| `input_snapshot_hash` | `input_snapshot_hash` | MAPPED | `sha256:` plus 64 lowercase hex. |
| `reference_price_decimal` | none | UNSUPPORTED | No reference price in the contract; `REJECTED_SCHEMA`. |
| `reference_price_numeric` | none | UNSUPPORTED | Binary numbers cannot be signed canonically (T-5); `REJECTED_SCHEMA`. |
| `stop_loss_decimal` | none | UNSUPPORTED | Execution field, forbidden by CP2-R02; `REJECTED_SCHEMA`. |
| `stop_loss_numeric` | none | UNSUPPORTED | As `stop_loss_decimal`: `REJECTED_SCHEMA`. |
| `take_profit_decimal` | none | UNSUPPORTED | As `stop_loss_decimal`: `REJECTED_SCHEMA`. |
| `take_profit_numeric` | none | UNSUPPORTED | As `stop_loss_decimal`: `REJECTED_SCHEMA`. |
| `invalidation_decimal` | `reference_levels` role `INVALIDATION` | DERIVED | Optional neutral level as a decimal string, only if D-4 option (b) is decided; otherwise `REJECTED_SCHEMA`. |
| `invalidation_numeric` | none | UNSUPPORTED | Duplicate numeric form; `REJECTED_SCHEMA`. |
| `target_decimal` | `reference_levels` role `OBJECTIVE` | DERIVED | Optional neutral level, only if D-4 option (b) is decided; otherwise `REJECTED_SCHEMA`. |
| `target_numeric` | none | UNSUPPORTED | Duplicate numeric form; `REJECTED_SCHEMA`. |
| `score_value` | none | UNSUPPORTED | No generic confidence in the contract (CP2-R02); `REJECTED_SCHEMA`. |
| `score_definition_id` | none | UNSUPPORTED | As `score_value`: `REJECTED_SCHEMA`. |
| `signing_key_id` | `signing_key_id` | DERIVED | `sha256:` of the raw public key (AS-4), not a free string. |
| `signature` | `signature` | DERIVED | Lowercase hex of the 64 signature bytes over the domain string and canonical bytes (AS-4). |

### 8.2 TRON D1 intake `falcon.trade_action.v1` (`wo/WO-TRON-D1` at `37d5f00`)

<!-- mapping-table tron-intake -->
| Source field | Target field | Disposition | Rule and fail-closed behaviour |
|---|---|---|---|
| `contract_version` | `schema` | DERIVED | The string `goal.strategy-trigger/v1` replaces the numeric contract version; otherwise `REJECTED_SCHEMA`. |
| `action_id` | `trigger_id` | DERIVED | Deterministic identifier; the 69-character `trg1_` form fits the D1 identifier pattern and length (checked by a test). |
| `action` | `signal_class` | DERIVED | `OPEN` corresponds to `SETUP_ACTIVE`; `CLOSE`, `MODIFY`, `CANCEL` have no v1 equivalent and are `REJECTED_SCHEMA`. |
| `instrument` | `instrument_id` | MAPPED | Canonical instrument id; a broker symbol is never carried. |
| `side` | `output_direction` | DERIVED | `LONG` and `SHORT` only. |
| `stop_loss` | none | UNSUPPORTED | TRON derives protection from its own policy behind `execution_policy_ref`; carrying it is `REJECTED_SCHEMA` (T-2). |
| `take_profit` | none | UNSUPPORTED | As `stop_loss`: `REJECTED_SCHEMA`. |
| `confidence` | none | UNSUPPORTED | No generic confidence; `REJECTED_SCHEMA`. |
| `valid_until_ms` | `valid_until_utc` | DERIVED | Epoch milliseconds become a fixed-width UTC string; the TRON-side conversion rounds conservatively (valid_until down) per D-6. |
| `strategy_ref` | `strategy_id`, `strategy_version`, `strategy_fingerprint` | UNSUPPORTED | One identifier cannot carry the identity triple; the trigger carries three explicit fields; absent triple is `REJECTED_SCHEMA`. |
| `signal_ref` | `evaluation_id` | DERIVED | Evidence linkage token; opaque pattern (AS-5). |
| `supersedes_action_id` | none | UNSUPPORTED | Supersession is expressed by a `SETUP_INVALIDATED` trigger for the same setup (CP2-R13); `REJECTED_SCHEMA` if carried. |
| `position_action_ref` | none | UNSUPPORTED | Position references belong to TRON core; `REJECTED_SCHEMA`. |
| `extensions` | none | UNSUPPORTED | The contract is a closed world; `REJECTED_SCHEMA`. |

### 8.3 Fields the contract requires that neither competing shape carries

<!-- mapping-table missing-sources -->
| Source field | Target field | Disposition | Rule and fail-closed behaviour |
|---|---|---|---|
| none | `execution_policy_ref` | UNSUPPORTED | Opaque reference copied from the strategy; absent is `REJECTED_SCHEMA`. |
| none | `setup_origin_bar_utc` | UNSUPPORTED | Part of the occurrence key; absent is `REJECTED_SCHEMA`. |
| none | `bar_close_utc` | UNSUPPORTED | Part of the occurrence key; absent is `REJECTED_SCHEMA`. |
| none | `state_from` | UNSUPPORTED | Contract state name; absent is `REJECTED_SCHEMA`. |
| none | `state_to` | UNSUPPORTED | Contract state name; absent is `REJECTED_SCHEMA`. |
| none | `signal_class` | UNSUPPORTED | Required in FALCON only through `action_type`; absent is `REJECTED_SCHEMA`. |

## 9. Assumptions the candidate leaves open

| Id | Statement | Offered to |
|---|---|---|
| AS-1 | An envelope with `signature` or `signing_key_id` absent is `REJECTED_SIGNATURE`, checked before schema, so T-A3 "unsigned copy" yields a named outcome. | `GOAL-TRIGGER-001` T-A3 |
| AS-2 | A setup is identified by the strategy identity triple, `binding_id`, `instrument_id`, `timeframe` and `setup_origin_bar_utc`; "an invalidation for the same setup arrived first" is judged on that key. | `GOAL-TRIGGER-001` outcomes |
| AS-3 | CONFLICT quarantines the **incoming** envelope; the original row is unaffected (the candidate does not say which envelope or whether the original is also blocked). | `GOAL-TRIGGER-001` D-1 corollary |
| AS-4 | `signature` is 128 lowercase hex characters; `signing_key_id` is `sha256:` of the raw 32-byte public key; the trust store carries the public key as hex. | `GOAL-TRIGGER-001` key custody |
| AS-5 | Opaque tokens (`binding_id`, `execution_policy_ref`, `evaluation_id`, `input_snapshot_id`) use the TRON identifier pattern `^[A-Za-z0-9_.:-]{1,128}$`; `strategy_id` and `strategy_version` use the shared HELIOS/HSA identity patterns. | `GOAL-CONTRACT-001` C-4 |
| AS-6 | A rejection before authentication (schema, unsigned, key, signature) is journaled by content digest and never records the `trigger_id`; only authenticated envelopes occupy a row (AC-22). | `GOAL-TRIGGER-001` outcomes |
| AS-7 | An accepted `SETUP_INVALIDATED` trigger has no terminal outcome in the candidate vocabulary; the model leaves its row `RECEIVED` (AC-21). | `GOAL-TRIGGER-001` outcomes |
| AS-8 | A `RETIRED` key remains valid for verification inside its validity window; only `REVOKED` or out-of-window keys are refused. Not fixture-tested. | `GOAL-TRIGGER-001` key custody |
| AS-9 | Publisher retry: an unavailable inbox charges no attempt; each rejection charges one; the entry is QUARANTINED at the configured bound (scenario value 3); later entries are never blocked. | `GOAL-TRIGGER-001` durable publication |
| AS-10 | Reconciliation truth tokens are `ORDER_PRESENT`, `ORDER_ABSENT_CONFIRMED`, `UNCERTAIN`; only the first two end the wait. | TRON-T1 / TRON-T4 |

## 10. Change requests and findings offered (never edited here)

Findings AC-16 to AC-28 are in `RECONCILIATION.md`. New register rows offered to the owning PID: AC-22 (pre-authentication rejection must not consume an identifier), AC-21 (no terminal outcome for an accepted invalidation), AC-23 (conflict target), AC-19 and AC-20 (encodings and unsigned outcome), AC-24 (setup key), AC-25 (claim-time verification not testable from the candidate).

## 11. Compatibility matrix rows (contributed by a separate GOAL PR after acceptance)

<!-- matrix-rows -->
| Provider | Provider version | Consumer | Consumer version | Status | Owner | Evidence |
|---|---|---|---|---|---|---|
| HELIOS trigger publisher | `goal.strategy-trigger/v1` candidate `64c843b`; no code exists | TRON TradingTriggerInbox | none exists; D1 intake is a different shape | ADAPTER | HELIOS-T3 and TRON-T4 | both sides MISSING; fixtures and models only |
| HELIOS `strategy_state` publication | `helios.strategy_state/1.0.0` at `7f7193d` | trigger publisher | none exists | ADAPTER | HELIOS architect (D-10) | state is published, a trigger is never produced by the engine |
| FALCON `helios.strategy_trigger` payload | v1 at `8f218ec` | TRON inbox as trigger transport | none exists | INCOMPATIBLE | CA/PO | competing shape; evidence-side only (AC-17) |
| TRON intake `falcon.trade_action.v1` | D1 branch `37d5f00` | `goal.strategy-trigger/v1` producer | candidate `64c843b` | INCOMPATIBLE | CA/PO and Matt (D-3) | requires stop-loss, take-profit, confidence, epoch milliseconds (AC-18) |
| TRON inbox evidence | `tron.trigger_observed`, `tron.admission_decision` at `8f218ec` | FALCON evidence families | `8f218ec` | ADAPTER | FALCON-T3 and TRON-T4 | Lane E registry facts pending; assumption recorded |
| `goal.strategy-trigger/v1` identity triple | candidate `64c843b` | `GOAL-CONTRACT-001` identity | candidate `64c843b` | ADAPTER | CA/PO (C-1, C-2, S-1) | both unpublished; fingerprint algorithms differ across components |

## 12. Conformance obligations

`conformance/PROVIDER-TESTS.md` and `conformance/CONSUMER-TESTS.md`. Fixtures: `fixtures/valid/` (5), `fixtures/invalid/` (29, each named `<outcome>__<case>.json` and declaring its rule), `fixtures/scenarios/` (16), and `fixtures/KEYS-PUBLIC.json` (ephemeral public keys only; no private key or seed was ever written to disk).
