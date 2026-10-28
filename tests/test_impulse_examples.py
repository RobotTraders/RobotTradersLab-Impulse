from collections.abc import Callable
from importlib.resources import as_file, files
from pathlib import Path

import pytest

from robottraderslab import BotConfig
from robottraderslab.scaffold import main as scaffold


@pytest.fixture
def load_example() -> Callable[[str], BotConfig]:
    def load(name: str) -> BotConfig:
        config_path = files("robottraderslab_impulse") / "examples" / name
        with as_file(config_path) as path:
            return BotConfig.from_file(str(path))

    return load


def test_backtest_example_config_loads(load_example):
    bot_config = load_example("bot.toml")

    assert bot_config.strategy.strategy_class == "impulse"


def test_optimisation_example_config_loads(load_example):
    bot_config = load_example("optimisation.toml")

    assert bot_config.strategy.strategy_class == "impulse"


def test_optimisation_example_sweeps_whole_lengths(load_example):
    profile = load_example("optimisation.toml").strategy.profiles[0]

    assert isinstance(profile["trix_length"], int)
    assert isinstance(profile["signal_length"], int)


def test_scaffold_creates_a_bot_folder_with_its_notebooks(tmp_path):
    scaffold("impulse", Path("first-bot"), tmp_path)
    folder = tmp_path / "first-bot"

    assert {path.name for path in folder.iterdir()} >= {
        "bot.toml",
        "optimisation.toml",
        "run_backtest.ipynb",
        "run_optimisation.ipynb",
    }
