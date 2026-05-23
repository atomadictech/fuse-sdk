"""Typed exception surface for the Atomadic Fuse SDK."""
from __future__ import annotations

from typing import Any


class FuseError(RuntimeError):
    """Base error for hosted Fuse API failures."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload or {}


class DecisionNeeded(FuseError):
    """Raised when the engine requests an explicit caller decision."""

    def __init__(
        self,
        decision_id: str,
        prompt: str,
        options: list[str],
        message: str = "Decision required",
        payload: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=200, payload=payload)
        self.decision_id = decision_id
        self.prompt = prompt
        self.options = options


class PaymentRequired(FuseError):
    """HTTP 402: fund via x402/credits and retry."""

    def __init__(
        self,
        message: str = "Payment required",
        payment_url: str | None = None,
        amount_usdc: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=402, payload=payload)
        self.payment_url = payment_url
        self.amount_usdc = amount_usdc


__all__ = ["FuseError", "DecisionNeeded", "PaymentRequired"]
