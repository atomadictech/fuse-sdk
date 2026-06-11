# ⛔ This repo is SUPERSEDED

> **Canonical SDK:** https://github.com/atomadictech/atomadic-sdk
> **PyPI:** https://pypi.org/project/atomadic/
> **Docs:** https://atomadic.tech/docs.html

This repository was an early per-product SDK that has been **merged into the
unified `atomadic-sdk`**. The product surface (Fuse / Nexus / Healer /
Security / Proving / Release / Evolve / Research / Mind Lab / Aegis /
Vanguard / Catalyst) is now one package, one MCP, one entitlement key.

## Migration

```bash
# OLD (this repo):
# pip install atomadic-<product>-sdk

# NEW (unified):
pip install atomadic
```

```python
from atomadic import Atomadic, fuse, nexus, security, healer  # etc.
ato = Atomadic(api_key='ato_...')
fuse.assess_architecture_pure(ato, source_text=..., module_name=...)
```

## Verify yourself

The unified SDK ships with an offline closure receipt verifier:

- **Trust Center:** https://atomadic.tech/trust.html
- **Polyglot Playground:** https://atomadic.tech/polyglot-playground.html
- **Proof:** https://atomadic.tech/proof.html
- **Independent verification kit:** https://github.com/atomadictech/omega-verification-kit

Map = Terrain. 🪨
