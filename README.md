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

## What's new in **1.1.0** (2026-05-20)

- **9 new MCP tools** — `quickstart`, `friction`, `promote_hypotheses`, `promote_candidate`, `explain_lineage`, `lint_store`, `validate_store`, `deduplicate_store`, `rebuild_indexes` — **30 total tools** (was 21). Full Gen14 engine parity.
- **Friction Protocol** — `friction()` reads the UX telemetry log. Every Fuse operation emits structured friction events (`zero_atoms`, `workspace_missing`, `bad_path`, etc.) you can query to understand what's going wrong and where.
- **Promotion pipeline** — `promote_hypotheses()` and `promote_candidate()` run the full 11-gate TOCC promotion pipeline. Candidates become verified canonical blocks you can trust absolutely.
- **Store governance** — `lint_store`, `validate_store`, `deduplicate_store`, `rebuild_indexes` give your logic-base a clean bill of health in one call each.
- **Lineage explorer** — `explain_lineage(block_id)` returns the full composed_from + depends_on tree for any block. See exactly what a block depends on, all the way to T0.
- **One-shot quickstart** — `quickstart(directory)` does scan → absorb → synthesize → emit in a single call. Permissive mode (default) works on any codebase with no CNAE setup.
- **162 language extension mappings** (was 123) — C++, PHP, and Rust pattern coverage improved in the Gen14 polyglot harvesters.
- **Engine v1.1.0 sovereign package** — `emit-self-host` now produces a complete, installable package with all 6 entry points (`fuse`, `fuse-engine`, `fuse-mcp`, `fuse-engine-mcp`, `fuse-gui`, `fuse-engine-gui`), hatchling build backend, optional `mcp[cli]` + `gradio` deps, and bundled README + tests.
- **IP boundary hardened** — `PUBLIC_THEMES` filter prevents private theme IDs (codex, aletheia, transmute, nexus) from leaking into public emits. `.lean` files opt-in only. No personal email in any emitted `pyproject.toml`.

## What's new in **1.0.0** (2026-05-19)

- **8 new client methods** — `scan`, `discover`, `synthesize`, `emit`, `validate`, `status`, `search`, `logic_map` — mirror the local Fuse engine MCP one-for-one. The 13 legacy verbs still work; 21 total now.
- **Bundled seed logic-base** — `pip install atomadic-fuse` now ships **49 verified blocks** (T0 schemas + T1 examples + T2 composites). Run `fuse init` to copy them to your CWD; `fuse harvest <repo>` populates from your own code.
- **Opt-in telemetry hook** — `FuseClient(telemetry_opt_in=True)` or `ATOMADIC_FUSE_TELEMETRY=1` sends anonymized CNAE/tier/domain metadata only. Never source, never intent text. Off by default.
- **`fuse init` and `fuse seed-info` CLI verbs** — bootstrap a local store in two commands.
- **Polyglot emit** — engine now covers **162 target language extensions** across 124 language families. Same `compile`/`emit_corpus` calls, more output choices.
- **Self-evolution surface** — the engine corpus now carries 29 evolution-related logic blocks (`manage_evolution_composite`, `loop_evolve_ecosystem_temporal`, `_append_evolution_log`) plus the canonical hypothesis-ledger schema. Hosted endpoints expose these via the existing `search_intent` / `compose_stack` verbs.

---

## 30-second proof — `pip install`, then ask the live engine

