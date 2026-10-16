"""Reference model of publisher outbox -> inbox -> claim -> disposition (tests only).

In-memory, deterministic, no I/O. It exercises the failure and recovery rules of PACKAGE.md
section 7 and nothing else: it is not an inbox, an outbox or a signer for any runtime. Door
verification is delegated to checker B. Items the PROPOSED contract leaves open are marked
ASSUMPTION in PACKAGE.md and are the only behaviours chosen here.
"""

from __future__ import annotations

import copy
from typing import Any, Optional

from . import cp2_canon as canon
from . import cp2_checker_b as door

POST_AUTH_OUTCOMES = {"EXPIRED", "REJECTED_STRATEGY", "REJECTED_CLOCK"}


class Broker:
    """Idempotent by client reference: a second submit with the same reference places no new order."""

    def __init__(self) -> None:
        self.orders: dict[str, int] = {}

    def submit(self, client_ref: str) -> None:
        self.orders.setdefault(client_ref, 1)

    @property
    def submissions(self) -> int:
        return sum(self.orders.values())


class Inbox:
    def __init__(self, ctx: dict, broker: Broker, falcon_up: bool = True) -> None:
        self.ctx = ctx
        self.broker = broker
        self.falcon_up = falcon_up
        self.rows: dict[str, dict] = {}
        self.rejections: list[dict] = []
        self.invalidated: set = set()
        self.events: list[str] = []
        self.spool: list[dict] = []
        self.up = True
        self._next_receipt = 1

    # -- evidence (asynchronous, best effort, never on the decision path)
    def _emit(self, name: str, trigger_id: str) -> None:
        if self.falcon_up:
            self.spool.append({"event": name, "trigger_id": trigger_id})

    def receive(self, env: Any, now_utc: str, lose_receipt: bool = False) -> dict:
        if not self.up:
            return {"status": "UNAVAILABLE"}
        ctx = dict(self.ctx, now_utc=now_utc)
        verdict, code = door.check_door(env, ctx)
        if verdict == "REJECT" and code not in POST_AUTH_OUTCOMES:
            self.rejections.append({"digest": canon.digest(env if isinstance(env, dict) else {}), "code": code})
            return {"status": "REJECTED", "code": code}
        tid, dg = env["trigger_id"], canon.content_digest(env)
        row = self.rows.get(tid)
        if row is not None:
            if row["digest"] == dg:
                self.events.append("DUPLICATE_DELIVERY")
                return {"status": "RECEIPT", "receipt": row["receipt"], "duplicate": True}
            self.rejections.append({"digest": dg, "code": "CONFLICT", "trigger_id": tid})
            self.events.append("CONFLICT")
            return {"status": "REJECTED", "code": "CONFLICT"}
        row = {"digest": dg, "state": "RECEIVED", "outcome": None, "receipt": f"rcpt-{self._next_receipt}",
               "setup": canon.setup_key(env), "signal_class": env["signal_class"], "env": copy.deepcopy(env)}
        self._next_receipt += 1
        self.rows[tid] = row
        if verdict == "REJECT":
            row["state"], row["outcome"] = "TERMINAL", code
        elif env["signal_class"] == "SETUP_ACTIVE" and row["setup"] in self.invalidated:
            row["state"], row["outcome"] = "TERMINAL", "SUPERSEDED"
        elif env["signal_class"] == "SETUP_INVALIDATED":
            self.invalidated.add(row["setup"])
            for other in self.rows.values():
                if other is not row and other["setup"] == row["setup"] and other["signal_class"] == "SETUP_ACTIVE" \
                        and other["state"] == "RECEIVED":
                    other["state"], other["outcome"] = "TERMINAL", "SUPERSEDED"
        self._emit("trigger_received", tid)
        if lose_receipt:
            return {"status": "UNAVAILABLE"}
        return {"status": "RECEIPT", "receipt": row["receipt"], "duplicate": False}

    def claim(self, tid: str, now_utc: str) -> str:
        row = self.rows[tid]
        if row["state"] != "RECEIVED":
            return row["state"]
        if row["signal_class"] == "SETUP_INVALIDATED":
            return "RECEIVED"
        if door.micros(now_utc) >= door.micros(row["env"]["valid_until_utc"]):
            row["state"], row["outcome"] = "TERMINAL", "EXPIRED"
            return "TERMINAL"
        row["state"] = "CLAIMED"
        return "CLAIMED"

    def core_submit(self, tid: str) -> None:
        """TRON core submits to the broker with client reference = trigger_id (journal first, then submit)."""
        row = self.rows[tid]
        assert row["state"] == "CLAIMED", "only a claimed row may be submitted"
        self.broker.submit(tid)

    def core_result(self, tid: str, outcome: str) -> None:
        row = self.rows[tid]
        assert row["state"] in ("CLAIMED", "RECONCILE") and outcome in {"EXECUTED", "REFUSED", "EXECUTION_REJECTED"}
        row["state"], row["outcome"] = "TERMINAL", outcome
        self._emit("trigger_disposed", tid)

    def crash_and_restart(self) -> None:
        """Durable table survives; every CLAIMED lease is treated as expired and goes to RECONCILE."""
        for row in self.rows.values():
            if row["state"] == "CLAIMED":
                row["state"] = "RECONCILE"

    def reconcile(self, tid: str, truth: str, now_utc: str) -> str:
        row = self.rows[tid]
        assert row["state"] == "RECONCILE"
        if truth == "ORDER_PRESENT":
            row["state"], row["outcome"] = "TERMINAL", "EXECUTED"
        elif truth == "ORDER_ABSENT_CONFIRMED":
            self.broker.submit(tid)  # first attempt provably never reached the broker
            row["state"], row["outcome"] = "TERMINAL", "EXECUTED"
        elif truth == "UNCERTAIN":
            if door.micros(now_utc) >= door.micros(row["env"]["valid_until_utc"]):
                row["state"], row["outcome"] = "TERMINAL", "ABANDONED_UNRESOLVED"
        return row["state"]

    def dispositions(self) -> dict:
        return {tid: (r["outcome"] if r["state"] == "TERMINAL" else r["state"]) for tid, r in sorted(self.rows.items())}


