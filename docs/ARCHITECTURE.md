# Architecture

This document describes the public architecture of Fuse SDK.

## Plain-English View

Fuse has three visible layers:
- the Python package developers import
- the CLI and MCP tools they launch locally
- the hosted Fuse endpoint those tools talk to

## Technical View

### Python package

Source files:
- [src/atomadic_fuse/client.py](../src/atomadic_fuse/client.py)
- [src/atomadic_fuse/cli.py](../src/atomadic_fuse/cli.py)
- [src/atomadic_fuse/mcp_server.py](../src/atomadic_fuse/mcp_server.py)
- [src/atomadic_fuse/exceptions.py](../src/atomadic_fuse/exceptions.py)

Bundled assets:
- [examples](../examples)
- [src/atomadic_fuse/logic-base-seed](../src/atomadic_fuse/logic-base-seed)

### Request flow

1. A caller invokes a `FuseClient` method or CLI verb.
2. The SDK constructs a typed request payload.
3. The hosted Fuse endpoint processes the request.
4. The SDK returns structured JSON-like data or raises a typed exception.
5. Verification-oriented calls can then be used to inspect health, validity, or traceability.

### MCP flow

1. An MCP host launches `fuse-mcp`.
2. MCP tool calls map to the public client surface.
3. Results are returned through stdio JSON-RPC.

## Public Boundary

This architecture document is intentionally limited to observable public behavior.

Included here:
- package structure
- request flow
- MCP flow
- public package metadata and examples

Excluded here:
- unpublished internal engine details
- private orchestration layers not required to use the SDK

## Packaging Facts

Current public package facts from [pyproject.toml](../pyproject.toml):
- package name: `atomadic-fuse`
- Python 3.10+
- runtime dependency: `httpx`
- optional extras: `mcp`, `gui`
- CLI entrypoints: `fuse`, `fuse-mcp`
