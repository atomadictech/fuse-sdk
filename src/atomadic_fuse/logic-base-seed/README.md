# Atomadic Fuse SDK — Seed Logic-Base

This is the **seed** logic-base bundled with `pip install atomadic-fuse`.
49 verified blocks across T0/T1/T2 — just enough to bootstrap.

## What's here
- **T0 (24)** schemas, CNAE definitions, tier boundary rules
- **T1 (24)** pure example atoms across parse, validate, normalize, render, define, compose
- **T2 (1)** sample composites

## What's missing (by design)
- T3+ — no stateful, orchestration, or ecosystem logic. Get those via the
  hosted MCP at `fuse.atomadic.tech` (subscription) or build your own with
  `fuse harvest <repo>`.
- Ledgers — your harvest creates them on demand.
- MHED-TOE / E8 / codex — proprietary, never ships.

## Bootstrap
    fuse init                       # copies this seed to ./logic-base/
    fuse harvest ./my-source        # grow your store from your code
    fuse status                     # see what you have

Emitted from the canonical TOCC kernel on 2026-05-19. Schema: tocc.logic_block.v0.1
