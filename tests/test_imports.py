"""Surface-import smoke tests for atomadic-fuse SDK."""
from __future__ import annotations


def test_package_imports():
    import atomadic_fuse
    # Version-agnostic SemVer-shaped check (don't pin a literal — same drift
    # pattern as the Nexus SDK 0.1.0->0.2.0 silent miss).
    import re
    assert isinstance(atomadic_fuse.__version__, str)
    assert re.match(r"^\d+\.\d+\.\d+", atomadic_fuse.__version__), (
        f"version {atomadic_fuse.__version__!r} not SemVer-shaped"
    )


def test_client_class_exists():
    from atomadic_fuse import FuseClient
    assert FuseClient is not None
    assert hasattr(FuseClient, "compile")
    assert hasattr(FuseClient, "classify")
    assert hasattr(FuseClient, "absorb")
    assert hasattr(FuseClient, "catalog")
    assert hasattr(FuseClient, "capabilities")
    assert hasattr(FuseClient, "intent")
    assert hasattr(FuseClient, "doctor")


def test_exceptions_are_typed():
    from atomadic_fuse import FuseError, DecisionNeeded, PaymentRequired
    assert issubclass(DecisionNeeded, FuseError)
    assert issubclass(PaymentRequired, FuseError)


def test_cli_help_does_not_crash():
    import subprocess, sys
    r = subprocess.run([sys.executable, "-m", "atomadic_fuse.cli", "list"],
                       capture_output=True, text=True, timeout=10)
    assert r.returncode == 0
    assert "Atomadic Fuse" in r.stdout


def test_client_has_engine_parity_methods():
    """Client must expose langs, polyglot, show (engine parity added in v1.0.0)."""
    from atomadic_fuse import FuseClient
    for method in ("langs", "polyglot", "show"):
        assert hasattr(FuseClient, method), (
            f"FuseClient missing .{method}() — engine parity method not found"
        )


def test_user_agent_uses_package_version():
    """User-Agent header must reflect the installed package version, not a literal."""
    from atomadic_fuse.client import FuseClient, _pkg_version
    client = FuseClient.__new__(FuseClient)
    client.api_key = None
    client.telemetry_opt_in = False
    headers = client._headers()
    ua = headers.get("User-Agent", "")
    version = _pkg_version()
    assert ua == f"atomadic-fuse/{version}", (
        f"User-Agent {ua!r} does not reflect installed version {version!r}"
    )
    assert "1.0.0" in ua or version in ua


def test_mcp_server_exposes_engine_parity_tools():
    """MCP server must register langs, polyglot, show tools."""
    import importlib
    mod = importlib.import_module("atomadic_fuse.mcp_server")
    tool_names = {t.name for t in mod.mcp._tool_manager.list_tools()}
    for expected in ("langs", "polyglot", "show"):
        assert expected in tool_names, (
            f"MCP server missing tool '{expected}' — engine parity not achieved"
        )
