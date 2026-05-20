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

    # ── Superhero tools (v0.2.0) ─────────────────────────────────────

    def verify_block(self, block_id: str) -> dict[str, Any]:
        """Anti-hallucination shield: returns a block with its SHA-256 verification receipt."""
        return self._post("verify-block", {"block_id": block_id})

    def search_intent(self, description: str, tier: str | None = None,
                      limit: int = 10) -> dict[str, Any]:
        """Semantic search: describe what you need, get matching verified blocks."""
        payload: dict[str, Any] = {"description": description, "limit": limit}
        if tier:
            payload["tier"] = tier
        return self._post("search-intent", payload)

    def compose_stack(self, intent: str, target_language: str | None = None) -> dict[str, Any]:
        """Walk the full tier dependency chain (T6→T0) for an intent."""
        payload: dict[str, Any] = {"intent": intent}
        if target_language:
            payload["target_language"] = target_language
        return self._post("compose-stack", payload)

    def emit_corpus(self, target_language: str, target_dir: str | None = None) -> dict[str, Any]:
        """Emit the complete verified corpus as a shippable package in one call."""
        payload: dict[str, Any] = {"target_language": target_language}
        if target_dir:
            payload["target_dir"] = target_dir
        return self._post("emit-corpus", payload)

    def explain_block(self, block_id: str, detail: bool = False) -> dict[str, Any]:
        """Context-aware explanation of a logic block's contract and dependencies."""
        return self._post("explain-block", {"block_id": block_id, "detail": detail})

    def usage_stats(self) -> dict[str, Any]:
        """Token savings dashboard: corpus size, block counts, estimated savings."""
        return self._post("usage-stats", {})

    # ── HTTP plumbing ────────────────────────────────────────────────

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        h = {"Content-Type": "application/json", "User-Agent": "atomadic-fuse/0.3.0"}
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
