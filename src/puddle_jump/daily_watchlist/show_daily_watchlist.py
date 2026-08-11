"""Create and show a small daily watchlist."""

from datetime import datetime
from zoneinfo import ZoneInfo

from puddle_jump.daily_watchlist import load_daily_watchlist, save_daily_watchlist
from puddle_jump.stock_pool import load_stock_pool

MARKET_TIME_ZONE = ZoneInfo("America/New_York")


def main() -> None:
    """Save and load today's sample daily watchlist."""
    trading_day = datetime.now(MARKET_TIME_ZONE).date()
    sample_symbols = ["AAPL", "MSFT", "NVDA"]
    stock_pool = load_stock_pool()

    save_daily_watchlist(trading_day, sample_symbols, stock_pool)
    daily_watchlist = load_daily_watchlist(trading_day, stock_pool)

    print(f"Daily watchlist: {daily_watchlist.trading_day.isoformat()}")

    for symbol in daily_watchlist.symbols:
        print(symbol)
