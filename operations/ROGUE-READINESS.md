# ROGUE Readiness

How ROGUE answers **"what work is ready next?"** from deterministic repository
state, without asking Matt.

Reader: ROGUE. Every answer below is computed from `backlog/backlog.yaml` and
nothing else. Nothing is inferred from prose, chat, issue bodies, or from this
document.

## The command

```bash
./tools/goal-ready
```

One line of JSON on stdout:

```json
{"ready":[{"id":"MT5-GW-001","target_repository":"maff0000/mt5-gateway"}]}
```

Each entry carries the item `id` and its declared `target_repository` — the
repository the work lands in. The `ready` list is sorted by `id` and the JSON
keys are sorted, so the same backlog always produces the same bytes. Diff the
output across runs and any change is a real change in programme state.

| exit | meaning | what ROGUE does |
|---|---|---|
| `0` | the backlog validated; the readiness answer is on stdout | act on it |
| `1` | the backlog is invalid; findings on stderr, **no answer produced** | do not dispatch — the backlog is repaired first |
| `2` | load or usage error (unreadable backlog, bad arguments) | do not dispatch — fix the invocation or the file |

## It validates before it answers

`./tools/goal-ready` runs the full validator first and **refuses to answer from
an invalid backlog**. When there are findings it prints them to stderr and
exits `1` without emitting a readiness list at all.

That refusal is the point. A readiness answer derived from malformed data looks
exactly like a correct one — a well-formed JSON list of ids — and is
indistinguishable downstream. If ROGUE dispatched FORGE on a list computed over
a duplicate id, a dangling dependency, a shorthand alias or a dependency cycle,
real engineering effort would be committed to a conclusion the data never
supported. So the command fails loudly instead of answering plausibly. There is
no flag to bypass the gate.

Exit `1` therefore means "the question was not answered", not "nothing is
ready". Treat it as a stop, never as an empty list.

## The readiness rule

An item is ready if and only if **both** of these hold:

1. `state == DELIVERY_READY`
2. every id in its `depends_on` resolves to a declared item whose state is an
   **accepted terminal state**

Accepted terminal states:

```text
MERGED  DEPLOYMENT_READY  PAPER  LIVE  CLOSED
```

- `CANCELLED` is terminal but **not** accepted. Cancelled work stopped
  permanently without ever delivering its outcome, so it must not unblock the
  work that needed that outcome.
- `BLOCKED` is not terminal at all — it is a live state awaiting resolution.
- `PO_ACCEPTANCE`, `MATT_DECISION` and `CANDIDATE` are in-flight gates, not
  acceptance. Work sitting in a gate may still be rejected.
- A dependency that does not resolve to a declared item makes the item **not
  ready**. Shorthand (`DCP-001`), aliases and wildcards (`OPS-SAFE-*`) do not
  resolve, and the validator rejects them before readiness is computed.

Those two conditions are the whole rule. No id is special-cased, no readiness
list is written down anywhere, and nothing is inferred from titles, markdown
tables or document text — only from the declared fields. The full state
vocabulary is in `governance/DELIVERY-STATE-MACHINE.md`.

## Planning projection — `--assume-closed`

```bash
./tools/goal-ready --assume-closed GOAL-DCP-001
./tools/goal-ready --assume-closed GOAL-DCP-001,MT5-GW-001
```

Treats the listed ids as `CLOSED` for the duration of that single answer and
recomputes readiness against the real backlog. It answers the planning question
**"what becomes dispatchable if these items close?"**

It is hypothetical and **mutates nothing** — not the backlog, not GitHub, not
delivery state, not the items named. It is a projection, not a transition.
Closing an item is a real state change made in `backlog/backlog.yaml`, never a
side effect of asking this question.

Takes one or more comma-separated canonical complete ids. An id that no item
declares is an error, not a silent no-op, so a typo cannot quietly produce a
confident wrong projection.

This is how ROGUE sees the next wave before committing to it. While an item has
not reached an accepted terminal state, everything depending on it is correctly
withheld from the ready list — that is the rule working, not a defect — and
`--assume-closed` on that item shows what unblocks when it lands. Always run
the command; never read a wave list out of a markdown file, including this one.

## `--with-pid`, and why ROGUE must check it

```bash
./tools/goal-ready --with-pid
```

Adds `pid_path` to each entry — the item's canonical PID, or `null` when it has
none.

**Readiness does not require a PID to exist.** `DELIVERY_READY` means
dependency-satisfied and mechanically dispatchable; authoring the canonical PID
is part of the dispatch that follows, not a precondition for appearing in the
list. Requiring one here would hide exactly the work that readiness exists to
surface.

The operationally important consequence: **a ready item whose `pid_path` is
`null` is not yet FORGE-dispatchable.** FORGE delivers against a canonical PID;
there is nothing for a PL to build to without one. For such an item ROGUE's
next action is to have the PO commission the canonical PID, not to start a
FORGE PL. ROGUE must check `pid_path` rather than assuming that ready means
immediately buildable.

Ready-with-PID and ready-without-PID are both valid answers. They route to
different places: one to FORGE, one back to the PO.

## Document linkage

Every dispatched item stays traceable along this chain:

```text
GOAL backlog
 ↕
GOAL issue
 ↕
canonical PID
 ↕
component PR
 ↕
implementation evidence
```

A readiness answer gives ROGUE the first link and names the target repository
for the fourth. The intermediate links are established by dispatch and
delivery. The chain is what makes programme state reconstructable from GitHub
alone: if it cannot be reconstructed from GitHub, it is not authoritative.

## What this is not

Per the non-goals of `pids/GOAL-DCP-001.md`:

- **Not automated dispatch.** `./tools/goal-ready` prints JSON and exits. It
  does not invoke FORGE, open an issue, assign work, or start a PL.
- **Not auto-merge.** Nothing here merges, releases or deploys anything.

ROGUE reads state and decides. Nothing launches itself.
