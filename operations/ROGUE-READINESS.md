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

One line of JSON on stdout, in the shape `pids/GOAL-DCP-001.md` publishes:

```json
{"ready":[{"id":"EXAMPLE-ID-001","target_repository":"owner/name"}]}
```

That example illustrates the **shape** of the answer and nothing else. It names
no declared backlog item on purpose: `EXAMPLE-ID-001` and `owner/name` are
deliberately not the id or the target repository of anything in
`backlog/backlog.yaml`, so the example cannot be read as a dispatch
authorisation for any real work. Which ids are actually in the answer is
whatever the rule below computes from the backlog at the moment you run it —
including, legitimately, none. Never assume a particular id appears, and never
take an id from this document.

Each entry carries the item `id` and its declared `target_repository` — the
repository the work lands in. The `ready` list is sorted by `id` and the JSON
keys are sorted, so the same backlog always produces the same bytes. Diff the
output across runs and any change is a real change in programme state.

| invocation | answer |
|---|---|
| `./tools/goal-ready` | `{"ready":[...]}` — work a FORGE PL could be dispatched on now |
| `./tools/goal-ready --assume-closed ID[,ID...]` | the same answer under a what-if projection; mutates nothing |
| `./tools/goal-ready --with-pid` | adds `pid_path` to each entry, in either mode |
| `./tools/goal-ready --pid-wave` | `{"pid_authoring_wave":[...]}` — items awaiting **PO PID authoring**, which is *not* FORGE-dispatchable work |

| exit | meaning | what ROGUE does |
|---|---|---|
| `0` | the backlog validated; the answer is on stdout | act on it |
| `1` | the backlog is invalid; findings on stderr, **no answer produced** | do not dispatch — the backlog is repaired first |
| `2` | load or usage error (unreadable backlog, bad arguments) | do not dispatch — fix the invocation or the file |

## It validates before it answers

`./tools/goal-ready` runs the full validator first and **refuses to answer from
an invalid backlog**. When there are findings it prints them to stderr and
exits `1` without emitting any list at all.

That refusal is the point. An answer derived from malformed data looks exactly
like a correct one — a well-formed JSON list of ids — and is indistinguishable
downstream. If ROGUE dispatched FORGE on a list computed over a duplicate id, a
dangling dependency, a shorthand alias, a dependency cycle or a PID that does
not exist, real engineering effort would be committed to a conclusion the data
never supported. So the command fails loudly instead of answering plausibly.
There is no flag to bypass the gate.

Exit `1` therefore means "the question was not answered", not "nothing is
ready". Treat it as a stop, never as an empty list.

This gate is also what makes the readiness answer trustworthy about PIDs. The
validator reports `MISSING_PID`, `PID_FILE_NOT_FOUND`, `PID_INVALID` and
`BACKLOG_PID_MISMATCH`, so a *successful* readiness answer can never contain an
item whose canonical PID is missing, unreadable, not actually a PID, or
inconsistent with the backlog: either the data is coherent and the answer is
emitted, or the command refuses and names the defect.

### It also refuses when a required PID exists but is not a PID

This is new, and it changes what exit `1` can mean for ROGUE. `PID_INVALID`
fires when an item in `DELIVERY_READY` or later declares a PID file that
exists and reads fine but does not meet **minimum PID validity**: its first
heading does not name the item, or it has no purpose, scope,
acceptance-criteria or approval-evidence section with substantive content.
`backlog/SCHEMA.md` holds the exact rule; `governance/DELIVERY-STATE-MACHINE.md`
is the authority for which states it applies in.

ROGUE's handling does not change: exit `1` is a stop, the findings name the
defect, and the next action belongs to the PO — authoring the PID properly, not
patching the file until the validator goes quiet. What changes is that one more
class of unbuildable work is now caught *before* a FORGE PL is dispatched
against it, rather than discovered by the PL on arrival.

Note what the check does **not** claim. It is structural: it establishes that
the five things are present and not content-free, and says nothing about
whether they are any good. A PID can satisfy it and still be a bad PID — that
judgement is the item's PO gate, and ROGUE should not read a GREEN validator
as the PO having blessed the content.

