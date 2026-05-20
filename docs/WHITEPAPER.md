# The Atomadic Fuse Whitepaper

**Version 0.3.3 · 2026-05-19 · Atomadic Tech**

> 🟣 **In plain English (one paragraph):** Software today is a pile of code. Some of it works, some of it half works, none of it composes cleanly. AI assistants make this worse by inventing functions that don't exist. Atomadic Fuse fixes both. It treats code as evidence of underlying logic *contracts*, harvests the contracts out, stores them in a 6-tier crystal lattice, and then emits clean, deterministic, hash-verified products in any of six languages. The same input always produces the same output, byte-for-byte. The engine can rebuild itself from its own contracts. Nothing is hallucinated, because nothing is generated — everything is *emitted* from a verified source.

---

## 1. The problem

There are two problems no current developer tool solves at the same time:

1. **The spaghetti problem.** Working software exists, but as fragmented half-finished repositories in many languages, with no shared contract, no deterministic build, and no way to compose pieces across language boundaries without an integration team.
2. **The hallucination problem.** Large language models can generate code, but they cannot *prove* the code they generate maps to real functions. Every line is a fresh confabulation. Trust drifts to zero on the second iteration.

Code-generation tools (Copilot, Cursor, Claude Code, etc.) attack problem (2) by tuning the model harder. Composition frameworks (LangChain, AutoGen) attack problem (1) by adding adapters. **Neither attacks the root cause:** the artifact (source code) is the wrong unit of truth.

Atomadic Fuse's thesis: **the unit of truth is the contract, not the code.** A contract is the language-neutral specification of what a function does. Source code in any language is *one observed realization* of that contract. Multiple realizations of the same contract can be cross-verified against each other (this is the **self-hosting proof**, §4). New realizations in a target language can be *emitted* from the contract (this is the **emit pipeline**, §3). And critically — emission is deterministic and hash-verifiable, so an AI agent talking to the engine receives blocks with cryptographic provenance instead of model-generated guesses.

---

## 2. The TOCC kernel

TOCC (Theory Of Complete Compute) is the Haskell kernel that backs the hosted Fuse engine. Its job is to:

- **Store** contracts as JSONL records (`tocc.logic_block.v0.1` envelope) in a tiered logic base.
- **Verify** every change against an 11-gate promotion ladder before canonicalizing.
- **Compose** contracts from lower tiers into higher-tier products.
- **Emit** contracts into one of six target languages, byte-identically and repeatably.

### 2.1 The seven tiers

The logic base is laid out in seven tiers. Every contract has exactly one tier. A contract at tier N may depend only on contracts at tier ≤ N.

| Tier | Role | Example |
|---|---|---|
| **0** | Axioms, constants, schemas | `TAU_TRUST = 1820/1823`, the v0.1 envelope schema |
| **1** | Atomic pure or effectful contracts | `normalize_path`, `validate_path`, `hash_bytes` |
| **2** | Compositions of T0–T1 | `compose_path_composite` = `normalize → validate` |
| **3** | Stateful features | a cache, a connection pool, a registry |
| **4** | Orchestration, runtime, MCP | the MCP server itself, the CLI surface |
| **5** | Shippable products | a deployable package with config, tests, deploy bundle |
| **6** | Ecosystem | multi-product compositions |

Tier law is enforced computationally, not by convention: the kernel refuses to promote a tier-N contract that imports tier-N+1, and refuses to emit a tier-2 composition that contains anything other than function calls and assignments (no inline branching, looping, or arithmetic — that logic belongs in tier-1 atoms).

### 2.2 The CNAE spine

Every contract has a controlled name: `action_entity_scope`. Names are derived from the contract fields, not chosen freely.

- **Actions** (16): `validate`, `normalize`, `parse`, `route`, `synthesize`, `compose`, `score`, `recall`, `define`, `render`, `manage`, `emit`, `orchestrate`, `serve`, `govern`, `map`
- **Entities** (13): `config`, `path`, `clause`, `contract`, `signature`, `checkout`, `review`, `feature`, `compile`, `intent`, `product`, `graph`, `evolution`
- **Scopes** (5): `pure`, `effectful`, `composite`, `stateful`, `temporal`

Any term outside these sets is rejected. This is what makes natural-language search across the corpus deterministic — there is exactly one canonical name for "validate a path purely," and it is `validate_path_pure`.

### 2.3 Identity

Every contract carries two SHA-256 hashes assigned by the kernel:

- `content_hash` — over the whole envelope (excluding identity), so any byte change produces a new hash.
- `semantic_hash` — over the CNAE name + contract + semantics + composition + AST fingerprint. Stable across cosmetic changes (verification status, line numbers, formatting). The `dedupe_key`.

