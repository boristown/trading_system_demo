"""Thin wrapper around ccxt exchanges for the demo."""
from __future__ import annotations

import logging
from typing import Any, Dict, List

import ccxt

from .config import TradingConfig

LOGGER = logging.getLogger(__name__)


class ExchangeClient:
    """Wraps a ccxt exchange with convenience helpers."""

    def __init__(self, config: TradingConfig) -> None:
        self._config = config
        try:
            exchange_class = getattr(ccxt, config.exchange_id)
        except AttributeError as exc:  # pragma: no cover - defensive
            raise ValueError(f"Unsupported exchange: {config.exchange_id}") from exc

        kwargs: Dict[str, Any] = {
            "apiKey": config.api_key,
            "secret": config.api_secret,
            "enableRateLimit": True,
        }
        if config.passphrase:
            kwargs["password"] = config.passphrase

        self._exchange = exchange_class(kwargs)

        if config.sandbox and hasattr(self._exchange, "set_sandbox_mode"):
            LOGGER.info("Enabling sandbox mode for exchange %s", config.exchange_id)
            self._exchange.set_sandbox_mode(True)

    @property
    def exchange(self) -> ccxt.Exchange:
        """Expose the raw ccxt exchange instance."""

        return self._exchange

    def fetch_ohlcv(self, limit: int = 100) -> List[List[Any]]:
        """Fetch recent OHLCV candles for the configured trading pair."""

        LOGGER.debug(
            "Fetching %s OHLCV candles for %s", limit, self._config.symbol
        )
        return self._exchange.fetch_ohlcv(
            self._config.symbol, timeframe=self._config.timeframe, limit=limit
        )

    def fetch_balance(self) -> Dict[str, Any]:
        """Fetch the account balance."""

        return self._exchange.fetch_balance()

    def create_market_order(self, side: str, amount: float) -> Dict[str, Any]:
        """Create a market order if not in dry-run mode."""

        if self._config.dry_run:
            LOGGER.info(
                "Dry run active: skipped %s market order for %s %s",
                side,
                amount,
                self._config.symbol,
            )
            return {
                "status": "simulated",
                "side": side,
                "amount": amount,
                "symbol": self._config.symbol,
            }

        LOGGER.info(
            "Submitting %s market order for %s %s", side, amount, self._config.symbol
        )
        return self._exchange.create_order(
            symbol=self._config.symbol,
            type="market",
            side=side,
            amount=amount,
        )


__all__ = ["ExchangeClient"]
