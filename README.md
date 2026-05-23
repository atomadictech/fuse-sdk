# Atomadic Fuse SDK

Spaghetti to Shippable.

Fuse is the public SDK for turning repository chaos into a clearer, more verifiable build workflow.

In plain English: Fuse helps you inspect a codebase, understand what is in it, search for useful building blocks, validate outputs, and drive agent or automation workflows through a typed Python client, a command-line tool, or MCP.

In technical terms: this repository ships the public Python package `atomadic-fuse`, the `fuse` CLI, the `fuse-mcp` stdio server, example workflows, and a bundled seed logic-base used for local bootstrapping.

## What's new in 1.3.0

- **Sovereign emitter domain dispatch** — emitters route by domain (`stripe`, `github`, `cloudflare`, `surfaces`, `notify`, `validate`). Every emitted atom is complete, deterministic, executable code. The stub hunter gate blocks any stub before it touches disk.
- **Full release pipeline** — `ship_release_sovereign` runs 9 stages: preflight gate → sync next→stable → bump version → changelog → manifest + tag → commit and push → CF deploy → notify. One call ships.
- **Sovereign preflight gate** — 7 gates run before any release: axiom check, audit gaps, stub scan, heal if needed, verify heal cycle, Nexus trust gate (confidence ≥ 0.85), hallucination oracle (risk < 0.15). Release blocks if any gate fails.
- **Auto-correction pipeline** — `post_write` hook runs on every `.py` write: ruff lint → CNAE compliance scan → `decouple_file_stateful` → `heal_workspace_stateful` → `stub_hunter_composite`. Agents write; the pipeline corrects.
- **Swarm hivemind wiring** — sessions register in the Atomadic Swarm at startup. New atoms emitted during a session become live for all agents without restart.
- **Hot-reload architecture** — hook scripts reload from disk per invocation. MCP servers fire `notifications/tools/list_changed` when new atoms are registered — agents see new tools without session restart.
- **814 atoms, 0 stubs** — stub hunter gate confirmed zero stubs across the full engine. 7 new tier_2 composites, 5 new tier_3 stateful atoms added.
- **Fuse-next → stable sync** — `sync_next_to_stable_stateful` MD5-diffs the dev workspace before every stable publish. Stable never receives a partial or half-baked commit.

## Why Fuse

Most AI-assisted build pipelines fail in familiar ways:
- the same workflow behaves differently across tools
- generation is easier than verification
- agent integrations drift away from direct developer tooling
- repo understanding, search, emit, and validation live in separate ad hoc scripts

Fuse gives you one public integration surface for:
- typed Python calls with `FuseClient`
- local CLI access with `fuse`
- MCP-based agent integration with `fuse-mcp`
- verification and store-health workflows that are explicit instead of hidden behind internal tooling

## What You Can Do

### For developers
- scan and classify repositories before making changes
- absorb a repo into a logic-base-backed workflow
- search by intent, inspect lineage, and explain blocks
- synthesize, emit, and compile through one client surface
- lint, validate, deduplicate, and rebuild indexes for store maintenance

### For agents and tooling teams
- expose Fuse through MCP without writing a custom adapter
- use the same public workflow surface across IDEs, scripts, CI jobs, and agent runtimes
- build verification-first automations around methods like `verify_block`, `validate`, `doctor`, and `status`

### For non-technical readers
- Fuse is the part that helps teams go from "we have a messy repo and too many brittle scripts" to "we have a repeatable interface for understanding, validating, and shipping work"
- it does not promise magic autopilot from a slogan alone; it gives you a concrete tool surface you can script, automate, and inspect

## Install

```bash
pip install atomadic-fuse
```

Optional extras:

```bash
pip install "atomadic-fuse[mcp]"
pip install "atomadic-fuse[gui]"
pip install "atomadic-fuse[mcp,gui]"
```

## Quick Start

```python
from atomadic_fuse import FuseClient

client = FuseClient()

print(client.scan('./repo'))
print(client.search_intent('validate and route input', tier='t2', limit=5))
print(client.verify_block('lb:t2:compose_path_composite:bd7e1d030ef5'))
print(client.synthesize('./repo'))
```

## Public API Surface

`FuseClient` currently exposes 34 public methods.

Repository workflows:
- `compile`
- `classify`
- `absorb`
- `scan`
- `discover`
- `synthesize`
- `emit`
- `intent`

Search, explain, and mapping:
- `catalog`
- `search`
- `search_intent`
- `logic_map`
- `compose_stack`
- `explain_block`
- `explain_lineage`
- `show`
- `langs`
- `polyglot`

Verification and operations:
- `doctor`
- `status`
- `validate`
- `verify_block`
- `usage_stats`
- `fuse_recovery_status`

Store and promotion helpers:
- `quickstart`
- `friction`
- `promote_hypotheses`
- `promote_candidate`
- `lint_store`
- `validate_store`
- `deduplicate_store`
- `rebuild_indexes`
- `emit_corpus`
- `capabilities`

Source of truth: [src/atomadic_fuse/client.py](src/atomadic_fuse/client.py)

## CLI Surface

The SDK also ships a `fuse` CLI with these public verbs:
- `init`
- `seed-info`
- `compile`
- `classify`
- `absorb`
- `catalog`
- `capabilities`
- `intent`
- `doctor`
- `list`

Example:

```bash
fuse doctor
fuse compile ./repo --output ./_fuse_out
fuse intent "turn this repo into a cleaner package" --output ./_intent_out
```

## MCP Surface

For agent runtimes, install the MCP extra and configure `fuse-mcp`:

```json
{
  "mcpServers": {
    "atomadic-fuse": {
      "command": "fuse-mcp"
    }
  }
}
```

Hosted MCP endpoint:
- `https://fuse.atomadic.tech/mcp`

## Pricing

Verified from the public pricing page at `atomadic.tech/pricing` on 2026-05-22.

API key credit packs:
- Starter: 500 calls for $8 one-time, no expiry
- Best Value: 2,500 calls for $30 one-time, no expiry
- Power: 10,000 calls for $98 one-time, no expiry

Public pricing notes currently shown on the site:
- credits work across 75+ endpoints
- card checkout is available
- USDC on Base L2 is available
- x402-style pay-per-call flows are described for autonomous agents

Pricing and endpoint coverage can change. For current public details, use:
- `https://atomadic.tech/pricing`
- `https://atomadic.tech/openapi.json`
- `https://atomadic.tech/api-status`

## Documentation

- [Docs Index](docs/README.md)
- [Whitepaper](docs/WHITEPAPER.md)
- [Architecture](docs/ARCHITECTURE.md)
- [MCP Quickstart](docs/MCP_QUICKSTART.md)
- [Security and Privacy](docs/SECURITY_AND_PRIVACY.md)
- [Operations Guide](docs/OPERATIONS.md)
- [Benchmarks Guidance](docs/BENCHMARKS.md)
- [Use Cases](docs/USE_CASES.md)
- [Comparison Guide](docs/COMPARISON.md)

## Public Boundary

This repository is a public SDK surface.
- it documents package contracts, observable workflows, and integration patterns
- it does not document private engine internals or unpublished orchestration systems
- public claims in this repo should be reproducible from source, tests, examples, or public endpoints

## License

MIT. See [LICENSE](LICENSE).


