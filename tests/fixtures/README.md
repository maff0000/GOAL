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

`repo_root` is a loaded backlog's `path.parent.parent`, so for a fixture at
`tests/fixtures/<name>.yaml` the root is `tests/`. Fixture `pid_path` and
`architecture_refs` values are therefore relative to `tests/` — for example
`fixtures/pid-fixture.md`. Nothing here resolves against the real repository
root, and nothing here reaches the canonical backlog.
