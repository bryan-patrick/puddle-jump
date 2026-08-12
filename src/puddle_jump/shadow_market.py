"""Run the wave strategy against live data without placing orders."""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from alpaca.trading.client import TradingClient

from puddle_jump.alpaca_data import create_stock_data_client, load_alpaca_credentials
from puddle_jump.daily_watchlist import save_daily_watchlist
from puddle_jump.shadow_bars import (
    ShadowBar,
    download_shadow_bars,
    merge_shadow_bars,
    read_shadow_bars,
    write_shadow_bars,
)
from puddle_jump.shadow_settings import ShadowSettings, load_shadow_settings
from puddle_jump.shadow_trading import ShadowEvent, ShadowResult, replay_shadow_session
from puddle_jump.stock_pool import load_stock_pool

MARKET_TIME_ZONE = ZoneInfo("America/New_York")
TRADING_DAYS_DIRECTORY = Path("data/trading-days")


def configure_logging(log_path: Path) -> logging.Logger:
    """Write plain shadow updates to both the process log and saved log."""

    logger = logging.getLogger("puddle_jump.shadow_market")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter(
        "%(asctime)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    process_handler = logging.StreamHandler()
    process_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(process_handler)

    return logger


def load_or_create_session_start(session_path: Path, current_time: datetime) -> datetime:
    """Keep the first start time so restarting cannot rewrite earlier decisions."""

    if session_path.is_file():
        with session_path.open(encoding="utf-8") as session_file:
            saved_session = json.load(session_file)

        return datetime.fromisoformat(saved_session["started_at"])

    saved_session = {"started_at": current_time.isoformat()}

    with session_path.open("w", encoding="utf-8") as session_file:
        json.dump(saved_session, session_file, indent=2)
        session_file.write("\n")

    return current_time


def write_shadow_events(events: list[ShadowEvent], events_path: Path) -> None:
    """Replace the canonical event file with the reconstructed event history."""

    with events_path.open("w", encoding="utf-8") as events_file:
        for event in events:
            saved_event = {
                "observed_at": event.observed_at.isoformat(),
                "symbol": event.symbol,
                "action": event.action,
                "price": event.price,
                "reason": event.reason,
            }
            events_file.write(json.dumps(saved_event))
            events_file.write("\n")


def build_shadow_report(
    shadow_result: ShadowResult,
    settings: ShadowSettings,
    session_started_at: datetime,
    latest_bar_at: datetime | None,
) -> str:
    """Build the current human-readable shadow result."""

    winner_count = 0
    total_return = 0.0

    for trade in shadow_result.trades:
        total_return += trade.return_percent

        if trade.return_percent > 0:
            winner_count += 1

    result_lines = [
        "# Live shadow report",
        "",
        "No Alpaca orders were submitted.",
        "",
        "## Session",
        "",
        f"- Started: {session_started_at.isoformat()}",
        f"- Latest completed bar: {latest_bar_at.isoformat() if latest_bar_at else 'None'}",
        f"- Stocks watched: {len(settings.symbols)}",
        f"- Wave window: {settings.wave_window_prices} prices",
        f"- Minimum wave rise: {settings.minimum_wave_rise_percent:.2f}%",
        f"- Maximum loss: {settings.maximum_loss_percent:.2f}%",
        "- Fill rule: next minute's opening price",
        "- Estimated execution costs: not applied",
        "",
        "## Current result",
        "",
        f"- Completed trades: {len(shadow_result.trades)}",
        f"- Winners: {winner_count}",
        f"- Sum of trade returns: {total_return:.4f}%",
        f"- Open positions: {len(shadow_result.open_positions)}",
        "",
        "## Completed trades",
        "",
        "| Stock | Bought | Buy | Sold | Sell | Return | Reason |",
        "| --- | --- | ---: | --- | ---: | ---: | --- |",
    ]

    for trade in shadow_result.trades:
        result_lines.append(
            f"| {trade.symbol} | {trade.bought_at.isoformat()} | {trade.buy_price:.4f} "
            f"| {trade.sold_at.isoformat()} | {trade.sell_price:.4f} "
            f"| {trade.return_percent:.4f}% | {trade.sell_reason} |"
        )

    result_lines.extend(
        [
            "",
            "## Open positions",
            "",
            "| Stock | Bought | Buy | Latest |",
            "| --- | --- | ---: | ---: |",
        ]
    )

    for position in shadow_result.open_positions:
        result_lines.append(
            f"| {position.symbol} | {position.bought_at.isoformat()} "
            f"| {position.buy_price:.4f} | {position.latest_price:.4f} |"
        )

    result_lines.append("")
    result = "\n".join(result_lines)

    return result


def write_shadow_report(report: str, report_path: Path) -> None:
    """Save the current Markdown shadow report."""

    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write(report)


def get_download_start(
    shadow_bars: list[ShadowBar],
    session_started_at: datetime,
    settings: ShadowSettings,
) -> datetime:
    """Request only enough overlap to warm up or replace the latest bar."""

    if shadow_bars:
        return shadow_bars[-1].observed_at - timedelta(minutes=1)

    warmup_minutes = settings.wave_window_prices + 2
    result = session_started_at - timedelta(minutes=warmup_minutes)

    return result


def get_completed_bar_end(current_time: datetime) -> datetime:
    """Exclude the market minute that is still being formed."""

    result = current_time.replace(second=0, microsecond=0)

    return result


def wait_for_next_check(current_time: datetime, check_every_seconds: int) -> None:
    """Pause until shortly after the next configured check boundary."""

    seconds_since_midnight = (
        current_time.hour * 60 * 60 + current_time.minute * 60 + current_time.second
    )
    seconds_until_check = check_every_seconds - (seconds_since_midnight % check_every_seconds)
    time.sleep(seconds_until_check + 2)


def run_shadow_market(check_once: bool = False) -> None:
    """Collect live bars and record hypothetical trades until market close."""

    settings = load_shadow_settings()
    credentials = load_alpaca_credentials()
    current_time = datetime.now(MARKET_TIME_ZONE)
    trading_day = current_time.date()
    trading_day_directory = TRADING_DAYS_DIRECTORY / trading_day.isoformat()
    trading_day_directory.mkdir(parents=True, exist_ok=True)
    logger = configure_logging(trading_day_directory / "shadow-market.log")
    session_path = trading_day_directory / "shadow-session.json"
    bars_path = trading_day_directory / "shadow-bars.parquet"
    events_path = trading_day_directory / "shadow-events.jsonl"
    report_path = trading_day_directory / "shadow-report.md"
    session_started_at = load_or_create_session_start(session_path, current_time)
    save_daily_watchlist(trading_day, settings.symbols, load_stock_pool())
    stock_data_client = create_stock_data_client(credentials)
    trading_client = TradingClient(credentials.api_key, credentials.secret_key, paper=True)
    market_clock = trading_client.get_clock()

    if not market_clock.is_open:
        logger.info("The regular market is closed. No shadow session was started.")

        return

    logger.info(
        "Shadow market started for %s stocks. No orders will be submitted.",
        len(settings.symbols),
    )
    shadow_bars = read_shadow_bars(bars_path)
    logged_event_count = 0

    while True:
        current_time = datetime.now(MARKET_TIME_ZONE)
        completed_bar_end = get_completed_bar_end(current_time)
        download_start = get_download_start(shadow_bars, session_started_at, settings)
        downloaded_bars = download_shadow_bars(
            stock_data_client=stock_data_client,
            symbols=settings.symbols,
            start_time=download_start,
            end_time=completed_bar_end,
        )
        shadow_bars = merge_shadow_bars(shadow_bars, downloaded_bars)
        write_shadow_bars(shadow_bars, bars_path)
        shadow_result = replay_shadow_session(shadow_bars, session_started_at, settings)
        write_shadow_events(shadow_result.events, events_path)
        latest_bar_at = shadow_bars[-1].observed_at if shadow_bars else None
        report = build_shadow_report(
            shadow_result=shadow_result,
            settings=settings,
            session_started_at=session_started_at,
            latest_bar_at=latest_bar_at,
        )
        write_shadow_report(report, report_path)

        for event in shadow_result.events[logged_event_count:]:
            logger.info(
                "%s %s at %.4f — %s",
                event.symbol,
                event.action,
                event.price,
                event.reason,
            )

        logged_event_count = len(shadow_result.events)
        logger.info(
            "Saved %s bars, %s completed trades, and %s open positions.",
            len(shadow_bars),
            len(shadow_result.trades),
            len(shadow_result.open_positions),
        )

        if check_once or current_time >= market_clock.next_close:
            break

        wait_for_next_check(current_time, settings.check_every_seconds)

    logger.info("Shadow market stopped. Report: %s", report_path)
