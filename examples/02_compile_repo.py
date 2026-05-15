"""Example: compile a messy repo into a clean Python package.

The marquee Fuse primitive. Hand it any repo (Python, TypeScript, Rust,
Go, etc.) and Fuse emits a clean 5-tier monadic Python package with a
CLI, an MCP server, tests, and a Cloudflare deploy bundle.

Run:
    pip install atomadic-fuse
    python examples/02_compile_repo.py /path/to/some/messy/repo
"""
import sys

from atomadic_fuse import FuseClient, DecisionNeeded, PaymentRequired


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: 02_compile_repo.py <repo_root> [output_root]")
        return 2

    repo_root   = argv[1]
    output_root = argv[2] if len(argv) > 2 else "./_fuse_out"

    client = FuseClient()
    try:
        report = client.compile(repo_root, output_root=output_root, max_chains=10)
    except DecisionNeeded as e:
        print(f"Cross-language decision needed ({e.decision_id}): {e.prompt}")
        print(f"Options: {e.options}")
        return 3
    except PaymentRequired as e:
        print(f"402 Payment Required. Top up: {e.payment_url}")
        return 1

    print(f"OK. Compiled {repo_root} -> {report.get('product_dir')}")
    print(f"   atoms:        {report.get('atom_count')}")
    print(f"   capabilities: {len(report.get('capabilities', []))}")
    print(f"   product_sha:  {report.get('product_sha')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
