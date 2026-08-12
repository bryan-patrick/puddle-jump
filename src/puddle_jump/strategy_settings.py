"""Load and validate the trading strategy settings."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

DEFAULT_STRATEGY_SETTINGS_PATH = Path("config/strategy.toml")


@dataclass(frozen=True)
class StrategySettings:
    """The values that control the initial trading strategy."""

    check_prices_every_seconds: int
    rising_prices_needed_to_buy: int
    falling_prices_needed_to_sell: int
    minimum_price_rise_percent: float
    minimum_falling_price_drop_percent: float
    maximum_fast_drop_percent: float
    maximum_loss_percent: float


def check_strategy_settings(settings: StrategySettings) -> None:
    """Reject strategy settings that cannot support the initial rules."""
    if settings.check_prices_every_seconds <= 0:
        raise ValueError("Price checks must be at least one second apart.")

    if settings.rising_prices_needed_to_buy < 2:
        raise ValueError("A rising trend needs at least two prices.")

    if settings.falling_prices_needed_to_sell < 2:
        raise ValueError("A falling trend needs at least two prices.")

    if settings.falling_prices_needed_to_sell > settings.rising_prices_needed_to_buy:
        raise ValueError("The falling-price window cannot exceed the rising-price window.")

    if settings.minimum_price_rise_percent <= 0:
        raise ValueError("The minimum price rise must be greater than zero percent.")

    if settings.minimum_falling_price_drop_percent <= 0:
        raise ValueError("The minimum falling price drop must be greater than zero percent.")

    if not 0 < settings.maximum_fast_drop_percent <= 100:
        raise ValueError(
            "The maximum fast drop must be greater than zero and no more than 100 percent."
        )

    if settings.minimum_falling_price_drop_percent >= settings.maximum_fast_drop_percent:
        raise ValueError("The normal falling price drop must be less than the fast drop.")

    if not 0 < settings.maximum_loss_percent <= 100:
        raise ValueError("The maximum loss must be greater than zero and no more than 100 percent.")


def load_strategy_settings(
    settings_path: Path = DEFAULT_STRATEGY_SETTINGS_PATH,
) -> StrategySettings:
    """Load the strategy settings from their TOML file."""
    with settings_path.open("rb") as settings_file:
        saved_settings = tomllib.load(settings_file)

    result = StrategySettings(
        check_prices_every_seconds=saved_settings["check_prices_every_seconds"],
        rising_prices_needed_to_buy=saved_settings["rising_prices_needed_to_buy"],
        falling_prices_needed_to_sell=saved_settings["falling_prices_needed_to_sell"],
        minimum_price_rise_percent=saved_settings["minimum_price_rise_percent"],
        minimum_falling_price_drop_percent=saved_settings["minimum_falling_price_drop_percent"],
        maximum_fast_drop_percent=saved_settings["maximum_fast_drop_percent"],
        maximum_loss_percent=saved_settings["maximum_loss_percent"],
    )

    check_strategy_settings(result)
    return result
