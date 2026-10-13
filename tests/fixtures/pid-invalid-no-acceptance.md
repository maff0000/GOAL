# NOACCEPT-001 — fixture PID missing only the acceptance-criteria section

Proves: the other end of the "four out of five" case. Identity holds, and
purpose, scope and approval evidence all have substantive content, so exactly
one reason fires — the missing acceptance criteria.

Paired with `pid-invalid-no-approval.md` on purpose: between them they show the
message names the requirement that is actually unmet rather than reporting a
generic failure, so a PO repairing a PID is told which section to write.

## Purpose

State why the work exists, in enough genuine words to clear the distinct-word
floor without padding.

## Scope

Describe what is and is not being built, again in real prose rather than a
repeated meaningless token.

## Approval

No real approval exists and none is claimed. This stands in for the
approval-evidence section, which the validator requires to be present and
non-trivial but deliberately never reads for meaning.
