# CP-1: HERMES Redis publication to HELIOS input

**Package version:** `cp-1/0.1.0`  
**Status:** PROPOSED. Nothing in this package is frozen, approved or authoritative.  
**Produced by:** GOLD-AUD-C (read-only audit); GOAL base `ceaf0291a43d029b1a47b1c192a62ff147f05ac0`.  
**Freeze owner of the normative text:** not yet decided (open decision D-C1 of `pids/GOLD-AUD-C.md`; recommendation recorded there: a `HERMES-FACT-001` PID for the publication contract, with GOAL approving this interface). Until then this package is a DRAFT with no frozen field, and it restates no decision of `GOAL-CONTRACT-001` or `GOAL-TRIGGER-001`.

## 1. Purpose and boundary

CA guidance 2026-10-15 (item 1): HERMES owns Redis publication; a HELIOS-side **external adapter**, outside the pure HELIOS engine, owns consumption and translation; GOAL approves the interface between them. CP-1 is that interface. It has two boundaries, so that each side can be tested without the other:

| Boundary | Provider | Consumer | What crosses |
|---|---|---|---|
| **CP-1a (wire)** | HERMES publication (read-only Redis values) | HELIOS-side external adapter | HERMES candle envelope v1 (latest and history record) and indicator envelope v1 (latest and history record) |
| **CP-1b (frame)** | the external adapter | the HELIOS engine (`MarketFactFrame` window) | canonical market-fact frames |

Out of scope: building the adapter, any Redis client, fact names and payload registration (`HERMES-FACT-001`), regime and risk (ARES), and anything FALCON-side.

## 2. Sources audited

| Source | Revision | Files |
|---|---|---|
| HERMES `main` | `ca1901789f8c7a7e085d02ebde8f7264d90d669e` | `utils/candle_contract_v1.py`, `utils/hermes_indicators_v1.py`, `utils/indicator_history_v1.py`, `utils/candle_history_v1.py`, `utils/candle_d1_history_v1.py`, `docs/contracts/hermes_redis_contract_manifest.md`, `docs/architecture/redis-consumer-integrity-boundary.md`, `docs/governance/PID-HERMES-MVP-001.md` |
| HELIOS `main` | `7f7193d55475e40583892b94dd461b1b64d6f1ef` | `helios/contracts/market_fact.py`, `helios/contracts/_fields.py`, `helios/contracts/timeframe.py`, `helios/contracts/freshness.py`, `helios/contracts/window.py`, `helios/clock.py`, `helios/hermes/fixture_source.py`, `helios/integration/hermes_boundary.py`, `docs/INTEGRATION.md`, `fixtures/hermes/`, `tests/test_hermes_fixtures.py`, `tests/test_execution_blind.py` |

Every claim below is traceable to those files at those revisions through `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-C/SOURCES.tsv`. Live HERMES production state was not read; it is UNVERIFIED here and belongs to Lane A.

## 3. Versioning and compatibility rules

* Package version `cp-1/MAJOR.MINOR.PATCH`. Wire versions are named by their owners: HERMES `schema_version` `v1` with `contract` `hermes.candles.latest` and indicator `indicator_set_version` `v1`. The frame schema version is `hermes.market_fact/1.0.0` (assumption AS-C1, see section 10).
* **Additive** (minor): a new HERMES indicator name added to the admissible set in section 5.3, a new accepted method token, a new rejection code. **Breaking** (major): any change to a field's meaning, number form, instant form, the pinned method tokens, or the removal of a field.
* The wire contract is a **closed world** on the adapter side: an unknown key or indicator name is refused, not ignored (`CP1-W04`, `CP1-J03`). A HERMES addition therefore forces a deliberate package version, never a silent pass-through. This is the same posture HELIOS takes for its own fact contract.
* A window is judged as a whole: one refused bar refuses the window (no partial acceptance, no repair, no re-sort, no default).
* Status words in the matrix rows (section 11): `COMPATIBLE` means no translation and no change on either side; `ADAPTER` means a named owner must build or change something; `INCOMPATIBLE` means the pair cannot work without changing one model, which is a CA/PO decision. No row is `COMPATIBLE` unless both sides' fixtures have been run against the component itself.

## 4. Evaluation order (verdict rule)

A candidate window is checked against every rule. **The verdict is the violated rule with the lowest ordinal in the order below**; a window that violates nothing is accepted. A rule whose prerequisite structure is absent contributes no violation (for example, number rules are not evaluated on a missing field, because the missing field is `CP1-W03`).

