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

## Public Documentation Rule

Public docs in this repository should describe security practices and public behavior only. They should not disclose confidential internals or unpublished control systems that are not required for SDK consumers.
