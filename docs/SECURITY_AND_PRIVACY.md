# Security and Privacy

## Scope

This document covers the public-surface security guidance for Fuse SDK consumers.

## Trust Model

- The SDK is a client and MCP bridge.
- Hosted Fuse endpoints are a remote trust boundary.
- Verification-oriented methods should be used in any high-assurance workflow.

## Credentials

Recommended practice:
- inject API keys through environment variables or secret managers
- avoid committing credentials to source control
- keep request logs free of secrets

## Data Handling

- send only the repository data needed for a workflow
- use isolated environments for CI and agent execution
- retain verification outputs when auditability matters

## MCP Runtime Safety

- scope MCP hosts to explicit workspaces
- use least-privilege runtime permissions
- separate development and production MCP configurations

## Public-safe Documentation Rule

Public docs in this repository should not disclose confidential internals, unpublished constants, or private orchestration details that are not required to consume the SDK.

## Incident Baseline

If unexpected behavior occurs:
1. capture request and response metadata without secrets
2. run `doctor` and `status`
3. isolate the failing workflow
4. roll back to a known-good SDK version if needed