Order: `W01 W02 W03 W05 W04 W08 W10 W09 W07 W06 S03 S01 S02 S04 H01 J01 J02 J03 J04 H02 H03 F18 F02 F17 F01 F08 F06 F07 F03 F04 F05 F09 F10 F12 F11 F13 F16 F20 F19 F14 F15`. The `R` codes (section 6) are produced by the reader loop, not by the checks.

`CP1-F14`, `CP1-F15`, `CP1-F16` and `CP1-F19` depend on HELIOS-owned policy (freshness limits, required facts). They are evaluated in consumer mode only; the adapter never evaluates freshness policy, it only passes through facts and refuses those HERMES itself marks unusable (`CP1-S04`).

## 5. Field-level mapping tables

Disposition is `MAPPED` (value carried unchanged), `DERIVED` (computed by the stated rule) or `UNSUPPORTED` (not carried; the fail-closed behaviour and error name are stated). Candle and indicator rows are HERMES to frame; the last block lists frame fields with no HERMES source.

### 5.1 HERMES candle envelope to frame

<!-- mapping-table candle -->
| Source field | Target field | Disposition | Rule and fail-closed behaviour |
|---|---|---|---|
| `schema_version` | `provenance.schema_version` | DERIVED | Must be the string `v1` (else `CP1-W01`). The output is the constant `hermes.market_fact/1.0.0` chosen by this package (AS-C1); HERMES never publishes that string. |
| `service` | none | UNSUPPORTED | Checked, not carried. Any value other than `HERMES` is `CP1-W02`. |
| `domain` | none | UNSUPPORTED | Checked, not carried. Any value other than `candles` is `CP1-W03`. |
| `contract` | none | UNSUPPORTED | Checked, not carried. Any value other than `hermes.candles.latest` is `CP1-W01`. |
| `contract_version` | none | UNSUPPORTED | Checked, not carried. Any value other than `v1` is `CP1-W01`. |
| `key` | none | UNSUPPORTED | Checked against instrument and timeframe: must equal the `latest:v1` key for them even on a history record. Mismatch is `CP1-W09`. |
| `generated_at_utc` | `provenance.observed_at_utc` | DERIVED | Observed instant is the later of the candle and indicator `generated_at_utc`, widened from millisecond to fixed-width microsecond with zero fill. Not millisecond form is `CP1-W07`. |
| `valid_until_utc` | none | UNSUPPORTED | Dropped: HELIOS measures age from the bar close with its own policy. Malformed instant is `CP1-W07`. |
| `ttl_seconds` | none | UNSUPPORTED | Dropped. Absent is `CP1-W03`. |
| `freshness_state` | none | UNSUPPORTED | `STALE` or `UNAVAILABLE` refuses the bar with `CP1-S04`; other values are dropped; a value outside the HERMES set is `CP1-W03`. |
| `status` | none | UNSUPPORTED | `OK` is usable. `NO_SOURCE_DATA`, `MARKET_CLOSED`, `PUBLISH_DISABLED` is `CP1-S03`; `FORMING` is `CP1-S01`; `SOURCE_INCOMPLETE`, `GAP_DETECTED` is `CP1-S02`; `STALE` is `CP1-S04`. |
| `reason_codes` | none | UNSUPPORTED | Dropped. Not a list is `CP1-W03`. |
| `provenance.publisher` | none | UNSUPPORTED | Checked, not carried. Not `HERMES` is `CP1-W02`. |
| `provenance.source` | none | UNSUPPORTED | Dropped: the upstream feed token has no HELIOS field and is not propagated. |
| `provenance.source_timeframe` | none | UNSUPPORTED | Dropped. Absent is `CP1-W03`. |
| `provenance.derivation` | none | UNSUPPORTED | Dropped. A value outside the two HERMES tokens is `CP1-W03`. |
| `provenance.generated_at_utc` | none | UNSUPPORTED | Dropped. Not millisecond form is `CP1-W07`. |
| `provenance.source_policy_epoch` | none | UNSUPPORTED | Dropped. Absent is `CP1-W03`. |
| `data.instrument` | `instrument` | MAPPED | Canonical instrument id. The inbound alias `XAUUSD` is `CP1-W10`; a value different from the key being read is `CP1-W09`. |
| `data.timeframe` | `timeframe` | MAPPED | One of `M1 M5 M15 H1 H4 D1`. The legacy daily token `D` is `CP1-W08` and is never renamed to `D1`. |
| `data.timestamp_utc` | `timestamp_utc` | DERIVED | Bar OPEN instant, millisecond `Z` widened to fixed-width microsecond `Z`. Not millisecond form is `CP1-W07`. |
| `data.open` | `candle.open` | DERIVED | JSON number to normalised exact decimal text from the literal (no binary float, no exponent, at most 6 fractional digits). Violation is `CP1-W06`. |
| `data.high` | `candle.high` | DERIVED | Same rule as `open`. Incoherent with low, open or close is `CP1-F03`. |
| `data.low` | `candle.low` | DERIVED | Same rule as `open`. |
| `data.close` | `candle.close` | DERIVED | Same rule as `open`. |
| `data.volume` | `candle.volume` | DERIVED | Same rule as `open`. Negative is `CP1-F04`. |
| `data.body_high` | none | UNSUPPORTED | Dropped: strategy-local derived geometry is not a HELIOS fact. Absent is `CP1-W03`. |
| `data.body_low` | none | UNSUPPORTED | Dropped, as `body_high`. |
| `data.body_size` | none | UNSUPPORTED | Dropped, as `body_high`. |
| `data.range_size` | none | UNSUPPORTED | Dropped, as `body_high`. |
| `data.wick_high` | none | UNSUPPORTED | Dropped, as `body_high`. |
| `data.wick_low` | none | UNSUPPORTED | Dropped, as `body_high`. |
| `data.candle_direction` | none | UNSUPPORTED | Dropped, as `body_high`. |
| `data.is_closed` | `candle.complete` | MAPPED | `false` refuses the bar with `CP1-S01`; the adapter therefore emits only `complete: true`. |
| `data.source_timeframe` | none | UNSUPPORTED | Dropped. Absent is `CP1-W03`. |
| `data.source_coverage` | none | UNSUPPORTED | Dropped. Absent is `CP1-W03`. |
| `data.source_count` | none | UNSUPPORTED | Fewer than `expected_source_count` is `CP1-S02`. |
| `data.expected_source_count` | none | UNSUPPORTED | Used only for the `CP1-S02` comparison. |
| `data.gap_state` | none | UNSUPPORTED | Any value other than `NONE` is `CP1-S02`. |
| `data.derivation_policy` | none | UNSUPPORTED | Dropped. Absent is `CP1-W03`. |
| `data.source_policy_epoch` | none | UNSUPPORTED | Dropped. Absent is `CP1-W03`. |
| `data.publisher` | none | UNSUPPORTED | Checked, not carried. Not `HERMES` is `CP1-W02`. |
| `data.contract_version` | none | UNSUPPORTED | Checked, not carried. Not `v1` is `CP1-W01`. |
| `history.history_contract_version` | none | UNSUPPORTED | Optional block on history records, dropped. A block whose key set differs from the five history keys is `CP1-W04`. |
| `history.backfill_run_id` | none | UNSUPPORTED | Dropped; see `history` block rule above (`CP1-W04`). |
| `history.backfill_inserted_at_utc` | none | UNSUPPORTED | Dropped. Not millisecond form is `CP1-W07`. |
| `history.source_table` | none | UNSUPPORTED | Dropped; see `history` block rule above (`CP1-W04`). |
| `history.source_timestamp_utc` | none | UNSUPPORTED | Dropped. Not millisecond form is `CP1-W07`. |

