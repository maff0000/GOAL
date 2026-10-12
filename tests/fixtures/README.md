# Validator fixtures

Deliberately invalid backlog documents, one per validator finding code, plus
one valid document and one structurally unloadable document.

Each fixture isolates exactly the one failure mode it exists to prove: every
other field is sound, so a fixture produces only the code under test. That is
what makes `tests/test_validate.py` able to assert on the *complete* set of
codes a fixture yields rather than merely that the expected code is present.

`repo_root` is a loaded backlog's `path.parent.parent`, so for a fixture at
`tests/fixtures/<name>.yaml` the root is `tests/`. Fixture `pid_path` and
`architecture_refs` values are therefore relative to `tests/` — for example
`fixtures/pid-fixture.md`. Nothing here resolves against the real repository
root, and nothing here reaches the canonical backlog.
