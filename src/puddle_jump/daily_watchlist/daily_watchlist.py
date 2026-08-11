"""Save and load the stocks selected for one trading day."""

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from puddle_jump.stock_pool import Stock

TRADING_DAYS_DIRECTORY = Path("data/trading-days")


@dataclass(frozen=True)
class DailyWatchlist:
    """The stock symbols selected for one trading day."""

    trading_day: date
    symbols: list[str]


def get_watchlist_path(
    trading_day: date,
    trading_days_directory: Path = TRADING_DAYS_DIRECTORY,
) -> Path:
    """Return the watchlist path for one trading day."""
    result = trading_days_directory / trading_day.isoformat() / "watchlist.json"
    return result


def check_watchlist_symbols(symbols: list[str], stock_pool: list[Stock]) -> None:
    """Reject empty, repeated, or ineligible stock symbols."""
    if not symbols:
        raise ValueError("The daily watchlist needs at least one stock symbol.")

    eligible_symbols: set[str] = set()
    checked_symbols: set[str] = set()

    for stock in stock_pool:
        eligible_symbols.add(stock.symbol)

    for symbol in symbols:
        if symbol in checked_symbols:
            raise ValueError(f"The daily watchlist contains {symbol} more than once.")

        if symbol not in eligible_symbols:
            raise ValueError(f"{symbol} is not in the eligible stock pool.")

        checked_symbols.add(symbol)


def save_daily_watchlist(
    trading_day: date,
    symbols: list[str],
    stock_pool: list[Stock],
    trading_days_directory: Path = TRADING_DAYS_DIRECTORY,
) -> Path:
    """Save the selected stock symbols under their trading day."""
    check_watchlist_symbols(symbols, stock_pool)
    watchlist_path = get_watchlist_path(trading_day, trading_days_directory)
    watchlist_path.parent.mkdir(parents=True, exist_ok=True)

    saved_watchlist = {
        "date": trading_day.isoformat(),
        "symbols": symbols,
    }

    with watchlist_path.open("w", encoding="utf-8") as watchlist_file:
        json.dump(saved_watchlist, watchlist_file, indent=2)
        watchlist_file.write("\n")

    return watchlist_path


def load_daily_watchlist(
    trading_day: date,
    stock_pool: list[Stock],
    trading_days_directory: Path = TRADING_DAYS_DIRECTORY,
) -> DailyWatchlist:
    """Load and validate the watchlist saved for one trading day."""
    watchlist_path = get_watchlist_path(trading_day, trading_days_directory)

    with watchlist_path.open(encoding="utf-8") as watchlist_file:
        saved_watchlist = json.load(watchlist_file)

    saved_trading_day = date.fromisoformat(saved_watchlist["date"])
    symbols = saved_watchlist["symbols"]

    if saved_trading_day != trading_day:
        raise ValueError("The saved watchlist date does not match its trading day.")

    check_watchlist_symbols(symbols, stock_pool)

    result = DailyWatchlist(
        trading_day=saved_trading_day,
        symbols=symbols,
    )
    return result
