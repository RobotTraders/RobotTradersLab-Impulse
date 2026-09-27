from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest
from robottraderslab_impulse import ImpulseStrategy

from robottraderslab.exchanges import FuturesExchangeProtocol
from robottraderslab.strategies import Balance, TradingMode, TradingSystem
from robottraderslab.strategies.futures import (
    FuturesAccount,
    MarginMode,
    MarginSettings,
)


@pytest.fixture
def mock_exchange() -> Mock:
    """Mocked futures exchange with a flat account and no open positions."""
    exchange = Mock(spec=FuturesExchangeProtocol)
    exchange.placement_reserve_rate = 0.0
    exchange.get_balances.return_value = {
        "USDT": Balance(locked=0.0, total=10_000.0),
    }
    exchange.get_open_positions.return_value = {}
    exchange.get_equity.return_value = 10_000.0
    exchange.get_quote_conversion_rate.return_value = 1.0
    exchange.get_open_orders.return_value = []
    exchange.get_margin_settings.side_effect = lambda symbols: {
        symbol: MarginSettings(leverage=None, margin_mode=MarginMode.CROSS)
        for symbol in symbols
    }
    return exchange


@pytest.fixture
def make_strategy(
    mock_exchange: Mock,
) -> Callable[..., ImpulseStrategy]:
    """Factory for creating ImpulseStrategy backed by the mocked exchange."""

    def _make(
        profiles: list[dict[str, Any]],
        trading_mode: TradingMode = TradingMode.BACKTEST,
    ) -> ImpulseStrategy:
        account = FuturesAccount(exchange=mock_exchange, name="test")
        return ImpulseStrategy(
            account=account,
            trading_system=TradingSystem(trading_mode=trading_mode),
            config_dir=Path("bot-config-dir"),
            profiles=profiles,
        )

    return _make
