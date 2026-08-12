"""Make plain trading decisions without placing orders."""

import math
from dataclasses import dataclass

from puddle_jump.falling_prices import check_falling_prices, check_fast_price_drop
from puddle_jump.rising_prices import check_rising_prices
from puddle_jump.stock_prices import StockPrice
from puddle_jump.strategy_settings import StrategySettings


@dataclass(frozen=True)
class TradeDecision:
    """One explained trading decision for one stock."""

    symbol: str
    action: str
    reason: str


def check_price_symbols(
    symbol: str,
    stock_prices: list[StockPrice],
) -> None:
    """Confirm that every price belongs to the expected stock."""
    for stock_price in stock_prices:
        if stock_price.symbol != symbol:
            raise ValueError("Every stock price must match the decision symbol.")


def decide_buy(
    symbol: str,
    stock_prices: list[StockPrice],
    stock_is_owned: bool,
    settings: StrategySettings,
) -> TradeDecision:
    """Return BUY only when the current rising-price rule passes."""

    if not symbol:
        raise ValueError("A buy decision needs a stock symbol.")

    if symbol != symbol.upper():
        raise ValueError("A buy decision stock symbol must be uppercase.")

    check_price_symbols(symbol, stock_prices)

    result = TradeDecision(
        symbol=symbol,
        action="NO_ACTION",
        reason=f"{symbol}'s recent prices are not rising enough.",
    )

    if stock_is_owned:
        result = TradeDecision(
            symbol=symbol,
            action="NO_ACTION",
            reason=f"{symbol} is already owned.",
        )
    elif check_rising_prices(
        stock_prices,
        settings.rising_prices_needed_to_buy,
        settings.minimum_price_rise_percent,
    ):
        result = TradeDecision(
            symbol=symbol,
            action="BUY",
            reason=f"{symbol}'s recent prices meet the buy rule.",
        )

    return result


def decide_sell(
    symbol: str,
    stock_prices: list[StockPrice],
    stock_is_owned: bool,
    buy_price: float,
    settings: StrategySettings,
) -> TradeDecision:
    """Return SELL when either initial sell rule passes for an owned stock."""
    if not symbol:
        raise ValueError("A sell decision needs a stock symbol.")

    if symbol != symbol.upper():
        raise ValueError("A sell decision stock symbol must be uppercase.")

    if not math.isfinite(buy_price) or buy_price <= 0:
        raise ValueError("A stock's buy price must be a positive number.")

    check_price_symbols(symbol, stock_prices)
    stop_price = buy_price - (buy_price * settings.maximum_loss_percent / 100)

    result = TradeDecision(
        symbol=symbol,
        action="NO_ACTION",
        reason=f"{symbol}'s recent prices do not meet a sell rule.",
    )

    if not stock_is_owned:
        result = TradeDecision(
            symbol=symbol,
            action="NO_ACTION",
            reason=f"{symbol} is not owned.",
        )
    elif not stock_prices:
        result = TradeDecision(
            symbol=symbol,
            action="NO_ACTION",
            reason=f"{symbol} does not have a current price.",
        )
    elif stock_prices[-1].price <= stop_price:
        result = TradeDecision(
            symbol=symbol,
            action="SELL",
            reason=(
                f"{symbol}'s latest price is at least "
                f"{settings.maximum_loss_percent}% below its buy price."
            ),
        )
    elif check_fast_price_drop(
        stock_prices,
        settings.falling_prices_needed_to_sell,
        settings.maximum_fast_drop_percent,
    ):
        result = TradeDecision(
            symbol=symbol,
            action="SELL",
            reason=(
                f"{symbol}'s latest price fell at least "
                f"{settings.maximum_fast_drop_percent}% from its recent high."
            ),
        )
    elif check_falling_prices(
        stock_prices,
        settings.falling_prices_needed_to_sell,
        settings.minimum_falling_price_drop_percent,
    ):
        result = TradeDecision(
            symbol=symbol,
            action="SELL",
            reason=f"{symbol}'s recent prices meet the falling-price rule.",
        )

    return result
