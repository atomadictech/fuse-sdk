# MCP Quickstart

Use Fuse MCP when you want an agent host or IDE to call the same public Fuse workflows available through the Python SDK.

## Install

```bash
pip install "atomadic-fuse[mcp]"
```

## Local stdio configuration

```json
{
  "mcpServers": {
    "atomadic-fuse": {
      "command": "fuse-mcp"
    }
  }
}
```

## Hosted MCP endpoint

- `https://fuse.atomadic.tech/mcp`

## Which mode should you use?

Use local stdio MCP when you want:
- local process ownership
- local environment control
- explicit shell and secret handling

Use hosted MCP when you want:
- a managed remote endpoint
- less local setup
- a simpler path for distributed agent clients

## Recommended smoke checks

After setup:
1. confirm the host can launch `fuse-mcp`
2. confirm the tool list includes public workflows you expect to use
3. run a small read-only or health-oriented request such as `doctor` or `usage_stats`

## Troubleshooting

- command not found: make sure the environment that owns `atomadic-fuse[mcp]` is active
- import failure: reinstall the package in the active environment
- hosted connection failure: verify endpoint reachability and credentials
- tool mismatch: compare installed package version with current docs and examples
