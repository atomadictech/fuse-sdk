"""Example: usage-stats dashboard — token economics + self-hosting proof.

`usage_stats` is the corpus-level dashboard. It returns block counts
per tier, the polyglot language family breakdown, an estimated token-
savings ratio versus raw shard browsing, and the self-hosting receipt
(`gen1 == gen2` rust-hash) that proves the kernel canonicalises itself.

Use this to cite real numbers when justifying MCP-first discipline to
your team: ~3M tokens per raw shard browse vs ~450 per MCP call =
**~11,763x savings**, ~$30,641/day estimated for 100 sessions.

Run:
    pip install atomadic-fuse
    python examples/06_usage_stats.py
"""
import json

from atomadic_fuse import FuseClient


def main() -> int:
    client = FuseClient()
    stats = client.usage_stats()

    # Headline numbers
    total = stats.get("total_blocks", "?")
    tiers = stats.get("tiers", {})
    langs = stats.get("emit_languages", "?")
    savings = (stats.get("token_savings") or {}).get("savings_factor", "?")
    self_host = stats.get("self_hosting", {})

    print("Atomadic Fuse — corpus dashboard")
    print("=" * 50)
    print(f"  total blocks            : {total}")
    print(f"  tiers                   : {tiers}")
    print(f"  emit languages          : {langs}")
    print(f"  token savings vs raw    : {savings}")
    print(f"  self-hosting proven     : {self_host.get('proven', False)}")
    print(f"  gen1 == gen2 (rust)     : {self_host.get('gen1_eq_gen2', False)}")
    print(f"  rust receipt hash       : {self_host.get('rust_hash', '?')[:32]}...")
    print()
    print("Full payload:")
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
