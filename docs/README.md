# Fuse SDK Docs

This directory is the public documentation set for Atomadic Fuse SDK.

Use this docs set if you want to understand Fuse at three levels:
- what it does in plain English
- what the public SDK, CLI, and MCP surfaces actually expose
- how to integrate Fuse safely in scripts, CI, IDE tooling, and agent runtimes

If you only read two files, start with the main README for the product overview and the whitepaper for the bigger picture.

## Read This First

- [README](../README.md): fast overview, install, quick start, pricing snapshot, and public surface summary
- [Whitepaper](WHITEPAPER.md): product framing, public trust boundary, integration model, and why Fuse exists

## Choose Your Path

- New to Fuse: start with the README, then MCP Quickstart or Use Cases
- Evaluating the SDK: read the Whitepaper, Architecture, and Comparison Guide
- Rolling out in production: read Operations and Security and Privacy first

## Integration Guides

- [Architecture](ARCHITECTURE.md)
- [S2S and Engine Boundary](S2S_AND_ENGINE_BOUNDARY.md)
- [MCP Quickstart](MCP_QUICKSTART.md)
- [Operations Guide](OPERATIONS.md)
- [Security and Privacy](SECURITY_AND_PRIVACY.md)

## Decision Support

- [Use Cases](USE_CASES.md)
- [Comparison Guide](COMPARISON.md)
- [Benchmarks Guidance](BENCHMARKS.md)

## Public Documentation Rules

This is a public-facing docs surface.
- describe shipped SDK behavior, not private internals
- keep claims tied to source, tests, examples, or public endpoints
- treat pricing and endpoint availability as live public data that may evolve over time

**Operator sync (internal):** regenerate `client.py` / `mcp_server.py` from engine `SDK_SURFACE` via `fuse emit-sdk-client --sdk-root C:\Atomadic-Omega\atomadic-fuse-sdk` (Atomadic-Omega monorepo). Omega internal index: `atomadic-fuse-next/docs/FUSE_INTERNAL_REFERENCE.md` §5.

**Last surface sync:** 2026-05-23 — 34 public methods; pytest 14 passed.

