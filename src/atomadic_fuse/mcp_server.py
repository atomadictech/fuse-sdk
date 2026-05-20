"""Atomadic Fuse MCP server — exposes the hosted Fuse engine as MCP tools.

Every tool here proxies via the FuseClient HTTPS layer to the hosted engine
at fuse.atomadic.tech. No local engine required.

Drop into Claude Desktop / Cursor / Windsurf / VS Code MCP config:
    {
    "mcpServers": {
    "atomadic-fuse": {"command": "fuse-mcp"}
    }
    }

THIS FILE IS GENERATED — do not edit by hand.
Re-emit via: fuse-engine emit-sdk-client --sdk-root <sdk-root>
Source of truth: atomadic_fuse_engine/tier_4/emit_sdk_client.py (SDK_SURFACE)
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



# ── classic hosted verbs ──────────────────────────────────────

@mcp.tool()
def compile(repo_root: str, output_root: str = './_fuse_out', max_chains: int = 500) -> Any:
    """Marquee primitive: messy repo → clean shippable package.

    Args:
        repo_root: absolute path of the source tree to compile
        output_root: output directory for the emitted package
        max_chains: maximum emergent chains to resolve
    """
    return _client.compile(repo_root, output_root=output_root, max_chains=max_chains)

@mcp.tool()
def classify(body_text: str, name: str = '') -> Any:
    """Classify a function by AST behavior → CNAE action + confidence.

    Args:
        body_text: function body source to classify
        name: optional function name hint
    """
    return _client.classify(body_text, name=name)

@mcp.tool()
def absorb(repo_root: str, repo_label: str = '') -> Any:
    """Add a repo to the Logic-Base catalog (incremental, deduped).

    Args:
        repo_root: absolute path of the source tree to absorb
        repo_label: optional human label for the repo
    """
    return _client.absorb(repo_root, repo_label=repo_label)

@mcp.tool()
def catalog(query: str, limit: int = 20) -> Any:
    """Query the catalog for atoms matching a behavior shape.

    Args:
        query: behavior-shape query string
        limit: max results to return
    """
    return _client.catalog(query, limit=limit)

@mcp.tool()
def capabilities(min_sources: int = 2, min_chain_length: int = 2, max_results: int = 50) -> Any:
    """List emergent cross-source chains in the catalog.

    Args:
        min_sources: minimum source repos per chain
        min_chain_length: minimum chain depth
        max_results: max chains to return
    """
    return _client.capabilities(min_sources=min_sources, min_chain_length=min_chain_length, max_results=max_results)

@mcp.tool()
def intent(intent_phrase: str, output_root: str = './_intent_out', candidate_limit: int = 25) -> Any:
    """Natural-language intent → emit a custom themed product.

    Args:
        intent_phrase: natural-language product intent
        output_root: output directory for the emitted product
        candidate_limit: max candidate atoms to consider
    """
    return _client.intent(intent_phrase, output_root=output_root, candidate_limit=candidate_limit)

@mcp.tool()
def doctor() -> Any:
    """Health probe across the hosted engine workspace."""
    return _client.doctor()

@mcp.tool()
def fuse_recovery_status() -> Any:
    """Read-only Fuse recovery gate status (hosted mirror of the live gate)."""
    return _client.fuse_recovery_status()


# ── superhero tools ───────────────────────────────────────────

@mcp.tool()
def verify_block(block_id: str) -> Any:
    """Anti-hallucination shield: returns block + SHA-256 verification receipt.

    Args:
        block_id: block ID or CNAE name to verify
    """
    return _client.verify_block(block_id)

@mcp.tool()
def search_intent(description: str, tier: str = '', limit: int = 10) -> Any:
    """Semantic search: describe what you need, get verified blocks ranked.

    Args:
        description: natural-language description of what you need
        tier: optional tier filter: t0–t5
        limit: max results
    """
    return _client.search_intent(description, tier=tier, limit=limit)

@mcp.tool()
def compose_stack(intent: str, target_language: str = '') -> Any:
    """Walk the full tier dependency chain (T5→T0) for an intent.

    Args:
        intent: top-level intent or CNAE name to compose
        target_language: optional target language
    """
    return _client.compose_stack(intent, target_language=target_language)

@mcp.tool()
def emit_corpus(target_language: str, target_dir: str = '') -> Any:
    """Emit the complete verified corpus as a shippable package.

    Args:
        target_language: target: rust, python, typescript, haskell, go, gui_web
        target_dir: optional output directory
    """
    return _client.emit_corpus(target_language, target_dir=target_dir)

@mcp.tool()
def explain_block(block_id: str, detail: bool = False) -> Any:
    """Context-aware block explanation: contract, tier, dependencies.

    Args:
        block_id: block ID or CNAE name
        detail: if True, return full contract + lineage
    """
    return _client.explain_block(block_id, detail=detail)

@mcp.tool()
def usage_stats() -> Any:
    """Token-savings dashboard: corpus size, block counts, savings estimate."""
    return _client.usage_stats()


# ── engine tools v1.0 ─────────────────────────────────────────

@mcp.tool()
def scan(directory: str, languages: str = 'python,typescript,rust') -> Any:
    """Walk a directory and return CNAE atoms found in source files.

    Args:
        directory: absolute path to scan for CNAE atoms
        languages: comma-separated language filter
    """
    return _client.scan(directory, languages=languages)

@mcp.tool()
def discover(workspace: str = '') -> Any:
    """Cluster, score, and discover emergent dependency chains. The emergent finder.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.discover(workspace=workspace)

