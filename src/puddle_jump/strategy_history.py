"""Replay the real strategy decisions against historical stock prices."""

from dataclasses import dataclass
from datetime import date, datetime

from puddle_jump.daily_outlook import DailyOutlook
from puddle_jump.decisions import decide_buy, decide_sell
from puddle_jump.stock_prices import StockPrice
from puddle_jump.strategy_settings import StrategySettings


@dataclass(frozen=True)
class ReplayTrade:
    """One completed historical buy and sell."""

    symbol: str
    bought_at: datetime
    buy_price: float
    sold_at: datetime
    sell_price: float
    return_percent: float
    sell_reason: str


@dataclass(frozen=True)
class SymbolReplayResult:
    """One stock's strategy and baseline result for one day."""

    symbol: str
    outlook_score: float | None
    trades: list[ReplayTrade]
    strategy_return_percent: float
    buy_and_hold_return_percent: float


@dataclass(frozen=True)
class DayReplayResult:
    """The equal-weight result across every watched stock for one day."""

    trading_day: date
    stock_results: list[SymbolReplayResult]
    strategy_return_percent: float
    buy_and_hold_return_percent: float


@dataclass(frozen=True)
class HistoryReplayResult:
    """The combined result from replaying several trading days."""

    day_results: list[DayReplayResult]
    strategy_return_percent: float
    buy_and_hold_return_percent: float


def calculate_trade_return_percent(
    buy_price: float,
    sell_price: float,
    estimated_trade_cost_percent: float,
) -> float:
    """Calculate a trade return after one estimated cost on each side."""

    if buy_price <= 0 or sell_price <= 0:
        raise ValueError("Historical trade prices must be greater than zero.")

    if not 0 <= estimated_trade_cost_percent < 100:
        raise ValueError("The estimated trade cost must be between zero and 100 percent.")

    cost_rate = estimated_trade_cost_percent / 100
    total_buy_price = buy_price * (1 + cost_rate)
    total_sell_price = sell_price * (1 - cost_rate)
    result = (total_sell_price / total_buy_price - 1) * 100

    return result


def close_replay_trade(
    symbol: str,
    bought_at: datetime,
    buy_price: float,
    sold_at: datetime,
    sell_price: float,
    sell_reason: str,
    estimated_trade_cost_percent: float,
) -> ReplayTrade:
    """Create one completed historical trade with its estimated return."""

    result = ReplayTrade(
        symbol=symbol,
        bought_at=bought_at,
        buy_price=buy_price,
        sold_at=sold_at,
        sell_price=sell_price,
        return_percent=calculate_trade_return_percent(
            buy_price=buy_price,
            sell_price=sell_price,
            estimated_trade_cost_percent=estimated_trade_cost_percent,
        ),
        sell_reason=sell_reason,
    )

    return result


def calculate_compounded_return(returns: list[float]) -> float:
    """Combine consecutive percentage returns without adding them directly."""

    growth = 1.0

    for return_percent in returns:
        growth *= 1 + return_percent / 100

    result = (growth - 1) * 100

    return result


