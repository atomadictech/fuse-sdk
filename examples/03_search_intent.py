"""Example: semantic intent search — find verified blocks by behavior.

`search_intent` is the token-economic search verb: instead of dumping
shards of JSONL into your context, you describe what you need in
natural language and get a ranked list of verified blocks back.

Roughly **3M tokens cheaper per lookup** than raw shard browsing.

Run:
    pip install atomadic-fuse
    export ATOMADIC_FUSE_API_KEY=...     # or use bundle ATOMADIC_API_KEY
    python examples/03_search_intent.py
"""
from atomadic_fuse import FuseClient


QUERIES = [
    ("validate a path against allowed roots", None),
    ("compose a deployment pipeline", "t4"),
    ("hash-chained append-only ledger writer", "t3"),
    ("emit a typescript package from a contract", "t4"),
]


def main() -> int:
    client = FuseClient()
    for description, tier in QUERIES:
        result = client.search_intent(description=description, tier=tier, limit=5)
        matches = result.get("matches", [])
        print(f"\n{description!r}  (tier={tier or 'any'})")
        for m in matches[:3]:
            block_id = m.get("block_id", m.get("id", "?"))
            cnae = m.get("cnae", "?")
            score = m.get("score", 0)
            print(f"  {score:.3f}  {cnae:35s}  {block_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
