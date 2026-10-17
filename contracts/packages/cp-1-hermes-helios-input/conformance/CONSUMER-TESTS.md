# CP-1 consumer conformance tests

Status: PROPOSED (`cp-1/0.1.0`). A consumer **accepts valid fixtures and rejects invalid ones with the stated code**. Offline, from `fixtures/`.

There are two consumers.

## C-A. External adapter (consumer at CP-1a)

| Id | Test | Pass condition |
|---|---|---|
| CA-1 | Accept every `fixtures/valid/wire` case | Frames produced, none refused |
| CA-2 | Refuse every `fixtures/invalid/wire` case | The code equals the code in the file name, using the evaluation order of `PACKAGE.md` section 4 (lowest ordinal wins) |
| CA-3 | Cross-implementation agreement | The adapter's verdict and code equal those of the two reference checkers (`tests/cp_support/cp1_checker_a.py` and `cp1_checker_b.py`) on every fixture |

CA-1 to CA-3 are the same tests as PB-1 and PB-2 seen from the other side; an adapter implementer runs them once.

## C-B. HELIOS engine (consumer at CP-1b)

The engine has no machine-readable rejection codes; it raises exceptions with message text. The consumer test therefore compares **accept or refuse** and, for the reused cases, the HELIOS message substring already asserted by its own tests. Mapping to CP-1 codes is the reference for the human reader.

| Id | Test | Pass condition |
|---|---|---|
| CB-1 | Accept every `fixtures/valid/frame` case and every frame in `expected_frames` of `fixtures/valid/wire`, configured with accepted schema version `hermes.market_fact/1.0.0` | Window built and the newest frame fresh at the stated reference instant |
| CB-2 | Refuse every `fixtures/invalid/frame` case with `"mode": "consumer"` | Refused; for the 15 reused malformed cases the message substring listed in HELIOS `tests/test_hermes_fixtures.py` (`MALFORMED_CASES`) appears |
| CB-3 | Policy cases `CP1-F14`, `CP1-F15`, `CP1-F19` with the freshness policy in each fixture's `context` | Refused with the HELIOS stale/incomplete/future-dated error |
| CB-4 | `CP1-F16`: a required fact is `null` on the newest frame | The evaluation of the strategy that requires it is refused; the value is never read as zero |
| CB-5 | Cases with `"mode": "adapter"` (provider-form violations: JSON number, trailing zeros, millisecond instants, bare `v1` version, regime supplied, an unknown indicator) | **Unspecified for the consumer** (the HELIOS fixture loader reads JSON numbers as exact decimals and accepts instants without fractions, so it may accept some of them); the consumer must not crash and must not misread the value. The provider obligation is PB-3, not this test |
| CB-6 | `describe_input_contract()` advertises a fact schema version that the same deployment accepts | Open: today it advertises `helios.market_fact/1.0.0` while fixtures, configuration and examples use `hermes.market_fact/1.0.0` (AC-2, D-C3); this test cannot pass until the HELIOS-side fix |

Not run in this audit: the HELIOS engine itself (the audit executes no component code). CB-1 to CB-6 are the obligations; their results belong to the HELIOS integration work item.
