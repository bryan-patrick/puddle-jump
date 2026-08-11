"""Read, validate, and save fixed inputs for a historical replay."""

import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from puddle_jump.stock_prices import StockPrice, check_stock_price, create_stock_price


@dataclass(frozen=True)
class HistoricalInputPlan:
    """The stocks and time range locked before a historical replay."""

    trading_day: date
    symbols: list[str]
    news_start: datetime
    market_open: datetime
    market_close: datetime
    price_interval_seconds: int
    price_feed: str


@dataclass(frozen=True)
class HistoricalNews:
    """News metadata that became available during the locked news window."""

    article_id: int
    headline: str
    source: str
    url: str
    created_at: datetime
    updated_at: datetime
    symbols: list[str]


def check_timestamp(timestamp: datetime, name: str) -> None:
    """Reject a historical timestamp without a timezone."""

    if timestamp.utcoffset() is None:
        raise ValueError(f"{name} must include a timezone.")


def check_historical_input_plan(plan: HistoricalInputPlan) -> None:
    """Reject an incomplete or inconsistent historical input plan."""

    if not plan.symbols:
        raise ValueError("A historical input plan needs at least one stock symbol.")

    checked_symbols: set[str] = set()

    for symbol in plan.symbols:
        if not symbol or symbol != symbol.upper():
            raise ValueError("Historical input symbols must be uppercase.")

        if symbol in checked_symbols:
            raise ValueError(f"The historical input plan contains {symbol} more than once.")

        checked_symbols.add(symbol)

    check_timestamp(plan.news_start, "The news start time")
    check_timestamp(plan.market_open, "The market open time")
    check_timestamp(plan.market_close, "The market close time")

    if not plan.news_start < plan.market_open < plan.market_close:
        raise ValueError("The news start, market open, and market close must be in order.")

    if plan.market_open.date() != plan.trading_day:
        raise ValueError("The market open time does not match the trading day.")

    if plan.market_close.date() != plan.trading_day:
        raise ValueError("The market close time does not match the trading day.")

    if plan.price_interval_seconds <= 0:
        raise ValueError("The historical price interval must be greater than zero.")

    market_seconds = int((plan.market_close - plan.market_open).total_seconds())

    if market_seconds % plan.price_interval_seconds != 0:
        raise ValueError("The historical price interval must divide the market day evenly.")

    if plan.price_feed != "iex":
        raise ValueError("Historical replay inputs currently support only the IEX feed.")


def load_historical_input_plan(plan_path: Path) -> HistoricalInputPlan:
    """Load and validate one fixed historical input plan."""

    with plan_path.open(encoding="utf-8") as plan_file:
        saved_plan = json.load(plan_file)

    result = HistoricalInputPlan(
        trading_day=date.fromisoformat(saved_plan["trading_day"]),
        symbols=saved_plan["symbols"],
        news_start=datetime.fromisoformat(saved_plan["news_start"]),
        market_open=datetime.fromisoformat(saved_plan["market_open"]),
        market_close=datetime.fromisoformat(saved_plan["market_close"]),
        price_interval_seconds=saved_plan["price_interval_seconds"],
        price_feed=saved_plan["price_feed"],
    )

    check_historical_input_plan(result)
    return result


def check_historical_news(news: HistoricalNews) -> None:
    """Reject incomplete historical news metadata."""

    if news.article_id <= 0:
        raise ValueError("Historical news needs a positive article ID.")

    if not news.headline.strip():
        raise ValueError("Historical news needs a headline.")

    if not news.source.strip():
        raise ValueError("Historical news needs a source.")

    if not news.url.strip():
        raise ValueError("Historical news needs a URL.")

    if not news.symbols:
        raise ValueError("Historical news needs at least one matching stock symbol.")

    check_timestamp(news.created_at, "The news creation time")
    check_timestamp(news.updated_at, "The news update time")

    if news.updated_at < news.created_at:
        raise ValueError("Historical news cannot be updated before it was created.")


def check_news_for_plan(
    news_items: list[HistoricalNews],
    plan: HistoricalInputPlan,
) -> None:
    """Confirm saved news stays inside the plan without unrelated symbols."""

    planned_symbols = set(plan.symbols)

    for news in news_items:
        check_historical_news(news)

        if news.created_at < plan.news_start or news.created_at > plan.market_close:
            raise ValueError("Historical news falls outside the planned news window.")

        if news.updated_at > plan.market_close:
            raise ValueError("Historical news was updated after the market closed.")

        if not set(news.symbols).issubset(planned_symbols):
            raise ValueError("Historical news contains a symbol outside the input plan.")


def write_historical_news(
    news_items: list[HistoricalNews],
    news_path: Path,
    plan: HistoricalInputPlan,
) -> None:
    """Save historical news metadata without article bodies or summaries."""

    check_news_for_plan(news_items, plan)
    saved_news: list[dict[str, object]] = []

    for news in news_items:
        saved_news.append(
            {
                "article_id": news.article_id,
                "headline": news.headline,
                "source": news.source,
                "url": news.url,
                "created_at": news.created_at.isoformat(),
                "updated_at": news.updated_at.isoformat(),
                "symbols": news.symbols,
            }
        )

    saved_file = {"news": saved_news}

    with news_path.open("w", encoding="utf-8") as news_file:
        json.dump(saved_file, news_file, indent=2)
        news_file.write("\n")


