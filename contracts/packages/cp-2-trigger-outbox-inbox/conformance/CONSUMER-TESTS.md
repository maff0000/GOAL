# CP-2 consumer conformance tests

Status: PROPOSED (`cp-2/0.1.0`). A consumer **accepts valid fixtures and rejects invalid ones with the stated outcome**. Offline, from `fixtures/`.

## Consumer: the TRON TradingTriggerInbox (door, store, claim)

| Id | Test | Pass condition |
|---|---|---|
| CC-1 | Every `fixtures/valid` envelope under its `context` | Accepted and recorded RECEIVED with a receipt |
| CC-2 | Every `fixtures/invalid` envelope under its `context` | Refused or terminally recorded with the outcome in the file name, using the order of `PACKAGE.md` section 5 (first failing rule) |
| CC-3 | Two independent verifiers agree | The consumer's door verdict equals both reference checkers (`tests/cp_support/cp2_checker_a.py`, `cp2_checker_b.py`) on every fixture |
| CC-4 | Signature primitive | The verifier reproduces the RFC 8032 public test vectors and rejects a one-bit change in signature, message and key |
| CC-5 | Duplicate delivery | Scenario `duplicate_delivery`: one row, the original receipt each time, original disposition unchanged |
| CC-6 | Conflict | Scenario `id_collision_different_digest`: CONFLICT, one row, original unaffected, never claimed |
| CC-7 | Pre-authentication rejection never consumes an identifier | Scenario `forged_copy_cannot_poison_id`: the genuine envelope is accepted after a forged copy was refused |
| CC-8 | Expiry at receipt and at claim; skew; supersession | Scenarios `expired_trigger`, `claim_after_window`, `clock_skew`, `invalidation_first_supersedes` |
| CC-9 | Crash between submission and journaled outcome | Scenario `crash_after_submit_no_double_execution`: total broker submissions 1; claim after RECONCILE or after a terminal outcome is refused |
| CC-10 | Uncertain broker state | Scenario `uncertain_broker_state_never_retried`: no new submission; ABANDONED_UNRESOLVED at window end |
| CC-11 | One immutable terminal outcome per authenticated trigger | In every scenario a terminal row never changes after it is set |
| CC-12 | Receipt is not acceptance | RECEIVED carries no execution right; claim, eligibility, sizing and execution remain TRON core |
| CC-13 | Key trust at claim | Not testable from the candidate (AC-25): the draft says verification happens at receipt and again at claim, but defines no fixture-level behaviour for a key revoked between the two |
