"""Atomadic Fuse SDK — typed HTTP client for the hosted compiler.

The hosted MCP endpoint is `https://fuse.atomadic.tech/v1`. Calls
either use an API key (Pro/Team subscription) or x402 micropayments
(autonomous agent) via the X-Payment-Proof header.

THIS FILE IS GENERATED — do not edit by hand.
Re-emit via: fuse-engine emit-sdk-client --sdk-root <sdk-root>
Source of truth: atomadic_fuse_engine/tier_4/emit_sdk_client.py (SDK_SURFACE)
"""
from __future__ import annotations

import os
from typing import Any

import httpx

from .exceptions import DecisionNeeded, FuseError, PaymentRequired


_DEFAULT_ENDPOINT = "https://fuse.atomadic.tech/v1"
_DEFAULT_TIMEOUT_S = 60.0


def _pkg_version() -> str:
    try:
        from importlib.metadata import version as _mv
        return _mv("atomadic-fuse")
    except Exception:
        return "1.1.0"


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

    # ── Verb-level methods (generated from SDK_SURFACE) ───────────────────

    # ── classic hosted verbs ──────────────────────────────────────
    def compile(
        self, repo_root: str, output_root: str = './_fuse_out', max_chains: int = 500
    ) -> dict[str, Any]:
        """Marquee primitive: messy repo → clean shippable package.

        Args:
            repo_root: absolute path of the source tree to compile
            output_root: output directory for the emitted package
            max_chains: maximum emergent chains to resolve
        """
        payload: dict[str, Any] = {"repo_root": repo_root}
        if output_root:
            payload["output_root"] = output_root
        payload["max_chains"] = int(max_chains)
        return self._post("compile", payload)

    def classify(
        self, body_text: str, name: str = ''
    ) -> dict[str, Any]:
        """Classify a function by AST behavior → CNAE action + confidence.

        Args:
            body_text: function body source to classify
            name: optional function name hint
        """
        payload: dict[str, Any] = {"body_text": body_text}
        if name:
            payload["name"] = name
        return self._post("classify", payload)

    def absorb(
        self, repo_root: str, repo_label: str = ''
    ) -> dict[str, Any]:
        """Add a repo to the Logic-Base catalog (incremental, deduped).

        Args:
            repo_root: absolute path of the source tree to absorb
            repo_label: optional human label for the repo
        """
        payload: dict[str, Any] = {"repo_root": repo_root}
        if repo_label:
            payload["repo_label"] = repo_label
        return self._post("absorb", payload)

    def catalog(
        self, query: str, limit: int = 20
    ) -> dict[str, Any]:
        """Query the catalog for atoms matching a behavior shape.

        Args:
            query: behavior-shape query string
            limit: max results to return
        """
        payload: dict[str, Any] = {"query": query}
        payload["limit"] = int(limit)
        return self._post("catalog", payload)

    def capabilities(
        self, min_sources: int = 2, min_chain_length: int = 2, max_results: int = 50
    ) -> dict[str, Any]:
        """List emergent cross-source chains in the catalog.

        Args:
            min_sources: minimum source repos per chain
            min_chain_length: minimum chain depth
            max_results: max chains to return
        """
        payload: dict[str, Any] = {}
        payload["min_sources"] = int(min_sources)
        payload["min_chain_length"] = int(min_chain_length)
        payload["max_results"] = int(max_results)
        return self._post("capabilities", payload)

    def intent(
        self, intent_phrase: str, output_root: str = './_intent_out', candidate_limit: int = 25
    ) -> dict[str, Any]:
        """Natural-language intent → emit a custom themed product.

        Args:
            intent_phrase: natural-language product intent
            output_root: output directory for the emitted product
            candidate_limit: max candidate atoms to consider
        """
        payload: dict[str, Any] = {"intent_phrase": intent_phrase}
        if output_root:
            payload["output_root"] = output_root
        payload["candidate_limit"] = int(candidate_limit)
        return self._post("intent", payload)

    def doctor(
        self
    ) -> dict[str, Any]:
        """Health probe across the hosted engine workspace."""
        payload: dict[str, Any] = {}
        return self._post("doctor", payload)

    def fuse_recovery_status(
        self
    ) -> dict[str, Any]:
        """Read-only Fuse recovery gate status (hosted mirror of the live gate)."""
        payload: dict[str, Any] = {}
        return self._post("fuse_recovery_status", payload)


    # ── superhero tools ───────────────────────────────────────────
    def verify_block(
        self, block_id: str
    ) -> dict[str, Any]:
        """Anti-hallucination shield: returns block + SHA-256 verification receipt.

        Args:
            block_id: block ID or CNAE name to verify
        """
        payload: dict[str, Any] = {"block_id": block_id}
        return self._post("verify_block", payload)

    def search_intent(
        self, description: str, tier: str = '', limit: int = 10
    ) -> dict[str, Any]:
        """Semantic search: describe what you need, get verified blocks ranked.

        Args:
            description: natural-language description of what you need
            tier: optional tier filter: t0–t5
            limit: max results
        """
        payload: dict[str, Any] = {"description": description}
        if tier:
            payload["tier"] = tier
        payload["limit"] = int(limit)
        return self._post("search_intent", payload)

    def compose_stack(
        self, intent: str, target_language: str = ''
    ) -> dict[str, Any]:
        """Walk the full tier dependency chain (T5→T0) for an intent.

        Args:
            intent: top-level intent or CNAE name to compose
            target_language: optional target language
        """
        payload: dict[str, Any] = {"intent": intent}
        if target_language:
            payload["target_language"] = target_language
        return self._post("compose_stack", payload)

    def emit_corpus(
        self, target_language: str, target_dir: str = ''
    ) -> dict[str, Any]:
        """Emit the complete verified corpus as a shippable package.

        Args:
            target_language: target: rust, python, typescript, haskell, go,
                gui_web
            target_dir: optional output directory
        """
        payload: dict[str, Any] = {"target_language": target_language}
        if target_dir:
            payload["target_dir"] = target_dir
        return self._post("emit_corpus", payload)

    def explain_block(
        self, block_id: str, detail: bool = False
    ) -> dict[str, Any]:
        """Context-aware block explanation: contract, tier, dependencies.

        Args:
            block_id: block ID or CNAE name
            detail: if True, return full contract + lineage
        """
        payload: dict[str, Any] = {"block_id": block_id}
        if detail:
            payload["detail"] = detail
        return self._post("explain_block", payload)

    def usage_stats(
        self
    ) -> dict[str, Any]:
        """Token-savings dashboard: corpus size, block counts, savings estimate."""
        payload: dict[str, Any] = {}
        return self._post("usage_stats", payload)


    # ── engine tools v1.0 ─────────────────────────────────────────
    def scan(
        self, directory: str, languages: str = 'python,typescript,rust'
    ) -> dict[str, Any]:
        """Walk a directory and return CNAE atoms found in source files.

        Args:
            directory: absolute path to scan for CNAE atoms
            languages: comma-separated language filter
        """
        payload: dict[str, Any] = {"directory": directory}
        if languages:
            payload["languages"] = languages
        return self._post("scan", payload)

    def discover(
        self, workspace: str = ''
    ) -> dict[str, Any]:
        """Cluster, score, and discover emergent dependency chains. The emergent finder.

        Args:
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("discover", payload)

    def synthesize(
        self, output: str = './synthesized', workspace: str = '', dry_run: bool = False
    ) -> dict[str, Any]:
        """Full synthesis pipeline: scan → absorb → cluster → score → chain → theme → emit.

        Args:
            output: output directory for emitted products
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
            dry_run: if True, compute the plan without writing files
        """
        payload: dict[str, Any] = {}
        if output:
            payload["output"] = output
        if workspace:
            payload["workspace"] = workspace
        if dry_run:
            payload["dry_run"] = dry_run
        return self._post("synthesize", payload)

    def emit(
        self, output: str, workspace: str = ''
    ) -> dict[str, Any]:
        """Emit product directory scaffolds for ranked products (T0-T5).

        Args:
            output: output directory for emitted product scaffolds
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {"output": output}
        if workspace:
            payload["workspace"] = workspace
        return self._post("emit", payload)

    def validate(
        self, name: str
    ) -> dict[str, Any]:
        """Validate a CNAE name against the canonical action_entity_scope vocabulary.

        Args:
            name: candidate CNAE name to validate
        """
        payload: dict[str, Any] = {"name": name}
        return self._post("validate", payload)

    def status(
        self, workspace: str = ''
    ) -> dict[str, Any]:
        """Read-only logic-base status: atom count, shards, ledgers, manifest.

        Args:
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("status", payload)

    def search(
        self, query: str, workspace: str = ''
    ) -> dict[str, Any]:
        """Substring + CNAE search across the logic-base.

        Args:
            query: natural-language or CNAE search query
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {"query": query}
        if workspace:
            payload["workspace"] = workspace
        return self._post("search", payload)

    def logic_map(
        self, workspace: str = ''
    ) -> dict[str, Any]:
        """Return the full composition graph of the logic-base (atom → dependencies, by tier).

        Args:
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("logic_map", payload)

    def langs(
        self
    ) -> dict[str, Any]:
        """List all supported language families grouped by emitter target."""
        payload: dict[str, Any] = {}
        return self._post("langs", payload)

    def polyglot(
        self, name: str, languages: str = '', workspace: str = ''
    ) -> dict[str, Any]:
        """Emit a specific logic-base atom as polyglot code across language targets.

        Args:
            name: CNAE atom name, e.g. 'validate_path_pure'
            languages: comma-separated target languages; '' = all
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {"name": name}
        if languages:
            payload["languages"] = languages
        if workspace:
            payload["workspace"] = workspace
        return self._post("polyglot", payload)

    def show(
        self, name: str, workspace: str = ''
    ) -> dict[str, Any]:
        """Drill into one atom: full contract, source, and next_actions guidance.

        Args:
            name: CNAE atom name or block ID to drill into
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {"name": name}
        if workspace:
            payload["workspace"] = workspace
        return self._post("show", payload)


    # ── v1.1.0 store governance and telemetry ─────────────────────
    def quickstart(
        self, directory: str, output: str = './_fuse_out', permissive: bool = True
    ) -> dict[str, Any]:
        """One-shot onboarding: scan a directory, absorb atoms, synthesize and emit products. The
        fastest path from a messy repo to a shippable package. Permissive mode (default)
        harvests all functions regardless of CNAE naming — ideal for first runs.

        Args:
            directory: absolute path of the source tree to compile
            output: output directory for emitted products
            permissive: harvest any function regardless of CNAE naming
        """
        payload: dict[str, Any] = {"directory": directory}
        if output:
            payload["output"] = output
        if permissive:
            payload["permissive"] = permissive
        return self._post("quickstart", payload)

    def friction(
        self, workspace: str = '', kind: str = '', n: int = 50, summary: bool = False
    ) -> dict[str, Any]:
        """Read the Friction Protocol telemetry log. Records every UX friction event (zero-result
        hints, errors, empty inputs, bad paths) so you can see what's causing the most
        friction in your workflow.

        Args:
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
            kind: filter by event kind (e.g. 'zero_atoms', 'workspace_missing')
            n: max events to return
            summary: if True, return counts grouped by kind instead of raw
                events
        """
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        if kind:
            payload["kind"] = kind
        payload["n"] = int(n)
        if summary:
            payload["summary"] = summary
        return self._post("friction", payload)

    def promote_hypotheses(
        self, workspace: str = '', dry_run: bool = False
    ) -> dict[str, Any]:
        """Promote hypothesis candidates in the logic-base to verified status. Scans all candidate
        blocks, runs the 11-gate promotion pipeline, and writes canonical blocks.

        Args:
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
            dry_run: if True, report what would be promoted without writing
        """
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        if dry_run:
            payload["dry_run"] = dry_run
        return self._post("promote_hypotheses", payload)

    def promote_candidate(
        self, block_id: str, workspace: str = ''
    ) -> dict[str, Any]:
        """Promote a specific candidate block by ID through the 11-gate pipeline.

        Args:
            block_id: the lb: prefixed block ID to promote
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {"block_id": block_id}
        if workspace:
            payload["workspace"] = workspace
        return self._post("promote_candidate", payload)

    def explain_lineage(
        self, block_id: str, workspace: str = ''
    ) -> dict[str, Any]:
        """Show the full lineage tree for a block — composed_from + depends_on paths.

        Args:
            block_id: the lb: prefixed block ID or CNAE name to trace
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {"block_id": block_id}
        if workspace:
            payload["workspace"] = workspace
        return self._post("explain_lineage", payload)

    def lint_store(
        self, workspace: str = ''
    ) -> dict[str, Any]:
        """Lint the logic-base for schema violations, stale references, and tier-law breaks.

        Args:
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("lint_store", payload)

    def validate_store(
        self, workspace: str = ''
    ) -> dict[str, Any]:
        """Run the full 11-gate validation sweep across every block in the logic-base.

        Args:
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("validate_store", payload)

    def deduplicate_store(
        self, workspace: str = ''
    ) -> dict[str, Any]:
        """Remove exact-duplicate blocks (same dedupe_key) from the logic-base.

        Args:
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("deduplicate_store", payload)

    def rebuild_indexes(
        self, workspace: str = ''
    ) -> dict[str, Any]:
        """Rebuild CNAE, fingerprint, lineage and composition indexes from scratch. Call this after
        bulk imports or manual shard edits to restore index consistency.

        Args:
            workspace: absolute path to the logic-base workspace; '' auto-
                detects
        """
        payload: dict[str, Any] = {}
        if workspace:
            payload["workspace"] = workspace
        return self._post("rebuild_indexes", payload)


    # ── HTTP plumbing ────────────────────────────────────────────────────────

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        h = {"Content-Type": "application/json", "User-Agent": f"atomadic-fuse/{_pkg_version()}"}
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
