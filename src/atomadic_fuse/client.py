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


def _seed_root() -> "pathlib.Path":
    """Return the absolute path of the bundled `logic-base-seed/` directory.

    The SDK package ships a small seed catalogue of verified CNAE atoms so
    callers can do an offline-only walk-through before pointing at the
    hosted engine. The directory lives alongside this module file.

    Returns a ``pathlib.Path`` (callers that need a ``str`` can cast).
    """
    import pathlib
    return pathlib.Path(__file__).resolve().parent / "logic-base-seed"


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
        telemetry_opt_in: bool = False,
    ):
        self.api_key = (
            api_key
            or os.environ.get("ATOMADIC_FUSE_API_KEY")
            or os.environ.get("ATOMADIC_API_KEY")
        )
        self.endpoint = endpoint or _DEFAULT_ENDPOINT
        self.timeout = timeout
        # Telemetry opt-in: when True, the client may send anonymized
        # CNAE/tier/domain/language metadata in request headers. Off by
        # default; the CLI exposes a `--telemetry` flag and the env var
        # ATOMADIC_FUSE_TELEMETRY=1 also enables it. Never sends code,
        # intent text, or secrets.
        self.telemetry_opt_in = bool(telemetry_opt_in) or (
            os.environ.get("ATOMADIC_FUSE_TELEMETRY", "").strip().lower()
            in ("1", "true", "yes", "on")
        )

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
    # ── Superhero tools (v0.3.2) — direct HTTP to hosted Fuse engine ─────

    def verify_block(self, block_id: str) -> dict[str, Any]:
        """Anti-hallucination: returns block + SHA-256 verification receipt."""
        return self._post("verify_block", {"block_id": block_id})

    def search_intent(self, description: str, tier: str | None = None,
                      limit: int = 10) -> dict[str, Any]:
        """Semantic search: describe what you need, get verified blocks ranked."""
        payload: dict[str, Any] = {"description": description, "limit": int(limit)}
        if tier:
            payload["tier"] = tier
        return self._post("search_intent", payload)

    def compose_stack(self, intent: str, target_language: str | None = None) -> dict[str, Any]:
        """Walk full tier dependency chain (T6→T0) for an intent."""
        payload: dict[str, Any] = {"intent": intent}
        if target_language:
            payload["target_language"] = target_language
        return self._post("compose_stack", payload)

    def emit_corpus(self, target_language: str, target_dir: str | None = None) -> dict[str, Any]:
        """Emit the complete verified corpus as a shippable package."""
        payload: dict[str, Any] = {"target_language": target_language}
        if target_dir:
            payload["target_dir"] = target_dir
        return self._post("emit_corpus", payload)

    def explain_block(self, block_id: str, detail: bool = False) -> dict[str, Any]:
        """Context-aware explanation of a block's contract and dependencies."""
        return self._post("explain_block", {"block_id": block_id, "detail": detail})

    def usage_stats(self) -> dict[str, Any]:
        """Token-savings dashboard: corpus size, block counts, savings estimate."""
        return self._post("usage_stats", {})

    # ── 8 engine tools (v1.0.0) — mirror of local fuse-engine-mcp surface ────
    # Until the hosted Wave-B backend lights up full execution, these proxy
    # to endpoints that return curated/stub responses with `local_route`
    # pointing at the local fuse-engine-mcp binary for full execution.

    def scan(self, directory: str,
             languages: str = "python,typescript,rust") -> dict[str, Any]:
        """Walk a directory and return CNAE atoms found in source files."""
        return self._post("scan", {"directory": directory, "languages": languages})

    def discover(self, workspace: str | None = None) -> dict[str, Any]:
        """Cluster, score, and discover emergent dependency chains."""
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("discover", payload)

    def synthesize(self, output: str = "./synthesized",
                   workspace: str | None = None,
                   dry_run: bool = False) -> dict[str, Any]:
        """Full synthesis pipeline: scan → absorb → cluster → score → chain → theme → emit."""
        payload: dict[str, Any] = {"output": output, "dry_run": bool(dry_run)}
        if workspace:
            payload["workspace"] = workspace
        return self._post("synthesize", payload)

    def emit(self, output: str, workspace: str | None = None) -> dict[str, Any]:
        """Emit product directory scaffolds for ranked products (T0-T5)."""
        payload: dict[str, Any] = {"output": output}
        if workspace:
            payload["workspace"] = workspace
        return self._post("emit", payload)

    def validate(self, name: str) -> dict[str, Any]:
        """Validate a CNAE name against the canonical action_entity_scope vocabulary."""
        return self._post("validate", {"name": name})

    def status(self, workspace: str | None = None) -> dict[str, Any]:
        """Read-only logic-base status: atom count, shards, ledgers, manifest."""
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("status", payload)

    def search(self, query: str, workspace: str | None = None) -> dict[str, Any]:
        """Substring + CNAE search across the logic-base."""
        payload: dict[str, Any] = {"query": query}
        if workspace:
            payload["workspace"] = workspace
        return self._post("search", payload)

    def logic_map(self, workspace: str | None = None) -> dict[str, Any]:
        """Return the full composition graph of the logic-base (atom → deps by tier)."""
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("logic_map", payload)

    # ── HTTP plumbing ────────────────────────────────────────────────

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        h = {"Content-Type": "application/json", "User-Agent": "atomadic-fuse/1.0.0"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        if self.telemetry_opt_in:
            h["X-Atomadic-Telemetry"] = "opt-in"
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
