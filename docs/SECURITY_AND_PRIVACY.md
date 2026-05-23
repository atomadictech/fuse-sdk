# Security and Privacy

This document covers the public-facing security guidance for Fuse SDK consumers.

## Plain-English Summary

Fuse is a public SDK and MCP bridge. Treat the hosted endpoint as a remote trust boundary, protect your credentials, and use verification methods as part of normal operation.

## Trust Model

- the SDK is a public client layer
- hosted Fuse endpoints are a remote service boundary
- verification-oriented methods should be used in high-assurance workflows
- MCP hosts should run with explicit workspace and permission boundaries

## Credentials

Recommended practice:
- inject API keys through environment variables or a secret manager
- avoid committing credentials to source control
- keep logs and crash reports free of secrets
- separate development, staging, and production credentials

## Data Handling

Recommended practice:
- send only the repository data needed for the workflow you are running
- use isolated environments for CI and agent execution
- retain verification outputs or response metadata when auditability matters
- review third-party storage and logging policy in the environments that call the SDK

## MCP Runtime Safety

- scope MCP hosts to explicit workspaces
- use least-privilege permissions where possible
- keep local stdio MCP and hosted MCP configurations separate when environments differ
- smoke-test the tool surface before broad rollout

## Incident Baseline

If unexpected behavior occurs:
1. capture request and response metadata without secrets
2. run health-oriented calls such as `doctor` and `status`
3. isolate the failing workflow to the smallest reproducible case
4. roll back to a known-good SDK version if needed

## Atomadic-Security (T5 overlay)

S2S and ingest paths compose with the **Atomadic-Security** T5 product for malicious-pattern screening and bubble health. These tools are public read-only (or trust-gated for harden) — not part of the base hosted SDK method list unless the security profile is active.

| Tool / CLI | Mode | Role in S2S |
|------------|------|-------------|
| `security_scan` / `security-scan` | Read-only | Pattern detect across gate categories |
| `bubble_status` / `bubble-status` | Read-only | Quarantine stats + defense catalog count |
| `harden` | Trust-gated (dry-run default) | Enterprise operator bubble harden |
| `gate_malicious_logic` (pipeline) | Automatic in S2S | REJECT blocks chain + thank-you contributor path |

**Not public:** `harden_bubble`, `loop_security_bubble`, `synthesize_defenses`, `harvest_logic`, `train_fuse` (T6 internal).

Config: `atomadic-fuse-next/.atomadic/sovereign/atomadic_security_config.json`  
Product README: [`Atomadic-Security/README.md`](../../Atomadic-Security/README.md)  
Authoritative boundary: [`docs/PUBLIC_INTERNAL_BOUNDARY.md`](../../docs/PUBLIC_INTERNAL_BOUNDARY.md) (Atomadic-Security overlay section).

When `FUSE_PRODUCT_PROFILE=atomadic_security`, `security_scan` and `bubble_status` join the effective public MCP allowlist.

## Public Documentation Rule

Public docs in this repository should describe security practices and public behavior only. They should not disclose confidential internals or unpublished control systems that are not required for SDK consumers.
