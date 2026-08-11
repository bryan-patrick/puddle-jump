"""Create stock prices and keep their observations in time order."""

import math
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StockPrice:
    """One observed price for one stock."""

    symbol: str
    price: float
    observed_at: datetime


def check_stock_price(stock_price: StockPrice) -> None:
    """Reject a stock price with missing or invalid values."""
    if not stock_price.symbol:
        raise ValueError("A stock price needs a stock symbol.")

    if stock_price.symbol != stock_price.symbol.upper():
        raise ValueError("A stock price symbol must be uppercase.")

    if not math.isfinite(stock_price.price) or stock_price.price <= 0:
        raise ValueError("A stock price must be a positive number.")

    if stock_price.observed_at.utcoffset() is None:
        raise ValueError("A stock price timestamp must include a timezone.")


def create_stock_price(
    symbol: str,
    price: float,
    observed_at: datetime,
) -> StockPrice:
    """Create and validate one observed stock price."""
    result = StockPrice(
        symbol=symbol,
        price=price,
        observed_at=observed_at,
    )

    check_stock_price(result)
    return result


def add_stock_price(
    stock_prices: dict[str, list[StockPrice]],
    stock_price: StockPrice,
    stocks_to_watch: list[str],
) -> dict[str, list[StockPrice]]:
    """Add one watched stock's price without changing the original collection."""
    check_stock_price(stock_price)

    if stock_price.symbol not in stocks_to_watch:
        raise ValueError(f"{stock_price.symbol} is not on the daily watchlist.")

    existing_prices = stock_prices.get(stock_price.symbol, [])

    if existing_prices:
        latest_price = existing_prices[-1]

        if stock_price.observed_at <= latest_price.observed_at:
            raise ValueError(
                f"The new {stock_price.symbol} price must be later than its latest price."
            )

    result: dict[str, list[StockPrice]] = {}

    for symbol, saved_prices in stock_prices.items():
        result[symbol] = saved_prices.copy()

    symbol_prices = result.get(stock_price.symbol, [])
    symbol_prices.append(stock_price)
    result[stock_price.symbol] = symbol_prices

    return result