@mcp.tool()
def synthesize(output: str = './synthesized', workspace: str = '', dry_run: bool = False) -> Any:
    """Full synthesis pipeline: scan → absorb → cluster → score → chain → theme → emit.

    Args:
        output: output directory for emitted products
        workspace: absolute path to the logic-base workspace; '' auto-detects
        dry_run: if True, compute the plan without writing files
    """
    return _client.synthesize(output=output, workspace=workspace, dry_run=dry_run)

@mcp.tool()
def emit(output: str, workspace: str = '') -> Any:
    """Emit product directory scaffolds for ranked products (T0-T5).

    Args:
        output: output directory for emitted product scaffolds
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.emit(output, workspace=workspace)

@mcp.tool()
def validate(name: str) -> Any:
    """Validate a CNAE name against the canonical action_entity_scope vocabulary.

    Args:
        name: candidate CNAE name to validate
    """
    return _client.validate(name)

@mcp.tool()
def status(workspace: str = '') -> Any:
    """Read-only logic-base status: atom count, shards, ledgers, manifest.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.status(workspace=workspace)

@mcp.tool()
def search(query: str, workspace: str = '') -> Any:
    """Substring + CNAE search across the logic-base.

    Args:
        query: natural-language or CNAE search query
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.search(query, workspace=workspace)

@mcp.tool()
def logic_map(workspace: str = '') -> Any:
    """Return the full composition graph of the logic-base (atom → dependencies, by tier).

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.logic_map(workspace=workspace)

@mcp.tool()
def langs() -> Any:
    """List all supported language families grouped by emitter target."""
    return _client.langs()

@mcp.tool()
def polyglot(name: str, languages: str = '', workspace: str = '') -> Any:
    """Emit a specific logic-base atom as polyglot code across language targets.

    Args:
        name: CNAE atom name, e.g. 'validate_path_pure'
        languages: comma-separated target languages; '' = all
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.polyglot(name, languages=languages, workspace=workspace)

@mcp.tool()
def show(name: str, workspace: str = '') -> Any:
    """Drill into one atom: full contract, source, and next_actions guidance.

    Args:
        name: CNAE atom name or block ID to drill into
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.show(name, workspace=workspace)


# ── v1.1.0 store governance and telemetry ─────────────────────

@mcp.tool()
def quickstart(directory: str, output: str = './_fuse_out', permissive: bool = True) -> Any:
    """One-shot onboarding: scan a directory, absorb atoms, synthesize and emit products. The
    fastest path from a messy repo to a shippable package. Permissive mode (default)
    harvests all functions regardless of CNAE naming — ideal for first runs.

    Args:
        directory: absolute path of the source tree to compile
        output: output directory for emitted products
        permissive: harvest any function regardless of CNAE naming
    """
    return _client.quickstart(directory, output=output, permissive=permissive)

@mcp.tool()
def friction(workspace: str = '', kind: str = '', n: int = 50, summary: bool = False) -> Any:
    """Read the Friction Protocol telemetry log. Records every UX friction event (zero-result
    hints, errors, empty inputs, bad paths) so you can see what's causing the most
    friction in your workflow.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects
        kind: filter by event kind (e.g. 'zero_atoms', 'workspace_missing')
        n: max events to return
        summary: if True, return counts grouped by kind instead of raw events
    """
    return _client.friction(workspace=workspace, kind=kind, n=n, summary=summary)

@mcp.tool()
def promote_hypotheses(workspace: str = '', dry_run: bool = False) -> Any:
    """Promote hypothesis candidates in the logic-base to verified status. Scans all candidate
    blocks, runs the 11-gate promotion pipeline, and writes canonical blocks.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects
        dry_run: if True, report what would be promoted without writing
    """
    return _client.promote_hypotheses(workspace=workspace, dry_run=dry_run)

@mcp.tool()
def promote_candidate(block_id: str, workspace: str = '') -> Any:
    """Promote a specific candidate block by ID through the 11-gate pipeline.

    Args:
        block_id: the lb: prefixed block ID to promote
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.promote_candidate(block_id, workspace=workspace)

@mcp.tool()
def explain_lineage(block_id: str, workspace: str = '') -> Any:
    """Show the full lineage tree for a block — composed_from + depends_on paths.

    Args:
        block_id: the lb: prefixed block ID or CNAE name to trace
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.explain_lineage(block_id, workspace=workspace)

@mcp.tool()
def lint_store(workspace: str = '') -> Any:
    """Lint the logic-base for schema violations, stale references, and tier-law breaks.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.lint_store(workspace=workspace)

@mcp.tool()
def validate_store(workspace: str = '') -> Any:
    """Run the full 11-gate validation sweep across every block in the logic-base.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.validate_store(workspace=workspace)

@mcp.tool()
def deduplicate_store(workspace: str = '') -> Any:
    """Remove exact-duplicate blocks (same dedupe_key) from the logic-base.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.deduplicate_store(workspace=workspace)

@mcp.tool()
def rebuild_indexes(workspace: str = '') -> Any:
    """Rebuild CNAE, fingerprint, lineage and composition indexes from scratch. Call this after
    bulk imports or manual shard edits to restore index consistency.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects
    """
    return _client.rebuild_indexes(workspace=workspace)


def launch() -> None:
    mcp.run()


if __name__ == "__main__":
    launch()
