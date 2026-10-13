# Validator fixtures

Deliberately invalid backlog documents, one per validator finding code, plus
one valid document and one structurally unloadable document.

Each fixture isolates exactly the one failure mode it exists to prove: every
other field is sound, so a fixture produces only the code under test. That is
what makes `tests/test_validate.py` able to assert on the *complete* set of
codes a fixture yields rather than merely that the expected code is present.

Most fixtures put their items in a **pre-delivery** state
(`ARCHITECTURE_REQUIRED`), because `DELIVERY_READY` requires a canonical PID:
an item in that state with `pid_path: null` is `MISSING_PID`, which would be
an extra finding that is an artefact of the fixture rather than the failure
mode it exists to isolate. Do not "tidy" these back to `DELIVERY_READY`.

The fixtures where the state is **not** incidental, and must stay as it is:

- `missing-pid.yaml` — `DELIVERY_READY` and `FORGE_AUDIT` both require a PID;
  `PID_DRAFT` must not.
- `delivery-ready-pid-key-absent.yaml`, `delivery-ready-pid-wrong-type.yaml` —
  the structural precedence rule at the `DELIVERY_READY` boundary.
- `pid-file-not-found.yaml`, `pid-path-not-repo-relative.yaml`,
  `backlog-pid-mismatch.yaml` — the ways a `DELIVERY_READY` item's declared
  PID can still be broken.
- `valid.yaml` — a `MERGED` item and a `DELIVERY_READY` item that both declare
  an agreeing PID: the positive case at both ends of the PID-required range.
- `pid-invalid.yaml` — eight ways a declared PID file can exist, be readable
  and still not be a PID.
- `pid-valid-minimal.yaml` — the two negative controls for that rule: the
  smallest PID that passes, and an incomplete draft in a pre-delivery state
  that must not be failed.

## Fixture PID files

A fixture `pid_path` points at one of the markdown files here, and those files
are now constrained by **minimum PID validity** (`backlog/SCHEMA.md`). From
`DELIVERY_READY` onwards a declared PID must also *be* a PID: its first ATX
heading must name the declaring item's `id` as a whole token, and it must carry
purpose, scope, acceptance-criteria and approval-evidence sections with
non-trivial bodies. Two consequences for anyone adding a fixture:

1. **A fixture PID cannot be shared by items with different ids.** Identity is
   per-item, so `fixtures/pid-fixture.md` (headed `PIDFIX-001`) serves only
   items declaring `PIDFIX-001`. `valid.yaml`'s `ALPHA-001` has
   `pid-fixture-alpha.md`, and the readiness fixtures' `TARGET-001` and
   `DEP-001` have `fixtures_readiness/pid-target.md` and
   `fixtures_readiness/pid-dep.md`, for exactly that reason. An
   `architecture_refs` entry is *not* an identity claim and may still name any
   file that exists.
2. **One fixture, one finding code still holds.** A fixture PID declared by an
   item in a PID-required state must carry identity and the four sections, or
   the fixture starts yielding an incidental `PID_INVALID` on top of the code
   it exists to prove — which is precisely what
   `backlog-pid-mismatch.yaml` must not do. The five pre-existing fixture PIDs
   were extended with those sections rather than replaced, because
   `tests/test_validate.py` and `valid.yaml` depend on their label sets and
   first headings.

A fixture PID in a **pre-delivery** state is deliberately unconstrained:
`tests/fixtures_readiness/state_not_delivery_ready.yaml` still points its
`ARCHITECTURE_REQUIRED` item at `pid-fixture.md`, and `pid-invalid-draft.md` is
a genuinely incomplete draft that must yield nothing. Those are live proofs
that the rule is state-scoped; do not "tidy" either of them.

`pid-invalid-empty.md` (zero bytes) and `pid-invalid-whitespace.md`
(whitespace only) are the two fixtures that **cannot** carry a header comment
explaining themselves — having no content is the case they prove. What they are
for is recorded in `pid-invalid.yaml`'s header comment and here, and nowhere
else.

`repo_root` is a loaded backlog's `path.parent.parent`, so for a fixture at
`tests/fixtures/<name>.yaml` the root is `tests/`. Fixture `pid_path` and
`architecture_refs` values are therefore relative to `tests/` — for example
`fixtures/pid-fixture.md`. Nothing here resolves against the real repository
root, and nothing here reaches the canonical backlog.
