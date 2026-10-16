# CP-2 fixtures

Signed fixtures cannot be regenerated. They were signed with ephemeral Ed25519 keys generated in memory; the keys were discarded and never written to disk, and no generator is committed (a committed generator would have to contain or derive a key). The files hold public keys (`KEYS-PUBLIC.json`) and signatures only. Tests verify them; they do not re-sign them. `tests/test_cp2_conformance.py` creates new throwaway keys at test time only for the round-trip test.

Any change to a signed fixture's content therefore needs a fresh signing run by the lane engineer, with new keys, followed by new `KEYS-PUBLIC.json` and trust-store values in the affected fixtures.
