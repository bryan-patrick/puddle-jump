"""Show a short summary of the stock pool."""

from puddle_jump.stock_pool import Stock, load_stock_pool


def count_stocks_in_group(stocks: list[Stock], group: str) -> int:
    """Count the stocks assigned to one group."""
    result = 0

    for stock in stocks:
        if stock.group == group:
            result += 1

    return result


def main() -> None:
    """Load the stock pool and print its totals."""
    stocks = load_stock_pool()
    sp500_stock_count = count_stocks_in_group(stocks, "sp500")
    extra_tech_stock_count = count_stocks_in_group(stocks, "extra_tech")

    print(f"S&P 500 stocks: {sp500_stock_count}")
    print(f"Extra tech stocks: {extra_tech_stock_count}")
    print(f"Total stocks: {len(stocks)}")
