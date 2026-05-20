"""Atomadic Fuse — Spaghetti to Shippable. Per-repo monadic compiler.

Public SDK v0.1.0. Wraps the hosted Fuse engine at fuse.atomadic.tech
behind a typed Python client + CLI + MCP server.

See README.md for quick start. See SoT.json for live ecosystem stats:
    https://sot.atomadic.tech/SoT.json
"""
from __future__ import annotations

from .client import FuseClient, _seed_root as _seed_root
from .exceptions import FuseError, DecisionNeeded, PaymentRequired


def seed_path():
    """Return the bundled seed logic-base directory path."""
    return _seed_root()


__all__ = [
    "FuseClient", "FuseError", "DecisionNeeded", "PaymentRequired",
    "seed_path",
]
__version__ = "1.0.0"
