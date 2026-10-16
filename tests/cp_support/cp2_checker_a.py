"""CP-2 door checker A: jsonschema for the envelope, `cryptography` for Ed25519, datetime arithmetic.

Skipped by the tests when `cryptography` or `jsonschema` is not installed; checker B always runs.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import jsonschema
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from . import cp2_canon as canon
from .cp_common import CP2_DIR, plain

SCHEMA = json.loads((CP2_DIR / "schema" / "trigger.envelope.schema.json").read_text(encoding="utf-8"))
_V = jsonschema.Draft202012Validator(SCHEMA)


def _dt(text: str) -> datetime:
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{6})Z$", text)
    y, mo, d, h, mi, s, f = (int(x) for x in m.groups())
    return datetime(y, mo, d, h, mi, s, f, tzinfo=timezone.utc)


def check_door(env: Any, ctx: dict) -> tuple[str, Optional[str]]:
    if not isinstance(env, dict) or env.get("schema") != "goal.strategy-trigger/v1":
        return "REJECT", "REJECTED_SCHEMA"
    if "signature" not in env or "signing_key_id" not in env:
        return "REJECT", "REJECTED_SIGNATURE"
    if any(_V.iter_errors(plain(env))):
        return "REJECT", "REJECTED_SCHEMA"
    if env["trigger_id"] != canon.trigger_id(env):
        return "REJECT", "REJECTED_SCHEMA"
    if env["valid_from_utc"] != env["bar_close_utc"]:
        return "REJECT", "REJECTED_SCHEMA"
    now = _dt(ctx["now_utc"])
    key = ctx["trust_store"].get(env["signing_key_id"])
    if key is None or key["status"] == "REVOKED" or key["environment"] != ctx["environment"] \
            or not (_dt(key["not_before"]) <= now < _dt(key["not_after"])):
        return "REJECT", "REJECTED_KEY"
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(key["public_key"])).verify(
            bytes.fromhex(env["signature"]), canon.signed_bytes(env))
    except InvalidSignature:
        return "REJECT", "REJECTED_SIGNATURE"
    if env["strategy_fingerprint"] not in ctx["pinned_fingerprints"]:
        return "REJECT", "REJECTED_STRATEGY"
    vf, vu = _dt(env["valid_from_utc"]), _dt(env["valid_until_utc"])
    if vu <= vf or vf - now > timedelta(seconds=int(ctx["skew_tolerance_seconds"])) \
            or vu - vf > timedelta(seconds=int(ctx["max_window_seconds"])):
        return "REJECT", "REJECTED_CLOCK"
    if now >= vu:
        return "REJECT", "EXPIRED"
    return "ACCEPT", None
