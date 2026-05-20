# Atomadic Fuse — Documentation

> 🟣 **In plain English:** the README on the front of the repo tells you what Fuse is and how to call it. These docs tell you everything else — the math, the architecture, the proof, the comparisons, and the use cases.

| Doc | Audience | Read this if you want… |
|---|---|---|
| [**WHITEPAPER.md**](./WHITEPAPER.md) | Engineering leaders, CTOs, reviewers | The full technical paper — what TOCC is, why it works, the self-hosting proof, the closed loop, the 11-gate promotion ladder. |
| [**USE_CASES.md**](./USE_CASES.md) | Buyers, builders | Five concrete scenarios with the exact API call and what comes back. Plain English on each. |
| [**BENCHMARKS.md**](./BENCHMARKS.md) | Procurement, finance | Live token-savings numbers, latency, corpus stats — every number cites a reproducible source. |
| [**COMPARISON.md**](./COMPARISON.md) | Anyone with an alternative on their shortlist | Side-by-side against LangChain, AutoGen, Copilot, Cursor, and other code-gen frameworks. |
| [**ARCHITECTURE.md**](./ARCHITECTURE.md) | Engineers integrating | The deep dive — kernel, hosted engine, SDK, MCP, x402, receipts. |
| [**TRADING_COMPILER.md**](./TRADING_COMPILER.md) | Quant teams, algo traders | The dedicated SKU built on top of Fuse — point it at messy strategy repos, get back clean backtestable bots. |

---

## Quick reproducible proof

```python
>>> from atomadic_fuse import FuseClient
>>> FuseClient().usage_stats()
# returns the live corpus stats every number in BENCHMARKS.md is sourced from
```

This is not a marketing brochure. Every number in these docs has a `c.usage_stats()` or `gh api` command you can run yourself.
