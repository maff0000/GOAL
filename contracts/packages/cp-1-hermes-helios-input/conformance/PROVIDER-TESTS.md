# CP-1 provider conformance tests

Status: PROPOSED (`cp-1/0.1.0`). All tests run offline from `fixtures/`; none needs Redis, a network or a clock other than the `now_utc` / `ingested_at_utc` given in each fixture. A provider **emits only valid fixtures and never an invalid one**.

There are two providers.

## P-A. HERMES publication (provider at CP-1a)

Run against what HERMES would publish, as JSON values read from the immutable history keys and the mutable latest keys.

| Id | Test | Pass condition |
|---|---|---|
| PA-1 | Every candle record HERMES publishes for an instrument and timeframe on the grid validates against `schema/hermes-candle-envelope.v1.schema.json` plus the rule table in `PACKAGE.md` section 5.1 | Same verdict and code as `fixtures/valid/wire` (accept) |
| PA-2 | Every indicator record validates against `schema/hermes-indicator-envelope.v1.schema.json` and carries only the fourteen admissible names with the pinned method tokens | Accept; any other name is `CP1-J03`, any other token `CP1-J04` |
| PA-3 | Numbers are JSON number literals with at most six fractional digits and no exponent; instants are millisecond `Z` | No `CP1-W06`, no `CP1-W07` |
| PA-4 | No key anywhere carries an interpretive token (regime, risk, signal and the others in `PACKAGE.md`) | No `CP1-W05` |
| PA-5 | A history index lists only epochs whose candle **and** indicator objects exist, strictly ascending, one entry per bar | No `CP1-H01`, `CP1-J01`, `CP1-H02` |
| PA-6 | The record under `latest` is never older than the newest history bar | No `CP1-H03` |
| PA-7 | A bar whose lower-timeframe coverage is incomplete is never published with status `OK` | A record with `source_count` below `expected_source_count` is status `SOURCE_INCOMPLETE` (`CP1-S02` at the adapter) |
| PA-8 | The provider never emits any fixture under `fixtures/invalid/wire/` | Each invalid fixture, replayed through the provider's own validator, is refused |

## P-B. External adapter (provider at CP-1b)

| Id | Test | Pass condition |
|---|---|---|
| PB-1 | For each `fixtures/valid/wire` case, produce frames | Output is **byte-identical** (canonical JSON, sorted keys, no whitespace) to `expected_frames` |
| PB-2 | For each `fixtures/invalid/wire` case, produce frames | No frame is produced; the reported code equals the file-name code |
| PB-3 | Adapter output frames pass the strict provider mode on `fixtures/invalid/frame` cases with `"mode": "adapter"` | Each such case is refused with its code, and the adapter never emits one |
| PB-4 | Never repair: for every refusal the adapter does not default, zero-fill, clamp `ingested_at_utc`, re-sort, de-duplicate, rename `D` to `D1`, or shorten a window | Asserted by PB-2 (no frame) |
| PB-5 | Scenarios in `fixtures/scenarios/` | Each step reports the stated `event` and `code`; the watermark rule of `PACKAGE.md` section 8 holds across restart |
| PB-6 | `regime` and `session` are `null` in every emitted frame | No `CP1-F20` |
| PB-7 | The adapter imports nothing into the pure HELIOS engine and the engine imports no Redis or network module (the existing HELIOS import-ban test continues to pass) | Evidence is the HELIOS `tests/test_execution_blind.py` result at the integration commit |
