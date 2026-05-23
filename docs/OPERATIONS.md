# Operations Guide

This guide covers public operational practice for shipping Fuse SDK in scripts, CI pipelines, and agent environments.

## Release Checklist

Before rollout:
1. install the package in a clean environment
2. run the test suite
3. run a basic import or CLI smoke check
4. verify the MCP server starts if you use MCP mode
5. validate one representative hosted workflow you rely on in production

## Suggested Smoke Checks

```bash
python -m pytest -q
python -c "from atomadic_fuse import FuseClient; print('sdk_import_ok')"
fuse doctor
fuse seed-info
```

## Runtime Health Checks

Recommended recurring checks:
- `doctor`
- `status`
- `usage_stats`
- verification-oriented methods for critical flows

## Upgrade Procedure

1. pin the current package version
2. upgrade in staging or a disposable environment
3. rerun tests and smoke checks
4. verify MCP startup if applicable
5. promote after the checks pass

## Rollback Procedure

1. revert the package version pin
2. restart services or MCP runtimes that use the package
3. rerun smoke checks to confirm recovery

## Documentation Maintenance

When the public API or pricing surface changes, review and update:
- [README.md](../README.md)
- [WHITEPAPER.md](WHITEPAPER.md)
- [MCP_QUICKSTART.md](MCP_QUICKSTART.md)
- [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md)
- relevant examples in [examples](../examples)