```python
>>> from atomadic_fuse import FuseClient
>>> c = FuseClient()
>>> c.usage_stats()
{
 "total_blocks": 8271,
 "tiers": {"Tier0": 87, "Tier1": 7544, "Tier2": 16, "Tier3": 354, "Tier4": 213, "Tier5": 25},
 "emit_languages": 123,
 "emit_languages_list_count": 123,
 "emit_language_families": ["mainstream(13)","systems(11)","functional(20)","scientific(7)","scripting(13)","web(9)","logic(4)","hardware(6)","blockchain(2)","legacy(9)","quantum(1)","research(6)","specialized(22)"],
 "emit_templates": 123,
 "token_savings": {
 "raw_tokens_per_lookup": 4_823_000,
 "mcp_tokens_per_lookup": 410,
 "savings_factor": "11,763x",
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

## What you get — 21 MCP tools, one engine

> 🟣 **In plain English:** Think of these as 21 buttons your AI assistant gets to push. Six of them are new superpowers (the hashes-on-every-answer ones). Eight are the classic verbs that turn messy repos into clean shippable products. Every button returns a receipt so your agent can prove the answer is real and not made up.

### The 6 Superhero Tools (returns SHA-256 receipts)

Each returns a **SHA-256 verification receipt**. The anti-hallucination shield no other MCP can provide.

> 🟣 **What a "receipt" means:** every answer comes back with a fingerprint (a SHA-256 hash) of the exact source it pulled from. If the agent ever says *"the function does X"*, you can re-check that hash and prove it came from real code — not from the model's imagination.

| Tool | What it does |
|---|---|
| **`verify_block`** | Returns block + content_hash + semantic_hash + verification status. Agent can prove `"this isn't hallucinated — it's hash 703b14ba…"` |
| **`search_intent`** | Natural-language semantic search across 8,271 verified contracts. Returns only what fits — ranked, pre-composed. |
| **`compose_stack`** | Full tier dependency walk (T5 -> T0). Ask for a feature, get the whole stack. |
| **`emit_corpus`** | One call emits a complete buildable + testable package in any of 123 languages. |
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
| **`fuse_recovery_status`** | Read-only Fuse recovery gate status. |

### The 8 Engine v1 Tools (new in 1.0.0)

These mirror the local Fuse engine MCP one-for-one. Hosted versions currently return
curated stub responses with `local_route` pointing at `fuse-engine-mcp.exe` for full
execution. Wave B wires hosted execution end-to-end.

| Verb | What it does |
|---|---|
| **`scan`** | Walk a directory and return CNAE atoms found in source files (no writes). |
| **`absorb`** | Scan + log atoms into the logic-base harvest ledger. |
| **`discover`** | Cluster + score + chain atoms — the emergent finder. |
| **`synthesize`** | Full pipeline: scan → absorb → cluster → score → chain → theme → emit. |
| **`emit`** | Emit product directory scaffolds from already-absorbed atoms. |
| **`validate`** | Check a CNAE name against the canonical `action_entity_scope` vocabulary. |
| **`status`** | Read-only logic-base status: atom count, shards, ledgers, manifest. |
| **`search`** | Substring + CNAE search across the logic-base. |
| **`logic_map`** | Return the full composition graph (atom → dependencies, by tier). |

---

## Bootstrap with the bundled seed

> 🟣 **In plain English:** `pip install atomadic-fuse` now ships 49 verified blocks
> right in the package. One command copies them to your machine; one more populates
> the rest from your own source code. No signup, no API key, no network round-trip
> for the basics.

```bash
fuse seed-info                    # what's in the bundled seed
# -> {"seed_path": ".../logic-base-seed", "blocks": 49, "shards": 10}

fuse init                         # copy seed to ./logic-base/
# -> {"ok": true, "target_dir": "./logic-base", "blocks_seeded": 49, "shards": 10}

# Then grow the store with your own code:
fuse-engine harvest ./my-repo     # via the local engine MCP (atomadic-fuse-engine)
```

The seed contains:
- **T0** — schemas, define atoms, kernel parse/validate (24 blocks)
- **T1** — pure example contracts: parse, validate, normalize, render, define, compose (24 blocks)
- **T2** — one canonical composite (`compose_path_composite`)

Public CNAE glossary (actions / entities / scopes) ships alongside so harvested atoms
classify correctly against the canonical vocabulary.

---

## Opt-in telemetry — feed the flywheel

> 🟣 **In plain English:** If you flip the switch, the SDK sends back anonymized
> metadata (which CNAE names showed up, which tiers, which source languages) — never
> source code, never intent text. It helps us prioritize emitter improvements for the
> patterns real teams actually use. Default is OFF.

```python
from atomadic_fuse import FuseClient

# Off by default — no telemetry leaves your machine
c = FuseClient()

