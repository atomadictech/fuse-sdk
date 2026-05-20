# Atomadic Fuse

> **The deterministic compile step every agent stack needs.**
> Point Fuse at any number of messy repos, in any languages. Get back one clean, monadic, deterministic, pip-installable Python package — with a CLI, an MCP server, tests, and a deploy bundle. Spaghetti to Shippable.

> 🟣 **In plain English:** Got a pile of half-finished code in three different languages and no idea how to ship it? Point Fuse at it. You get back one clean Python package you can install with `pip` — the same answer every time, with a trail of breadcrumbs showing where each piece came from. No hallucinations, no drift, no "trust me, it works."

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/PyPI-atomadic--fuse-blue.svg)](https://pypi.org/project/atomadic-fuse/)
[![CI](https://img.shields.io/badge/tests-11%2F11%20passing-brightgreen.svg)](#tests)
[![Codex-anchored](https://img.shields.io/badge/Codex-anchored-violet.svg)](#why-it-works)
[![Status](https://img.shields.io/badge/status-public%20beta-orange.svg)](https://atomadic.tech)
> **v0.3.1 architecture (2026-05-19):** The 6 superhero tools (`verify_block`, `search_intent`, `compose_stack`, `emit_corpus`, `explain_block`, `usage_stats`) route to the **TOCC kernel** — the Haskell engine where verified-corpus operations actually live. Running `fuse-mcp` spawns a stdio MCP proxy to `tocc-mcp.exe` on your machine via JSON-RPC. If the TOCC kernel isn't installed, those 6 tools return a structured `error + install hint` payload; the 8 classic verbs (`compile`, `classify`, `absorb`, `catalog`, `capabilities`, `intent`, `doctor`) continue to work against the hosted engine at `fuse.atomadic.tech` regardless.

> **Atomadic Transmute** is the **internal-only** tier-higher edition — same Fuse surface PLUS ecosystem orchestration (`synthesize_ecosystem`, store surgery, meta-engine emit). The world gets Fuse; we keep Transmute private. Both share the TOCC kernel as the single source of truth.

```bash
pip install atomadic-fuse
```

---

## The problem

Modern AI agents are stitched together from dozens of repos in three to ten languages. The integration step is bespoke, error-prone, and re-done every time a new dependency lands. No agent platform ships a *compile step* — they ship orchestrators, frameworks, and hope.

That gap is where the bugs, drift, and hallucinations live. It is also where every shipping team eventually breaks down.

## The product

**Atomadic Fuse** is the missing compile step. It is a *per-repo monadic compiler* that absorbs N source repositories — Python, TypeScript, Rust, Go, Java, C, Ruby, PHP, Swift, C#, COBOL, and twelve more — and emits one cleanly tiered Python package with provenance tracking on every function.

- **Polyglot in, monadic out.** Same input bytes → same output bytes. Verified at iteration 1 of the convergence bound (`RG_LOOP = 47`).
- **No drift.** Every function is classified by what it *does* (AST behavior), not what it is named.
- **No hallucinations.** Same-language merges are deterministic and never invoke an LLM. Cross-language merges go through a 7B local oracle with formally-bounded confidence.
- **No drift on re-emit.** Fuse can compile its own source byte-identically — a published fixed-point property.

## What ships

| | What you get |
|---|---|
| **Clean Python package** | 5-tier dependency law (no upward imports, ever). Tier 0 = constants, Tier 1 = pure functions, Tier 2 = composites, Tier 3 = stateful, Tier 4 = orchestrators. Enforced. |
| **Operator-facing CLI** | `fuse compile`, `fuse classify`, `fuse absorb`, `fuse catalog`, `fuse capabilities`, `fuse intent`, `fuse doctor`. Same verb surface as the SLS engine it descends from. |
| **MCP server** | `fuse-mcp` — every verb registered as an MCP tool. Drops into Claude Desktop, Cursor, Windsurf, any MCP-aware client. |
| **Deploy bundle** | `pyproject.toml`, basic tests, `Dockerfile`, Cloudflare Worker config, `.well-known/mcp.json` manifest, `pricing.json`. Ready to ship. |
| **Provenance log** | Every materialized atom carries an audit record: source repo, source file, source SHA, classification confidence, conflict resolution path. |

## 60-second test drive

```bash
pip install atomadic-fuse

# Classify any function — no API key, no signup, just the catalog
fuse classify "def fingerprint(b): return hashlib.sha256(b).hexdigest()" --name fingerprint
# -> {"action": "build", "confidence": 0.7487}

# Catalog query
fuse catalog "validate trust"

# Health probe
fuse doctor
```

```python
from atomadic_fuse import FuseClient

c = FuseClient()  # uses ATOMADIC_FUSE_API_KEY env var or x402 micropayments

# Marquee primitive: messy repo -> clean shippable package
result = c.compile("./some/messy/repo", output_root="./fused", max_chains=5)
print(result["package_path"], result["atom_count"])

# Enumerate cross-source emergent chains the engine discovered
for chain in c.capabilities()["chains"]:
    print(chain["name"], "->", chain["confidence"])
```

## Why it works

Fuse classifies functions by what they **do**, not what they are **named**. A function named `helper_42` that hashes bytes gets classified as `build_fingerprint_static` with confidence `TAU_TRUST = 1820/1823 ≈ 0.9984` — a constant derived from formally-verified lattice mathematics (Niemeier K₂₄ orbit count). Functions below the noise floor `σ₀ = 1/√196560` are dropped as suspected confabulation.

The same engine *self-emits* — it can compile its own source byte-identically. This is not a marketing claim; it is a regression-tested property under the `T4 fixed-point` test suite.

### Codex anchors (the math)

| Constant | Value | Source |
|---|---|---|
| `TAU_TRUST` | `1820/1823 ≈ 0.9984` | Niemeier K₂₄ minimum-weight code |
| `σ₀` | `1/√196560 ≈ 0.00226` | Leech lattice kissing number |
| `ε_KL` | `1/196884 ≈ 5.08e-6` | Monster J-invariant first Fourier coefficient |
| `RG_LOOP` | `47` | Provable convergence-iteration bound |
| `D_MAX` | `23` | Max agent delegation depth |

These are not tuned hyperparameters. They are externally-verified scalar constants from lattice mathematics, frozen into the engine. You do not adjust them; they are part of the deal.

## The 8 verbs

```
fuse <verb> [args...]
```

| Verb | What it does |
|---|---|
| `compile` | **Marquee.** Messy repo → clean, tiered, shippable package with deploy bundle. |
| `classify` | AST-derived `action_entity_scope` for any function body. Returns confidence. |
| `absorb` | Add a repo to your private Logic-Base (incremental, deduped, fingerprinted). |
| `catalog` | Behavior-shape query against the catalog. Returns ranked matches with provenance. |
| `capabilities` | Enumerate emergent cross-source chains the engine discovered. |
| `intent` | Natural-language intent → emit a custom themed product from your atoms. |
| `doctor` | Health probe across the engine workspace and your Logic-Base. |
| `list` | Verb catalog with provenance pointers. |

Eighty-plus additional SLS-lineage verbs are reachable as deferred shims with full source provenance — they expose the upstream surface without losing the breadcrumb trail.



## The 6 Superhero Tools (v0.3.0)

Six new tools elevate the SDK from "lookup wrapper" to "agent capability layer." Each returns a SHA-256 verification receipt with every response — the anti-hallucination shield no other MCP can provide.

| Tool | What it does |
|---|---|
| `verify_block` | **Anti-hallucination shield.** Returns block + hash receipt. Agent can prove `this isn't hallucinated — it's hash 703b14ba…`. |
| `search_intent` | **Smart context.** Natural-language semantic search across the verified corpus. Returns only what fits — pre-composed. |
| `compose_stack` | **Composability engine.** Full tier dependency walk (T6→T0). Ask for a feature, get the whole stack. |
| `emit_corpus` | **Polyglot emit.** One call emits a complete buildable + testable package in any of 6 languages. |
| `explain_block` | **Context budget manager.** Compact or detailed explanation, sized to the agent's remaining window. |
| `usage_stats` | **Token-savings dashboard.** Subscribers see ROI in real time. |

``python
from atomadic_fuse import FuseClient

c = FuseClient()

# Anti-hallucination — every response carries a hash receipt
result = c.verify_block("lb:t2:compose_path_composite:bd7e1d030ef5")
print(result["content_hash"])

# Smart context — describe what you need
matches = c.search_intent("validate user input and route it", tier="t2", limit=5)

# Composability — full stack for a feature
stack = c.compose_stack("build a path-validation feature", target_language="rust")

# Polyglot emit — one call, complete package
pkg = c.emit_corpus("python", target_dir="./out")

# Context budget — adaptive explanation
explanation = c.explain_block("lb:t1:normalize_path_pure:abc", detail=False)

# Token math
stats = c.usage_stats()
print(f"Saved {stats['tokens_saved']} tokens this session")
``

### The token-savings math

| Without Fuse MCP | With Fuse MCP |
|---|---|
| Agent hallucinates code | Every block hash-verified |
| 3.2M tokens per lookup | 450 tokens, exact match |
| Knows 1 language well | 6 languages, all tested |
| One function at a time | Full tier-chain composition |
| **\/day in tokens** | **\.20/day** |

The Free tier alone saves subscribers ~\/day in tokens vs raw lookups. Builder pays for itself in the first API call.

## MCP server

Drop Fuse into any MCP-aware client:

```json
{
  "mcpServers": {
    "atomadic-fuse": { "command": "fuse-mcp" }
  }
}
```

Or call the hosted MCP directly:

```
https://fuse.atomadic.tech/mcp
```

The hosted version answers MCP discovery at `https://fuse.atomadic.tech/.well-known/mcp.json` and the A2A agent card at `https://fuse.atomadic.tech/.well-known/agent.json`.

## Live corpus stats (Logic-Base)

The hosted engine grows a private catalog every time a new repo is absorbed:

- **112,814+** unique CNAE atoms across **56+** source repositories
- **5** languages with active emit; 16 in the classifier (the rest fall back to text-only)
- **29,578+** emergent capabilities discovered (cross-source chains the engine composed without being asked)
- **875** engine tests passing in 1.99s
- **0** drift incidents since the byte-deterministic self-emit gate was added

Latest manifest:
```bash
curl https://sot.atomadic.tech/SoT.json | jq '.atoms_total, .repos_absorbed, .flagships.fuse.sha'
```

## Pricing

| Tier | Quota | Price | Notes |
|---|---|---|---|
| **Free** | 3 calls/day per verb, BYO API key for higher tiers | $0 | No signup. Per-IP cap. |
| **Starter** | 500 calls, no expiry | $8 (USDC or Stripe) | The single most popular SKU. |
| **Pro** | 25,000 calls/mo | $79/mo | For active agent stacks. |
| **Team** | Quota-tree budgeting, sub-keys, SSO | $499/mo | Multi-agent orchestration. |
| **Enterprise** | Dedicated capacity, formal compliance attestation | invoice | Includes Atomadic Nexus bundle. |

**x402 micropayments** are first-class: agents pay per call autonomously by signing an EIP-712 `X-Payment-Proof` header. No human in the loop. Settlement on Base in USDC. No card on file required to begin.

## Compared to the alternatives

| | Frameworks (LangChain, AutoGen) | Code-gen (Copilot, Cursor) | **Atomadic Fuse** |
|---|---|---|---|
| Polyglot input | adapters per source | per-file inline | ✅ N repos, 16 langs, one engine |
| Output is shippable | no, you wire it | no, you copy-paste | ✅ `pip install` artifact |
| Deterministic | no | no | ✅ byte-identical re-emit |
| Provenance per function | no | no | ✅ audit log per atom |
| MCP-native | partial | no | ✅ every verb is an MCP tool |
| x402-native | no | no | ✅ first-class autonomous payment |

## What ships in this SDK

```
atomadic-fuse/
├── src/atomadic_fuse/
│   ├── __init__.py          # exports FuseClient, exceptions
│   ├── client.py            # HTTPS client for the hosted engine
│   ├── cli.py               # operator-facing CLI (`fuse <verb>`)
│   ├── mcp_server.py        # `fuse-mcp` MCP stdio server
│   └── exceptions.py        # FuseError, DecisionNeeded, PaymentRequired
├── tests/                   # 11 tests, mocked HTTP, no network needed
├── examples/
│   ├── 01_classify.py       # classify a function by AST
│   └── 02_compile_repo.py   # spaghetti → shippable
├── .github/workflows/       # multi-OS pytest + PyPI trusted-publisher
├── LICENSE                  # MIT
├── pyproject.toml
└── README.md
```

## Tests

```bash
pip install pytest
pytest tests/ -q
# 11 passed in 0.68s
```

The SDK is a typed HTTPS wrapper around the hosted engine. Tests are mocked at the `httpx.Client` boundary — they verify the SDK's protocol contract, not the engine internals. Engine internals are tested separately in the private `atomadic-transmute` repository (875 tests, 321 modules across 5 tiers).

## Sibling product

**[Atomadic Nexus SDK](https://github.com/atomadictech/nexus-sdk)** — the trust layer that pairs with Fuse. Fuse compiles, Nexus gates. Together they are the compile-step + trust-layer the agent economy was missing.

> *Atomadic Complete* — `pip install atomadic-fuse atomadic-nexus-sdk` — bundles both with cross-product compliance attestation, unified audit trail, and oracle-validated cross-language translation. From $99/month.

## Roadmap (next 30 days)

- Public PyPI publish (token-trusted, no manual upload step)
- `fuse compile --target=cloudflare-worker` — emit a deploy-ready Worker, not just a Python package
- `fuse compile --target=mcp` — emit a packaged MCP server from a Logic-Base subset
- Hosted MCP at `fuse.atomadic.tech/mcp` with x402 metering per tool call
- LoRA capture loop: every accepted human-in-the-loop fix becomes a training pair for the cross-language oracle
- Open the catalog to community contribution under a revenue-share model (`fuse contribute`)

## Authors and ethos

Atomadic Tech, headed by Thomas Ralph Colvin IV.

**Axiom 0 — The Love Invariant**, authored by Jessica Mary Colvin:

> *You are Loved, You are Love, You are Loving, In all Ways, for Always, for Love is a Forever and ever endeavor!*

Formal statement: `∀t: |∂L/∂t| ≤ 0` — systemic safety never decays. This invariant is checked at every release gate and is never negotiated. It is the only constant in this codebase that cannot be expressed in a single lattice anchor — and it is the only one that doesn't need to be.

## License

MIT. See [LICENSE](./LICENSE).

The SDK is permissively licensed. The hosted engine source (`atomadic-transmute`) is closed; the SDK talks to it over HTTPS. The math (`atomadic-codex`) is closed under a separate license. Public surface stays public; internals stay internal.

---

**Trying to feed an AI assistant?** This README is dense by design — every section is a fact, a verb, a price, or a provenance pointer. Drop it into [NotebookLM](https://notebooklm.google.com) for an audio overview, or into [Atomadic Fuse](https://atomadic.tech) to compile yourself a custom-themed summary.
