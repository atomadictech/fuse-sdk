# Benchmarks Guidance

This repository keeps benchmark language intentionally conservative.

## Rule

Only publish performance claims that can be reproduced from:
- package tests
- public endpoints
- source in this repository
- a documented benchmark procedure another developer can repeat

## Good Public Benchmark Areas

- package import time
- CLI startup success
- MCP startup success
- hosted call latency for read-only or health-oriented methods
- regression stability across released versions

## Suggested Procedure

1. capture environment details
2. run the same method multiple times
3. record median and tail latency separately
4. distinguish local stdio MCP measurements from hosted endpoint measurements
5. separate SDK overhead from remote endpoint latency where possible

## What Not To Do

- do not publish private infrastructure figures as public SDK claims
- do not mix synthetic local numbers with hosted latency without labeling them clearly
- do not claim superiority without a reproducible public comparison method
