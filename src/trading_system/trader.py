"""Trading orchestration logic."""
from __future__ import annotations

import logging
from typing import Dict, Optional

from .config import TradingConfig
from .exchange import ExchangeClient
from .strategy import SMACrossoverStrategy, StrategyResult

LOGGER = logging.getLogger(__name__)


class Trader:
    """Coordinates strategy evaluation and order execution."""

    def __init__(self, config: TradingConfig, exchange: ExchangeClient) -> None:
        self.config = config
        self.exchange = exchange
        self.strategy = SMACrossoverStrategy(
            fast_window=config.fast_window, slow_window=config.slow_window
        )
        self.base_currency = config.symbol.split("/")[0]

    def evaluate(self) -> StrategyResult:
        LOGGER.debug("Fetching candles for evaluation")
        candles = self.exchange.fetch_ohlcv(limit=self.config.slow_window * 3)
        result = self.strategy.evaluate(candles)
        LOGGER.info(
            "Strategy signal=%s fast_ma=%.4f slow_ma=%.4f",
            result.signal,
            result.fast_ma,
            result.slow_ma,
        )
        return result

    def _resolve_order_amount(self, signal: Optional[str]) -> Optional[float]:
        if signal not in {"buy", "sell"}:
            return None

        if signal == "buy":
            return self.config.base_order_size

        balance = self.exchange.fetch_balance()
        amount = balance.get(self.base_currency, {}).get("free")
        if amount is None:
            LOGGER.warning(
                "Unable to determine free balance for %s, defaulting to base order size",
                self.base_currency,
            )
            return self.config.base_order_size

        return min(amount, self.config.base_order_size)

    def execute(self, result: StrategyResult) -> Optional[Dict]:
        amount = self._resolve_order_amount(result.signal)
        if not amount:
            LOGGER.info("No actionable signal from strategy")
            return None

        LOGGER.debug("Resolved order amount %s", amount)
        return self.exchange.create_market_order(result.signal or "buy", amount)


__all__ = ["Trader"]
