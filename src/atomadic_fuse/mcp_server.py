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
    """Walk the full tier dependency chain (T5 -> T0) for an intent."""
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


# ── 8 engine tools (Fuse v1.0.0 — mirror of local fuse-engine-mcp surface) ──
# These proxy to the hosted endpoints which currently return curated/stub
# responses with `local_route` pointing at fuse-engine-mcp.exe for full
# execution. Wave B will wire hosted backend execution.

@mcp.tool()
def scan(directory: str, languages: str = "python,typescript,rust") -> Any:
    """Walk a directory and return CNAE atoms found in source files."""
    return _client.scan(directory, languages=languages)


@mcp.tool()
def discover(workspace: str = "") -> Any:
    """Cluster, score, and discover emergent dependency chains. The emergent finder."""
    return _client.discover(workspace=(workspace or None))


@mcp.tool()
def synthesize(output: str = "./synthesized", workspace: str = "", dry_run: bool = False) -> Any:
    """Full synthesis pipeline: scan -> absorb -> cluster -> score -> chain -> theme -> emit."""
    return _client.synthesize(output=output, workspace=(workspace or None), dry_run=dry_run)


@mcp.tool()
def emit(output: str, workspace: str = "") -> Any:
    """Emit product directory scaffolds for ranked products (T0-T5)."""
    return _client.emit(output=output, workspace=(workspace or None))


@mcp.tool()
def validate(name: str) -> Any:
    """Validate a CNAE name against the canonical action_entity_scope vocabulary."""
    return _client.validate(name)


@mcp.tool()
def status(workspace: str = "") -> Any:
    """Read-only logic-base status: atom count, shards, ledgers, manifest."""
    return _client.status(workspace=(workspace or None))


@mcp.tool()
def search(query: str, workspace: str = "") -> Any:
    """Substring + CNAE search across the logic-base."""
    return _client.search(query, workspace=(workspace or None))


@mcp.tool()
def logic_map(workspace: str = "") -> Any:
    """Return the full composition graph of the logic-base (atom -> dependencies, by tier)."""
    return _client.logic_map(workspace=(workspace or None))


@mcp.tool()
def langs() -> Any:
    """List all supported language families grouped by emitter target."""
    return _client.langs()


@mcp.tool()
def polyglot(name: str, languages: str = "", workspace: str = "") -> Any:
    """Emit a specific logic-base atom as polyglot code across language targets."""
    return _client.polyglot(name, languages=languages, workspace=(workspace or None))


@mcp.tool()
def show(name: str, workspace: str = "") -> Any:
    """Drill into one atom: full contract, source, and next_actions guidance."""
    return _client.show(name, workspace=(workspace or None))


# ── v1.1.0 tools: store governance + telemetry ───────────────────────────────

@mcp.tool()
def quickstart(directory: str, output: str = "./_fuse_out", permissive: bool = True) -> Any:
    """One-shot onboarding: scan a directory, absorb atoms, synthesize and emit products.

    The fastest path from a messy repo to a shippable package. Permissive mode
    (default) harvests all functions regardless of CNAE naming — ideal for first runs.

    Args:
        directory: absolute path of the source tree to compile.
        output: output directory for emitted products (default ./_fuse_out).
        permissive: if True (default), harvest any function found — behavior-based
            classification proposes canonical CNAE names automatically.
    """
    return _client.quickstart(directory, output=output, permissive=permissive)


@mcp.tool()
def friction(workspace: str = "", kind: str = "", n: int = 50, summary: bool = False) -> Any:
    """Read the Friction Protocol telemetry log.

    The Friction Protocol records every UX friction event (zero-result hints,
    errors, empty inputs, bad paths) so you can see what's causing the most
    friction in your workflow. Returns recent events or a summary rollup.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects.
        kind: filter by event kind (e.g. 'zero_atoms', 'workspace_missing').
        n: max events to return (default 50).
        summary: if True, return counts grouped by kind instead of raw events.
    """
    return _client.friction(workspace=(workspace or None), kind=(kind or ""), n=n, summary=summary)


@mcp.tool()
def promote_hypotheses(workspace: str = "", dry_run: bool = False) -> Any:
    """Promote hypothesis candidates in the logic-base to verified status.

    Scans all candidate blocks, runs the 11-gate promotion pipeline, and
    writes canonical blocks. Use dry_run=True to preview what would be promoted
    without making changes.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects.
        dry_run: if True, report what would be promoted without writing.
    """
    return _client.promote_hypotheses(workspace=(workspace or None), dry_run=dry_run)


@mcp.tool()
def promote_candidate(block_id: str, workspace: str = "") -> Any:
    """Promote a specific candidate block by ID through the 11-gate pipeline.

    Args:
        block_id: the lb: prefixed block ID to promote.
        workspace: absolute path to the logic-base workspace; '' auto-detects.
    """
    return _client.promote_candidate(block_id, workspace=(workspace or None))


@mcp.tool()
def explain_lineage(block_id: str, workspace: str = "") -> Any:
    """Show the full lineage tree for a block — composed_from + depends_on paths.

    Args:
        block_id: the lb: prefixed block ID or CNAE name to trace.
        workspace: absolute path to the logic-base workspace; '' auto-detects.
    """
    return _client.explain_lineage(block_id, workspace=(workspace or None))


@mcp.tool()
def lint_store(workspace: str = "") -> Any:
    """Lint the logic-base for schema violations, stale references, and tier-law breaks.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects.
    """
    return _client.lint_store(workspace=(workspace or None))


@mcp.tool()
def validate_store(workspace: str = "") -> Any:
    """Run the full 11-gate validation sweep across every block in the logic-base.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects.
    """
    return _client.validate_store(workspace=(workspace or None))


@mcp.tool()
def deduplicate_store(workspace: str = "") -> Any:
    """Remove exact-duplicate blocks (same dedupe_key) from the logic-base.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects.
    """
    return _client.deduplicate_store(workspace=(workspace or None))


@mcp.tool()
def rebuild_indexes(workspace: str = "") -> Any:
    """Rebuild CNAE, fingerprint, lineage and composition indexes from scratch.

    Call this after bulk imports or manual shard edits to restore index consistency.

    Args:
        workspace: absolute path to the logic-base workspace; '' auto-detects.
    """
    return _client.rebuild_indexes(workspace=(workspace or None))


def launch() -> None:
    mcp.run()


if __name__ == "__main__":
    launch()