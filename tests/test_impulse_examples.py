from collections.abc import Callable
from importlib.resources import as_file, files

import pytest

from robottraderslab import BotConfig


@pytest.fixture
def load_example() -> Callable[[str], BotConfig]:
    def load(name: str) -> BotConfig:
        config_path = files("robottraderslab_impulse") / "examples" / name
        with as_file(config_path) as path:
            return BotConfig.from_file(str(path))

    return load


def test_backtest_example_config_loads(load_example):
    bot_config = load_example("impulse-bot-example.toml")

    assert bot_config.strategy.strategy_class == "impulse"


def test_optimisation_example_config_loads(load_example):
    bot_config = load_example("impulse-optimisation-example.toml")

    assert bot_config.strategy.strategy_class == "impulse"


def test_optimisation_example_sweeps_whole_lengths(load_example):
    profile = load_example("impulse-optimisation-example.toml").strategy.profiles[0]

    assert isinstance(profile["trix_length"], int)
    assert isinstance(profile["signal_length"], int)
