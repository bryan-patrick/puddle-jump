"""Run fixed prices through the real buy and sell decision functions."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from puddle_jump.daily_outlook import create_daily_outlook
from puddle_jump.decisions import TradeDecision, decide_buy, decide_sell
from puddle_jump.stock_prices import StockPrice, create_stock_price
from puddle_jump.strategy_settings import load_strategy_settings

MARKET_TIME_ZONE = ZoneInfo("America/New_York")


def create_example_prices(
    symbol: str,
    price_values: list[float],
    start_time: datetime,
    seconds_between_prices: int,
) -> list[StockPrice]:
    """Create ordered stock prices for one fixed replay example."""
    result: list[StockPrice] = []

    for index, price in enumerate(price_values):
        observed_at = start_time + timedelta(seconds=index * seconds_between_prices)
        stock_price = create_stock_price(
            symbol=symbol,
            price=price,
            observed_at=observed_at,
        )
        result.append(stock_price)

    return result


def replay_decisions() -> list[TradeDecision]:
    """Return one fixed buy decision and one fixed sell decision."""
    result: list[TradeDecision] = []
    symbol = "AAPL"
    start_time = datetime(2026, 8, 11, 9, 30, tzinfo=MARKET_TIME_ZONE)
    settings = load_strategy_settings()

    daily_outlook = create_daily_outlook(
        symbol=symbol,
        score=0.50,
        explanation="The fixed replay uses a favorable news outlook.",
        sources=["https://example.com/aapl-news"],
        recorded_at=start_time,
    )
    rising_prices = create_example_prices(
        symbol=symbol,
        price_values=[100.00, 100.05, 100.10, 100.15, 100.20, 100.30],
        start_time=start_time,
        seconds_between_prices=settings.check_prices_every_seconds,
    )
    buy_decision = decide_buy(
        daily_outlook=daily_outlook,
        stock_prices=rising_prices,
        stock_is_owned=False,
        settings=settings,
    )
    result.append(buy_decision)

    falling_prices = create_example_prices(
        symbol=symbol,
        price_values=[101.00, 100.75, 100.50],
        start_time=start_time,
        seconds_between_prices=settings.check_prices_every_seconds,
    )
    sell_decision = decide_sell(
        symbol=symbol,
        stock_prices=falling_prices,
        stock_is_owned=True,
        reference_price=100.00,
        settings=settings,
    )
    result.append(sell_decision)

    return result


def main() -> None:
    """Print the fixed replay decisions and their reasons."""
    decisions = replay_decisions()

    for decision in decisions:
        print(f"{decision.symbol}: {decision.action} - {decision.reason}")


if __name__ == "__main__":
    main()
