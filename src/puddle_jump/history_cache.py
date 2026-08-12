"""Download and cache the historical prices used by replay."""

import json
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import polars as pl
from alpaca.common.enums import Sort
from alpaca.data.enums import DataFeed
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from puddle_jump.stock_prices import StockPrice, create_stock_price

DEFAULT_HISTORY_CACHE_DIRECTORY = Path("data/cache/history")
NEW_YORK_TIME = ZoneInfo("America/New_York")


def get_market_open(trading_day: date) -> datetime:
    """Return the regular market open for an exchange date."""

    result = datetime.combine(trading_day, time(hour=9, minute=30), NEW_YORK_TIME)

    return result


def get_market_close(trading_day: date) -> datetime:
    """Return the regular market close for an exchange date."""

    result = datetime.combine(trading_day, time(hour=16), NEW_YORK_TIME)

    return result


def cache_is_fresh(cache_path: Path, cache_days: int) -> bool:
    """Return whether a cached file is still inside its retention period."""

    if cache_days <= 0:
        raise ValueError("The historical cache must be kept for at least one day.")

    result = False

    if cache_path.is_file():
        oldest_allowed_time = datetime.now(timezone.utc) - timedelta(days=cache_days)
        cached_time = datetime.fromtimestamp(cache_path.stat().st_mtime, timezone.utc)

        if cached_time >= oldest_allowed_time:
            result = True

    return result


def remove_expired_cache(cache_directory: Path, cache_days: int) -> int:
    """Remove only expired files inside the configured historical cache."""

    if cache_days <= 0:
        raise ValueError("The historical cache must be kept for at least one day.")

    result = 0

    if not cache_directory.exists():
        return result

    oldest_allowed_time = datetime.now(timezone.utc) - timedelta(days=cache_days)

    for cache_path in cache_directory.rglob("*"):
        if not cache_path.is_file():
            continue

        cached_time = datetime.fromtimestamp(cache_path.stat().st_mtime, timezone.utc)

        if cached_time < oldest_allowed_time:
            cache_path.unlink()
            result += 1

    return result