### 5.2 Fields the frame needs that HERMES does not publish

<!-- mapping-table frame-only -->
| Source field | Target field | Disposition | Rule and fail-closed behaviour |
|---|---|---|---|
| adapter constant | `candle.source` | DERIVED | The constant `hermes`, the publisher token lower-cased; the upstream feed token is not used. |
| adapter constant | `provenance.source` | DERIVED | The constant `hermes`. |
| adapter read instant | `provenance.ingested_at_utc` | DERIVED | The adapter's UTC clock at the moment it read the window, fixed-width microsecond. If it precedes `observed_at_utc` the window is refused with `CP1-F09`; the adapter never clamps or substitutes. |
| none (no supplier) | `indicators.regime` | UNSUPPORTED | Always `null`. HERMES forbids regime in its payload (ARES owns it). A provider emitting a value is `CP1-F20`. |
| none (no supplier) | `indicators.session` | UNSUPPORTED | Always `null`. No HERMES source exists. A provider emitting a value is `CP1-F20`. |

### 5.3 HERMES indicator envelope to frame

The admissible HERMES indicator names at `cp-1/0.1.0` are exactly the fourteen published by the indicator foundation: `ema_9 ema_12 ema_21 ema_26 ema_50 ema_200 rsi_14 atr_14 bollinger_upper_20_2 bollinger_middle_20_2 bollinger_lower_20_2 adx_14 adx_plus_di_14 adx_minus_di_14`. Any other name is `CP1-J03`.