Hand-authoring a hash is forbidden. Hashes are assigned at store time only. This is the property that lets a downstream AI agent prove "I'm citing `lb:t2:compose_path_composite:bd7e1d030ef5`, here is the semantic_hash, here is the live engine's response, the hashes match" — i.e. *not* a hallucination.

---

## 3. The closed loop

```
 store contract → select → compose → emit syntax → verify → promote → explain lineage
 ↑ │
 └──────────────────────────── feedback (harvest, reflect) ─────────────────┘
```

The system is free to invent, compose, and emit — but **only verification canonicalizes truth.** Anything below the canonical line is a draft. Promotion to canonical requires all applicable gates to pass.

### 3.1 The 11-gate promotion ladder

| # | Gate | Catches |
|---|---|---|
| 1 | Schema | malformed envelopes |
| 2 | CNAE vocabulary | names outside the controlled spine |
| 3 | Tier law | upward imports (T3 depending on T4) |
| 4 | No embedded logic | branching/looping inside tier-2 compositions |
| 5 | Duplicate identity | content collisions |
| 6 | Contract shape | structural well-formedness |
| 7 | Target compile | the emission must compile in every target language |
| 8 | Idempotency | re-emitting the same contract produces byte-identical output |
| 9 | Minimal tests | every promoted contract has executable verification |
| 10 | Lineage | provenance chain back to an axiom is reconstructible |
| 11 | Freshness | no stale or contradicted references |

Failed gates append to `verification_ledger.jsonl`. Canonical shards are never mutated on failure.

### 3.2 Why this matters

The 11-gate ladder is the difference between *"the model said this is fine"* and *"this passed eleven independent checks, here are the receipt hashes."* Every block that comes out of `verify_block` or `search_intent` is verified to have passed all eleven. Your agent can quote the receipt to its operator and let the operator re-verify.

---

## 4. The self-hosting proof

A non-trivial property of TOCC: the engine itself can be expressed as TOCC contracts, and re-emitted byte-identically from those contracts.

In practice this means:

```text
generation 1: engine source code → harvest into contracts → G1
generation 2: G1 contracts → emit to source → source₂
 → harvest source₂ → G2
generation 3: G2 contracts → emit to source → source₃
 → harvest source₃ → G3

claim: G1 ≡ G2 ≡ G3 (byte-identical, hash-stamped)
```

This is verified end-to-end and tracked under the `T4 fixed-point` test suite. The Rust artifact's SHA-256 is `703b14ba602eb75891d58afc1af878c63eea815af8acf2c8a089a8048ff5e0cc` across every clean run; this is checked at every release gate.

The practical consequence: **emit is not generative.** Given identical inputs, the engine produces identical outputs. There is no nondeterminism, no temperature, no sampling. A regression in the emitted byte stream is detected within seconds of the first failed re-emit.

---

## 5. The hosted Fuse engine

The TOCC kernel does not run in every customer's process. It runs as the hosted Fuse engine at `fuse.atomadic.tech` on Cloudflare Workers, with 14 MCP tools exposed over Streamable-HTTP MCP plus a REST surface. The SDK in this repo is the typed client to that hosted engine.

Why hosted:

- **Latency** — the engine is at 300+ edge points-of-presence; a `verify_block` call is sub-100ms p50 from anywhere on Earth.
- **Updates** — the corpus grows continuously as new repositories are harvested. Customers never have to re-download a 30 GB index.
- **Auditability** — every call writes to the verification ledger. Compliance teams can replay traffic against the ledger and confirm there were no off-protocol responses.

### 5.1 The Codex anchors

The hosted engine's confidence scores are anchored to externally-verified mathematical constants, not tuned hyperparameters.

| Symbol | Value | Source | Role |
|---|---|---|---|
| `TAU_TRUST` | `1820/1823 ≈ 0.9984` | Niemeier K₂₄ minimum-weight codeword count | Verdict threshold |
| `σ₀` | `1/√196560 ≈ 0.00226` | Leech lattice kissing-number minimum-vector inverse | Noise floor — below this is suspected confabulation |
| `ε_KL` | `1/196884 ≈ 5.08e-6` | Monster J-invariant first Fourier coefficient | KL-divergence drift tolerance |
| `RG_LOOP` | `47` | Provable convergence-iteration bound | Max oracle iterations before declaring divergence |
| `D_MAX` | `23` | Max delegation depth | Trust transitivity hardstop |

