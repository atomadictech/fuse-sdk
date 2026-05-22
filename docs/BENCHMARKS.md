# Benchmarks

This document is intentionally conservative.

## Rule

Only publish benchmark or performance claims that can be reproduced from:
- package tests
- public endpoints
- source in this repository

## Recommended Measurement Areas

- package import time
- local MCP startup success
- basic hosted call latency for read-only methods
- regression stability across released versions

## Suggested Procedure

1. capture environment details
2. run the same method multiple times
3. record median and tail latency separately
4. distinguish local stdio MCP results from hosted endpoint results

Avoid mixing private infrastructure data with public documentation.
