# Atomadic Fuse SDK

Deterministic Python SDK and MCP server for the hosted Fuse engine.

This repository is the public integration surface for Atomadic Fuse. It provides:
- a typed Python client for hosted Fuse operations
- a stdio MCP server for agent runtimes
- example scripts for common workflows
- a bundled seed logic-base for local bootstrapping

## Install

```bash
pip install atomadic-fuse
```

Optional extras:

```bash
pip install "atomadic-fuse[mcp]"
pip install "atomadic-fuse[gui]"
```

## Quick Start

```python
from atomadic_fuse import FuseClient

client = FuseClient()

print(client.scan("./repo"))
print(client.absorb("./repo"))
print(client.synthesize("./repo"))

print(client.verify_block("lb:t2:compose_path_composite:bd7e1d030ef5"))
print(client.search_intent("validate and route input", tier="t2", limit=5))
```

## Package Surface

The package currently exposes:
- `FuseClient` for hosted API calls
- `fuse-mcp` for stdio MCP usage
- bundled examples under [examples](examples)
- bundled seed data under [src/atomadic_fuse/logic-base-seed](src/atomadic_fuse/logic-base-seed)

`FuseClient` currently exposes 34 public methods grouped around:
- repo flow: `scan`, `absorb`, `discover`, `synthesize`, `emit`, `compile`
- verification: `verify_block`, `validate`, `status`, `doctor`, `fuse_recovery_status`
- search and explanation: `search`, `search_intent`, `catalog`, `compose_stack`, `logic_map`, `explain_block`, `explain_lineage`
- language and output helpers: `langs`, `polyglot`, `show`, `emit_corpus`, `intent`, `capabilities`
- store and promotion helpers: `quickstart`, `friction`, `promote_hypotheses`, `promote_candidate`, `lint_store`, `validate_store`, `deduplicate_store`, `rebuild_indexes`

The source of truth for signatures is [src/atomadic_fuse/client.py](src/atomadic_fuse/client.py).

## MCP Setup

Local stdio MCP example:

```json
{
  "mcpServers": {
    "atomadic-fuse": {
      "command": "fuse-mcp"
    }
  }
}
```

Hosted MCP endpoint:
- `https://fuse.atomadic.tech/mcp`

## Documentation

- [Documentation Index](docs/README.md)
- [Public Whitepaper](docs/WHITEPAPER.md)
- [Architecture](docs/ARCHITECTURE.md)
- [MCP Quickstart](docs/MCP_QUICKSTART.md)
- [Security and Privacy](docs/SECURITY_AND_PRIVACY.md)
- [Operations Guide](docs/OPERATIONS.md)
- [Benchmarks](docs/BENCHMARKS.md)
- [Use Cases](docs/USE_CASES.md)
- [Comparison](docs/COMPARISON.md)

## Public-safe Scope

This repository is a public package surface.
- documentation should focus on verifiable behavior, package contracts, and integration guidance
- private implementation details are intentionally excluded from public docs
- operational claims should be reproducible from source, tests, or public endpoints

## License

MIT. See [LICENSE](LICENSE).
