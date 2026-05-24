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
- Discovery: `https://fuse.atomadic.tech/.well-known/mcp.json`
- Agent card: `https://fuse.atomadic.tech/.well-known/agent.json`

### Public tools (14)

`classify`, `catalog`, `doctor`, `fuse_recovery_status`, `verify_block`, `search_intent`, `explain_block`, `usage_stats`, `scan`, `validate`, `status`, `search`, `show`, `langs`

Master key (`ATOMADIC_MASTER_KEY`) unlocks 20 additional internal operator tools (`compile`, `absorb`, `synthesize`, etc.).

```bash
export ATOMADIC_FUSE_API_KEY=your_pro_key   # 14 public tools
# or ATOMADIC_MASTER_KEY for full hosted surface
```

## Which mode should you use?

Use local stdio MCP when you want:
- local process ownership
- local environment control
- explicit shell and secret handling
- **Spaghetti to Shippable (S2S)** via `spaghetti_to_shippable` / `s2s` tools on `fuse-engine`

Use hosted MCP when you want:
- a managed remote endpoint
- less local setup
- a simpler path for distributed agent clients
- catalog, classify, compile, and verification against the curated public logic-base slice

### S2S: hosted vs local fuse-engine

| Need | Use |
|------|-----|
| Full single-repo S2S (ingest → heal → fitness gate → T5 bow) | **Local `fuse-engine` MCP** or `fuse s2s` CLI — **fuse-next only until stable promotion** |
| Dry-run S2S plan | Local MCP with `dry_run=true` (default) — public, no trust token |
| Live S2S apply | Local MCP with `dry_run=false` — trust-gated (`gate_intent` + malicious gate + Nexus/token) |
| Remote catalog / compile / doctor | Hosted `https://fuse.atomadic.tech/mcp` or `FuseClient` HTTP |

Local fuse-engine configuration (dev workspace):

```json
{
  "mcpServers": {
    "fuse-engine": {
      "command": "C:\\Atomadic-Omega\\atomadic-fuse-next\\fuse-mcp-system.cmd",
      "env": {
        "PYTHONPATH": "C:\\Atomadic-Omega\\atomadic-fuse-next\\src",
        "FUSE_DEV_WORKSPACE": "C:\\Atomadic-Omega\\atomadic-fuse-next",
        "FUSE_WORKSPACE": "C:\\Atomadic-Omega\\atomadic-fuse"
      }
    }
  }
}
```

See [S2S and Engine Boundary](S2S_AND_ENGINE_BOUNDARY.md) for repo map and polyglot output layout.

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
