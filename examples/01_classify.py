"""Example: classify any function body by AST behavior.

The hosted Fuse engine returns ``[action, confidence]`` — confidence
is Codex-anchored (TAU_TRUST = 1820/1823 ~ 0.9984 is the high end).

Run:
    pip install atomadic-fuse
    export ATOMADIC_FUSE_API_KEY=...     # or use bundle ATOMADIC_API_KEY
    python examples/01_classify.py
"""
from atomadic_fuse import FuseClient


SAMPLES = [
    ("def fingerprint(b): return hashlib.sha256(b).hexdigest()",   "fingerprint"),
    ("def is_even(n): return n % 2 == 0",                          "is_even"),
    ("def get_user(uid): return db.execute('SELECT ...').fetchone()", "get_user"),
    ("def validate_email(s): assert '@' in s; return True",        "validate_email"),
]


def main() -> int:
    client = FuseClient()
    for body, name in SAMPLES:
        out = client.classify(body, name=name)
        action, confidence = out["action"], out["confidence"]
        print(f"{name:30s}  ->  {action:12s}  conf={confidence:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
