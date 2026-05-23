# Spaghetti to Shippable (S2S) and Engine Boundary

**Tagline:** Spaghetti to Shippable in one call

This document maps where S2S lives across the Atomadic-Omega monorepo, how the public SDK relates to the private engine, and how to regenerate SDK client artifacts.

---

## Repo map

| Repo / product | Tier | Visibility | S2S role |
|----------------|------|------------|----------|
| **`atomadic-fuse-sdk`** | T5 public | Public PyPI + docs | Hosted `FuseClient`, `fuse` CLI, `fuse-mcp` — **does not embed the full S2S pipeline** |
| **`atomadic-fuse`** | Engine stable | Operator / golden master | Stable engine; S2S promotion target after fuse-next validation |
| **`atomadic-fuse-next`** | Engine dev | Internal (dev lane) | **Canonical S2S implementation today** — `fuse s2s`, `spaghetti_to_shippable` MCP |
| **`Atomadic-Security`** | T5 product | Public overlay | Malicious gate, `security_scan`, `bubble_status` — composes with S2S security stages |

**Rule:** Public SDK consumers use hosted HTTP/MCP for catalog, compile, classify, and verification. **Single-repo S2S (ingest → heal → fitness gate → T5 bow)** runs on the **local Fuse engine** (`atomadic-fuse-next` today; `atomadic-fuse` after stable promotion).

Cross-reference: [`C:\Atomadic-Omega\docs\SPAGHETTI_TO_SHIPPABLE.md`](../../docs/SPAGHETTI_TO_SHIPPABLE.md) (Omega canonical pipeline doc).

---

## Two surfaces — do not conflate

### Hosted `FuseClient` (this SDK)

- Package: `atomadic-fuse` (`pip install atomadic-fuse`)
- Endpoint: `https://fuse.atomadic.tech/v1`
- Transport: HTTP + optional x402 payment proofs
- Typical calls: `compile`, `classify`, `catalog`, `doctor`, `verify_block`, store maintenance
- **S2S:** Not exposed as a hosted SDK method today. Use local engine for full S2S.

### Local engine `fuse s2s` (fuse-next)

- Workspace: `C:\Atomadic-Omega\atomadic-fuse-next` (dev) → promoted to `atomadic-fuse` (stable)
- CLI: `./fuse.cmd s2s --source <repo> --output <product> [--live]`
- MCP: `spaghetti_to_shippable` / `s2s` on `fuse-engine` stdio server
- **Dry-run (default):** plan only; no trust token required
- **Live (`--live` / `dry_run=false`):** applies heal, emit, fitness gate, T5 bow — **trust-gated** (`gate_intent` → malicious gate → Nexus trust or `ATOMADIC_TRUST_TOKEN`)

---

## Regenerate SDK client from engine

The SDK `client.py` and `mcp_server.py` are **generated artifacts**. Authoritative surface: `atomadic_fuse_engine/tier_4/emit_sdk_client.py` (`SDK_SURFACE`).

```powershell
cd C:\Atomadic-Omega\atomadic-fuse-next
$env:PYTHONPATH = 'C:\Atomadic-Omega\atomadic-fuse-next\src'
$env:FUSE_WORKSPACE = 'C:\Atomadic-Omega\atomadic-fuse'
$env:FUSE_DEV_WORKSPACE = 'C:\Atomadic-Omega\atomadic-fuse-next'

python -m atomadic_fuse_engine.tier_4.cli emit-sdk-client `
  --sdk-root C:\Atomadic-Omega\atomadic-fuse-sdk
```

After engine emitter changes, hotload MCP:

```powershell
.\fuse.cmd mcp --workspace .
pwsh -NoProfile -File scripts/refresh-fuse-runtime.ps1
```

---

## Polyglot output layout (S2S live)

When S2S runs with `polyglot=true` (default), `emit_polyglot_product_stateful` writes per-language corpus packages under the product output root:

```
target_output/
  repo/                          # synced source tree (live)
  src/atomadic_fuse_engine/      # T5 engine layout (Python)
  fuse-s2s-<product>-python/     # Python corpus package
    tier_0/ … tier_4/            # CNAE-named .py files
    pyproject.toml
    .tocc-contracts.jsonl
    .tocc-lineage.jsonl
  fuse-s2s-<product>-rust/
    src/tier_*/                  # .rs files
    Cargo.toml
    …
  fuse-s2s-<product>-typescript/
    src/tier_*/                  # .ts files
    package.json
    …
  .atomadic/logic-base/          # customer shard (not full Omega brain)
  product.json                   # T5 bow metadata
  README.md
  CLAUDE.md
```

Prefix `fuse-` is overridable via `FUSE_DIR_PREFIX`.

Default languages: `python`, `rust`, `typescript`.

---

## Public boundary summary

| Capability | Hosted SDK | Local engine S2S |
|------------|------------|------------------|
| Single-repo ingest + heal | No | Yes |
| Malicious logic gate | Via Atomadic-Security overlay | Yes (pipeline stage) |
| Fitness gate before T5 bow | No | Yes (`process_gate_fitness_stateful`) |
| Multi-repo harvest / train | No | No (T6 internal) |
| Trust-gated live emit | N/A | Yes |

Authoritative boundary table: [`C:\Atomadic-Omega\docs\PUBLIC_INTERNAL_BOUNDARY.md`](../../docs/PUBLIC_INTERNAL_BOUNDARY.md).

---

## Related docs

- [README](../README.md) — SDK overview + S2S pointer
- [WHITEPAPER](WHITEPAPER.md) — product framing + trust boundary
- [MCP_QUICKSTART](MCP_QUICKSTART.md) — hosted vs local fuse-engine S2S
- [SECURITY_AND_PRIVACY](SECURITY_AND_PRIVACY.md) — Atomadic-Security cross-links
- [Omega S2S pipeline](../../docs/SPAGHETTI_TO_SHIPPABLE.md) — 19-stage canonical list
