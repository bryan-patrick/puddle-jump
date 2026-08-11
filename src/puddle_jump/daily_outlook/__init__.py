"""News-based outlooks for stocks on the daily watchlist."""

from puddle_jump.daily_outlook.daily_outlook import (
    DailyOutlook,
    create_daily_outlook,
    read_daily_outlook,
    write_daily_outlook,
)

__all__ = [
    "DailyOutlook",
    "create_daily_outlook",
    "read_daily_outlook",
    "write_daily_outlook",
]
