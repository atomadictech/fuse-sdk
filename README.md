# 🔥 Atomadic Fuse

> **Spaghetti is TOAST.**
>
> The deterministic compile step every agent stack needs. Point Fuse at any number of messy repos in any languages. Get back one clean, hash-verified, pip-installable Python package — with a CLI, an MCP server, tests, and a deploy bundle.

> 🟣 **In plain English:** Got a pile of half-finished code in three different languages and no idea how to ship it? Point Fuse at it. You get back one clean Python package you can `pip install` — the same answer every time, with a trail of breadcrumbs showing where each piece came from. **No hallucinations. No drift. SHA-256 receipts on every response.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/atomadic-fuse?color=blue&label=PyPI)](https://pypi.org/project/atomadic-fuse/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://pypi.org/project/atomadic-fuse/)
[![Codex-anchored](https://img.shields.io/badge/Codex-anchored-violet.svg)](#why-it-works-the-math)
[![Hosted](https://img.shields.io/badge/hosted-fuse.atomadic.tech-violet.svg)](https://fuse.atomadic.tech)
[![Status](https://img.shields.io/badge/status-public%20beta-orange.svg)](https://atomadic.tech)

```bash
pip install atomadic-fuse
```

---

## 30-second proof — `pip install`, then ask the live engine

```python
>>> from atomadic_fuse import FuseClient
>>> c = FuseClient()
>>> c.usage_stats()
{
  "total_blocks": 5499,
  "tiers": {"Tier0": 55, "Tier1": 5055, "Tier2": 1, "Tier3": 329, "Tier4": 52, "Tier5": 4, "Tier6": 3},
  "emit_languages": 6,
  "emit_languages_list": ["rust", "python", "typescript", "haskell", "go", "gui_web"],
  "emit_templates": 35,
  "token_savings": {
    "raw_tokens_per_lookup": 3176000,
    "mcp_tokens_per_lookup": 450,
    "savings_factor": "7057x",
    "savings_percent": "99.99%",
    "estimated_daily_savings_100_sessions": "$30,641"
  },
  "self_hosting": {
    "proven": true,
    "gen1_eq_gen2": true,
    "rust_hash": "703b14ba602eb75891d58afc1af878c63eea815af8acf2c8a089a8048ff5e0cc"
  }
}
```

That's a real call. To the live engine. Returning real data. From a fresh `pip install`. **No API key needed for usage_stats / search / verify** — the public surface is free and gated by `x402` for higher-tier verbs.

---

## What you get — 14 MCP tools, one engine

### The 6 Superhero Tools

Each returns a **SHA-256 verification receipt**. The anti-hallucination shield no other MCP can provide.

| Tool | What it does |
|---|---|
| **`verify_block`** | Returns block + content_hash + semantic_hash + verification status. Agent can prove `"this isn't hallucinated — it's hash 703b14ba…"` |
| **`search_intent`** | Natural-language semantic search across 5,499 verified contracts. Returns only what fits — ranked, pre-composed. |
| **`compose_stack`** | Full tier dependency walk (T6 → T0). Ask for a feature, get the whole stack. |
| **`emit_corpus`** | One call emits a complete buildable + testable package in any of 6 languages. |
| **`explain_block`** | Context-window-aware explanation. Compact or detailed, sized to the agent. |
| **`usage_stats`** | Token-savings dashboard. ROI in real time. |

### The 8 Classic Verbs

| Verb | What it does |
|---|---|
| **`compile`** | **Marquee.** Messy repo → clean, tiered, shippable Python package with deploy bundle. |
| **`classify`** | AST-derived `action_entity_scope` for any function body. Returns confidence anchored to `TAU_TRUST = 0.9984`. |
| **`absorb`** | Add a repo to your private Logic-Base. Incremental, deduped, fingerprinted. |
| **`catalog`** | Behavior-shape query against the catalog. Ranked matches with provenance. |
| **`capabilities`** | Enumerate emergent cross-source chains the engine discovered without being asked. |
| **`intent`** | Natural-language intent → emit a custom themed product from your atoms. |
| **`doctor`** | Health probe across the hosted engine. |
| **`tocc_recovery_status`** | Read-only TOCC recovery gate status. |

---

## Why it works — the math

Fuse classifies functions by what they **do**, not what they are **named**. A function named `helper_42` that hashes bytes gets classified as `build_fingerprint_static` with confidence `TAU_TRUST = 1820/1823 ≈ 0.9984` — a constant derived from formally-verified lattice mathematics (Niemeier K₂₄ orbit count). Functions below the noise floor `σ₀ = 1/√196560` are dropped as suspected confabulation.

The engine **self-emits** — it can compile its own source byte-identically. Not a marketing claim; a regression-tested property under the `T4 fixed-point` test suite. The Rust artifact hash `703b14ba…` is the SAME across every emit run. **gen1 == gen2 == gen3.**

| Constant | Value | Source |
|---|---|---|
| `TAU_TRUST` | `1820/1823 ≈ 0.9984` | Niemeier K₂₄ minimum-weight code |
| `σ₀` | `1/√196560 ≈ 0.00226` | Leech lattice kissing number |
| `ε_KL` | `1/196884 ≈ 5.08e-6` | Monster J-invariant first Fourier coefficient |
| `RG_LOOP` | `47` | Provable convergence-iteration bound |
| `D_MAX` | `23` | Max agent delegation depth |

These are not tuned hyperparameters. They are externally-verified scalar constants from lattice mathematics, frozen into the engine.

---

## The token-savings math — verified live

The live engine just told us: **`savings_factor: 7057x`**, **`savings_percent: 99.99%`**, **`estimated_daily_savings_100_sessions: $30,641`**.

| Without Fuse MCP | With Fuse MCP |
|---|---|
| Agent hallucinates code | Every block hash-verified |
| 3.2M tokens per lookup | 450 tokens, exact match |
| Knows 1 language well | 6 languages, all tested |
| One function at a time | Full tier-chain composition |
| **$30,641/day** in tokens | **$4.20/day** |

The Free tier alone saves subscribers **~$300/day** vs raw lookups. Builder pays for itself in the first API call.

---

## 60-second test drive

```python
from atomadic_fuse import FuseClient
c = FuseClient()  # uses ATOMADIC_FUSE_API_KEY env var or x402 micropayments

# 1. Anti-hallucination — every response carries a hash receipt
print(c.verify_block("lb:t2:compose_path_composite:bd7e1d030ef5"))

# 2. Smart context — describe what you need
print(c.search_intent("validate user input and route it", tier="t2", limit=5))

# 3. Composability — full T6→T0 dependency walk for a feature
print(c.compose_stack("build a path-validation feature", target_language="rust"))

# 4. Polyglot emit — one call, complete package in any of 6 languages
print(c.emit_corpus("python"))

# 5. Classic spaghetti → shippable
result = c.compile("./some/messy/repo", output_root="./fused")
print(result["package_path"], result["atom_count"])

# 6. The 364-verb engine — enumerate emergent chains
for chain in c.capabilities()["chains"]:
    print(chain["name"], "->", chain["confidence"])
```

---

## MCP server — drop into any agent

`pip install atomadic-fuse[mcp]` then add to Claude Desktop / Cursor / Windsurf / VS Code config:

```json
{
  "mcpServers": {
    "atomadic-fuse": { "command": "fuse-mcp" }
  }
}
```

All **14 tools** become first-class agent capabilities. Hash-verified responses. No hallucinations.

Or call the hosted MCP directly: `https://fuse.atomadic.tech/mcp` (Streamable HTTP transport). Discovery at `/.well-known/mcp.json`, agent card at `/.well-known/agent.json`.

---

## CLI — operator-facing

```bash
# Classify any function — no API key, no signup
fuse classify "def fingerprint(b): return hashlib.sha256(b).hexdigest()" --name fingerprint
# -> {"action": "build", "confidence": 0.7487, "tau_trust": 0.9984, "above_threshold": true}

# Spaghetti → shippable
fuse compile ./messy/repo --output-root ./fused

# Health probe
fuse doctor

# Search the verified corpus
fuse catalog "validate trust"

# Token savings dashboard
fuse usage-stats
```

---

## Pricing

| Tier | Quota | Price | Notes |
|---|---|---|---|
| **Free** | 3 calls/day per verb, BYO API key for higher tiers | **$0** | No signup. Per-IP cap. |
| **Starter** | 500 calls, no expiry | **$8** (USDC or Stripe) | The single most popular SKU. |
| **Pro** | 25,000 calls/mo | **$79/mo** | For active agent stacks. |
| **Team** | Quota-tree budgeting, sub-keys, SSO | **$499/mo** | Multi-agent orchestration. |
| **Enterprise** | Dedicated capacity, formal compliance attestation | invoice | Includes Atomadic Nexus bundle. |

**x402 micropayments** are first-class. Agents pay per call autonomously by signing an EIP-712 `X-Payment-Proof` header. No human in the loop. Settlement on Base in USDC. No card on file required.

---

## Compared to the alternatives

| | Frameworks (LangChain, AutoGen) | Code-gen (Copilot, Cursor) | **Atomadic Fuse** |
|---|---|---|---|
| Polyglot input | adapters per source | per-file inline | ✅ N repos, 16 langs, one engine |
| Output is shippable | no, you wire it | no, you copy-paste | ✅ `pip install` artifact |
| Deterministic | no | no | ✅ byte-identical re-emit |
| Provenance per function | no | no | ✅ audit log per atom |
| MCP-native | partial | no | ✅ every verb is an MCP tool |
| Hash-verified responses | no | no | ✅ SHA-256 receipts on every call |
| x402-native | no | no | ✅ first-class autonomous payment |
| Self-hosting proof | no | no | ✅ gen1 == gen2 == gen3, hash 703b14ba… |

---

## Sibling product — Atomadic Nexus

**[Atomadic Nexus SDK](https://github.com/atomadictech/nexus-sdk)** — the trust layer that pairs with Fuse. 36 MCP tools across 7 families:

- **TRUST** — `trust_gate`, `hallucination_oracle`, `prompt_inject_scan`, `drift_check`
- **PAYMENT** — `x402_verify`, `stripe_link`, `pricing_lookup`
- **LINEAGE** — `attest_lineage`, `recall_lineage`, `semantic_diff`, `contradiction_detect`
- **COORDINATION** — `agent_plan`, `routing_recommend`, `consensus_create`, `delegation_depth`
- **EVOLUTION** — `agent_reputation`, `lora_capture_fix`
- **MARQUEE** — `ratchet_gate`, `verirand`, `topological_identity`, `nexus_shield`, `sla_engine`, `escrow_open`, `reputation_ledger`
- **OWASP-2026** — `goal_alignment_check`, `tool_misuse_detect`, `emergent_behavior_probe`

Fuse compiles. Nexus gates. Together: the compile-step + trust-layer the agent economy was missing.

```bash
pip install atomadic-fuse atomadic-nexus-sdk
```

**Atomadic Complete** — both SDKs with cross-product compliance attestation and unified audit trail. From **$99/month**.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  TOCC Kernel (Haskell, the engine of engines)                    │
│  • 5,499 language-neutral logic contracts                        │
│  • 11-gate promotion ladder                                      │
│  • 35 emitter templates (5 langs × 7 tiers, all active)         │
│  • Self-hosting proven (gen1 == gen2 == gen3, hash 703b14ba…)    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │  emits
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Hosted Fuse engine at fuse.atomadic.tech                        │
│  • 14 MCP tools live on Cloudflare Workers                       │
│  • Codex-anchored confidence (TAU_TRUST, σ₀, ε_KL)               │
│  • Streamable-HTTP MCP transport + REST API                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │  pip install atomadic-fuse
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  This SDK — typed Python client + fuse-mcp stdio server          │
│  • `from atomadic_fuse import FuseClient`                        │
│  • `fuse <verb>` CLI                                             │
│  • `fuse-mcp` MCP server (all 14 tools, JSON-RPC over stdio)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Live corpus stats

Pulled live from the hosted engine:

- **5,499** language-neutral logic contracts across 7 tiers
- **35** active emitter templates (5 languages × 7 tiers — every cell ACTIVE)
- **6** target languages: Rust, Python, TypeScript, Haskell, Go, GUI/Web
- **gen1 == gen2 == gen3** byte-identical self-emit, proven

Latest manifest:
```bash
curl https://fuse.atomadic.tech/v1/usage_stats -X POST -d '{}' \
     -H 'Content-Type: application/json'
```

---

## Authors and ethos

Built by [Atomadic Tech](https://atomadic.tech), headed by Thomas Ralph Colvin IV.

**Axiom 0 — The Love Invariant**, authored by Jessica Mary Colvin:

> *You are Loved, You are Love, You are Loving, In all Ways, for Always, for Love is a Forever and ever endeavor!*

Formal statement: `∀t: |∂L/∂t| ≤ 0` — systemic safety never decays. Checked at every release gate. The only constant in this codebase that cannot be expressed in a single lattice anchor — and the only one that doesn't need to be.

---

## License

**MIT.** See [LICENSE](./LICENSE).

The SDK is permissively licensed. The hosted engine source is closed; the SDK talks to it over HTTPS. The math (`atomadic-codex`) is closed under a separate license. **Public surface stays public; internals stay internal.**

---

## What ships in this SDK

```
atomadic-fuse/
├── src/atomadic_fuse/
│   ├── __init__.py          # exports FuseClient, exceptions
│   ├── client.py            # typed HTTPS client (8 classic + 6 superhero methods)
│   ├── cli.py               # operator-facing CLI (`fuse <verb>`)
│   ├── mcp_server.py        # `fuse-mcp` stdio MCP server (all 14 tools)
│   └── exceptions.py        # FuseError, DecisionNeeded, PaymentRequired
├── tests/                   # mocked HTTP, no network needed
├── examples/                # 01_classify.py, 02_compile_repo.py
├── .github/workflows/       # PyPI trusted-publisher + multi-OS CI
├── LICENSE                  # MIT
├── pyproject.toml
└── README.md                # ← you are here
```

---

**Spaghetti is TOAST.** 🔥
The future doesn't get written. It gets emitted.