# Opt in at construction:
c = FuseClient(telemetry_opt_in=True)

# Or via env var:
# $ ATOMADIC_FUSE_TELEMETRY=1 fuse compile ./my-repo

# Or programmatic toggle:
c.opt_in_telemetry()    # enable
c.opt_out_telemetry()   # disable
```

**Whitelist enforced** — only these fields are ever sent:
`event` · `sdk_version` · `cnae` · `tier` · `domain` · `source_language` · `scope` · `action` · `entity`

Endpoint: `https://fuse.atomadic.tech/telemetry` · 2-second timeout · best-effort,
swallowed errors. Never blocks the main call. Aggregate anonymized patterns may be
used to improve the engine.

---

## Why it works — the math

> 🟣 **In plain English:** Most AI tools tune their confidence knob by trying things until it looks right. Fuse anchors its confidence numbers to constants from 60-year-old published mathematics — numbers nobody, including us, can fudge. If the engine says *"I'm 99.84% sure this function hashes bytes"*, that 99.84% comes from lattice geometry, not from a guess. The signal-to-noise floor (`σ₀`) is just the minimum gap between two real points in a 24-dimensional crystal — below that gap, the engine refuses to answer rather than make something up.

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

> 🟣 **In plain English:** When an AI assistant has to read whole codebases to answer a question, it burns ~3.2 million tokens (a stack of paper a few feet tall, every time). Fuse pre-chews everything down to the one block that answers the question — about 450 tokens (a sticky note). That's the same answer for 1/7000th the cost. If your team runs 100 agent sessions a day, that's roughly $30,641 a day in tokens you don't have to spend.

The live engine just told us: **`savings_factor: 11,763x`**, **`savings_percent: 99.99%`**, **`estimated_daily_savings_100_sessions: $30,641`**.

| Without Fuse MCP | With Fuse MCP |
|---|---|
| Agent hallucinates code | Every block hash-verified |
| 3.2M tokens per lookup | 450 tokens, exact match |
| Knows 1 language well | 123 languages, all tested |
| One function at a time | Full tier-chain composition |
| **$30,641/day** in tokens | **$4.20/day** |

The Free tier alone saves subscribers **~$300/day** vs raw lookups. Builder pays for itself in the first API call.

---

## 60-second test drive

```python
from atomadic_fuse import FuseClient
c = FuseClient() # uses ATOMADIC_FUSE_API_KEY env var or x402 micropayments

# 1. Anti-hallucination — every response carries a hash receipt
print(c.verify_block("lb:t2:compose_path_composite:bd7e1d030ef5"))

# 2. Smart context — describe what you need
print(c.search_intent("validate user input and route it", tier="t2", limit=5))

# 3. Composability — full T5 -> T0 dependency walk for a feature
print(c.compose_stack("build a path-validation feature", target_language="rust"))

# 4. Polyglot emit — one call, complete package in any of 123 languages
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

All **21 tools** become first-class agent capabilities. Hash-verified responses. No hallucinations.

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

> 🟣 **In plain English:** Free to try, no signup. Starter is a one-time $8 for 500 calls — that's the version most teams buy. The grown-up tiers add quotas, sub-keys, and audit. And if you're an *AI agent* spending its own money, you can pay per-call in USDC stablecoin with no human in the loop — that's what x402 is. No card on file, no monthly bill, the agent settles in cents on Base.

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
| Polyglot input | adapters per source | per-file inline | ✅ N repos, 123 langs, one engine |
| Output is shippable | no, you wire it | no, you copy-paste | ✅ `pip install` artifact |
| Deterministic | no | no | ✅ byte-identical re-emit |
| Provenance per function | no | no | ✅ audit log per atom |
| MCP-native | partial | no | ✅ every verb is an MCP tool |
| Hash-verified responses | no | no | ✅ SHA-256 receipts on every call |
| x402-native | no | no | ✅ first-class autonomous payment |
| Self-hosting proof | no | no | ✅ gen1 == gen2 == gen3, hash 703b14ba… |

---

## Sibling product — Atomadic Nexus

> 🟣 **In plain English:** Fuse turns messy code into shippable products. Nexus is its partner — it's the bouncer at the door. Before one of your agents forwards a request, spends money, or signs a contract, Nexus checks it: *is this prompt safe, is the answer real, is the counterparty trustworthy?* You use Fuse to build the product, Nexus to keep it from being tricked.

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

> 🟣 **In plain English:** Three boxes, top to bottom. The top box is the math engine that holds 8,271 verified building blocks of logic. The middle box is the live website (`fuse.atomadic.tech`) that turns those blocks into answers over HTTPS. The bottom box is this Python library — when you `pip install atomadic-fuse`, you're getting the doorbell to the middle box. You never talk to the top box directly; you don't need to.

```
┌─────────────────────────────────────────────────────────────────┐
│ TOCC Kernel (Haskell, the engine of engines) │
│ • 8,271 language-neutral logic contracts │
│ • 11-gate promotion ladder │
│ • 123 emitter templates (123 langs × 5 tiers — T0-T5) │
│ • Self-hosting proven (gen1 == gen2 == gen3, hash 703b14ba…) │
└─────────────────────────────────────────────────────────────────┘
 │
 │ emits
 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Hosted Fuse engine at fuse.atomadic.tech │