def read_historical_news(
    news_path: Path,
    plan: HistoricalInputPlan,
) -> list[HistoricalNews]:
    """Read saved historical news without connecting to Alpaca."""

    result: list[HistoricalNews] = []

    with news_path.open(encoding="utf-8") as news_file:
        saved_file = json.load(news_file)

    for saved_news in saved_file["news"]:
        news = HistoricalNews(
            article_id=saved_news["article_id"],
            headline=saved_news["headline"],
            source=saved_news["source"],
            url=saved_news["url"],
            created_at=datetime.fromisoformat(saved_news["created_at"]),
            updated_at=datetime.fromisoformat(saved_news["updated_at"]),
            symbols=saved_news["symbols"],
        )
        check_historical_news(news)
        result.append(news)

    check_news_for_plan(result, plan)
    return result


def sample_stock_prices(
    trades: list[StockPrice],
    market_open: datetime,
    market_close: datetime,
    interval_seconds: int,
) -> list[StockPrice]:
    """Use the latest known trade at each historical observation time."""

    if not trades:
        raise ValueError("Historical price sampling needs at least one trade.")

    if interval_seconds <= 0:
        raise ValueError("The historical price interval must be greater than zero.")

    symbol = trades[0].symbol
    previous_trade_time: datetime | None = None

    for trade in trades:
        check_stock_price(trade)

        if trade.symbol != symbol:
            raise ValueError("Historical trades must belong to one stock.")

        if previous_trade_time and trade.observed_at < previous_trade_time:
            raise ValueError("Historical trades must be in chronological order.")

        previous_trade_time = trade.observed_at

    result: list[StockPrice] = []
    trade_index = 0
    latest_trade: StockPrice | None = None
    observation_time = market_open + timedelta(seconds=interval_seconds)

    while observation_time <= market_close:
        while trade_index < len(trades) and trades[trade_index].observed_at <= observation_time:
            latest_trade = trades[trade_index]
            trade_index += 1

        if latest_trade is None:
            raise ValueError(f"{symbol} has no trade before {observation_time.isoformat()}.")

        stock_price = create_stock_price(
            symbol=symbol,
            price=latest_trade.price,
            observed_at=observation_time,
        )
        result.append(stock_price)
        observation_time += timedelta(seconds=interval_seconds)

    return result


def check_prices_for_plan(
    stock_prices: dict[str, list[StockPrice]],
    plan: HistoricalInputPlan,
) -> None:
    """Confirm every planned observation is present at its exact time."""

    if set(stock_prices) != set(plan.symbols):
        raise ValueError("Historical prices must contain every planned stock and no others.")

    expected_count = int(
        (plan.market_close - plan.market_open).total_seconds() / plan.price_interval_seconds
    )

    for symbol in plan.symbols:
        symbol_prices = stock_prices[symbol]

        if len(symbol_prices) != expected_count:
            raise ValueError(f"{symbol} does not have every planned price observation.")

        expected_time = plan.market_open + timedelta(seconds=plan.price_interval_seconds)

        for stock_price in symbol_prices:
            check_stock_price(stock_price)

            if stock_price.symbol != symbol:
                raise ValueError(f"The saved {symbol} prices contain another stock.")

            if stock_price.observed_at != expected_time:
                raise ValueError(f"The saved {symbol} prices are not on the planned interval.")

            expected_time += timedelta(seconds=plan.price_interval_seconds)


def write_historical_prices(
    stock_prices: dict[str, list[StockPrice]],
    prices_path: Path,
    plan: HistoricalInputPlan,
) -> None:
    """Save fixed historical price observations in readable JSON."""

    check_prices_for_plan(stock_prices, plan)
    saved_prices: dict[str, list[dict[str, object]]] = {}

    for symbol, symbol_prices in stock_prices.items():
        saved_symbol_prices: list[dict[str, object]] = []

        for stock_price in symbol_prices:
            check_stock_price(stock_price)
            saved_symbol_prices.append(
                {
                    "price": stock_price.price,
                    "observed_at": stock_price.observed_at.isoformat(),
                }
            )

        saved_prices[symbol] = saved_symbol_prices

    saved_file = {"prices": saved_prices}

    with prices_path.open("w", encoding="utf-8") as prices_file:
        json.dump(saved_file, prices_file, indent=2)
        prices_file.write("\n")


def read_historical_prices(
    prices_path: Path,
    plan: HistoricalInputPlan,
) -> dict[str, list[StockPrice]]:
    """Read saved historical prices without connecting to Alpaca."""

    result: dict[str, list[StockPrice]] = {}

    with prices_path.open(encoding="utf-8") as prices_file:
        saved_file = json.load(prices_file)

    for symbol, saved_symbol_prices in saved_file["prices"].items():
        symbol_prices: list[StockPrice] = []

        for saved_stock_price in saved_symbol_prices:
            stock_price = create_stock_price(
                symbol=symbol,
                price=saved_stock_price["price"],
                observed_at=datetime.fromisoformat(saved_stock_price["observed_at"]),
            )
            symbol_prices.append(stock_price)

        result[symbol] = symbol_prices

    check_prices_for_plan(result, plan)
    return result
