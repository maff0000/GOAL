# IDENTITY-0011 — fixture PID for a different backlog id

Proves: a complete, substantive PID still fails when it is not *this item's*
PID. Every one of the four required sections below has real content, so the
only unmet requirement is identity — and it is unmet for the adversarial
reason, not the obvious one.

The heading names `IDENTITY-0011`. The item declaring this file is
`IDENTITY-001`, and `IDENTITY-001` does occur inside `IDENTITY-0011` as a
substring. It is not a whole token there: the occurrence is immediately
followed by `1`. A validator that searched for the id as a substring would
accept this document as `IDENTITY-001`'s PID, which is exactly the bypass the
whole-token rule exists to refuse.

## Purpose

State why some other work exists, in enough words to clear the distinct-word
floor comfortably.

## Scope

Describe the boundary of that other work, again in genuine prose rather than
padding or a single repeated token.

## Acceptance

List what GREEN would mean for that other work, with enough distinct words to
count as substantive content.

## Approval

No real approval exists and none is claimed. This stands in for the
approval-evidence section, which the validator requires to be present and
non-trivial but deliberately never reads for meaning.
