# Atomadic Fuse SDK Whitepaper

Version 1.0  
Date 2026-05-22

## 1. Abstract

Atomadic Fuse SDK is a deterministic Python client and MCP bridge for the hosted Fuse engine. Its purpose is to provide a stable public interface for repository scanning, atom absorption, synthesis, emit workflows, verification, and explainability without requiring consumers to implement a custom transport or agent bridge.

This whitepaper is intentionally public-safe. It describes the SDK surface, trust boundary, and integration model using only externally verifiable information.

## 2. Problem

Software teams adopting AI-assisted workflows typically encounter the same set of failure modes:
- repeated runs produce inconsistent outputs
- generated code is hard to verify or trace back to a concrete source
- local tooling and agent tooling drift into separate interfaces
- verification is added as an afterthought instead of being built into the call surface

Fuse SDK addresses these issues by exposing one consistent package surface for both direct Python usage and MCP-based agent orchestration.

## 3. Design Goals

The SDK is built around five public goals:
- Deterministic interface contract: stable method semantics for equivalent inputs
- Verifiable workflows: verification-oriented calls are first-class instead of bolt-on
- MCP portability: the same operational surface is available through stdio MCP
- Operational clarity: health, status, and store-governance verbs are explicit
- Public-safe separation: the client exposes public behavior without requiring private implementation detail disclosure

## 4. System Overview

The public system has three visible layers:

1. SDK package
   The Python package `atomadic-fuse` supplies the typed client, local MCP server, examples, and bundled seed data.

2. MCP bridge
   The `fuse-mcp` command exposes the package surface to MCP-compatible runtimes over stdio JSON-RPC.

3. Hosted engine
   The hosted Fuse engine receives typed requests from the SDK and returns structured responses for build, verification, and explanation workflows.

## 5. Public API Surface

The source of truth for the client contract is [src/atomadic_fuse/client.py](../src/atomadic_fuse/client.py).

At the time of writing, `FuseClient` exposes 34 public methods covering:
- repository flow
- verification and diagnostics
- search and explainability
- language and output helpers
- store and promotion helpers

The MCP source of truth is [src/atomadic_fuse/mcp_server.py](../src/atomadic_fuse/mcp_server.py). The MCP tool surface mirrors the public operational shape of the client so agent runtimes can call the same workflows without inventing an adapter layer.

## 6. Determinism and Verification

The SDK is a transport and contract layer. It does not itself perform compilation or reasoning; instead, it provides structured access to hosted deterministic workflows.

The important public consequence is that consumers can build automation around explicit verification calls such as:
- `verify_block`
- `search_intent`
- `compose_stack`
- `usage_stats`

These methods should be treated as the primary trust signal for automated or high-assurance integrations.

## 7. MCP Integration Model

The package exposes a local stdio MCP server through `fuse-mcp`.

This gives teams two integration modes:
- direct Python client usage in scripts and services
- MCP-based usage in agent hosts, IDE integrations, and automation runtimes

The advantage of this model is operational consistency: one repository can validate flows through the Python API and then expose the same surface to agents through MCP.

## 8. Public Trust Boundary

This repository intentionally documents only the public integration boundary.

Publicly documented:
- package metadata
- method surface
- MCP setup patterns
- validation and operational guidance

Intentionally excluded from public docs:
- unpublished implementation internals
- confidential constants or non-public architecture details
- private orchestration or deployment machinery not required by SDK consumers

## 9. Operational Use

In production environments, teams should:
- pin package versions explicitly
- run SDK tests and smoke checks in CI
- verify MCP startup before agent rollout
- keep credentials in environment variables or secret stores
- record verification outputs for critical workflows

## 10. Limits

Fuse SDK does not eliminate the need for operator review, policy controls, or deployment discipline. It provides a deterministic public interface and verification-friendly workflow surface, but product governance remains the responsibility of the integrator.

## 11. Conclusion

Atomadic Fuse SDK is best understood as a deterministic public interface layer for repository transformation and verification workflows. Its value lies in interface stability, MCP compatibility, and verifiable workflow primitives that fit both direct developer usage and agent orchestration environments.
