"""Trading strategies for the demo trading system."""
from __future__ import annotations

import dataclasses
from statistics import mean
from typing import Iterable, List, Optional


@dataclasses.dataclass
class StrategyResult:
    signal: Optional[str]
    fast_ma: float
    slow_ma: float


class SMACrossoverStrategy:
    """Simple moving average crossover strategy."""

    def __init__(self, fast_window: int, slow_window: int) -> None:
        if fast_window >= slow_window:
            raise ValueError("fast_window must be smaller than slow_window")
        self.fast_window = fast_window
        self.slow_window = slow_window

    @staticmethod
    def _closing_prices(candles: Iterable[List[float]]) -> List[float]:
        return [candle[4] for candle in candles]

    def evaluate(self, candles: List[List[float]]) -> StrategyResult:
        if len(candles) < self.slow_window:
            raise ValueError(
                "Not enough candles to evaluate strategy: "
                f"need {self.slow_window}, got {len(candles)}"
            )

        closes = self._closing_prices(candles)
        fast = mean(closes[-self.fast_window :])
        slow = mean(closes[-self.slow_window :])

        signal: Optional[str]
        if fast > slow:
            signal = "buy"
        elif fast < slow:
            signal = "sell"
        else:
            signal = None

        return StrategyResult(signal=signal, fast_ma=fast, slow_ma=slow)


__all__ = ["SMACrossoverStrategy", "StrategyResult"]