<!-- mapping-table indicator -->
| Source field | Target field | Disposition | Rule and fail-closed behaviour |
|---|---|---|---|
| `publisher` | none | UNSUPPORTED | Checked, not carried. Not `HERMES` is `CP1-W02`. |
| `schema_version` | none | UNSUPPORTED | Checked, not carried. Not `v1` is `CP1-W01`. |
| `contract_version` | none | UNSUPPORTED | Checked, not carried. Not `v1` is `CP1-W01`. |
| `source_candle_contract` | none | UNSUPPORTED | Checked, not carried. Not `v1` is `CP1-W01`. |
| `indicator_set_version` | none | UNSUPPORTED | Checked, not carried. Not `v1` is `CP1-W01`. |
| `instrument` | none | UNSUPPORTED | Must equal the instrument being read; mismatch is `CP1-W09`. |
| `timeframe` | none | UNSUPPORTED | Must equal the timeframe being read; mismatch is `CP1-W09`. |
| `generated_at_utc` | `provenance.observed_at_utc` | DERIVED | Contributes to the later-of rule for the observed instant (see candle `generated_at_utc`). Not millisecond form is `CP1-W07`. |
| `value_open_time_utc` | none | UNSUPPORTED | Join key: must equal the candle `data.timestamp_utc` of the same bar, else `CP1-J02`. Not millisecond form is `CP1-W07`. |
| `source_timeframes` | none | UNSUPPORTED | Dropped. Not a list is `CP1-W03`. |
| `indicators.rsi_14` | `indicators.rsi_14` | DERIVED | Exact decimal text from the literal; explicit `null` stays `null` (absent, never zero). Outside 0..100 is `CP1-F05`. |
| `indicators.ema_9` | `indicators.ema_9` | DERIVED | Exact decimal text; `null` stays `null`. |
| `indicators.ema_21` | `indicators.ema_21` | DERIVED | Exact decimal text; `null` stays `null`. |
| `indicators.ema_50` | `indicators.ema_50` | DERIVED | Exact decimal text; `null` stays `null`. |
| `indicators.ema_200` | `indicators.ema_200` | DERIVED | Exact decimal text; `null` stays `null` (HERMES emits `null` below 200 usable closes, never a fabricated value). |
| `indicators.atr_14` | `indicators.atr_14` | DERIVED | Exact decimal text; `null` stays `null`. Negative is `CP1-F05`. |
| `indicators.ema_12` | none | UNSUPPORTED | Dropped: outside the closed HELIOS fact set. Forwarding it would be `CP1-F02`. |
| `indicators.ema_26` | none | UNSUPPORTED | Dropped, as `ema_12`. |
| `indicators.bollinger_upper_20_2` | none | UNSUPPORTED | Dropped, as `ema_12`. |
| `indicators.bollinger_middle_20_2` | none | UNSUPPORTED | Dropped, as `ema_12`. |
| `indicators.bollinger_lower_20_2` | none | UNSUPPORTED | Dropped, as `ema_12`. |
| `indicators.adx_14` | none | UNSUPPORTED | Dropped, as `ema_12`. |
| `indicators.adx_plus_di_14` | none | UNSUPPORTED | Dropped, as `ema_12`. |
| `indicators.adx_minus_di_14` | none | UNSUPPORTED | Dropped, as `ema_12`. |
| `indicators.<any other name>` | none | UNSUPPORTED | Refused with `CP1-J03`; a name carrying a forbidden interpretive token is `CP1-W05`. |
| `methods.ema_method` | none | UNSUPPORTED | Must be `STANDARD_2_OVER_N_PLUS_1_SMA_SEED` when any `ema_*` value is present, else `CP1-J04`. |
| `methods.rsi_method` | none | UNSUPPORTED | Must be `CUTLER_SMA_14` when `rsi_14` is present (a smoothing change silently changes meaning), else `CP1-J04`. |
| `methods.atr_method` | none | UNSUPPORTED | Must be `SMA_14` when `atr_14` is present, else `CP1-J04`. |
| `freshness_state` | none | UNSUPPORTED | Dropped; a value outside the HERMES set is `CP1-W03`. |
| `deterministic_only` | none | UNSUPPORTED | Must be `true`, else `CP1-W03`. |
| `history.history_contract_version` | none | UNSUPPORTED | Optional block on history records, dropped; a key set different from the five history keys is `CP1-W04`. |
| `history.publish_run_id` | none | UNSUPPORTED | Dropped; see `history` block rule (`CP1-W04`). |
| `history.published_at_utc` | none | UNSUPPORTED | Dropped. Not millisecond form is `CP1-W07`. |
| `history.source_candle_history_key` | none | UNSUPPORTED | Dropped; see `history` block rule (`CP1-W04`). |
| `history.source_timestamp_utc` | none | UNSUPPORTED | Dropped. Not millisecond form is `CP1-W07`. |