## The readiness rule

An item is ready if and only if **all three** of these hold:

1. its own state is `DELIVERY_READY`;
2. every id in its `depends_on` resolves to a declared item whose state is an
   **accepted terminal state**;
3. it declares a canonical PID.

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

Those three conditions are the whole rule. No id is special-cased, no readiness
list is written down anywhere, and nothing is inferred from titles, markdown
tables or document text — only from the declared fields. The full state
vocabulary, the canonical sequence and the PID rule are in
`governance/DELIVERY-STATE-MACHINE.md`.

### No PID means the item is not ready — and not `DELIVERY_READY` either

Clause 3 is not an extra filter bolted onto the state machine; it is the state
machine. `DELIVERY_READY` and every later delivery state **require** a
canonical PID, so an item with no PID stays in a **pre-delivery** state —
`PID_DRAFT` or earlier — and cannot reach `DELIVERY_READY` at all.
`governance/DELIVERY-STATE-MACHINE.md` lists both sets in full. What permits
that transition is an approved canonical
PID — one that exists, agrees with the backlog, and has passed the item's PO
gate. Only then may `./tools/goal-ready` surface it.

Put plainly: **no PID = not `DELIVERY_READY`.** A ready item's `pid_path` is
never `null`.

The reason this matters to ROGUE specifically: FORGE delivers against a
canonical PID. Without one there is no statement of scope, no non-goals and no
definition of acceptance, so there is nothing for a PL to build to. An answer
that listed such work as ready would be promising a dispatch that cannot
happen, and would quietly move the job of noticing that onto whoever acted on
it. The canonical sequence — *architecture before PID, PID before build* — is
what keeps the readiness answer honest: by the time something is ready, the
authoritative statement of what "done" means already exists.

Items without PIDs are not invisible. They are the subject of `--pid-wave`
below, and their next action belongs to the PO, not to FORGE.

## Planning projection — `--assume-closed`

```bash
./tools/goal-ready --assume-closed GOAL-DCP-001
./tools/goal-ready --assume-closed GOAL-DCP-001,MT5-GW-001
```

Treats the listed ids as `CLOSED` for the duration of that single answer and
recomputes against the real backlog. It answers the planning question **"what
becomes available if these items close?"**

It is hypothetical and **mutates nothing** — not the backlog, not GitHub, not
delivery state, not the items named. It is a projection, not a transition.
Closing an item is a real state change made in `backlog/backlog.yaml`, never a
side effect of asking this question.

Takes one or more comma-separated canonical complete ids. An id that no item
declares is an error, not a silent no-op, so a typo cannot quietly produce a
confident wrong projection.

This is how ROGUE sees the next wave before committing to it. While an item has
not reached an accepted terminal state, everything depending on it is correctly
withheld — that is the rule working, not a defect — and `--assume-closed` on
that item shows what unblocks when it lands. The flag composes with the others:
with `--pid-wave` it projects which items would enter the PID-authoring wave,
rather than which would become dispatchable. Always run the command; never read
a wave list out of a markdown file, including this one.

## `--with-pid`

```bash
./tools/goal-ready --with-pid
./tools/goal-ready --pid-wave --with-pid
```

Adds `pid_path` to each entry. The flag is uniform: it applies in either mode,
to `ready` entries and to `pid_authoring_wave` entries alike.

In a `ready` entry, `pid_path` is **never `null`**, because a ready item always
declares a canonical PID. The flag is therefore not a check ROGUE performs
before trusting the answer; it is a convenience, so the dispatch brief can name
the PID without a second lookup into the backlog. If a `ready` entry ever did
carry `pid_path: null`, that would be a defect in the tooling, not a routing
decision for ROGUE to make.

In a `pid_authoring_wave` entry — the wave described below — `pid_path` will in
practice be `null`, and there that is **correct and expected**: these items
have no authored canonical PID yet, which is the whole reason they are in the
list rather than in `ready`.

That contrast is worth reading twice, because it is exactly the distinction
this document exists to draw:

