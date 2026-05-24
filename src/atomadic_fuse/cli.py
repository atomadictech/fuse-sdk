"""Atomadic Fuse public SDK CLI — hosted read-only surface only."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from .client import FuseClient
from .exceptions import DecisionNeeded, FuseError, PaymentRequired

# Hosted public tools — mirrors atomadic-ops/workers/atomadic-fuse-api/src/tool_manifest.json
PUBLIC_HOSTED_VERBS: tuple[str, ...] = (
    "classify",
    "catalog",
    "doctor",
    "fuse_recovery_status",
    "verify_block",
    "search_intent",
    "explain_block",
    "usage_stats",
    "scan",
    "validate",
    "status",
    "search",
    "show",
    "langs",
)

LOCAL_VERBS: tuple[str, ...] = ("init", "seed-info", "list")


def _client_from_args(args: argparse.Namespace) -> FuseClient:
    return FuseClient(
        api_key=args.api_key,
        endpoint=args.endpoint,
        telemetry_opt_in=bool(getattr(args, "telemetry", False)),
    )


def _register_public_parsers(sub: argparse._SubParsersAction) -> None:
    sp = sub.add_parser("init", help="copy the bundled seed logic-base to ./logic-base/")
    sp.add_argument("--target", default="./logic-base", help="Where to seed the logic-base")
    sub.add_parser("seed-info", help="show the bundled seed logic-base path + counts")
    sub.add_parser("list", help="list available public verbs")

    sp = sub.add_parser("classify", help="classify a function by AST behavior")
    sp.add_argument("body_text")
    sp.add_argument("--name", default="")

    sp = sub.add_parser("catalog", help="query the curated public catalog")
    sp.add_argument("query")
    sp.add_argument("--limit", type=int, default=20)

    sub.add_parser("doctor", help="health probe across hosted engine + public seed")
    sub.add_parser("fuse_recovery_status", help="read-only Fuse recovery gate status")
    sub.add_parser("usage_stats", help="token-savings dashboard for public seed corpus")

    sp = sub.add_parser("verify_block", help="return block + SHA-256 verification receipt")
    sp.add_argument("block_id")

    sp = sub.add_parser("search_intent", help="semantic intent search over public seed")
    sp.add_argument("description")
    sp.add_argument("--tier", default="")
    sp.add_argument("--limit", type=int, default=10)

    sp = sub.add_parser("explain_block", help="context-aware block explanation")
    sp.add_argument("block_id")
    sp.add_argument("--detail", action="store_true")

    sp = sub.add_parser("scan", help="hosted guidance to scan a local directory")
    sp.add_argument("directory")
    sp.add_argument("--languages", default="python,typescript,rust")

    sp = sub.add_parser("validate", help="validate a CNAE name against vocabulary")
    sp.add_argument("name")

    sp = sub.add_parser("status", help="read-only curated logic-base status")
    sp.add_argument("--workspace", default="")

    sp = sub.add_parser("search", help="substring + CNAE search across public seed")
    sp.add_argument("query")
    sp.add_argument("--workspace", default="")

    sp = sub.add_parser("show", help="drill into one atom in the public seed")
    sp.add_argument("name")
    sp.add_argument("--workspace", default="")

    sub.add_parser("langs", help="list supported polyglot language targets")


def _dispatch_public(client: FuseClient, args: argparse.Namespace) -> dict:
    verb = args.verb
    if verb == "classify":
        return client.classify(args.body_text, name=args.name)
    if verb == "catalog":
        return client.catalog(args.query, limit=args.limit)
    if verb == "doctor":
        return client.doctor()
    if verb == "fuse_recovery_status":
        return client.fuse_recovery_status()
    if verb == "verify_block":
        return client.verify_block(args.block_id)
    if verb == "search_intent":
        return client.search_intent(args.description, tier=args.tier, limit=args.limit)
    if verb == "explain_block":
        return client.explain_block(args.block_id, detail=args.detail)
    if verb == "usage_stats":
        return client.usage_stats()
    if verb == "scan":
        return client.scan(args.directory, languages=args.languages)
    if verb == "validate":
        return client.validate(args.name)
    if verb == "status":
        return client.status(workspace=args.workspace)
    if verb == "search":
        return client.search(args.query, workspace=args.workspace)
    if verb == "show":
        return client.show(args.name, workspace=args.workspace)
    if verb == "langs":
        return client.langs()
    raise FuseError(f"unknown public verb: {verb}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="fuse-sdk",
        description="Atomadic Fuse public SDK — hosted read-only tools at fuse.atomadic.tech.",
    )
    p.add_argument("--api-key", default=None)
    p.add_argument("--endpoint", default=None)
    p.add_argument(
        "--telemetry",
        action="store_true",
        help="Opt-in to anonymized metadata telemetry (CNAE/tier/domain/language — never code or intent text)",
    )
    sub = p.add_subparsers(dest="verb", required=True)
    _register_public_parsers(sub)

    args = p.parse_args(argv)

    if args.verb == "list":
        verbs = ", ".join([*LOCAL_VERBS, *PUBLIC_HOSTED_VERBS])
        print(f"Atomadic Fuse public SDK — verbs: {verbs}")
        print("Docs: https://github.com/atomadictech/fuse-sdk")
        print("Live stats: https://sot.atomadic.tech/SoT.json")
        return 0

    if args.verb == "seed-info":
        from . import seed_path

        sp = seed_path()
        if not sp.is_dir():
            print(f"seed not bundled at {sp} -- reinstall atomadic-fuse", file=sys.stderr)
            return 1
        blocks = 0
        shards = 0
        for shard in sp.rglob("*.jsonl"):
            shards += 1
            blocks += sum(1 for ln in open(shard, encoding="utf-8") if ln.strip())
        print(json.dumps({"seed_path": str(sp), "blocks": blocks, "shards": shards}, indent=2))
        return 0

    if args.verb == "init":
        target = Path(args.target)
        from . import seed_path

        src = seed_path()
        if not src.is_dir():
            print(f"seed not bundled at {src} -- reinstall atomadic-fuse", file=sys.stderr)
            return 1
        if target.exists():
            print(json.dumps({"ok": True, "target": str(target.resolve()), "skipped": "already exists"}, indent=2))
            return 0
        shutil.copytree(src, target)
        print(json.dumps({"ok": True, "target": str(target.resolve()), "copied_from": str(src)}, indent=2))
        return 0

    client = _client_from_args(args)
    try:
        out = _dispatch_public(client, args)
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
