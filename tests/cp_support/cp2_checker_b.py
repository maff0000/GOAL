"""CP-2 door checker B: hand-written, standard library only, pure-Python Ed25519 verification.

Order of checks (PACKAGE.md section 6): shape of the schema marker, unsigned, schema, key trust,
signature, strategy pin, clock window, expiry. First failing check decides.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from . import cp2_canon as canon
from . import ed25519_ref
from .cp1_checker_b import _micros, MICRO_RE

TOK = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")
HEX64 = re.compile(r"^sha256:[0-9a-f]{64}$")
DEC = re.compile(r"^(0|[1-9][0-9]*)(\.[0-9]*[1-9])?$")
STATES = {"DORMANT", "FORMING", "MATCHED", "ACTIVE", "WEAKENING", "INVALID", "EXPIRED"}
REQUIRED = [
    "schema", "trigger_id", "strategy_id", "strategy_version", "strategy_fingerprint", "binding_id",
    "execution_policy_ref", "instrument_id", "timeframe", "signal_class", "output_direction", "state_from",
    "state_to", "setup_origin_bar_utc", "bar_close_utc", "valid_from_utc", "valid_until_utc", "evaluation_id",
    "input_snapshot_id", "input_snapshot_hash", "signing_key_id", "signature",
]
ALLOWED = set(REQUIRED) | {"reference_levels"}


def micros(text: Any) -> Optional[int]:
    if not isinstance(text, str):
        return None
    m = MICRO_RE.match(text)
    return _micros(m, 6) if m else None


def _schema_ok(e: dict) -> bool:
    if set(e) - ALLOWED or any(k not in e for k in REQUIRED):
        return False
    s = lambda k: isinstance(e[k], str)
    if not all(s(k) for k in REQUIRED):
        return False
    if e["schema"] != "goal.strategy-trigger/v1":
        return False
    if not re.match(r"^trg1_[0-9a-f]{64}$", e["trigger_id"]):
        return False
    if not re.match(r"^[a-z][a-z0-9_]{2,63}$", e["strategy_id"]):
        return False
    if not re.match(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$", e["strategy_version"]):
        return False
    for k in ("strategy_fingerprint", "input_snapshot_hash", "signing_key_id"):
        if not HEX64.match(e[k]):
            return False
    for k in ("binding_id", "execution_policy_ref", "evaluation_id", "input_snapshot_id"):
        if not TOK.match(e[k]):
            return False
    if not re.match(r"^[A-Z0-9]{2,10}(_[A-Z0-9]{2,10})?$", e["instrument_id"]):
        return False
    if e["timeframe"] not in ("M1", "M5", "M15", "H1", "H4", "D1"):
        return False
    if e["signal_class"] not in ("SETUP_ACTIVE", "SETUP_INVALIDATED"):
        return False
    if e["output_direction"] not in ("LONG", "SHORT", "NEUTRAL", "NONE"):
        return False
    if e["signal_class"] == "SETUP_ACTIVE" and e["output_direction"] not in ("LONG", "SHORT"):
        return False
    if e["state_from"] not in STATES or e["state_to"] not in STATES:
        return False
    if any(micros(e[k]) is None for k in ("setup_origin_bar_utc", "bar_close_utc", "valid_from_utc", "valid_until_utc")):
        return False
    if not re.match(r"^[0-9a-f]{128}$", e["signature"]):
        return False
    lv = e.get("reference_levels")
    if lv is not None:
        if not isinstance(lv, list) or len(lv) > 8:
            return False
        for item in lv:
            if not isinstance(item, dict) or set(item) != {"role", "value"}:
                return False
            if item["role"] not in ("INVALIDATION", "OBJECTIVE") or not isinstance(item["value"], str) or not DEC.match(item["value"]):
                return False
    # CP2-R04 identifier derivation, CP2-R05 valid_from equals bar_close
    if e["trigger_id"] != canon.trigger_id(e) or e["valid_from_utc"] != e["bar_close_utc"]:
        return False
    return True


def check_door(env: Any, ctx: dict) -> tuple[str, Optional[str]]:
    if not isinstance(env, dict) or env.get("schema") != "goal.strategy-trigger/v1":
        return "REJECT", "REJECTED_SCHEMA"
    if "signature" not in env or "signing_key_id" not in env:
        return "REJECT", "REJECTED_SIGNATURE"
    if not _schema_ok(env):
        return "REJECT", "REJECTED_SCHEMA"
    now = micros(ctx["now_utc"])
    key = ctx["trust_store"].get(env["signing_key_id"])
    if key is None or key["status"] == "REVOKED" or key["environment"] != ctx["environment"]:
        return "REJECT", "REJECTED_KEY"
    if not (micros(key["not_before"]) <= now < micros(key["not_after"])):
        return "REJECT", "REJECTED_KEY"
    if not ed25519_ref.verify(bytes.fromhex(env["signature"]), canon.signed_bytes(env), bytes.fromhex(key["public_key"])):
        return "REJECT", "REJECTED_SIGNATURE"
    if env["strategy_fingerprint"] not in ctx["pinned_fingerprints"]:
        return "REJECT", "REJECTED_STRATEGY"
    vf, vu = micros(env["valid_from_utc"]), micros(env["valid_until_utc"])
    skew = int(ctx["skew_tolerance_seconds"]) * 1_000_000
    maxw = int(ctx["max_window_seconds"]) * 1_000_000
    if vu <= vf or vf - now > skew or vu - vf > maxw:
        return "REJECT", "REJECTED_CLOCK"
    if now >= vu:
        return "REJECT", "EXPIRED"
    return "ACCEPT", None
