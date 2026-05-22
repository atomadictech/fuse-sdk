# Atomadic Fuse SDK Whitepaper

Version 1.1
Date 2026-05-22

## Abstract

Atomadic Fuse SDK is the public integration layer for Fuse.

Public-facing tagline: Spaghetti to Shippable.

In plain English, Fuse helps teams move from "we have a messy repository and too many brittle scripts" to "we have one consistent way to inspect, validate, search, and drive build workflows."

In technical terms, the SDK provides:
- a typed Python client
- a public CLI
- a stdio MCP server
- bundled seed logic-base data for local bootstrapping

This whitepaper is intentionally public-safe. It describes the public SDK surface, trust boundary, pricing model, and integration patterns using only externally verifiable information from source code, package metadata, examples, and public endpoints.

## The Problem Fuse Solves

Teams adopting AI-assisted development typically run into four recurring problems:
- repo understanding is separated from generation and verification
- direct developer tooling and agent tooling diverge over time
- output quality is hard to inspect after the fact
- operational checks are bolted on instead of exposed as first-class calls

Fuse addresses this by giving teams a single public interface for repository workflow, intent-driven search, output inspection, verification, and store maintenance.

## Product Positioning

Fuse is best understood as a public developer and agent interface, not as a claim about unpublished internal systems.

What is publicly visible today:
- `atomadic-fuse` Python package
- `fuse` CLI
- `fuse-mcp` stdio MCP server
- examples and seed data in this repository
- public pricing and public endpoint references on `atomadic.tech`

What this repository does not attempt to expose:
- private orchestration internals
- unpublished engine details
- non-public research or control systems that are not required to consume the SDK

## Public Surface Overview

The package exposes three developer-facing ways to use Fuse.

### 1. Python SDK

The public class is `FuseClient` in [src/atomadic_fuse/client.py](../src/atomadic_fuse/client.py).

It exposes 34 public methods spanning:
- repository flow: compile, absorb, scan, discover, synthesize, emit, intent
- search and explainability: catalog, search, search_intent, logic_map, explain_block, explain_lineage, compose_stack, show
- verification and health: doctor, status, validate, verify_block, usage_stats, fuse_recovery_status
- store maintenance: lint_store, validate_store, deduplicate_store, rebuild_indexes, promote_hypotheses, promote_candidate
- language and output helpers: langs, polyglot, emit_corpus, capabilities, quickstart, friction

### 2. CLI

The public CLI in [src/atomadic_fuse/cli.py](../src/atomadic_fuse/cli.py) exposes these verbs:
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

### 3. MCP

The MCP server in [src/atomadic_fuse/mcp_server.py](../src/atomadic_fuse/mcp_server.py) exposes Fuse to agent hosts over stdio JSON-RPC.

This matters because it gives teams one operational surface for both direct scripts and agent runtimes instead of requiring separate adapters.

## Why This Matters

Fuse is useful when a team wants:
- one SDK instead of scattered curl snippets and ad hoc wrappers
- one CLI instead of custom glue scripts per workflow
- one MCP surface instead of writing a new integration layer for every agent host
- explicit verification and store-health calls in the same surface as build-oriented flows

## Public Trust Boundary

The SDK is a public contract and transport layer.

It should be evaluated by what is observable:
- package metadata
- method signatures
- examples
- tests
- public endpoint references
- CLI and MCP behavior

It should not be evaluated by assumptions about private internals that are not documented in this repository.

## Determinism and Verification

Fuse does not ask users to trust only generation. It exposes verification and operational calls as part of the public surface.

Examples of public verification-oriented calls:
- `verify_block`
- `validate`
- `doctor`
- `status`
- `usage_stats`
- `lint_store`
- `validate_store`
- `deduplicate_store`
- `rebuild_indexes`

For high-assurance workflows, these methods should be part of the normal path, not an afterthought.

## Pricing Model

The public pricing page currently describes Fuse and related public endpoints as pay-per-call with no subscription.

Verified from the public pricing page on 2026-05-22:
- Starter: 500 calls for $8
- Best Value: 2,500 calls for $30
- Power: 10,000 calls for $98

The public page also states:
- one-time purchase
- no expiry for credit packs
- credits work across 75+ endpoints
- card and Base L2 USDC payment options are available
- x402-style pay-per-call flows are described for autonomous agents

Because pricing is a live public surface, consumers should always verify current terms at:
- `https://atomadic.tech/pricing`
- `https://atomadic.tech/openapi.json`
- `https://atomadic.tech/api-status`

## Integration Modes

### Direct Python

Use the Python SDK when you want typed calls in application code, scripts, services, notebooks, or CI jobs.

### CLI

Use the CLI when you want shell-friendly workflows, quick smoke checks, or lightweight automation.

### MCP

Use MCP when you want IDEs, copilots, or agent runtimes to call the same public surface through a standard protocol.

## Operational Guidance

Before production rollout, teams should:
- pin SDK versions
- test critical workflows in a clean environment
- verify MCP startup explicitly
- keep credentials in environment variables or a secret manager
- log verification receipts or response metadata when auditability matters

## Limitations

This public SDK does not eliminate the need for operator review, product policy, or deployment discipline.

What it does provide is a more structured and verifiable interface for repository workflow and agent integration.

## Conclusion

Fuse is the public layer that makes repository workflow, verification, CLI automation, and MCP integration feel like one product instead of many disconnected tools.

That is the practical meaning of the Fuse promise:
- less glue code
- clearer contracts
- better automation ergonomics
- stronger verification habits