│ • 21 MCP tools live on Cloudflare Workers │
│ • Codex-anchored confidence (TAU_TRUST, σ₀, ε_KL) │
│ • Streamable-HTTP MCP transport + REST API │
└─────────────────────────────────────────────────────────────────┘
 │
 │ pip install atomadic-fuse
 ▼
┌─────────────────────────────────────────────────────────────────┐
│ This SDK — typed Python client + fuse-mcp stdio server │
│ • `from atomadic_fuse import FuseClient` │
│ • `fuse <verb>` CLI │
│ • `fuse-mcp` MCP server (all 21 tools, JSON-RPC over stdio) │
└─────────────────────────────────────────────────────────────────┘
```

---

## Live corpus stats

Pulled live from the hosted engine:

- **8,271** language-neutral logic contracts across 5 tiers (T0-T5)
- **123** active emitter templates (one per target language, all reachable via `emit_corpus`)
- **123** target languages — mainstream (Python/Rust/TypeScript/JavaScript/Go/Java/C#/Ruby/PHP/Swift/Kotlin/Scala/Dart), systems (C/C++/Zig/Nim/Crystal/D/Odin/Mojo/Carbon/V/Hare/ATS), functional (Haskell/F#/OCaml/SML/Elixir/Erlang/Clojure/Scheme/Racket/Lean/Idris/Agda/Coq/Roc/Gleam/...), scientific (Julia/R/MATLAB/Mathematica/Wolfram/Q/APL/K), scripting (Lua/Perl/Raku/TCL/AWK/Bash/PowerShell/Vim), web (Vue/Svelte/Astro/CoffeeScript/LiveScript/Hack), hardware (Verilog/SystemVerilog/VHDL/GLSL/HLSL/CUDA/WGSL), blockchain (Solidity/Vyper), legacy (COBOL/Fortran/Ada/Pascal/Modula-2/Oberon/Rexx/Forth/Smalltalk), quantum (Q#), and 20+ research/specialized. Run `fuse langs` for the full taxonomy.
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
│ ├── __init__.py # exports FuseClient, exceptions
│ ├── client.py # typed HTTPS client (8 classic + 6 superhero + 8 engine v1 methods)
│ ├── cli.py # operator-facing CLI (`fuse <verb>`)
│ ├── mcp_server.py # `fuse-mcp` stdio MCP server (all 21 tools)
│ └── exceptions.py # FuseError, DecisionNeeded, PaymentRequired
├── tests/ # mocked HTTP, no network needed
├── examples/ # 01_classify.py, 02_compile_repo.py
├── .github/workflows/ # PyPI trusted-publisher + multi-OS CI
├── LICENSE # MIT
├── pyproject.toml
└── README.md # ← you are here
```

---

**Spaghetti is TOAST.** 🔥
The future doesn't get written. It gets emitted.
