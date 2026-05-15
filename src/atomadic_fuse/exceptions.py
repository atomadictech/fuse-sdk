"""Atomadic Fuse SDK exceptions."""
from __future__ import annotations


class FuseError(Exception):
    """Base for any Fuse-side error returned by the hosted engine."""


class DecisionNeeded(FuseError):
    """Hosted engine returned a typed DECISION_NEEDED packet — caller
    must resolve (e.g. cross-language oracle) and resume via
    ``client.resume(decision_id, choice)``."""

    def __init__(self, decision_id: str, prompt: str, options: list[str]):
        super().__init__(f"decision required: {prompt}")
        self.decision_id = decision_id
        self.prompt = prompt
        self.options = options


class PaymentRequired(FuseError):
    """HTTP 402 — fund the wallet (x402) or add a credit pack (Stripe)
    and retry. ``error.payment_url`` carries a 1-click top-up link."""

    def __init__(self, message: str, payment_url: str | None = None,
                 amount_usdc: str | None = None):
        super().__init__(message)
        self.payment_url = payment_url
        self.amount_usdc = amount_usdc
