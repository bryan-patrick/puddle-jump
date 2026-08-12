"""Load the settings used by the multi-day historical replay."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

DEFAULT_HISTORY_REPLAY_SETTINGS_PATH = Path("config/history_replay.toml")


@dataclass(frozen=True)
class HistoryReplaySettings:
    """The stocks, dates, costs, and local cache used by a replay."""

    symbols: list[str]
    trading_days: int
    cache_days: int
    estimated_trade_cost_percent: float
    price_feed: str
    report_path: Path


def check_history_replay_settings(settings: HistoryReplaySettings) -> None:
    """Reject settings that cannot produce a useful historical replay."""

    if not settings.symbols:
        raise ValueError("A historical replay needs at least one stock symbol.")

    checked_symbols: set[str] = set()

    for symbol in settings.symbols:
        if not symbol or symbol != symbol.upper():
            raise ValueError("Historical replay symbols must be uppercase.")

        if symbol in checked_symbols:
            raise ValueError(f"The historical replay contains {symbol} more than once.")

        checked_symbols.add(symbol)

    if settings.trading_days <= 0:
        raise ValueError("The historical replay needs at least one trading day.")

    if settings.cache_days <= 0:
        raise ValueError("The historical cache must be kept for at least one day.")

    if not 0 <= settings.estimated_trade_cost_percent < 100:
        raise ValueError("The estimated trade cost must be between zero and 100 percent.")

    if settings.price_feed != "iex":
        raise ValueError("Historical replay currently supports only the IEX feed.")

    if not settings.report_path.name:
        raise ValueError("The historical replay needs a report path.")


def load_history_replay_settings(
    settings_path: Path = DEFAULT_HISTORY_REPLAY_SETTINGS_PATH,
) -> HistoryReplaySettings:
    """Load and validate the historical replay settings."""

    with settings_path.open("rb") as settings_file:
        saved_settings = tomllib.load(settings_file)

    result = HistoryReplaySettings(
        symbols=saved_settings["symbols"],
        trading_days=saved_settings["trading_days"],
        cache_days=saved_settings["cache_days"],
        estimated_trade_cost_percent=saved_settings["estimated_trade_cost_percent"],
        price_feed=saved_settings["price_feed"],
        report_path=Path(saved_settings["report_path"]),
    )

    check_history_replay_settings(result)

    return result
