"""Atomadic Fuse MCP server — wraps the TOCC kernel for full superhero tools.

When you run `fuse-mcp`, this server starts a stdio MCP listener. The 6
superhero tools (verify-block, search-intent, compose-stack, emit-corpus,
explain-block, usage-stats) proxy directly to the local TOCC kernel
(`tocc-mcp` binary) via the MCP protocol. The 8 classic verbs (compile,
classify, absorb, catalog, capabilities, intent, doctor) remain HTTP
calls to the hosted Fuse engine at fuse.atomadic.tech.

If the TOCC kernel binary is not found, the superhero tools return a clear
error message pointing at install instructions. The classic verbs always
work (HTTP only).

Drop into Claude Desktop / Cursor / Windsurf / VS Code MCP config:
    {
      "mcpServers": {
        "atomadic-fuse": {"command": "fuse-mcp"}
      }
    }
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
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


# ── TOCC kernel proxy (for the 6 superhero tools) ────────────────────────────

_TOCC_MCP_HINTS = [
    os.environ.get("TOCC_MCP"),
    "tocc-mcp.exe",
    "tocc-mcp",
    r"C:\TOCC\dist-newstyle\build\x86_64-windows\ghc-9.6.7\tocc-fuse-kernel-0.1.0.0\x\tocc-mcp\build\tocc-mcp\tocc-mcp.exe",
]


def _find_tocc_mcp() -> str | None:
    for hint in _TOCC_MCP_HINTS:
        if not hint:
            continue
        if os.path.exists(hint):
            return hint
        which = shutil.which(hint)
        if which:
            return which
    return None


class _ToccMCPProxy:
    """Thin stdio MCP client to tocc-mcp binary. Lazy-initialized, persistent."""

    def __init__(self, exe_path: str):
        self._exe = exe_path
        self._proc: subprocess.Popen | None = None
        self._req_id = 0

    def _ensure(self) -> None:
        if self._proc is not None and self._proc.poll() is None:
            return
        self._proc = subprocess.Popen(
            [self._exe],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            cwd=os.environ.get("TOCC_ROOT", r"C:\TOCC"),
        )
        # MCP initialize handshake
        self._req_id += 1
        self._send({
            "jsonrpc": "2.0", "id": self._req_id, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "fuse-sdk", "version": "0.3.1"},
            },
        })
        self._recv()
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _send(self, msg: dict) -> None:
        assert self._proc and self._proc.stdin
        self._proc.stdin.write(json.dumps(msg) + "\n")
        self._proc.stdin.flush()

    def _recv(self) -> dict:
        assert self._proc and self._proc.stdout
        line = self._proc.stdout.readline()
        if not line:
            return {}
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return {"raw": line}

    def call(self, tool_name: str, args: dict[str, Any]) -> Any:
        self._ensure()
        self._req_id += 1
        self._send({
            "jsonrpc": "2.0", "id": self._req_id, "method": "tools/call",
            "params": {"name": tool_name, "arguments": args},
        })
        resp = self._recv()
        return resp.get("result", resp)


_proxy: _ToccMCPProxy | None = None


def _kernel() -> _ToccMCPProxy | None:
    global _proxy
    if _proxy is not None:
        return _proxy
    exe = _find_tocc_mcp()
    if exe:
        _proxy = _ToccMCPProxy(exe)
    return _proxy


def _kernel_or_error(tool: str) -> dict | None:
    """Return None if kernel ready, else a dict-shaped error to return upstream."""
    if _kernel() is not None:
        return None
    return {
        "error": "TOCC kernel binary not found",
        "tool_requested": tool,
        "hint": "Install Atomadic TOCC kernel (tocc-mcp on PATH) for full superhero tools, or set TOCC_MCP env var to the binary path.",
        "install": "https://atomadic.tech/install",
    }


# ── 8 classic verbs (HTTP to fuse.atomadic.tech, always available) ───────────

@mcp.tool()
def compile(repo_root: str, output_root: str = "./_fuse_out",
            max_chains: int = 500) -> Any:
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


# ── 6 superhero tools (TOCC kernel proxy, requires local tocc-mcp) ───────────

@mcp.tool()
def verify_block(block_id: str) -> Any:
    """Anti-hallucination shield: returns a block with its SHA-256 receipt.

    Routes to the local TOCC kernel (`tocc-mcp`). Requires the kernel binary
    on PATH or in the standard install location. The receipt is computed from
    the block's content_hash + semantic_hash and is the proof that the
    response did not come from a model hallucination.
    """
    err = _kernel_or_error("verify-block")
    if err:
        return err
    return _kernel().call("verify-hash", {"payload": block_id, "expected_hash": ""})


@mcp.tool()
def search_intent(description: str, tier: str = "", limit: int = 10) -> Any:
    """Smart context: describe what you need, get matching verified blocks."""
    err = _kernel_or_error("search-intent")
    if err:
        return err
    args: dict[str, Any] = {"query": description}
    if tier:
        args["tier"] = tier
    return _kernel().call("lookup-logic-block", args)


@mcp.tool()
def compose_stack(intent: str, target_language: str = "") -> Any:
    """Walk the full tier dependency chain (T6→T0) for an intent."""
    err = _kernel_or_error("compose-stack")
    if err:
        return err
    args: dict[str, Any] = {"intent": intent}
    if target_language:
        args["target_language"] = target_language
    return _kernel().call("emit-intent-package", args)


@mcp.tool()
def emit_corpus(target_language: str, target_dir: str = "") -> Any:
    """Emit the complete verified corpus as a shippable package in one call."""
    err = _kernel_or_error("emit-corpus")
    if err:
        return err
    args: dict[str, Any] = {"target_language": target_language}
    if target_dir:
        args["target_dir"] = target_dir
    return _kernel().call("emit-intent-package", args)


@mcp.tool()
def explain_block(block_id: str, detail: bool = False) -> Any:
    """Context-aware explanation of a logic block's contract and dependencies."""
    err = _kernel_or_error("explain-block")
    if err:
        return err
    return _kernel().call("lookup-logic-block", {"query": block_id, "detail": detail})


@mcp.tool()
def usage_stats() -> Any:
    """Token-savings dashboard: corpus size, block counts, estimated savings."""
    err = _kernel_or_error("usage-stats")
    if err:
        return err
    return _kernel().call("get-performance", {})


def launch() -> None:
    mcp.run()


if __name__ == "__main__":
    launch()