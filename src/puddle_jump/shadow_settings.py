"""Load the settings for a live shadow session."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from puddle_jump.stock_pool import load_stock_pool

DEFAULT_SHADOW_SETTINGS_PATH = Path("config/shadow_market.toml")


@dataclass(frozen=True)
class ShadowSettings:
    """The stocks and wave values used without placing orders."""

    symbols: list[str]
    check_every_seconds: int
    wave_window_prices: int
    minimum_wave_rise_percent: float
    maximum_loss_percent: float


def check_shadow_settings(settings: ShadowSettings) -> None:
    """Reject shadow settings that cannot run the wave strategy."""

    if not settings.symbols:
        raise ValueError("Shadow trading needs at least one stock symbol.")

    eligible_symbols = {stock.symbol for stock in load_stock_pool()}
    checked_symbols: set[str] = set()

    for symbol in settings.symbols:
        if symbol in checked_symbols:
            raise ValueError(f"The shadow watchlist contains {symbol} more than once.")

        if symbol not in eligible_symbols:
            raise ValueError(f"{symbol} is not in the eligible stock pool.")

        checked_symbols.add(symbol)

    if settings.check_every_seconds <= 0:
        raise ValueError("Shadow price checks must be at least one second apart.")

    if settings.wave_window_prices < 2:
        raise ValueError("A shadow wave needs at least two prices.")

    if settings.minimum_wave_rise_percent <= 0:
        raise ValueError("The shadow wave rise must be greater than zero percent.")

    if not 0 < settings.maximum_loss_percent <= 100:
        raise ValueError("The shadow maximum loss must be between zero and 100 percent.")


def load_shadow_settings(
    settings_path: Path = DEFAULT_SHADOW_SETTINGS_PATH,
) -> ShadowSettings:
    """Load and validate the saved live shadow settings."""

    with settings_path.open("rb") as settings_file:
        saved_settings = tomllib.load(settings_file)

    result = ShadowSettings(
        symbols=saved_settings["symbols"],
        check_every_seconds=saved_settings["check_every_seconds"],
        wave_window_prices=saved_settings["wave_window_prices"],
        minimum_wave_rise_percent=saved_settings["minimum_wave_rise_percent"],
        maximum_loss_percent=saved_settings["maximum_loss_percent"],
    )

    check_shadow_settings(result)

    return result
