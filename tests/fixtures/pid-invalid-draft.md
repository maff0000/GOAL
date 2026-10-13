# DRAFT-001 — fixture PID that is still being written

Proves: minimum PID validity is state-scoped. This document is genuinely
incomplete — the four required sections are present and all four are empty, so
it is exactly as invalid as `pid-invalid-empty-sections.md` is — and the item
declaring it is in `PID_DRAFT`, which is not a PID-required state. It must
therefore yield **no finding at all**.

`PID_DRAFT` is the state in which the PO authors a PID. A rule that failed a
half-written draft there would make the state unusable and would have the
validator demanding the finished document before the state that exists to
produce it.

The non-vacuity half of this — that the same file *is* RED once the item
reaches a PID-required state — is proven in `tests/test_validate.py` by
copying this file and parametrising over both state sets, rather than by a
second committed fixture that would differ only in one field.

## Purpose

## Scope

## Acceptance

## Approval