## 6. Rejection matrix

Effect vocabulary: **refuse window** (no frame for this read, previous state unchanged, alert if repeated), **no frame, informational** (an expected condition, not an alert), **refuse frame** (HELIOS-side). The consumer never repairs, defaults, re-sorts or substitutes. Side is the party that rejects.

| Code | Name | Side | Effect |
|---|---|---|---|
| CP1-W01 | WIRE_VERSION_UNKNOWN | adapter | refuse window (whole window, no mixing of versions) |
| CP1-W02 | PUBLISHER_NOT_HERMES | adapter | refuse window, alert |
| CP1-W03 | ENVELOPE_MALFORMED | adapter | refuse window, alert |
| CP1-W04 | WIRE_FIELD_UNKNOWN | adapter | refuse window, alert (closed world) |
| CP1-W05 | FORBIDDEN_INTERPRETIVE_FIELD | adapter | refuse window, alert |
| CP1-W06 | NUMBER_FORM | adapter | refuse window, alert |
| CP1-W07 | INSTANT_FORM | adapter | refuse window, alert |
| CP1-W08 | TIMEFRAME_UNSUPPORTED | adapter | refuse window, alert |
| CP1-W09 | IDENTITY_MISMATCH | adapter | refuse window, alert |
| CP1-W10 | INSTRUMENT_FORM | adapter | refuse window, alert |
| CP1-S01 | BAR_NOT_CLOSED | adapter | no frame, informational |
| CP1-S02 | SOURCE_INCOMPLETE | adapter | refuse window, alert |
| CP1-S03 | NO_DATA | adapter | no frame, informational |
| CP1-S04 | HERMES_MARKS_STALE | adapter | refuse window, alert |
| CP1-H01 | HISTORY_OBJECT_MISSING | adapter | refuse window, alert (never shorten the window) |
| CP1-H02 | BARS_UNORDERED_OR_DUPLICATE | adapter | refuse window, alert (never re-sort) |
| CP1-H03 | LATEST_BEHIND_HISTORY | adapter | refuse window, alert |
| CP1-J01 | INDICATOR_RECORD_MISSING | adapter | refuse window, alert |
| CP1-J02 | BAR_IDENTITY_MISMATCH | adapter | refuse window, alert |
| CP1-J03 | INDICATOR_UNKNOWN | adapter | refuse window, alert |
| CP1-J04 | INDICATOR_METHOD_UNPINNED | adapter | refuse window, alert |
| CP1-F01 | DECIMAL_FORM | adapter (provider) and HELIOS | refuse frame |
| CP1-F02 | FIELD_UNKNOWN | adapter (provider) and HELIOS | refuse frame (closed world) |
| CP1-F03 | CANDLE_INCOHERENT | adapter (provider) and HELIOS | refuse frame |
| CP1-F04 | VOLUME_NEGATIVE | adapter (provider) and HELIOS | refuse frame |
| CP1-F05 | INDICATOR_RANGE | adapter (provider) and HELIOS | refuse frame |
| CP1-F06 | INSTANT_FORM_OR_NAIVE | adapter (provider) and HELIOS | refuse frame |
| CP1-F07 | INSTANT_MISALIGNED | adapter (provider) and HELIOS | refuse frame |
| CP1-F08 | FRAME_TIMEFRAME_UNSUPPORTED | adapter (provider) and HELIOS | refuse frame |
| CP1-F09 | PROVENANCE_ORDER | adapter (provider) and HELIOS | refuse frame |
| CP1-F10 | WINDOW_MIXED | adapter (provider) and HELIOS | refuse window |
| CP1-F11 | WINDOW_DUPLICATE | adapter (provider) and HELIOS | refuse window |
| CP1-F12 | WINDOW_UNORDERED | adapter (provider) and HELIOS | refuse window |
| CP1-F13 | FRAME_SCHEMA_VERSION_NOT_ACCEPTED | adapter (provider) and HELIOS | refuse frame |
| CP1-F14 | FACT_STALE | HELIOS | refuse frame (policy) |
| CP1-F15 | BAR_INCOMPLETE | HELIOS | refuse frame (policy) |
| CP1-F16 | REQUIRED_FACT_ABSENT | HELIOS | refuse evaluation of the strategy (never zero) |
| CP1-F17 | FRAME_FIELD_MISSING | adapter (provider) and HELIOS | refuse frame |
| CP1-F18 | DOCUMENT_FORMAT_UNKNOWN | HELIOS fixture loader | refuse document |
| CP1-F19 | FACT_FUTURE_DATED | HELIOS | refuse frame (policy) |
| CP1-F20 | REGIME_OR_SESSION_SUPPLIED | adapter (provider obligation) | provider defect; consumer behaviour unspecified |
| CP1-R01 | SOURCE_UNAVAILABLE | adapter | no read, no state change, alert if persistent |
| CP1-R02 | KEY_ABSENT | adapter | no frame, nothing invented |
| CP1-R03 | NO_NEW_BAR | adapter | no frame, informational (already evaluated) |

