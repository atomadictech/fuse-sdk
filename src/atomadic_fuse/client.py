"""Atomadic Fuse SDK — typed HTTP client for the hosted compiler.

The hosted MCP endpoint is `https://fuse.atomadic.tech/v1`. Calls
either use an API key (Pro/Team subscription) or x402 micropayments
(autonomous agent) via the X-Payment-Proof header.

This is a thin HTTP wrapper. The engine internals (CNAE classifier,
5-tier monadic lattice, Codex-anchored confidence) live server-side
on the private Fuse engine and are not shipped in the public SDK.
"""
from __future__ import annotations

import os
from typing import Any

import httpx

from .exceptions import DecisionNeeded, FuseError, PaymentRequired


_DEFAULT_ENDPOINT = "https://fuse.atomadic.tech/v1"
_DEFAULT_TIMEOUT_S = 60.0


class FuseClient:
    """Synchronous client for the hosted Atomadic Fuse engine.

    Args:
        api_key: defaults to ``ATOMADIC_FUSE_API_KEY`` env var, falls
            back to ``ATOMADIC_API_KEY`` (bundle key). If neither is
            set, the client operates in x402 mode and per-call signed
            payment proofs are expected.
        endpoint: override the hosted engine URL. Default is
            ``https://fuse.atomadic.tech/v1``.
        timeout: per-call timeout in seconds (default 60).
    """

    def __init__(
        self,
        api_key: str | None = None,
        endpoint: str | None = None,
        timeout: float = _DEFAULT_TIMEOUT_S,
    ):
        self.api_key = (
            api_key
            or os.environ.get("ATOMADIC_FUSE_API_KEY")
            or os.environ.get("ATOMADIC_API_KEY")
        )
        self.endpoint = endpoint or _DEFAULT_ENDPOINT
        self.timeout = timeout

    # ── Verb-level methods ────────────────────────────────────────────

    def compile(
        self,
        repo_root: str,
        output_root: str = "./_fuse_out",
        max_chains: int = 500,
    ) -> dict[str, Any]:
        """Marquee primitive: messy repo → clean shippable package."""
        return self._post("compile", {
            "repo_root":   repo_root,
            "output_root": output_root,
            "max_chains":  int(max_chains),
        })

    def classify(self, body_text: str, name: str = "") -> dict[str, Any]:
        """Classify a function by AST behavior → action + confidence."""
        return self._post("classify", {"body_text": body_text, "name": name})

    def absorb(self, repo_root: str, repo_label: str | None = None) -> dict[str, Any]:
        """Add a repo to the Logic-Base catalog (incremental, deduped)."""
        return self._post("absorb", {"repo_root": repo_root, "repo_label": repo_label})

    def catalog(self, query: str, limit: int = 20) -> dict[str, Any]:
        """Query the catalog for atoms matching a behavior shape."""
        return self._post("catalog", {"query": query, "limit": int(limit)})

    def capabilities(self, min_sources: int = 2, min_chain_length: int = 2,
                     max_results: int = 50) -> dict[str, Any]:
        """List emergent cross-source chains in your catalog."""
        return self._post("capabilities", {
            "min_sources":      int(min_sources),
            "min_chain_length": int(min_chain_length),
            "max_results":      int(max_results),
        })

    def intent(self, intent_phrase: str, output_root: str = "./_intent_out",
               candidate_limit: int = 25) -> dict[str, Any]:
        """Natural-language intent → emit a custom themed product."""
        return self._post("intent", {
            "intent_phrase":   intent_phrase,
            "output_root":     output_root,
            "candidate_limit": int(candidate_limit),
        })

    def doctor(self) -> dict[str, Any]:
        """Health probe across the hosted engine workspace."""
        return self._post("doctor", {})

    # ── HTTP plumbing ────────────────────────────────────────────────

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        h = {"Content-Type": "application/json", "User-Agent": "atomadic-fuse/0.3.1"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        if extra:
            h.update(extra)
        return h

    def _post(self, verb: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.endpoint}/{verb}"
        with httpx.Client(timeout=self.timeout) as c:
            r = c.post(url, headers=self._headers(), json=payload)
        return self._handle(r)

    def _handle(self, r: httpx.Response) -> dict[str, Any]:
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict) and data.get("decision_required"):
                raise DecisionNeeded(
                    decision_id=data["decision_id"],
                    prompt=data.get("prompt", ""),
                    options=data.get("options", []),
                )
            return data
        if r.status_code == 402:
            data = r.json() if r.content else {}
            raise PaymentRequired(
                message=data.get("error", "Payment required"),
                payment_url=data.get("payment_url"),
                amount_usdc=data.get("amount_usdc"),
            )
        raise FuseError(f"HTTP {r.status_code}: {r.text[:200]}")
