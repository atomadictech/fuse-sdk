"""Atomadic Fuse MCP server — wraps the hosted FuseClient as MCP tools.

Usage:
    fuse-mcp     # stdio MCP server

Drop into Claude Desktop / Cursor / Windsurf MCP config:
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


@mcp.tool()
def compile(repo_root: str, output_root: str = "./_fuse_out",
            max_chains: int = 5) -> Any:
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
    """Health probe across the hosted engine workspace."""
    return _client.doctor()


def launch() -> None:
    mcp.run()


if __name__ == "__main__":
    launch()