| mode | `pid_path: null` means |
|---|---|
| `ready` | impossible — a tooling defect if it ever appears |
| `pid_authoring_wave` | expected — it is why the item is in the list |

So a `null` is not a signal ROGUE interprets case by case. Which key the entry
arrived under has already decided what it means, and already decided where the
item routes.

## The PID-authoring wave — `--pid-wave`

```bash
./tools/goal-ready --pid-wave
./tools/goal-ready --pid-wave --assume-closed GOAL-DCP-001
```

```json
{"pid_authoring_wave":[...]}
```

The rule: an item is in the wave when its own state is `PID_DRAFT` and every
dependency has reached an accepted terminal state. It is the deterministic
answer to a different question from readiness — **"which items are the next
PO/PID-authoring wave?"** — and like readiness it is computed from the backlog
every time. The wave is never a written-down list, here or anywhere else.

**This is not a dispatch authorisation.** Nothing in
`{"pid_authoring_wave":[...]}` is FORGE-dispatchable: these items have no
approved canonical PID, which is precisely why they are in the wave. The output
is **advisory input to the PO** — it says "these items are unblocked and need
canonical PIDs commissioned next", and that is the whole of its authority.
ROGUE routes it to the PO and dispatches nothing on it.

Two further consequences worth being explicit about:

- ROGUE must **always run the command** and must never read a wave out of a
  markdown file, including this one. A wave copied into prose is a snapshot
  that goes stale and then lies with confidence.
- An item leaves the wave by having a canonical PID authored and passed through
  PO review, which is what moves it to `DELIVERY_READY`. It then appears in the
  `ready` answer on its own, with no further bookkeeping. No placeholder or
  shim PID is ever created to shortcut that.

  That last sentence used to be a claim about discipline, and it used to come
  with an admission: a stub PID *would* satisfy the validator while delivering
  none of the authority a PID exists to carry. **Minimum PID validity is what
  makes it mechanically true instead.** A `touch`ed file, a copied template
  with empty sections, or a shim carrying the right bold labels and nothing
  else is now a `PID_INVALID` finding, and `./tools/goal-ready` refuses to
  answer at all rather than reporting the item as ready. The shortcut is
  closed by the tooling, not merely deprecated by this document.

  It is closed, not sealed: the check is structural, so a determined author
  could still write six distinct words under each required heading. What that
  buys them is a document a PO can read and reject — which is the right place
  for that judgement, and a strictly better failure than silent dispatch
  against an empty file.

## Two answers, two destinations

The two lists must never be confused, so they are deliberately different keys
with different meanings:

| key | what it means | where ROGUE routes it |
|---|---|---|
| `ready` | dependency-satisfied, `DELIVERY_READY`, canonical PID exists | ROGUE may dispatch a FORGE PL |
| `pid_authoring_wave` | dependency-satisfied, `PID_DRAFT`, PID not yet authored and through PO review | ROGUE routes to the PO to commission a canonical PID |

An item appears in exactly one of them, because the states are mutually
exclusive. `ready` is work; `pid_authoring_wave` is work *about to be
specified*. Treating the second as the first is how FORGE gets dispatched with
nothing to build to — the specific failure these two keys exist to prevent.

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

A readiness answer gives ROGUE the first link, names the target repository for
the fourth, and — because readiness requires a PID — guarantees the third
already exists. The remaining links are established by dispatch and delivery.
The chain is what makes programme state reconstructable from GitHub alone: if
it cannot be reconstructed from GitHub, it is not authoritative.

## What this is not

Per the non-goals of `pids/GOAL-DCP-001.md`:

- **Not automated dispatch.** `./tools/goal-ready` prints JSON and exits. It
  does not invoke FORGE, open an issue, assign work, or start a PL.
- **Not a daemon, and not a second tool.** Both answers come from this one
  command, run on demand. Nothing polls, schedules or runs in the background.
- **Not auto-merge.** Nothing here merges, releases or deploys anything.
- **Not a PID author.** `--pid-wave` reports which PIDs are needed. Writing
  them is the PO's work, and no placeholder stands in for one.

ROGUE reads state and decides. Nothing launches itself.
