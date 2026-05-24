"""Example: compose-stack preview, then emit_corpus to a target language.

`compose_stack` walks the full dependency chain for an intent (highest tier → T0)
and returns the complete composed stack — every block that would be
emitted, with its tier and inter-dependencies. Run it before `emit_corpus`
to see exactly what you'll get.

`emit_corpus` then writes the verified blocks as a target-language
package (rust, python, typescript, go, haskell_native, gui_web).

Run:
    pip install atomadic-fuse
    export ATOMADIC_FUSE_API_KEY=...
    python examples/05_compose_emit.py
"""
from atomadic_fuse import FuseClient


def main() -> int:
    client = FuseClient()

    # 1. Preview the composition graph for an intent.
    intent = "validate a contract and persist the result to a hash-chained ledger"
    preview = client.compose_stack(intent=intent, target_language="rust")
    stack = preview.get("stack", preview.get("blocks", []))
    print(f"Composition preview for: {intent!r}")
    print(f"  blocks in stack: {len(stack)}")
    for entry in stack[:8]:
        cnae = entry.get("cnae", "?")
        tier = entry.get("tier", "?")
        print(f"  - t{tier} {cnae}")

    # 2. Emit the verified corpus for the same target.
    out = client.emit_corpus(target_language="rust", target_dir="./_fuse_emit_rust")
    artifact_hash = out.get("artifact_hash") or out.get("hash", "?")
    file_count = out.get("file_count") or len(out.get("files", []))
    print(f"\nEmit complete: {file_count} files written; artifact_hash={artifact_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
