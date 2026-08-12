"""Check whether recent stock prices show the configured downward trend."""

from puddle_jump.stock_prices import StockPrice


def check_falling_prices(
    stock_prices: list[StockPrice],
    prices_needed: int,
    minimum_drop_percent: float,
) -> bool:
    """Return whether recent prices fall in order and by enough overall."""
    if prices_needed < 2:
        raise ValueError("A falling-price check needs at least two prices.")

    if minimum_drop_percent <= 0:
        raise ValueError("The minimum price drop must be greater than zero percent.")

    result = False

    if len(stock_prices) < prices_needed:
        return result

    recent_prices = stock_prices[-prices_needed:]

    for index in range(1, len(recent_prices)):
        previous_price = recent_prices[index - 1]
        current_price = recent_prices[index]

        if current_price.price >= previous_price.price:
            return result

    first_price = recent_prices[0].price
    last_price = recent_prices[-1].price
    price_drop_percent = (first_price - last_price) / first_price * 100

    if price_drop_percent >= minimum_drop_percent:
        result = True

    return result


def check_fast_price_drop(
    stock_prices: list[StockPrice],
    prices_to_check: int,
    maximum_drop_percent: float,
) -> bool:
    """Return whether the current price fell sharply from the recent high."""
    if prices_to_check < 2:
        raise ValueError("A fast-drop check needs at least two prices.")

    if maximum_drop_percent <= 0:
        raise ValueError("The maximum fast drop must be greater than zero percent.")

    result = False

    if len(stock_prices) < 2:
        return result

    recent_prices = stock_prices[-prices_to_check:]
    highest_price = recent_prices[0].price

    for stock_price in recent_prices:
        if stock_price.price > highest_price:
            highest_price = stock_price.price

    current_price = recent_prices[-1].price
    fast_drop_price = highest_price - (highest_price * maximum_drop_percent / 100)

    if current_price <= fast_drop_price:
        result = True

    return result
