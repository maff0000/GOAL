"""CP-2 (HELIOS trigger -> outbox -> TRON inbox) offline conformance: GOLD-AUD-C acceptance A-1 to A-4.

The reference models are test-only. No key material is committed: fixtures hold public keys and
signatures; the pure-Python verifier is checked against the RFC 8032 public test vectors.
"""

import re

import pytest

from cp_support import cp2_canon as C
from cp_support import cp2_checker_b as B
from cp_support import cp2_reference_model as M
from cp_support import ed25519_ref
from cp_support.cp_common import CP2_DIR, fixture_files, load_json, plain, unnum

FIXTURES = CP2_DIR / "fixtures"
DOORS = [p for p in fixture_files(FIXTURES) if "scenarios" not in p.parts and p.name != "KEYS-PUBLIC.json"]
SCENARIOS = sorted((FIXTURES / "scenarios").glob("*.json"))
PACKAGE = (CP2_DIR / "PACKAGE.md").read_text(encoding="utf-8")
OUTCOMES = set(re.findall(r"^\| (REJECTED_[A-Z]+|EXPIRED|CONFLICT|SUPERSEDED|DUPLICATE_DELIVERY|ABANDONED_UNRESOLVED|EXECUTED|REFUSED|EXECUTION_REJECTED) \|", PACKAGE, flags=re.M))
#: outcomes decided by the TRON core after a claim, not by the receiving door (CP-2 only exercises the ones the inbox model needs)
CORE_OWNED_NOT_EXERCISED = {"EXECUTION_REJECTED"}


RFC8032_VECTORS = [  # RFC 8032 section 7.1, TEST 1, TEST 2, TEST 3 (public values only)
    ("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a", "",
     "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"),
    ("3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c", "72",
     "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"),
    ("fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025", "af82",
     "6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a"),
]


@pytest.mark.parametrize("pk,msg,sig", RFC8032_VECTORS, ids=["rfc8032-test1", "rfc8032-test2", "rfc8032-test3"])
def test_ed25519_verifier_accepts_rfc8032_vectors_and_rejects_one_bit_changes(pk, msg, sig):
    pk, msg, sig = bytes.fromhex(pk), bytes.fromhex(msg), bytes.fromhex(sig)
    assert ed25519_ref.verify(sig, msg, pk)
    assert not ed25519_ref.verify(sig, msg + b"x", pk)
    assert not ed25519_ref.verify(sig[:-1] + bytes([sig[-1] ^ 1]), msg, pk)
    assert not ed25519_ref.verify(sig, msg, bytes([pk[0] ^ 1]) + pk[1:])


@pytest.mark.parametrize("path", DOORS, ids=lambda p: p.name)
def test_checker_b_reproduces_the_declared_outcome(path):
    case = load_json(path)
    verdict, code = B.check_door(plain(case["envelope"]), unnum(case["context"]))
    assert (None if verdict == "ACCEPT" else code) == case["expected_outcome"], path.name
    assert path.name.startswith(("VALID__" if case["kind"] == "valid" else case["expected_outcome"] + "__"))


def test_trigger_id_is_the_deterministic_hash_of_the_occurrence_key_for_every_envelope():
    seen = set()
    for path in DOORS:
        env = plain(load_json(path)["envelope"])
        if isinstance(env, dict) and "trigger_id" in env and path.name.startswith("VALID__"):
            assert env["trigger_id"] == C.trigger_id(env), path.name
            seen.add(env["trigger_id"])
    assert len(seen) >= 3


def test_occurrence_key_excludes_snapshot_so_a_replay_regenerates_the_same_id():
    a = plain(load_json(FIXTURES / "valid" / "VALID__active_long.json")["envelope"])
    other = dict(a, input_snapshot_id="snap_other", evaluation_id="eval_other", input_snapshot_hash="sha256:" + "1" * 64)
    assert C.trigger_id(other) == a["trigger_id"]
    assert C.content_digest(other) != C.content_digest(a)


