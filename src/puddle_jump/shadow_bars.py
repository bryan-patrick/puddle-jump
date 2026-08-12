"""Download and cache complete minute bars for a live shadow session."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import polars as pl
from alpaca.common.enums import Sort
from alpaca.data.enums import DataFeed
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


@dataclass(frozen=True)
class ShadowBar:
    """One completed market minute with its full available bar values."""

    symbol: str
    observed_at: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    trade_count: int
    volume_weighted_price: float


def download_shadow_bars(
    stock_data_client: StockHistoricalDataClient,
    symbols: list[str],
    start_time: datetime,
    end_time: datetime,
) -> list[ShadowBar]:
    """Download completed IEX minute bars in one batched request."""

    if start_time.utcoffset() is None or end_time.utcoffset() is None:
        raise ValueError("Shadow bar request times must include a timezone.")

    result: list[ShadowBar] = []

    if end_time <= start_time:
        return result

    request = StockBarsRequest(
        symbol_or_symbols=symbols,
        start=start_time,
        end=end_time,
        timeframe=TimeFrame.Minute,
        feed=DataFeed.IEX,
        sort=Sort.ASC,
    )
    bars_by_symbol = stock_data_client.get_stock_bars(request).data

    for symbol in symbols:
        for alpaca_bar in bars_by_symbol.get(symbol, []):
            observed_at = alpaca_bar.timestamp.astimezone(start_time.tzinfo) + timedelta(minutes=1)
            shadow_bar = ShadowBar(
                symbol=symbol,
                observed_at=observed_at,
                open_price=float(alpaca_bar.open),
                high_price=float(alpaca_bar.high),
                low_price=float(alpaca_bar.low),
                close_price=float(alpaca_bar.close),
                volume=float(alpaca_bar.volume),
                trade_count=int(alpaca_bar.trade_count or 0),
                volume_weighted_price=float(alpaca_bar.vwap or alpaca_bar.close),
            )
            result.append(shadow_bar)

    result.sort(key=lambda bar: (bar.observed_at, bar.symbol))

    return result


def merge_shadow_bars(
    saved_bars: list[ShadowBar],
    downloaded_bars: list[ShadowBar],
) -> list[ShadowBar]:
    """Combine bars without keeping repeated symbol timestamps."""

    bars_by_key: dict[tuple[str, datetime], ShadowBar] = {}

    for shadow_bar in saved_bars + downloaded_bars:
        key = (shadow_bar.symbol, shadow_bar.observed_at)
        bars_by_key[key] = shadow_bar

    result = list(bars_by_key.values())
    result.sort(key=lambda bar: (bar.observed_at, bar.symbol))

    return result


def write_shadow_bars(shadow_bars: list[ShadowBar], bars_path: Path) -> None:
    """Save all collected bars as one compact Parquet file."""

    saved_rows = []

    for shadow_bar in shadow_bars:
        saved_rows.append(
            {
                "symbol": shadow_bar.symbol,
                "observed_at": shadow_bar.observed_at.isoformat(),
                "open": shadow_bar.open_price,
                "high": shadow_bar.high_price,
                "low": shadow_bar.low_price,
                "close": shadow_bar.close_price,
                "volume": shadow_bar.volume,
                "trade_count": shadow_bar.trade_count,
                "vwap": shadow_bar.volume_weighted_price,
            }
        )

    bars_path.parent.mkdir(parents=True, exist_ok=True)

    if not saved_rows:
        return

    pl.DataFrame(saved_rows).write_parquet(bars_path)


def read_shadow_bars(bars_path: Path) -> list[ShadowBar]:
    """Read previously collected bars so a session can resume."""

    result: list[ShadowBar] = []

    if not bars_path.is_file():
        return result

    saved_rows = pl.read_parquet(bars_path).sort(["observed_at", "symbol"]).to_dicts()

    for saved_row in saved_rows:
        result.append(
            ShadowBar(
                symbol=saved_row["symbol"],
                observed_at=datetime.fromisoformat(saved_row["observed_at"]),
                open_price=saved_row["open"],
                high_price=saved_row["high"],
                low_price=saved_row["low"],
                close_price=saved_row["close"],
                volume=saved_row["volume"],
                trade_count=saved_row["trade_count"],
                volume_weighted_price=saved_row["vwap"],
            )
        )

    return result
