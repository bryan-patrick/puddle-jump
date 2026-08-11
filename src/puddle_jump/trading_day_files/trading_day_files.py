"""Create trading-day directories and preserve daily outlook updates."""

from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from puddle_jump.daily_outlook import DailyOutlook, read_daily_outlook, write_daily_outlook

TRADING_DAYS_DIRECTORY = Path("data/trading-days")
MARKET_TIME_ZONE = ZoneInfo("America/New_York")


def get_trading_day_directory(
    trading_day: date,
    trading_days_directory: Path = TRADING_DAYS_DIRECTORY,
) -> Path:
    """Return the directory for one trading day."""
    result = trading_days_directory / trading_day.isoformat()
    return result


def get_outlook_updates_directory(
    trading_day: date,
    trading_days_directory: Path = TRADING_DAYS_DIRECTORY,
) -> Path:
    """Return the directory containing one day's outlook updates."""
    trading_day_directory = get_trading_day_directory(trading_day, trading_days_directory)
    result = trading_day_directory / "outlooks"
    return result


def get_update_time(outlooks: list[DailyOutlook]) -> datetime:
    """Return the shared timestamp for one complete outlook update."""
    if not outlooks:
        raise ValueError("An outlook update needs at least one stock outlook.")

    result = outlooks[0].recorded_at

    for outlook in outlooks:
        if outlook.recorded_at != result:
            raise ValueError("Every stock in one outlook update must use the same timestamp.")

    return result


def check_update_day(trading_day: date, update_time: datetime) -> None:
    """Confirm that an outlook update belongs to the requested market day."""
    if update_time.utcoffset() is None:
        raise ValueError("An outlook update timestamp must include a timezone.")

    market_day = update_time.astimezone(MARKET_TIME_ZONE).date()

    if market_day != trading_day:
        raise ValueError("The outlook update timestamp does not match the trading day.")


def get_outlook_update_path(
    trading_day: date,
    update_time: datetime,
    trading_days_directory: Path = TRADING_DAYS_DIRECTORY,
) -> Path:
    """Return a safe timestamped path for one outlook update."""
    check_update_day(trading_day, update_time)
    outlook_updates_directory = get_outlook_updates_directory(
        trading_day,
        trading_days_directory,
    )
    market_time = update_time.astimezone(MARKET_TIME_ZONE)
    update_filename = market_time.isoformat(timespec="seconds").replace(":", "-")
    result = outlook_updates_directory / f"{update_filename}.json"
    return result


def save_outlook_update(
    trading_day: date,
    outlooks: list[DailyOutlook],
    trading_days_directory: Path = TRADING_DAYS_DIRECTORY,
) -> Path:
    """Save one outlook update without replacing an earlier update."""
    update_time = get_update_time(outlooks)
    outlook_path = get_outlook_update_path(
        trading_day,
        update_time,
        trading_days_directory,
    )
    outlook_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        write_daily_outlook(outlooks, outlook_path, replace_existing=False)
    except FileExistsError:
        raise FileExistsError(f"An outlook update already exists at {outlook_path}.") from None

    return outlook_path


def list_outlook_updates(
    trading_day: date,
    trading_days_directory: Path = TRADING_DAYS_DIRECTORY,
) -> list[Path]:
    """List one day's outlook updates from oldest to newest."""
    result: list[Path] = []
    outlook_updates_directory = get_outlook_updates_directory(
        trading_day,
        trading_days_directory,
    )

    if not outlook_updates_directory.exists():
        return result

    saved_updates: list[tuple[datetime, Path]] = []

    for outlook_path in outlook_updates_directory.glob("*.json"):
        outlooks = read_daily_outlook(outlook_path)
        update_time = get_update_time(outlooks)
        check_update_day(trading_day, update_time)
        saved_updates.append((update_time, outlook_path))

    saved_updates.sort(key=lambda saved_update: saved_update[0])

    for _, outlook_path in saved_updates:
        result.append(outlook_path)

    return result
