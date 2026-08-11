"""Check whether recent stock prices show the configured downward trend."""

from puddle_jump.stock_prices import StockPrice


def check_falling_prices(
    stock_prices: list[StockPrice],
    prices_needed: int,
) -> bool:
    """Return whether every price in the latest window is lower than the previous one."""
    if prices_needed < 2:
        raise ValueError("A falling-price check needs at least two prices.")

    result = False

    if len(stock_prices) < prices_needed:
        return result

    recent_prices = stock_prices[-prices_needed:]

    for index in range(1, len(recent_prices)):
        previous_price = recent_prices[index - 1]
        current_price = recent_prices[index]

        if current_price.price >= previous_price.price:
            return result

    result = True
    return result