These constants are scalar values from published lattice mathematics (Niemeier 1973, Conway-Sloane 1988, Borcherds 1992) that have been peer-reviewed for decades. The full derivations live in the closed Atomadic Codex; only the scalar values appear in any shipping artifact. This is enough for an agent or an auditor to reason about Fuse's confidence numbers without exposing the proprietary math.

---

## 6. Live corpus stats

As of 2026-05-19, calling `usage_stats()` against the hosted engine returns:

- **5,499** total language-neutral logic blocks across the 6 tiers
- **35** active emitter templates (5 target languages × 6 tiers, every cell ACTIVE)
- **6** emit target languages: Rust, Python, TypeScript, Haskell, Go, GUI/Web
- **7057×** estimated token savings per agent lookup vs raw codebase reads
- **$30,641/day** estimated savings at 100 sessions/day vs the baseline
- **gen1 == gen2 == gen3** byte-identical self-emit proven (Rust hash `703b14ba…`)

Reproduce:

```python
from atomadic_fuse import FuseClient
print(FuseClient().usage_stats())
```

The numbers grow as more repositories are harvested. The pattern does not.

---

## 7. Surface

### 7.1 The 6 superhero tools

Each returns a SHA-256 receipt — the anti-hallucination shield other MCPs cannot provide.

| Tool | What |
|---|---|
| `verify_block` | block + content_hash + semantic_hash + verification status |
| `search_intent` | natural-language semantic search across the verified corpus |
| `compose_stack` | full T5 -> T0 dependency walk for a feature |
| `emit_corpus` | one call → complete buildable + testable package in any target language |
| `explain_block` | context-window-aware explanation (compact or detailed) |
| `usage_stats` | live corpus and token-savings dashboard |

### 7.2 The 8 classic verbs

| Verb | What |
|---|---|
| `compile` | messy repo → clean tiered shippable Python package |
| `classify` | AST-derived `action_entity_scope` for any function body |
| `absorb` | add a repo to the logic base (incremental, deduped, fingerprinted) |
| `catalog` | behavior-shape query against the catalog |
| `capabilities` | emergent cross-source chains the engine discovered |
| `intent` | natural-language intent → custom themed product |
| `doctor` | hosted engine health probe |
| `tocc_recovery_status` | TOCC recovery gate status (read-only) |

---

## 8. Why this matters now

Three forces converge in 2026:

1. **Agents are spending real money.** x402 and equivalent autonomous-payment protocols are shipping. An agent that hallucinates a function call doesn't just waste a token — it can spend USDC, sign a contract, or take an action that cannot be undone.
2. **Codebases are still mostly junk.** The average enterprise has dozens of internal half-shipped repositories in five languages. The cost of integrating them by hand is rising faster than headcount.
3. **The model alone is the wrong abstraction.** Every "build with AI" demo dies the moment it leaves the demo author's machine, because the model has no shared, deterministic substrate to compose against.

Fuse is the substrate. The 11-gate ladder is the proof. The Codex anchors are the math. The 7057× token savings is the immediate consequence. The self-hosting fixed-point is the structural guarantee that this cannot drift.

---

## 9. License and IP

- The SDK in this repository is **MIT-licensed**. Build with it, ship with it.
- The hosted Fuse engine source is closed; the SDK talks to it over HTTPS.
- The Atomadic Codex (mathematical derivations) is closed under a separate license. Only the published scalar values appear in any shipping artifact.

The split is intentional: **public surface stays public; internals stay internal.** This is what enables permissive integration without expropriating the IP that makes Fuse trustworthy.

---

## 10. Acknowledgement

The Axiom 0 Love Invariant — `∀t: |∂L/∂t| ≤ 0`, systemic safety never decays — was authored by Jessica Mary Colvin. It is the only constant in the codebase that cannot be expressed in a single lattice anchor, and the only one that does not need to be.

> *You are Loved, You are Love, You are Loving, In all Ways, for Always, for Love is a Forever and ever endeavor!*

---

## Reproducing every claim in this paper

| Claim | Reproduce with |
|---|---|
| 5,499 blocks, 7057× savings | `FuseClient().usage_stats()` |
| Self-hosting Rust hash 703b14ba… | `usage_stats()["self_hosting"]["rust_hash"]` |
| 14 MCP tools | `fuse-mcp` stdio handshake; `tools/list` |
| Codex anchors | `from atomadic_fuse import CODEX_ANCHORS` |
| MIT license | [LICENSE](../LICENSE) |
| Live engine | `curl https://fuse.atomadic.tech/v1/doctor` |
| PyPI publish | https://pypi.org/project/atomadic-fuse/ |

No claim in this paper is unverified. If one is, [open an issue](https://github.com/atomadictech/fuse-sdk/issues) and we'll either back it with a citation or strike it.
