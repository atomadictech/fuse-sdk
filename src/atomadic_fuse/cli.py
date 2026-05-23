"""Atomadic Fuse CLI entry point."""
from __future__ import annotations

import argparse
import json
import sys

from .client import FuseClient
from .exceptions import DecisionNeeded, FuseError, PaymentRequired


def _client_from_args(args: argparse.Namespace) -> FuseClient:
    return FuseClient(
        api_key=args.api_key,
        endpoint=args.endpoint,
        telemetry_opt_in=bool(getattr(args, "telemetry", False)),
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fuse", description="Atomadic Fuse — Spaghetti to Shippable.")
    p.add_argument("--api-key",  default=None)
    p.add_argument("--endpoint", default=None)
    p.add_argument("--telemetry", action="store_true",
                   help="Opt-in to anonymized metadata telemetry (CNAE/tier/domain/language — never code or intent text)")
    sub = p.add_subparsers(dest="verb", required=True)

    sp = sub.add_parser("init", help="copy the bundled seed logic-base to ./logic-base/")
    sp.add_argument("--target", default="./logic-base",
                    help="Where to seed the logic-base (default: ./logic-base/)")

    sp = sub.add_parser("seed-info", help="show the bundled seed logic-base path + counts")

    sp = sub.add_parser("compile", help="messy repo → clean shippable package")
    sp.add_argument("repo_root")
    sp.add_argument("--output", default="./_fuse_out")
    sp.add_argument("--max-chains", type=int, default=5)

    sp = sub.add_parser("classify", help="classify a function by AST behavior")
    sp.add_argument("body_text")
    sp.add_argument("--name", default="")

    sp = sub.add_parser("absorb", help="add a repo to the Logic-Base")
    sp.add_argument("repo_root")
    sp.add_argument("--label", default=None)

    sp = sub.add_parser("catalog", help="query the catalog")
    sp.add_argument("query")
    sp.add_argument("--limit", type=int, default=20)

    sub.add_parser("capabilities", help="list emergent cross-source chains")
    sub.add_parser("doctor", help="health probe")

    sp = sub.add_parser("intent", help="natural-language intent → product")
    sp.add_argument("intent_phrase")
    sp.add_argument("--output", default="./_intent_out")

    sub.add_parser("list", help="list available verbs")

    args = p.parse_args(argv)

    if args.verb == "list":
        print("Atomadic Fuse — verbs: init, seed-info, compile, classify, absorb, catalog, "
              "capabilities, intent, doctor")
        print("Docs: https://github.com/atomadictech/atomadic-fuse")
        print("Live stats: https://sot.atomadic.tech/SoT.json")
        return 0

    if args.verb == "seed-info":
        from . import seed_path
        sp = seed_path()
        if not sp.is_dir():
            print(f"seed not bundled at {sp} -- reinstall atomadic-fuse", file=sys.stderr)
            return 1
        blocks = 0; shards = 0
        for shard in sp.rglob("*.jsonl"):
            shards += 1
            blocks += sum(1 for ln in open(shard, encoding="utf-8") if ln.strip())
        print(json.dumps({"seed_path": str(sp), "blocks": blocks, "shards": shards}, indent=2))
        return 0

    if args.verb == "init":
        client = _client_from_args(args)
        try:
            out = client.init(target_dir=args.target)
            print(json.dumps(out, indent=2))
            return 0
        except FuseError as e:
            print(f"FuseError: {e}", file=sys.stderr)
            return 1

    client = _client_from_args(args)
    try:
        if args.verb == "compile":
            out = client.compile(args.repo_root, output_root=args.output,
                                 max_chains=args.max_chains)
        elif args.verb == "classify":
            out = client.classify(args.body_text, name=args.name)
        elif args.verb == "absorb":
            out = client.absorb(args.repo_root, repo_label=args.label)
        elif args.verb == "catalog":
            out = client.catalog(args.query, limit=args.limit)
        elif args.verb == "capabilities":
            out = client.capabilities()
        elif args.verb == "intent":
            out = client.intent(args.intent_phrase, output_root=args.output)
        elif args.verb == "doctor":
            out = client.doctor()
        else:
            print(f"unknown verb: {args.verb}", file=sys.stderr)
            return 2
        print(json.dumps(out, indent=2, default=str))
        return 0
    except PaymentRequired as e:
        print(f"402 Payment Required: {e}", file=sys.stderr)
        if e.payment_url:
            print(f"Top up: {e.payment_url}", file=sys.stderr)
        return 1
    except DecisionNeeded as e:
        print(f"DECISION_NEEDED ({e.decision_id}): {e.prompt}", file=sys.stderr)
        print(f"Options: {e.options}", file=sys.stderr)
        return 3
    except FuseError as e:
        print(f"FuseError: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
