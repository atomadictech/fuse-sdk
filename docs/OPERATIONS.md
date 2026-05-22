# Operations Guide

## Validation Checklist

Before release or rollout:
1. install the package in a clean environment
2. run unit tests
3. run a smoke sequence through the client surface
4. verify MCP startup and tool availability

## Suggested Commands

```bash
python -m pytest -q
python -c "from atomadic_fuse import FuseClient; print('sdk_import_ok')"
```

## Runtime Health Checks

Recommended recurring checks:
- `doctor`
- `status`
- `usage_stats`

## Upgrade Procedure

1. pin the current package version
2. upgrade in staging
3. rerun tests and smoke checks
4. promote after verification passes

## Rollback Procedure

1. revert the package version pin
2. restart MCP runtimes using the package
3. rerun smoke checks to confirm the recovered baseline

## Documentation Maintenance

When the API surface changes, update:
- [README.md](../README.md)
- [WHITEPAPER.md](WHITEPAPER.md)
- [MCP_QUICKSTART.md](MCP_QUICKSTART.md)
- examples in [examples](../examples) where relevant