def test_every_declared_outcome_has_a_fixture_or_scenario_except_core_owned_ones():
    covered = set()
    for p in DOORS:
        out = load_json(p)["expected_outcome"]
        if out:
            covered.add(out)
    for p in SCENARIOS:
        scn = unnum(load_json(p))
        for step, res in zip(scn["steps"], M.run(scn, scn["envelopes"])):
            exp = step.get("expect", {})
            covered |= {v for v in exp.get("dispositions", {}).values() if v}
            covered |= set(exp.get("rejections", [])) | set(exp.get("events", []))
            if step.get("expect_code"):
                covered.add(step["expect_code"])
    assert OUTCOMES - covered - CORE_OWNED_NOT_EXERCISED == set(), sorted(OUTCOMES - covered)


@pytest.mark.parametrize("path", SCENARIOS, ids=lambda p: p.stem)
def test_scenarios_reproduce_their_expected_outcome_tables(path):
    assert M.check_scenario(load_json(path)) == []


def test_a_wrong_expectation_is_detected_by_the_scenario_checker():
    scn = load_json(FIXTURES / "scenarios" / "duplicate_delivery.json")
    scn["steps"][0]["expect_status"] = "REJECTED"
    assert M.check_scenario(scn) != []


def test_falcon_sink_down_gives_logically_equivalent_dispositions():
    up, down = (unnum(load_json(CP2_DIR / "fixtures" / "scenarios" / f"falcon_sink_{x}.json")) for x in ("up", "down"))
    run_up, run_down = M.run(up, up["envelopes"]), M.run(down, down["envelopes"])
    pick = lambda res: [(r["dispositions"], r["submissions"], r["rows"]) for r in res if "dispositions" in r]
    assert pick(run_up) == pick(run_down) != []


def test_no_double_execution_across_crash_redelivery_and_reclaim():
    scn = unnum(load_json(CP2_DIR / "fixtures" / "scenarios" / "crash_after_submit_no_double_execution.json"))
    last = [r for r in M.run(scn, scn["envelopes"]) if "submissions" in r][-1]
    assert last["submissions"] == 1


# ------------------------------------------------------------------ checker A (cryptography + jsonschema)
@pytest.fixture(scope="module")
def checker_a():
    pytest.importorskip("jsonschema", reason="checker A needs jsonschema; checker B ran")
    pytest.importorskip("cryptography", reason="checker A needs cryptography; checker B ran")
    from cp_support import cp2_checker_a

    return cp2_checker_a


@pytest.mark.parametrize("path", DOORS, ids=lambda p: p.name)
def test_checker_a_equals_checker_b_on_every_door_fixture(checker_a, path):
    case = load_json(path)
    env, ctx = case["envelope"], unnum(case["context"])
    ra = checker_a.check_door(env, ctx)
    rb = B.check_door(plain(env), ctx)
    assert ra == rb, path.name
    assert (None if ra[0] == "ACCEPT" else ra[1]) == case["expected_outcome"]


def test_ephemeral_round_trip_is_deterministic_and_tamper_evident(checker_a):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    sk = Ed25519PrivateKey.generate()  # ephemeral, in memory only
    pk = sk.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    base = plain(load_json(FIXTURES / "valid" / "VALID__active_long.json")["envelope"])
    case = load_json(FIXTURES / "valid" / "VALID__active_long.json")
    ctx = unnum(case["context"])
    ctx["trust_store"] = {C.key_id(pk): {"public_key": pk.hex(), "not_before": "2025-12-01T00:00:00.000000Z",
                                         "not_after": "2026-12-01T00:00:00.000000Z", "status": "ACTIVE", "environment": "TEST"}}
    env = dict(base, signing_key_id=C.key_id(pk))
    env["signature"] = sk.sign(C.signed_bytes(env)).hex()
    again = dict(env, signature=sk.sign(C.signed_bytes(env)).hex())
    assert env == again  # replay of the same occurrence is byte-identical with a deterministic signer
    assert B.check_door(env, ctx) == ("ACCEPT", None)
    assert B.check_door(dict(env, execution_policy_ref="policy_ref_changed"), ctx) == ("REJECT", "REJECTED_SIGNATURE")
