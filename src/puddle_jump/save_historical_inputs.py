"""Save one frozen set of historical news and prices from Alpaca."""

from pathlib import Path

from alpaca.common.enums import Sort
from alpaca.data.enums import DataFeed
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest, StockTradesRequest

from puddle_jump.alpaca_data import (
    create_news_client,
    create_stock_data_client,
    load_alpaca_credentials,
)
from puddle_jump.daily_outlook import DailyOutlook, read_daily_outlook
from puddle_jump.historical_inputs import (
    HistoricalInputPlan,
    HistoricalNews,
    load_historical_input_plan,
    read_historical_news,
    read_historical_prices,
    sample_stock_prices,
    write_historical_news,
    write_historical_prices,
)
from puddle_jump.stock_prices import StockPrice, create_stock_price

INPUT_DIRECTORY = Path("data/replay-inputs/2026-08-10")
PLAN_PATH = INPUT_DIRECTORY / "plan.json"
OUTLOOKS_PATH = INPUT_DIRECTORY / "initial-outlooks.json"
NEWS_PATH = INPUT_DIRECTORY / "news.json"
PRICES_PATH = INPUT_DIRECTORY / "prices.json"


def get_historical_news(
    news_client: NewsClient,
    plan: HistoricalInputPlan,
) -> list[HistoricalNews]:
    """Get news available from the prior close through the historical day."""

    request = NewsRequest(
        symbols=",".join(plan.symbols),
        start=plan.news_start,
        end=plan.market_close,
    )
    alpaca_news = news_client.get_news(request).data.get("news", [])
    result: list[HistoricalNews] = []

    for article in alpaca_news:
        matching_symbols: list[str] = []

        for symbol in article.symbols:
            if symbol in plan.symbols:
                matching_symbols.append(symbol)

        if not matching_symbols or not article.url:
            continue

        if article.created_at > plan.market_close:
            continue

        if article.updated_at > plan.market_close:
            continue

        news = HistoricalNews(
            article_id=article.id,
            headline=article.headline,
            source=article.source,
            url=article.url,
            created_at=article.created_at,
            updated_at=article.updated_at,
            symbols=matching_symbols,
        )
        result.append(news)

    result.sort(key=lambda news: news.created_at)
    return result


def check_outlooks(
    outlooks: list[DailyOutlook],
    news_items: list[HistoricalNews],
    plan: HistoricalInputPlan,
) -> None:
    """Confirm every planned stock has a premarket outlook using saved news."""

    outlook_symbols: set[str] = set()
    news_by_url: dict[str, HistoricalNews] = {}

    for news in news_items:
        news_by_url[news.url] = news

    for outlook in outlooks:
        if outlook.symbol not in plan.symbols:
            raise ValueError(f"{outlook.symbol} is not in the historical input plan.")

        if outlook.symbol in outlook_symbols:
            raise ValueError(f"The historical outlooks contain {outlook.symbol} twice.")

        if outlook.recorded_at >= plan.market_open:
            raise ValueError("Historical outlooks must be recorded before the market opens.")

        for source in outlook.sources:
            if source not in news_by_url:
                raise ValueError(f"The saved news does not contain outlook source {source}.")

            source_news = news_by_url[source]

            if source_news.updated_at > outlook.recorded_at:
                raise ValueError(f"Outlook source {source} was not available when recorded.")

        outlook_symbols.add(outlook.symbol)

    if outlook_symbols != set(plan.symbols):
        raise ValueError("Every planned stock needs one historical outlook.")


def get_historical_prices(
    stock_data_client: StockHistoricalDataClient,
    plan: HistoricalInputPlan,
) -> dict[str, list[StockPrice]]:
    """Get IEX trades and turn them into fixed price observations."""

    request = StockTradesRequest(
        symbol_or_symbols=plan.symbols,
        start=plan.market_open,
        end=plan.market_close,
        feed=DataFeed.IEX,
        sort=Sort.ASC,
    )
    alpaca_trades = stock_data_client.get_stock_trades(request).data
    result: dict[str, list[StockPrice]] = {}

    for symbol in plan.symbols:
        trades: list[StockPrice] = []

        for alpaca_trade in alpaca_trades.get(symbol, []):
            trade = create_stock_price(
                symbol=symbol,
                price=alpaca_trade.price,
                observed_at=alpaca_trade.timestamp,
            )
            trades.append(trade)

        result[symbol] = sample_stock_prices(
            trades=trades,
            market_open=plan.market_open,
            market_close=plan.market_close,
            interval_seconds=plan.price_interval_seconds,
        )

    return result


def save_historical_inputs() -> None:
    """Fetch and save the news and prices locked by the input plan."""

    plan = load_historical_input_plan(PLAN_PATH)
    outlooks = read_daily_outlook(OUTLOOKS_PATH)
    credentials = load_alpaca_credentials()
    news_client = create_news_client(credentials)
    stock_data_client = create_stock_data_client(credentials)

    news_items = get_historical_news(news_client, plan)
    check_outlooks(outlooks, news_items, plan)
    stock_prices = get_historical_prices(stock_data_client, plan)

    write_historical_news(news_items, NEWS_PATH, plan)
    write_historical_prices(stock_prices, PRICES_PATH, plan)


def main() -> None:
    """Save the fixed replay inputs and confirm they load without Alpaca."""

    save_historical_inputs()
    plan = load_historical_input_plan(PLAN_PATH)
    news_items = read_historical_news(NEWS_PATH, plan)
    stock_prices = read_historical_prices(PRICES_PATH, plan)

    print(f"Historical day: {plan.trading_day.isoformat()}")
    print(f"Historical news: {len(news_items)} articles")

    for symbol in plan.symbols:
        print(f"{symbol}: {len(stock_prices[symbol])} price observations")


if __name__ == "__main__":
    main()
