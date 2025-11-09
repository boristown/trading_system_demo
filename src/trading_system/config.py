"""Configuration helpers for the trading bot demo."""
from __future__ import annotations

import dataclasses
import os
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency in tests
    load_dotenv = None  # type: ignore


@dataclasses.dataclass
class TradingConfig:
    """Runtime configuration for the trading system demo."""

    exchange_id: str = "binance"
    symbol: str = "BTC/USDT"
    timeframe: str = "1m"
    fast_window: int = 5
    slow_window: int = 20
    base_order_size: float = 0.001
    quote_currency: str = "USDT"
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    passphrase: Optional[str] = None
    dry_run: bool = True
    sandbox: bool = False
    poll_interval: int = 60


def load_config(env_path: Optional[str] = None) -> TradingConfig:
    """Load configuration from environment variables.

    Args:
        env_path: Optional path to a ``.env`` file to load before reading the
            environment. If set and python-dotenv is installed, the file will be
            parsed. When the package is not available the argument is ignored.

    Returns:
        A :class:`TradingConfig` instance populated with environment values.
    """

    if env_path and load_dotenv:
        load_dotenv(env_path)
    elif load_dotenv:
        load_dotenv()

    def _get_int(name: str, default: int) -> int:
        value = os.getenv(name)
        return int(value) if value is not None else default

    def _get_float(name: str, default: float) -> float:
        value = os.getenv(name)
        return float(value) if value is not None else default

    return TradingConfig(
        exchange_id=os.getenv("TS_EXCHANGE_ID", "binance"),
        symbol=os.getenv("TS_SYMBOL", "BTC/USDT"),
        timeframe=os.getenv("TS_TIMEFRAME", "1m"),
        fast_window=_get_int("TS_FAST_WINDOW", 5),
        slow_window=_get_int("TS_SLOW_WINDOW", 20),
        base_order_size=_get_float("TS_BASE_ORDER_SIZE", 0.001),
        quote_currency=os.getenv("TS_QUOTE_CURRENCY", "USDT"),
        api_key=os.getenv("TS_API_KEY"),
        api_secret=os.getenv("TS_API_SECRET"),
        passphrase=os.getenv("TS_API_PASSPHRASE"),
        dry_run=os.getenv("TS_DRY_RUN", "true").lower() != "false",
        sandbox=os.getenv("TS_SANDBOX", "false").lower() == "true",
        poll_interval=_get_int("TS_POLL_INTERVAL", 60),
    )


__all__ = ["TradingConfig", "load_config"]
