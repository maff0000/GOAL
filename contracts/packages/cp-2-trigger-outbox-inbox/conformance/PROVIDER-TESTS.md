# CP-2 provider conformance tests

Status: PROPOSED (`cp-2/0.1.0`). Offline, from `fixtures/`. A provider **emits only valid fixtures' kind of envelope and never an invalid one**. Normative text is `GOAL-TRIGGER-001`; these tests execute it, they do not extend it.

## Provider: the HELIOS-side trigger publisher (signer and outbox)

| Id | Test | Pass condition |
|---|---|---|
| PP-1 | For each valid fixture's inputs, produce the envelope | The envelope passes the door (`ACCEPT`) under the fixture's context; `trigger_id` equals the derivation of CP2-R04 |
| PP-2 | Replay of an occurrence key (same ten occurrence fields) | Same `trigger_id`; with a deterministic signer, byte-identical envelope |
| PP-3 | Two evaluations of the same setup that differ only in snapshot, evaluation identifier or signing time | Same `trigger_id`, different content digest; the second is a conflict candidate, so the publisher emits only one (it refuses locally and alerts) |
| PP-4 | The publisher never emits any envelope under `fixtures/invalid/` | Each, replayed through the publisher's own validator, is refused before it reaches the outbox |
| PP-5 | No field outside the signed set, no execution vocabulary, no number in a decimal field, microsecond instants | No `REJECTED_SCHEMA` on the publisher's output |
| PP-6 | The signer holds no broker credential and the process holds no key material in source, image or fixtures | Review evidence from the secrets standard (`OPS-SAFE-003`), not a fixture |
| PP-7 | Outbox: the entry is durable before the upstream event is acknowledged | Scenario `publisher_outbox_crash_restart`: after a crash and restart the entry is delivered exactly once |
| PP-8 | Delivery marks an entry DELIVERED only on the inbox's durable receipt | Scenarios `partial_publication_receipt_lost`, `inbox_down`: an entry with no receipt stays PENDING |
| PP-9 | Bounded retry and quarantine without head-of-line block | Scenario `poison_message_no_head_of_line_block` with the configured bound |
| PP-10 | FALCON sink down | Scenarios `falcon_sink_up` and `falcon_sink_down` give identical dispositions and submissions |
| PP-11 | Publisher heartbeat | Not testable here: D-8 is undecided |
