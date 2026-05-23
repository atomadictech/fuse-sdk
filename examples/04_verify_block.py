"""Example: anti-hallucination — prove that emitted code traces to a
verified contract, not a model's confabulation.

`verify_block` returns the block plus a SHA-256 receipt. The same
receipt is reproducible by the caller, so a downstream consumer can
independently confirm the block came from the kernel and was not
tampered with.

Run:
    pip install atomadic-fuse
    export ATOMADIC_FUSE_API_KEY=...     # or use bundle ATOMADIC_API_KEY
    python examples/04_verify_block.py
"""
from atomadic_fuse import FuseClient


# These IDs are stable across the hosted engine — they're the Tier 0
# axiom blocks. `define_clause_pure:d2d53efbde33` is Axiom 0 (Love
# Invariant). `define_clause_pure:fbe25ae75f03` is Axiom 1 (Invention).
AXIOM_BLOCK_IDS = [
    "lb:t0:define_clause_pure:d2d53efbde33",  # Axiom 0
    "lb:t0:define_clause_pure:fbe25ae75f03",  # Axiom 1
    "lb:t0:define_clause_pure:188030880113",  # Axiom 2
]


def main() -> int:
    client = FuseClient()
    for block_id in AXIOM_BLOCK_IDS:
        out = client.verify_block(block_id)
        receipt = out.get("receipt_hash") or out.get("content_hash", "?")
        cnae = out.get("cnae", "?")
        tier = out.get("tier", "?")
        status = out.get("verification_status") or out.get("status", "?")
        print(f"{block_id}")
        print(f"  cnae={cnae}  tier={tier}  status={status}")
        print(f"  receipt={receipt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
