"""Confirm that Alpaca stock history is readable."""

from datetime import UTC, datetime, timedelta

from alpaca.data.enums import DataFeed
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from puddle_jump.alpaca_data import create_stock_data_client, load_alpaca_credentials

EXAMPLE_SYMBOL = "AAPL"
LOOKBACK_DAYS = 30


def check_stock_history(
    stock_data_client: StockHistoricalDataClient,
    start_time: datetime,
    end_time: datetime,
) -> int:
    """Read recent AAPL daily bars and return how many were found."""

    request = StockBarsRequest(
        symbol_or_symbols=EXAMPLE_SYMBOL,
        timeframe=TimeFrame.Day,
        start=start_time,
        end=end_time,
        feed=DataFeed.IEX,
    )
    stock_bars = stock_data_client.get_stock_bars(request)
    result = len(stock_bars.data.get(EXAMPLE_SYMBOL, []))

    if result == 0:
        raise RuntimeError("Alpaca returned no recent AAPL stock bars.")

    return result


def main() -> None:
    """Check the read-only Alpaca stock client and print a safe result."""

    credentials = load_alpaca_credentials()
    stock_data_client = create_stock_data_client(credentials)
    end_time = datetime.now(UTC)
    start_time = end_time - timedelta(days=LOOKBACK_DAYS)

    stock_bar_count = check_stock_history(stock_data_client, start_time, end_time)

    print(f"Alpaca stock history: {stock_bar_count} recent AAPL daily bars")


if __name__ == "__main__":
    main()