Mapping of the HELIOS `INPUT_REJECTION_RULES` tuple (`helios/integration/hermes_boundary.py`, `7f7193d`) to codes is in the conformance tests (`tests/test_cp1_conformance.py`, `HELIOS_RULES`); every entry has at least one invalid fixture. HELIOS itself raises exceptions with message text, not codes (AC-3); the fifteen reused malformed cases carry the HELIOS message substring in `tests/test_hermes_fixtures.py` (`MALFORMED_CASES`), which is the consumer-side evidence for the same cases.

## 7. Canonical forms the adapter must emit (CP-1b)

* **Decimals:** exact, normalised decimal text: no exponent, no leading `+`, no trailing zeros in the fractional part, negative zero written `0`. Source: the JSON literal text of the HERMES number, never a binary float. A HERMES number with more than six fractional digits, an exponent, or non-number type is refused (`CP1-W06`); six digits is HERMES's own price quantisation.
* **Instants:** fixed-width UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ` (microseconds always present).
* **Window:** strictly ascending by bar-open instant, one instrument, one timeframe, closed bars only, at most the newest bar newer than the adapter watermark (section 8). Gaps are permitted (markets close); duplicates and out-of-order entries are refused.
* **Absent facts:** `null`, never zero and never omitted. Every frame carries all eight indicator keys.
* **`ingested_at_utc`:** the adapter's read instant. It has no HERMES source (AC-13).
* The consumer (HELIOS) may accept more than these forms (it does today: instants without fractions, offsets, decimal trailing zeros). That leniency is not part of this contract: the provider obligation is strict, the consumer obligation is to accept every canonical frame and to refuse the cases in section 6.

## 8. Failure and recovery semantics

Each scenario is a fixture under `fixtures/scenarios/` with a step list and the required observable outcome per step; `tests/cp_support/cp1_reference_adapter.py` reproduces every one. The reference model is a test device, not an adapter.

| Scenario | Required observable outcome |
|---|---|
| Redis unavailable | `CP1-R01`: no frame, no state change. After recovery the newest unevaluated bar is evaluated exactly once. |
| Key absent | `CP1-R02`: no frame; nothing is invented or defaulted. |
| Latest older than history | `CP1-H03`: refuse the window; the immutable history is not overridden by the mutable latest record, nor the reverse. |
| Reader restart, watermark kept | Re-read; the already evaluated bar is not replayed (`CP1-R03`). |
| Reader restart, watermark lost | At most the newest bar is re-evaluated once; history is never replayed. Downstream idempotency is the CP-2 occurrence key, which excludes the snapshot, so a re-evaluation regenerates the same trigger identifier. |
| Out-of-order or duplicate bars | `CP1-H02`: refuse; the adapter takes the index as listed and never sorts. |
| History gap (index lists a bar whose object is absent) | `CP1-H01`: refuse the window; never shorten it. |
| Incomplete (forming) bar | Never read as history; the closed bar is evaluated once when it appears. A history record marked not closed is `CP1-S01`. |
| Schema bump | A window containing any bar of an unknown envelope version is refused as a whole (`CP1-W01`) until a package version accepts it. |

Durable state owned by the adapter: one watermark per instrument and timeframe (the newest open instant handed to evaluation). Loss of the watermark is tolerated by the rule above; it is never reconstructed by guessing.

## 9. Findings carried by this package

The numbered findings AC-1 to AC-15 (CP-1) are in `RECONCILIATION.md` of the lane evidence directory. The ones that change behaviour here: AC-2 (version string), AC-4 and AC-5 (number and instant form), AC-6 (regime and session have no supplier), AC-7 (HERMES-only indicators), AC-8 (method tokens), AC-9 (history activation), AC-10 and AC-11 (H4/D1 grid and depth), AC-13 (`ingested_at_utc`).

## 10. Assumptions and open decisions

| Id | Statement | Owner |
|---|---|---|
| AS-C1 | The frame schema version is `hermes.market_fact/1.0.0` because every HELIOS fixture, test configuration and deployment example uses it, although the constant advertised by `describe_input_contract()` is `helios.market_fact/1.0.0`. Fixing the constant is a HELIOS-side change (D-C3). | HELIOS architect via CA/PO |
| AS-C2 | The observed instant of a frame is the later of the candle and indicator generation instants. HERMES has one generation instant per envelope and HELIOS one observed instant per frame. | CA/PO |
| AS-C3 | Exact decimal conversion from the HERMES JSON literal with at most six fractional digits (D-C5 is the open decision on the numeric form on the Redis wire). | CA/PO |
| AS-C4 | The adapter emits closed bars only; deployments that allow incomplete frames need a minor version. | CA/PO |
| D-C1, D-C3, D-C5 | By reference to `pids/GOLD-AUD-C.md`. CP-1 cannot freeze while `C-12` of `GOAL-CONTRACT-001` is open. | PO |

## 11. Compatibility matrix rows (contributed by a separate GOAL PR after acceptance)

<!-- matrix-rows -->
| Provider | Provider version | Consumer | Consumer version | Status | Owner | Evidence |
|---|---|---|---|---|---|---|
| HERMES candle envelope | v1 at `ca19017` | HELIOS-side external adapter | not built | ADAPTER | HELIOS-T2 (HELIOS architect) | fixtures pass in the reference models; adapter MISSING |
| HERMES indicator latest | v1 at `ca19017` | HELIOS-side external adapter | not built | ADAPTER | HELIOS-T2 (HELIOS architect) | as above; production activation of history UNVERIFIED (Lane A) |
| HERMES indicator history | v1 at `ca19017` | HELIOS-side external adapter | not built | ADAPTER | HERMES architect and HELIOS-T2 | code in main, deployed activation not executed per the HERMES PID |
| HERMES D1 candle and indicator history | v1 at `ca19017` | HELIOS-side external adapter | not built | INCOMPATIBLE | CA/PO | no D1 indicator history is designed and D1 candle history retains 35 bars, below any 200-bar indicator (AC-11) |
| External adapter | cp-1/0.1.0 frames | HELIOS engine | `7f7193d` | ADAPTER | HELIOS architect | version constant mismatch (AC-2); engine not run in this audit |
| HERMES `v1` envelopes passed through unchanged | v1 | HELIOS engine | `7f7193d` | INCOMPATIBLE | CA/PO | every shape differs (version, numbers, instants, keys, closed world) |
| FALCON `hermes.market_fact` payload | v1 at `8f218ec` | HELIOS engine | `7f7193d` | INCOMPATIBLE | CA/PO | evidence-side shape, not an input (AC-14) |

## 12. Conformance obligations

`conformance/PROVIDER-TESTS.md` and `conformance/CONSUMER-TESTS.md` list the tests each side must pass offline from the fixtures. Fixtures: `fixtures/valid/` (2 wire, 2 frame), `fixtures/invalid/` (wire, frame; every file is named `<code>__<case>.json` and declares its rule and code), `fixtures/scenarios/`, and `fixtures/REUSE-MANIFEST.json` listing the 18 reused HELIOS cases with source path, revision and SHA-256.
