# GOLD-AUD-F identity snapshots (before / after)

Status: DRAFT (replacement record), pending independent audit by ROGUE. Before = state at clone and branch creation (start of audit). After = state at end of audit, before the local evidence commits. Equal means no inspected checkout changed.

| Checkout | HEAD before | HEAD after | porcelain lines before | after |
|---|---|---|---|---|
| CER (audit clone) | 60eae45305a25f8b1ad03769e5bf4264b4d294e2 | 60eae45305a25f8b1ad03769e5bf4264b4d294e2 | 0 | 0 |
| HSA (audit clone) | 279ec181b5cd78df953671e087e01b7c1190ff96 | 279ec181b5cd78df953671e087e01b7c1190ff96 | 0 | 0 |
| DARWIN (audit clone) | bf1142b5be9f6988ec36b60ba3db9022c76a47af | bf1142b5be9f6988ec36b60ba3db9022c76a47af | 0 | 0 |
| HELIOS (audit clone) | 7f7193d55475e40583892b94dd461b1b64d6f1ef | 7f7193d55475e40583892b94dd461b1b64d6f1ef | 0 | 0 |
| tron (audit clone) | 5577039b5db05e70effef72c7e59df14db408419 | 5577039b5db05e70effef72c7e59df14db408419 | 0 | 0 |
| GOAL (audit clone; the one porcelain line is this audit own new evidence directory) | ceaf0291a43d029b1a47b1c192a62ff147f05ac0 | ceaf0291a43d029b1a47b1c192a62ff147f05ac0 | 0 | 1 |

Two non-public source checkouts were also unchanged before and after; their identities are held in the confidential record. No audited source was written to. Test runs used git-archive copies outside every clone; no container, service or database was touched.

Candidate package identity snapshot (audit-local file hashes, identical before and after):

    1b60e9721e18e33ab2aa02f7ceb824476a57583bfda92cb2196648411d8cf5c0  HSA/strategies/gold_context_breakout/1.0.0/package.json
    5ce9fdc275d10a5f1fdfb68d52ec30b27eca982c5100f178996f1c9cb89ea957  HSA/strategies/wick_rejection_sequence/0.1.0/package.json
