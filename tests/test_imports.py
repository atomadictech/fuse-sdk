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
