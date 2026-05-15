# Atomadic Fuse

> **Spaghetti to Shippable.** Point at one messy repo. Get back a clean, monadic, polyglot, deployable package — with a CLI, an MCP server, tests, and a deploy bundle. One command.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/PyPI-atomadic--fuse-blue.svg)](https://pypi.org/project/atomadic-fuse/)
[![Status](https://img.shields.io/badge/status-public%20beta-orange.svg)](https://atomadic.tech)

## What it does

Fuse is the per-repo compiler from the Atomadic stack. Feed it any source repo (Python, TypeScript, Rust, Go, Java, C, Ruby, PHP, Swift, C#, COBOL — 16 languages), and it emits:

- **A clean Python package** with a 5-tier dependency law (no upward imports, ever).
- **A CLI** with the same verbs your operators already know: `classify`, `catalog`, `materialize`, `absorb`, `compile`, `capabilities`, `intent`, `doctor`.
- **An MCP server** wired to each capability as a tool.
- **A pyproject.toml**, basic tests, a Dockerfile, a Cloudflare Worker config, a `.well-known/mcp.json` manifest, and a `pricing.json`.

**Polyglot in, monadic out.** Deterministic-by-construction: same input bytes → same output bytes (verified at iteration 1 of the convergence bound).

## Install

```bash
pip install atomadic-fuse
```

Or:

```bash
git clone https://github.com/atomadictech/atomadic-fuse.git
cd atomadic-fuse && pip install -e .
```

## Quick start

```bash
# Point Fuse at any messy repo
fuse compile /path/to/some/repo --output ./fused

# See what verbs are wired
fuse list

# Classify any function by behavior (AST → action_entity_scope)
fuse classify "def fingerprint(b): return hashlib.sha256(b).hexdigest()" "fingerprint"
# -> ["build", 0.7487]

# Catalog query
fuse catalog "validate trust"
```

## CLI verbs

`fuse <verb> [args...]` — the operator-facing surface.

| Verb | Description |
|---|---|
| `compile` | Marquee: messy repo → clean shippable package. Spaghetti to Shippable. |
| `classify` | Classify any function by AST behavior (returns `action`, confidence). |
| `absorb` | Add a repo to your Logic-Base (incremental, deduped). |
| `catalog` | Query the catalog for atoms matching a behavior shape. |
| `materialize` | Write the atom corpus to disk (one file per atom). |
| `capabilities` | List emergent cross-source chains in your catalog. |
| `intent` | Natural-language intent → emit a custom themed product. |
| `doctor` | Health probe across your workspace. |

…plus 80+ SLS-lineage verbs lifted from the catalog as deferred shims with full source provenance.

## MCP server

```bash
fuse-mcp
```

Exposes every verb as an MCP tool. Drop into Claude Desktop, Cursor, Windsurf, or any MCP-aware client:

```json
{
  "mcpServers": {
    "atomadic-fuse": {
      "command": "fuse-mcp"
    }
  }
}
```

## Why it works

Fuse classifies functions by what they **do**, not what they're **named**. A function named `helper_42` that hashes bytes gets classified as `build_fingerprint_static` with confidence `TAU_TRUST = 1820/1823 ≈ 0.9984` — a constant derived from formally-verified lattice mathematics (Leech, Niemeier). Functions below the noise floor `σ₀ = 1/√196560` are dropped. The same engine self-emits: it can compile its own source byte-identically.

## Pricing

- **Free tier**: 3 calls/day, no signup, BYO API key for higher tiers.
- **Pro**: $8 → 500 calls.
- **Team / Enterprise**: see [atomadic.tech/pricing](https://atomadic.tech).
- **x402 USDC** micropayments supported (autonomous agents pay per call).

Buyer-funded: agents that need Fuse pay agents-to-agents via `X-PAYMENT` (EIP-712). No human in the loop.

## Live ecosystem stats

Pulled from a Cloudflare-hosted source-of-truth manifest:

```bash
curl https://sot.atomadic.tech/SoT.json | jq .atoms_total
```

Live as of writing: **113,533+ atoms** across **56+ source repos**, 8 emitted products, byte-deterministic self-emit.

## Sibling products

- **[atomadic-nexus-sdk](https://github.com/atomadictech/atomadic-nexus-sdk)** — Trust Layer for the Agent Economy. Wraps Fuse purchases with x402 + Stripe + reputation.
- **atomadic-marketplace** — sell + buy + rate logic chains (coming).
- **atomadic-harvest** — production lane that grows the catalog (coming).

## Authors

Atomadic Tech. Headed by Thomas Ralph Colvin IV. Axiom 0: `∀t: |∂L/∂t| ≤ 0` — The Love Invariant, authored by Jessica Mary Colvin. Never negotiated.

## License

MIT. See [LICENSE](./LICENSE).
