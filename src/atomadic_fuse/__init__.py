"""Atomadic Fuse — Spaghetti to Shippable. Per-repo monadic compiler.

Public SDK v0.1.0. Wraps the hosted Fuse engine at fuse.atomadic.tech
behind a typed Python client + CLI + MCP server.

See README.md for quick start. See SoT.json for live ecosystem stats:
    https://sot.atomadic.tech/SoT.json
"""
from __future__ import annotations

from .client import FuseClient
from .exceptions import FuseError, DecisionNeeded, PaymentRequired

__all__ = ["FuseClient", "FuseError", "DecisionNeeded", "PaymentRequired"]
__version__ = "0.3.1"