class Publisher:
    def __init__(self, max_attempts: int) -> None:
        self.max_attempts = max_attempts
        self.outbox: list[dict] = []  # durable
        self.alerts: list[str] = []

    def publish(self, env: dict) -> None:
        tid, dg = env["trigger_id"], canon.content_digest(env)
        for e in self.outbox:
            if e["trigger_id"] == tid:
                if e["digest"] != dg:
                    self.alerts.append("LOCAL_CONFLICT")
                return
        self.outbox.append({"trigger_id": tid, "digest": dg, "envelope": copy.deepcopy(env), "state": "PENDING", "attempts": 0})

    def restart(self) -> None:
        """Process restart: the outbox is durable, nothing else is carried."""

    def pump(self, inbox: Inbox, now_utc: str, lose_receipt: bool = False) -> None:
        for e in self.outbox:
            if e["state"] != "PENDING":
                continue
            resp = inbox.receive(e["envelope"], now_utc, lose_receipt)
            if resp["status"] == "RECEIPT":
                e["state"] = "DELIVERED"
            elif resp["status"] == "REJECTED":
                e["attempts"] += 1
                if e["attempts"] >= self.max_attempts:
                    e["state"] = "QUARANTINED"
                    self.alerts.append("QUARANTINED:" + resp["code"])
            # UNAVAILABLE: entry stays PENDING, no attempt is charged, the next entry is still tried (no head-of-line block)

    def states(self) -> dict:
        return {e["trigger_id"]: e["state"] for e in self.outbox}


def run(scn: dict, env_by_name: dict) -> list[dict]:
    ctx = scn["context"]
    broker = Broker()
    inbox = Inbox(ctx, broker, falcon_up=scn.get("falcon_up", True))
    pub = Publisher(int(scn.get("max_attempts", 3)))
    tid = lambda n: env_by_name[n]["trigger_id"]
    results = []
    for step in scn["steps"]:
        op = step["op"]
        out: dict = {"op": op}
        if op == "publish":
            pub.publish(env_by_name[step["env"]])
        elif op == "pump":
            inbox.up = step.get("inbox_up", True)
            pub.pump(inbox, step["now_utc"], step.get("lose_receipt", False))
            inbox.up = True
        elif op == "deliver_raw":
            out["response"] = inbox.receive(env_by_name[step["env"]], step["now_utc"])
        elif op == "claim":
            out["state"] = inbox.claim(tid(step["env"]), step["now_utc"])
        elif op == "submit":
            inbox.core_submit(tid(step["env"]))
        elif op == "core_result":
            inbox.core_result(tid(step["env"]), step["outcome"])
        elif op == "inbox_crash":
            inbox.crash_and_restart()
        elif op == "publisher_restart":
            pub.restart()
        elif op == "reconcile":
            out["state"] = inbox.reconcile(tid(step["env"]), step["truth"], step["now_utc"])
        elif op == "snapshot":
            out["dispositions"] = {env_name: inbox.dispositions().get(tid(env_name)) for env_name in step.get("names", [])} \
                if step.get("names") else inbox.dispositions()
            out["outbox"] = {n: pub.states().get(tid(n)) for n in step.get("outbox_names", [])}
            out["submissions"] = broker.submissions
            out["rows"] = len(inbox.rows)
            out["rejections"] = [r["code"] for r in inbox.rejections]
            out["events"] = list(inbox.events)
            out["alerts"] = list(pub.alerts)
            out["outbox_len"] = len(pub.outbox)
        else:
            raise ValueError(op)
        results.append(out)
    return results


def check_scenario(scn: dict) -> list[str]:
    """Run a scenario and return a list of mismatch descriptions (empty means it reproduces)."""
    from .cp_common import unnum
    scn = unnum(scn)
    results = run(scn, scn["envelopes"])
    problems = []
    for i, (step, res) in enumerate(zip(scn["steps"], results)):
        if "expect_status" in step and res["response"]["status"] != step["expect_status"]:
            problems.append(f"step {i}: status {res['response']['status']} != {step['expect_status']}")
        if "expect_duplicate" in step and res["response"].get("duplicate", False) != step["expect_duplicate"]:
            problems.append(f"step {i}: duplicate flag")
        if "expect_code" in step and res["response"].get("code") != step["expect_code"]:
            problems.append(f"step {i}: code {res['response'].get('code')} != {step['expect_code']}")
        if "expect_state" in step and res.get("state") != step["expect_state"]:
            problems.append(f"step {i}: state {res.get('state')} != {step['expect_state']}")
        for key, want in step.get("expect", {}).items():
            got = res.get(key)
            if got != want:
                problems.append(f"step {i}: {key} {got!r} != {want!r}")
    return problems
