"""Check whether recent stock prices show the configured upward trend."""

from puddle_jump.stock_prices import StockPrice


def check_rising_prices(
    stock_prices: list[StockPrice],
    prices_needed: int,
    minimum_rise_percent: float,
) -> bool:
    """Return whether the latest prices rise enough at every observation."""
    if prices_needed < 2:
        raise ValueError("A rising-price check needs at least two prices.")

    if minimum_rise_percent <= 0:
        raise ValueError("The minimum price rise must be greater than zero percent.")

    result = False

    if len(stock_prices) < prices_needed:
        return result

    recent_prices = stock_prices[-prices_needed:]

    for index in range(1, len(recent_prices)):
        previous_price = recent_prices[index - 1]
        current_price = recent_prices[index]

        if current_price.price <= previous_price.price:
            return result

    first_price = recent_prices[0].price
    last_price = recent_prices[-1].price
    minimum_last_price = first_price + (first_price * minimum_rise_percent / 100)

    if last_price >= minimum_last_price:
        result = True

    return result
