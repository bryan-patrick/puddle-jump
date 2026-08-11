"""Make plain trading decisions without placing orders."""

from dataclasses import dataclass

from puddle_jump.daily_outlook import DailyOutlook
from puddle_jump.rising_prices import check_rising_prices
from puddle_jump.stock_prices import StockPrice
from puddle_jump.strategy_settings import StrategySettings


@dataclass(frozen=True)
class TradeDecision:
    """One explained trading decision for one stock."""

    symbol: str
    action: str
    reason: str


def check_matching_symbols(
    daily_outlook: DailyOutlook,
    stock_prices: list[StockPrice],
) -> None:
    """Confirm that the outlook and prices belong to the same stock."""
    for stock_price in stock_prices:
        if stock_price.symbol != daily_outlook.symbol:
            raise ValueError("The daily outlook and stock prices must use the same symbol.")


def decide_buy(
    daily_outlook: DailyOutlook,
    stock_prices: list[StockPrice],
    stock_is_owned: bool,
    settings: StrategySettings,
) -> TradeDecision:
    """Return BUY only when every initial buy rule passes."""
    check_matching_symbols(daily_outlook, stock_prices)

    result = TradeDecision(
        symbol=daily_outlook.symbol,
        action="NO_ACTION",
        reason=f"{daily_outlook.symbol}'s recent prices are not rising enough.",
    )

    if stock_is_owned:
        result = TradeDecision(
            symbol=daily_outlook.symbol,
            action="NO_ACTION",
            reason=f"{daily_outlook.symbol} is already owned.",
        )
    elif daily_outlook.score < settings.minimum_news_outlook:
        result = TradeDecision(
            symbol=daily_outlook.symbol,
            action="NO_ACTION",
            reason=f"{daily_outlook.symbol}'s daily outlook is below the minimum.",
        )
    elif check_rising_prices(
        stock_prices,
        settings.rising_prices_needed_to_buy,
        settings.minimum_price_rise_percent,
    ):
        result = TradeDecision(
            symbol=daily_outlook.symbol,
            action="BUY",
            reason=f"{daily_outlook.symbol}'s outlook and rising prices meet the buy rules.",
        )

    return result
