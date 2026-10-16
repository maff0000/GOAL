"""Pure-Python Ed25519 signature VERIFICATION (RFC 8032), tests only.

There is no signing function here by design: the packages commit public keys and
signatures only, never key material of any kind. Checked against the RFC 8032
section 7.1 public test vectors in tests/test_cp2_conformance.py.
"""

from __future__ import annotations

import hashlib

_p = 2**255 - 19
_q = 2**252 + 27742317777372353535851937790883648493
_d = -121665 * pow(121666, _p - 2, _p) % _p
_I = pow(2, (_p - 1) // 4, _p)


def _inv(x: int) -> int:
    return pow(x, _p - 2, _p)


def _xrecover(y: int) -> int:
    xx = (y * y - 1) * _inv(_d * y * y + 1)
    x = pow(xx, (_p + 3) // 8, _p)
    if (x * x - xx) % _p != 0:
        x = (x * _I) % _p
    if x % 2 != 0:
        x = _p - x
    return x


_By = 4 * _inv(5) % _p
_Bx = _xrecover(_By)
_B = (_Bx % _p, _By % _p)


def _add(P, Q):
    x1, y1 = P
    x2, y2 = Q
    t = _d * x1 * x2 * y1 * y2
    return ((x1 * y2 + x2 * y1) * _inv(1 + t) % _p, (y1 * y2 + x1 * x2) * _inv(1 - t) % _p)


def _mul(P, e: int):
    result = (0, 1)
    addend = P
    while e:
        if e & 1:
            result = _add(result, addend)
        addend = _add(addend, addend)
        e >>= 1
    return result


def _on_curve(P) -> bool:
    x, y = P
    return (-x * x + y * y - 1 - _d * x * x * y * y) % _p == 0


def _decode(s: bytes):
    if len(s) != 32:
        raise ValueError("bad point length")
    y = int.from_bytes(s, "little") & ((1 << 255) - 1)
    if y >= _p:
        raise ValueError("non-canonical y")
    x = _xrecover(y)
    if (x & 1) != (s[31] >> 7):
        x = _p - x
    P = (x, y)
    if not _on_curve(P):
        raise ValueError("point not on curve")
    return P


def _encode(P) -> bytes:
    x, y = P
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def verify(signature: bytes, message: bytes, public_key: bytes) -> bool:
    """True iff `signature` is a valid Ed25519 signature of `message` under `public_key`."""
    try:
        if len(signature) != 64 or len(public_key) != 32:
            return False
        R = _decode(signature[:32])
        A = _decode(public_key)
        S = int.from_bytes(signature[32:], "little")
        if S >= _q:
            return False
        h = int.from_bytes(hashlib.sha512(_encode(R) + public_key + message).digest(), "little") % _q
        return _mul(_B, S) == _add(R, _mul(A, h))
    except ValueError:
        return False