def get_recent_trading_days(
    stock_data_client: StockHistoricalDataClient,
    trading_days_needed: int,
    current_time: datetime | None = None,
    cache_directory: Path = DEFAULT_HISTORY_CACHE_DIRECTORY,
) -> tuple[list[date], bool]:
    """Read today's trading-day list or find it from daily AAPL bars."""

    if trading_days_needed <= 0:
        raise ValueError("At least one historical trading day is needed.")

    if current_time is None:
        current_time = datetime.now(NEW_YORK_TIME)

    if current_time.utcoffset() is None:
        raise ValueError("The current historical replay time needs a timezone.")

    current_exchange_date = current_time.astimezone(NEW_YORK_TIME).date()
    cache_path = cache_directory / "trading-days.json"

    if cache_path.is_file():
        with cache_path.open(encoding="utf-8") as cache_file:
            saved_file = json.load(cache_file)

        cached_for_date = date.fromisoformat(saved_file["cached_for_date"])
        cached_days = [date.fromisoformat(saved_day) for saved_day in saved_file["trading_days"]]

        if cached_for_date == current_exchange_date and len(cached_days) >= trading_days_needed:
            return cached_days[-trading_days_needed:], True

    search_start = current_time - timedelta(days=max(45, trading_days_needed * 4))
    request = StockBarsRequest(
        symbol_or_symbols="AAPL",
        start=search_start,
        end=current_time,
        timeframe=TimeFrame.Day,
        feed=DataFeed.IEX,
        sort=Sort.ASC,
    )
    alpaca_bars = stock_data_client.get_stock_bars(request).data.get("AAPL", [])
    found_days: list[date] = []

    for alpaca_bar in alpaca_bars:
        trading_day = alpaca_bar.timestamp.astimezone(NEW_YORK_TIME).date()

        if trading_day == current_exchange_date:
            market_close = get_market_close(trading_day)

            if current_time < market_close:
                continue

        if trading_day not in found_days:
            found_days.append(trading_day)

    if len(found_days) < trading_days_needed:
        raise ValueError("Alpaca did not return enough completed trading days.")

    result = found_days[-trading_days_needed:]
    saved_file = {
        "cached_for_date": current_exchange_date.isoformat(),
        "trading_days": [trading_day.isoformat() for trading_day in result],
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    with cache_path.open("w", encoding="utf-8") as cache_file:
        json.dump(saved_file, cache_file, indent=2)
        cache_file.write("\n")

    return result, False


def get_prices_cache_path(cache_directory: Path, trading_day: date) -> Path:
    """Return one exchange day's local price cache path."""

    result = cache_directory / "prices" / f"{trading_day.isoformat()}.parquet"

    return result


def write_prices_cache(
    stock_prices: dict[str, list[StockPrice]],
    cache_path: Path,
) -> None:
    """Save one day of minute prices as compact local Parquet data."""

    saved_prices: list[dict[str, object]] = []

    for symbol, symbol_prices in stock_prices.items():
        for stock_price in symbol_prices:
            saved_prices.append(
                {
                    "symbol": symbol,
                    "price": stock_price.price,
                    "observed_at": stock_price.observed_at.isoformat(),
                }
            )

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    price_table = pl.DataFrame(saved_prices)
    price_table.write_parquet(cache_path)


def read_prices_cache(cache_path: Path) -> dict[str, list[StockPrice]]:
    """Read one day of minute prices from the local Parquet cache."""

    result: dict[str, list[StockPrice]] = {}
    price_rows = pl.read_parquet(cache_path).sort(["symbol", "observed_at"]).to_dicts()

    for price_row in price_rows:
        symbol = price_row["symbol"]
        stock_price = create_stock_price(
            symbol=symbol,
            price=price_row["price"],
            observed_at=datetime.fromisoformat(price_row["observed_at"]),
        )
        symbol_prices = result.get(symbol, [])
        symbol_prices.append(stock_price)
        result[symbol] = symbol_prices

    return result


def download_historical_prices(
    stock_data_client: StockHistoricalDataClient,
    symbols: list[str],
    trading_day: date,
) -> dict[str, list[StockPrice]]:
    """Download one-minute closes without pretending they are 30-second prices."""

    market_open = get_market_open(trading_day)
    market_close = get_market_close(trading_day)
    request = StockBarsRequest(
        symbol_or_symbols=symbols,
        start=market_open,
        end=market_close,
        timeframe=TimeFrame.Minute,
        feed=DataFeed.IEX,
        sort=Sort.ASC,
        limit=10000,
    )
    alpaca_bars = stock_data_client.get_stock_bars(request).data
    result: dict[str, list[StockPrice]] = {}

    for symbol in symbols:
        symbol_prices: list[StockPrice] = []

        for alpaca_bar in alpaca_bars.get(symbol, []):
            observed_at = alpaca_bar.timestamp.astimezone(NEW_YORK_TIME) + timedelta(minutes=1)

            if observed_at > market_close:
                continue

            stock_price = create_stock_price(
                symbol=symbol,
                price=alpaca_bar.close,
                observed_at=observed_at,
            )
            symbol_prices.append(stock_price)

        if not symbol_prices:
            raise ValueError(f"Alpaca returned no historical prices for {symbol} on {trading_day}.")

        result[symbol] = symbol_prices

    return result


def get_historical_prices(
    stock_data_client: StockHistoricalDataClient,
    symbols: list[str],
    trading_day: date,
    cache_directory: Path,
    cache_days: int,
) -> tuple[dict[str, list[StockPrice]], bool]:
    """Read fresh cached prices or download and cache them once."""

    cache_path = get_prices_cache_path(cache_directory, trading_day)

    if cache_is_fresh(cache_path, cache_days):
        cached_prices = read_prices_cache(cache_path)

        if set(cached_prices) == set(symbols):
            return cached_prices, True

    result = download_historical_prices(
        stock_data_client=stock_data_client,
        symbols=symbols,
        trading_day=trading_day,
    )
    write_prices_cache(result, cache_path)

    return result, False
