# Atomadic Fuse SDK

Spaghetti to Shippable.

Fuse is the public SDK for turning repository chaos into a clearer, more verifiable build workflow.

In plain English: Fuse helps you inspect a codebase, understand what is in it, search for useful building blocks, validate outputs, and drive agent or automation workflows through a typed Python client, a command-line tool, or MCP.

In technical terms: this repository ships the public Python package `atomadic-fuse`, the `fuse` CLI, the `fuse-mcp` stdio server, example workflows, and a bundled seed logic-base used for local bootstrapping.

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

The Python package exposes **34 `FuseClient` methods** for local and hosted integration. The **hosted MCP worker** at `https://fuse.atomadic.tech/mcp` exposes **14 read-only public tools** (master tier unlocks 20 additional operator tools). Use `fuse-sdk` CLI for hosted verbs only; use local `fuse-engine` for full emit/repair.

### Hosted public MCP tools (14)

These match `atomadic-ops/workers/atomadic-fuse-api/src/tool_manifest.json` visibility `public`:

- `classify`, `catalog`, `doctor`, `fuse_recovery_status`, `verify_block`
- `search_intent`, `explain_block`, `usage_stats`, `scan`, `validate`
- `status`, `search`, `show`, `langs`

Auth: `Authorization: Bearer $ATOMADIC_FUSE_API_KEY` (pro) or `$ATOMADIC_MASTER_KEY` (all tools). Free anonymous tier: 3 calls/day per verb (`classify` unmetered).

### Full FuseClient methods (34)

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

The SDK ships **`fuse-sdk`** (public hosted read-only verbs) and **`fuse-mcp`** (local stdio MCP):

```bash
fuse-sdk doctor
fuse-sdk classify --body-text "def foo(): return 1"
fuse-sdk list   # hosted + local verbs
```

Hosted verbs (14): classify, catalog, doctor, fuse_recovery_status, verify_block, search_intent, explain_block, usage_stats, scan, validate, status, search, show, langs.

Local-only: `init`, `seed-info`, `list`.

Example:

```bash
fuse-sdk doctor
fuse-sdk search --query validate
```

## Spaghetti to Shippable (S2S)

**Tagline:** Spaghetti to Shippable in one call.

S2S is the single-repo pipeline that ingests one messy repository, runs security + heal + emit stages, passes a **fitness gate**, and wraps a **T5 product bow** (README, `product.json`, local logic-base shard).

| Surface | What it is | S2S support |
|---------|------------|-------------|
| **Hosted `FuseClient`** | HTTP client to `fuse.atomadic.tech` | Catalog, compile, verify — **not** full local S2S |
| **Local Fuse engine** | `atomadic-fuse-next` (dev) → `atomadic-fuse` (stable) | **`fuse s2s`** / MCP `spaghetti_to_shippable` |

```powershell
# Local engine only (fuse-next today)
./fuse.cmd s2s --source C:\path\to\spaghetti --output C:\path\to\product          # dry-run
./fuse.cmd s2s --source C:\path\to\spaghetti --output C:\path\to\product --live # trust-gated
```

- **Dry-run (default):** plan and stage report; no disk mutations; no trust token.
- **Live:** heal, emit, fitness gate, T5 bow — requires `gate_intent` PASS + trust attestation (`ATOMADIC_TRUST_TOKEN` or Nexus).
- **Single repo only** on the public profile; multi-repo harvest/train stays T6 internal.

Deep dive: [docs/S2S_AND_ENGINE_BOUNDARY.md](docs/S2S_AND_ENGINE_BOUNDARY.md)  
Omega pipeline reference: [../docs/SPAGHETTI_TO_SHIPPABLE.md](../docs/SPAGHETTI_TO_SHIPPABLE.md)

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
- [S2S and Engine Boundary](docs/S2S_AND_ENGINE_BOUNDARY.md)
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