def replay_stock_day(
    symbol: str,
    daily_outlook: DailyOutlook | None,
    stock_prices: list[StockPrice],
    strategy_settings: StrategySettings,
    estimated_trade_cost_percent: float,
) -> SymbolReplayResult:
    """Replay one stock through the same buy and sell decision functions."""

    if not stock_prices:
        raise ValueError(f"A historical replay needs prices for {symbol}.")

    observed_prices: list[StockPrice] = []
    trades: list[ReplayTrade] = []
    stock_is_owned = False
    bought_at: datetime | None = None
    buy_price = 0.0

    for stock_price in stock_prices:
        if stock_price.symbol != symbol:
            raise ValueError(f"Every historical price must belong to {symbol}.")

        observed_prices.append(stock_price)

        if stock_is_owned:
            sell_decision = decide_sell(
                symbol=symbol,
                stock_prices=observed_prices,
                stock_is_owned=True,
                buy_price=buy_price,
                settings=strategy_settings,
            )

            if sell_decision.action == "SELL":
                if bought_at is None:
                    raise ValueError(f"{symbol} is owned without a recorded buy time.")

                trade = close_replay_trade(
                    symbol=symbol,
                    bought_at=bought_at,
                    buy_price=buy_price,
                    sold_at=stock_price.observed_at,
                    sell_price=stock_price.price,
                    sell_reason=sell_decision.reason,
                    estimated_trade_cost_percent=estimated_trade_cost_percent,
                )
                trades.append(trade)
                stock_is_owned = False
                bought_at = None
                buy_price = 0.0

        elif daily_outlook is not None:
            buy_decision = decide_buy(
                daily_outlook=daily_outlook,
                stock_prices=observed_prices,
                stock_is_owned=False,
                settings=strategy_settings,
            )

            if buy_decision.action == "BUY":
                stock_is_owned = True
                bought_at = stock_price.observed_at
                buy_price = stock_price.price

    if stock_is_owned:
        if bought_at is None:
            raise ValueError(f"{symbol} is owned without a recorded buy time.")

        closing_price = stock_prices[-1]
        trade = close_replay_trade(
            symbol=symbol,
            bought_at=bought_at,
            buy_price=buy_price,
            sold_at=closing_price.observed_at,
            sell_price=closing_price.price,
            sell_reason="The position was marked at the market close.",
            estimated_trade_cost_percent=estimated_trade_cost_percent,
        )
        trades.append(trade)

    trade_returns: list[float] = []

    for trade in trades:
        trade_returns.append(trade.return_percent)

    strategy_return_percent = calculate_compounded_return(trade_returns)
    buy_and_hold_return_percent = calculate_trade_return_percent(
        buy_price=stock_prices[0].price,
        sell_price=stock_prices[-1].price,
        estimated_trade_cost_percent=estimated_trade_cost_percent,
    )
    outlook_score = None

    if daily_outlook is not None:
        outlook_score = daily_outlook.score

    result = SymbolReplayResult(
        symbol=symbol,
        outlook_score=outlook_score,
        trades=trades,
        strategy_return_percent=strategy_return_percent,
        buy_and_hold_return_percent=buy_and_hold_return_percent,
    )

    return result


def replay_trading_day(
    trading_day: date,
    symbols: list[str],
    outlooks: dict[str, DailyOutlook],
    stock_prices: dict[str, list[StockPrice]],
    strategy_settings: StrategySettings,
    estimated_trade_cost_percent: float,
) -> DayReplayResult:
    """Replay every stock with equal weight for one historical day."""

    stock_results: list[SymbolReplayResult] = []

    for symbol in symbols:
        stock_result = replay_stock_day(
            symbol=symbol,
            daily_outlook=outlooks.get(symbol),
            stock_prices=stock_prices[symbol],
            strategy_settings=strategy_settings,
            estimated_trade_cost_percent=estimated_trade_cost_percent,
        )
        stock_results.append(stock_result)

    strategy_return_total = 0.0
    buy_and_hold_return_total = 0.0

    for stock_result in stock_results:
        strategy_return_total += stock_result.strategy_return_percent
        buy_and_hold_return_total += stock_result.buy_and_hold_return_percent

    result = DayReplayResult(
        trading_day=trading_day,
        stock_results=stock_results,
        strategy_return_percent=strategy_return_total / len(stock_results),
        buy_and_hold_return_percent=buy_and_hold_return_total / len(stock_results),
    )

    return result


def combine_replay_days(day_results: list[DayReplayResult]) -> HistoryReplayResult:
    """Compound the equal-weight daily strategy and baseline results."""

    if not day_results:
        raise ValueError("A historical replay needs at least one completed day.")

    strategy_returns: list[float] = []
    buy_and_hold_returns: list[float] = []

    for day_result in day_results:
        strategy_returns.append(day_result.strategy_return_percent)
        buy_and_hold_returns.append(day_result.buy_and_hold_return_percent)

    result = HistoryReplayResult(
        day_results=day_results,
        strategy_return_percent=calculate_compounded_return(strategy_returns),
        buy_and_hold_return_percent=calculate_compounded_return(buy_and_hold_returns),
    )

    return result
