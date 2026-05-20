"""Atomadic Fuse MCP server — exposes the hosted Fuse engine as MCP tools.

Every tool here proxies via the FuseClient HTTPS layer to the hosted engine
at fuse.atomadic.tech. No local engine required.

Drop into Claude Desktop / Cursor / Windsurf / VS Code MCP config:
    {
      "mcpServers": {
        "atomadic-fuse": {"command": "fuse-mcp"}
      }
    }
"""
from __future__ import annotations

import sys
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("mcp[cli] not installed -- install with: pip install 'atomadic-fuse[mcp]'",
          file=sys.stderr)
    sys.exit(1)

from .client import FuseClient


mcp = FastMCP("atomadic-fuse")
_client = FuseClient()


# ── 8 classic verbs ───────────────────────────────────────────────────────

@mcp.tool()
def compile(repo_root: str, output_root: str = "./_fuse_out", max_chains: int = 500) -> Any:
    """Marquee primitive: messy repo → clean shippable package."""
    return _client.compile(repo_root, output_root=output_root, max_chains=max_chains)


@mcp.tool()
def classify(body_text: str, name: str = "") -> Any:
    """Classify a function by AST behavior → action + confidence."""
    return _client.classify(body_text, name=name)


@mcp.tool()
def absorb(repo_root: str, repo_label: str = "") -> Any:
    """Add a repo to the Logic-Base catalog."""
    return _client.absorb(repo_root, repo_label=repo_label or None)


@mcp.tool()
def catalog(query: str, limit: int = 20) -> Any:
    """Query the catalog for atoms matching a behavior shape."""
    return _client.catalog(query, limit=limit)


@mcp.tool()
def capabilities() -> Any:
    """List emergent cross-source chains in the catalog."""
    return _client.capabilities()


@mcp.tool()
def intent(intent_phrase: str, output_root: str = "./_intent_out") -> Any:
    """Natural-language intent → emit a custom themed product."""
    return _client.intent(intent_phrase, output_root=output_root)


@mcp.tool()
def doctor() -> Any:
    """Health probe across the hosted engine."""
    return _client.doctor()


# ── 6 superhero tools (v0.3.2 — direct HTTP to hosted Fuse engine) ───────

@mcp.tool()
def verify_block(block_id: str) -> Any:
    """Anti-hallucination shield: returns block + SHA-256 verification receipt."""
    return _client.verify_block(block_id)


@mcp.tool()
def search_intent(description: str, tier: str = "", limit: int = 10) -> Any:
    """Semantic search: describe what you need, get verified blocks ranked."""
    return _client.search_intent(description, tier=(tier or None), limit=limit)


@mcp.tool()
def compose_stack(intent: str, target_language: str = "") -> Any:
    """Walk the full tier dependency chain (T6→T0) for an intent."""
    return _client.compose_stack(intent, target_language=(target_language or None))


@mcp.tool()
def emit_corpus(target_language: str, target_dir: str = "") -> Any:
    """Emit the complete verified corpus as a shippable package."""
    return _client.emit_corpus(target_language, target_dir=(target_dir or None))


@mcp.tool()
def explain_block(block_id: str, detail: bool = False) -> Any:
    """Context-aware block explanation."""
    return _client.explain_block(block_id, detail=detail)


@mcp.tool()
def usage_stats() -> Any:
    """Token-savings dashboard: corpus size, block counts, savings."""
    return _client.usage_stats()


def launch() -> None:
    mcp.run()


if __name__ == "__main__":
    launch()