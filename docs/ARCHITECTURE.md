# Architecture

## Components

- SDK client: [src/atomadic_fuse/client.py](../src/atomadic_fuse/client.py)
- MCP server: [src/atomadic_fuse/mcp_server.py](../src/atomadic_fuse/mcp_server.py)
- Exceptions: [src/atomadic_fuse/exceptions.py](../src/atomadic_fuse/exceptions.py)
- Examples: [examples](../examples)
- Seed logic-base: [src/atomadic_fuse/logic-base-seed](../src/atomadic_fuse/logic-base-seed)

## Request Flow

1. A caller invokes a `FuseClient` method.
2. The client serializes a request payload and headers.
3. The hosted endpoint processes the request.
4. The response is converted into either structured output or a typed exception.
5. Verification-oriented methods return receipt-bearing payloads suitable for audit and automation.

## MCP Flow

1. An MCP host launches `fuse-mcp`.
2. MCP tool invocations map to the underlying client surface.
3. Results are returned through stdio JSON-RPC.

This gives agent runtimes and direct Python callers a shared operational surface.

## Public Boundary

This repository documents the public package contract, not private engine internals. The architectural material here is limited to the observable client, MCP, and hosted request path needed for integration.

## Package Metadata

Current package metadata is defined in [pyproject.toml](../pyproject.toml).

Notable public characteristics:
- Python 3.10+
- `httpx` runtime dependency
- optional MCP extra via `mcp[cli]`
- optional GUI extra via `gradio`
