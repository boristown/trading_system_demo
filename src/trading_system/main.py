"""CLI entry point for the trading system demo."""
from __future__ import annotations

import argparse
import json
import logging
import signal
import sys
import time
from typing import Optional

from .config import TradingConfig, load_config
from .exchange import ExchangeClient
from .trader import Trader

LOGGER = logging.getLogger(__name__)


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", help="Path to .env file", default=None)
    parser.add_argument(
        "--once",
        action="store_true",
        help="Evaluate the strategy once and exit instead of running a loop.",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable debug logging"
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)
    _configure_logging(args.verbose)

    config = load_config(args.env_file)
    LOGGER.info("Loaded configuration: %s", config)

    exchange = ExchangeClient(config)
    trader = Trader(config, exchange)

    running = True

    def _signal_handler(signum, frame):  # type: ignore[override]
        nonlocal running
        LOGGER.info("Received signal %s, shutting down", signum)
        running = False

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    while running:
        try:
            result = trader.evaluate()
            order_info = trader.execute(result)
            if order_info:
                LOGGER.info("Order result: %s", json.dumps(order_info))
        except Exception as exc:  # pragma: no cover - runtime safety
            LOGGER.exception("Error during trading loop: %s", exc)

        if args.once:
            break

        time.sleep(config.poll_interval)

    LOGGER.info("Trader stopped")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
