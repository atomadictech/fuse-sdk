"""Tests for FuseClient (mocked HTTP)."""
from __future__ import annotations

import json
from unittest.mock import patch, MagicMock

import pytest

from atomadic_fuse import FuseClient, FuseError, DecisionNeeded, PaymentRequired


def _mock_resp(status: int, body: dict | None = None) -> MagicMock:
    m = MagicMock()
    m.status_code = status
    m.json.return_value = body or {}
    m.text = json.dumps(body or {})
    m.content = m.text.encode() if body else b""
    return m


@patch("atomadic_fuse.client.httpx.Client")
def test_classify_happy_path(mock_client):
    inst = mock_client.return_value.__enter__.return_value
    inst.post.return_value = _mock_resp(200, {"action": "build", "confidence": 0.7487})
    c = FuseClient(api_key="k")
    out = c.classify("def f(x): return hash(x)", name="f")
    assert out["action"] == "build"
    assert out["confidence"] == 0.7487


@patch("atomadic_fuse.client.httpx.Client")
def test_payment_required_raises(mock_client):
    inst = mock_client.return_value.__enter__.return_value
    inst.post.return_value = _mock_resp(402, {
        "error": "Insufficient credits",
        "payment_url": "https://fuse.atomadic.tech/pay",
        "amount_usdc": "0.50",
    })
    c = FuseClient(api_key="k")
    with pytest.raises(PaymentRequired) as exc:
        c.compile("/tmp/repo")
    assert "Insufficient" in str(exc.value)
    assert exc.value.payment_url == "https://fuse.atomadic.tech/pay"


@patch("atomadic_fuse.client.httpx.Client")
def test_decision_needed_raises(mock_client):
    inst = mock_client.return_value.__enter__.return_value
    inst.post.return_value = _mock_resp(200, {
        "decision_required": True,
        "decision_id":       "dec_42",
        "prompt":            "Pick a Rust→Python type for *args",
        "options":           ["*args=tuple", "*args=list"],
    })
    c = FuseClient(api_key="k")
    with pytest.raises(DecisionNeeded) as exc:
        c.compile("/tmp/repo")
    assert exc.value.decision_id == "dec_42"
    assert len(exc.value.options) == 2


@patch("atomadic_fuse.client.httpx.Client")
def test_generic_5xx_raises_fuse_error(mock_client):
    inst = mock_client.return_value.__enter__.return_value
    inst.post.return_value = _mock_resp(503, {"error": "engine busy"})
    c = FuseClient(api_key="k")
    with pytest.raises(FuseError):
        c.doctor()


def test_endpoint_default():
    c = FuseClient(api_key="k")
    assert c.endpoint == "https://fuse.atomadic.tech/v1"


def test_endpoint_override():
    c = FuseClient(api_key="k", endpoint="http://localhost:8000/v1")
    assert c.endpoint == "http://localhost:8000/v1"


def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv("ATOMADIC_FUSE_API_KEY", "envk")
    c = FuseClient()
    assert c.api_key == "envk"
