# MCP Quickstart

## Install

```bash
pip install "atomadic-fuse[mcp]"
```

## Local stdio MCP configuration

```json
{
  "mcpServers": {
    "atomadic-fuse": {
      "command": "fuse-mcp"
    }
  }
}
```

## Hosted endpoint

- `https://fuse.atomadic.tech/mcp`

Use local stdio mode when you want local process ownership and environment control. Use the hosted endpoint when you want a managed remote MCP surface.

## Recommended smoke checks

After setup:
1. confirm the MCP host can launch `fuse-mcp`
2. confirm the tool list includes `scan`, `synthesize`, `verify_block`, and `usage_stats`
3. run a small read-only call such as `usage_stats`

## Troubleshooting

- `command not found`: ensure the Python environment that owns `atomadic-fuse[mcp]` is active
- import failure: reinstall the package in the active environment
- connection failure: verify network reachability for hosted mode or path resolution for stdio mode
