"""Run and report a cached multi-day replay of the trading strategy."""

from pathlib import Path

from puddle_jump.alpaca_data import create_stock_data_client, load_alpaca_credentials
from puddle_jump.history_cache import (
    DEFAULT_HISTORY_CACHE_DIRECTORY,
    get_historical_prices,
    get_recent_trading_days,
    remove_expired_cache,
)
from puddle_jump.history_replay_settings import (
    HistoryReplaySettings,
    load_history_replay_settings,
)
from puddle_jump.strategy_history import (
    HistoryReplayResult,
    combine_replay_days,
    replay_trading_day,
)
from puddle_jump.strategy_settings import StrategySettings, load_strategy_settings


def count_replay_trades(replay_result: HistoryReplayResult) -> tuple[int, int]:
    """Count completed trades and profitable trades in one replay."""

    trade_count = 0
    winner_count = 0

    for day_result in replay_result.day_results:
        for stock_result in day_result.stock_results:
            for trade in stock_result.trades:
                trade_count += 1

                if trade.return_percent > 0:
                    winner_count += 1

    return trade_count, winner_count


def build_history_report(
    replay_result: HistoryReplayResult,
    replay_settings: HistoryReplaySettings,
    strategy_settings: StrategySettings,
    cache_hits: int,
    downloads: int,
    expired_files_removed: int,
) -> str:
    """Build a plain Markdown report from the recorded replay results."""

    trade_count, winner_count = count_replay_trades(replay_result)
    result_lines = [
        "# Ten-day strategy replay",
        "",
        "This is an exploration run, not evidence that the strategy will make money.",
        "",
        "## Setup",
        "",
        f"- Trading days: {len(replay_result.day_results)}",
        f"- Stocks per day: {len(replay_settings.symbols)}",
        "- Price resolution: one-minute IEX bars",
        "- Buy input: price movement only",
        f"- Estimated cost: {replay_settings.estimated_trade_cost_percent:.2f}% per side",
        f"- Rising prices needed: {strategy_settings.rising_prices_needed_to_buy}",
        f"- Falling prices needed: {strategy_settings.falling_prices_needed_to_sell}",
        f"- Cache retention: {replay_settings.cache_days} days",
        "",
        "## Combined result",
        "",
        f"- Strategy return: {replay_result.strategy_return_percent:.4f}%",
        f"- Equal-weight buy and hold: {replay_result.buy_and_hold_return_percent:.4f}%",
        f"- Completed trades: {trade_count}",
        f"- Profitable trades after estimated costs: {winner_count}",
        f"- Cache hits: {cache_hits}",
        f"- Downloads: {downloads}",
        f"- Expired cache files removed: {expired_files_removed}",
        "",
        "## Daily results",
        "",
        "| Day | Strategy | Buy and hold | Trades | Winners |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for day_result in replay_result.day_results:
        day_trade_count = 0
        day_winner_count = 0

        for stock_result in day_result.stock_results:
            for trade in stock_result.trades:
                day_trade_count += 1

                if trade.return_percent > 0:
                    day_winner_count += 1

        result_lines.append(
            f"| {day_result.trading_day.isoformat()} "
            f"| {day_result.strategy_return_percent:.4f}% "
            f"| {day_result.buy_and_hold_return_percent:.4f}% "
            f"| {day_trade_count} | {day_winner_count} |"
        )

    for day_result in replay_result.day_results:
        result_lines.extend(
            [
                "",
                f"## {day_result.trading_day.isoformat()}",
                "",
                "| Stock | Trades | Strategy | Buy and hold |",
                "| --- | ---: | ---: | ---: |",
            ]
        )

        for stock_result in day_result.stock_results:
            result_lines.append(
                f"| {stock_result.symbol} | {len(stock_result.trades)} "
                f"| {stock_result.strategy_return_percent:.4f}% "
                f"| {stock_result.buy_and_hold_return_percent:.4f}% |"
            )

        day_trades = []

        for stock_result in day_result.stock_results:
            for trade in stock_result.trades:
                day_trades.append(trade)

        if day_trades:
            result_lines.extend(
                [
                    "",
                    "### Trades",
                    "",
                    "| Stock | Bought | Sold | Return | Exit |",
                    "| --- | --- | --- | ---: | --- |",
                ]
            )

            for trade in day_trades:
                bought_at = trade.bought_at.strftime("%H:%M")
                sold_at = trade.sold_at.strftime("%H:%M")
                result_lines.append(
                    f"| {trade.symbol} | {bought_at} | {sold_at} "
                    f"| {trade.return_percent:.4f}% | {trade.sell_reason} |"
                )

    result_lines.extend(
        [
            "",
            "## Reading this result",
            "",
            "The replay gives every stock an equal share of the day and compounds the daily "
            "results. "
            "A position still open at the close is marked at the final minute price. This replay "
            "uses the current short rising-price rule; the planned 30-minute rule is not included.",
            "",
        ]
    )
    result = "\n".join(result_lines)

    return result


def write_history_report(report: str, report_path: Path) -> None:
    """Write the completed historical replay report."""

    report_path.parent.mkdir(parents=True, exist_ok=True)

    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write(report)


def replay_history() -> HistoryReplayResult:
    """Download missing inputs, replay ten days, and write one report."""

    replay_settings = load_history_replay_settings()
    strategy_settings = load_strategy_settings()
    credentials = load_alpaca_credentials()
    stock_data_client = create_stock_data_client(credentials)
    expired_files_removed = remove_expired_cache(
        cache_directory=DEFAULT_HISTORY_CACHE_DIRECTORY,
        cache_days=replay_settings.cache_days,
    )
    trading_days, trading_days_were_cached = get_recent_trading_days(
        stock_data_client=stock_data_client,
        trading_days_needed=replay_settings.trading_days + 1,
    )
    replay_days = trading_days[1:]
    day_results = []
    cache_hits = int(trading_days_were_cached)
    downloads = int(not trading_days_were_cached)

    for trading_day in replay_days:
        stock_prices, prices_were_cached = get_historical_prices(
            stock_data_client=stock_data_client,
            symbols=replay_settings.symbols,
            trading_day=trading_day,
            cache_directory=DEFAULT_HISTORY_CACHE_DIRECTORY,
            cache_days=replay_settings.cache_days,
        )

        if prices_were_cached:
            cache_hits += 1
        else:
            downloads += 1

        day_result = replay_trading_day(
            trading_day=trading_day,
            symbols=replay_settings.symbols,
            stock_prices=stock_prices,
            strategy_settings=strategy_settings,
            estimated_trade_cost_percent=replay_settings.estimated_trade_cost_percent,
        )
        day_results.append(day_result)

    result = combine_replay_days(day_results)
    report = build_history_report(
        replay_result=result,
        replay_settings=replay_settings,
        strategy_settings=strategy_settings,
        cache_hits=cache_hits,
        downloads=downloads,
        expired_files_removed=expired_files_removed,
    )
    write_history_report(report, replay_settings.report_path)

    return result


def main() -> None:
    """Run the historical replay and print its plain result."""

    result = replay_history()
    trade_count, winner_count = count_replay_trades(result)
    replay_settings = load_history_replay_settings()

    print(f"Strategy return: {result.strategy_return_percent:.4f}%")
    print(f"Equal-weight buy and hold: {result.buy_and_hold_return_percent:.4f}%")
    print(f"Trades: {trade_count}")
    print(f"Winners after estimated costs: {winner_count}")
    print(f"Report: {replay_settings.report_path}")


if __name__ == "__main__":
    main()
