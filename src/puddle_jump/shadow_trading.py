"""Replay collected live bars into hypothetical wave trades."""

from dataclasses import dataclass
from datetime import datetime, time

from puddle_jump.shadow_bars import ShadowBar
from puddle_jump.shadow_settings import ShadowSettings


@dataclass(frozen=True)
class ShadowEvent:
    """One timestamped explanation of a shadow action."""

    observed_at: datetime
    symbol: str
    action: str
    price: float
    reason: str


@dataclass(frozen=True)
class ShadowTrade:
    """One completed hypothetical trade using later-bar fills."""

    symbol: str
    bought_at: datetime
    buy_price: float
    sold_at: datetime
    sell_price: float
    return_percent: float
    sell_reason: str


@dataclass(frozen=True)
class OpenShadowPosition:
    """One hypothetical position without a later sell fill yet."""

    symbol: str
    bought_at: datetime
    buy_price: float
    latest_price: float


@dataclass(frozen=True)
class ShadowResult:
    """The complete result reconstructed from collected bars."""

    events: list[ShadowEvent]
    trades: list[ShadowTrade]
    open_positions: list[OpenShadowPosition]


def calculate_return_percent(buy_price: float, sell_price: float) -> float:
    """Calculate an unadjusted shadow return from later-bar fills."""

    result = (sell_price / buy_price - 1) * 100

    return result


def replay_symbol(
    symbol: str,
    shadow_bars: list[ShadowBar],
    session_started_at: datetime,
    settings: ShadowSettings,
) -> tuple[list[ShadowEvent], ShadowTrade | None, OpenShadowPosition | None]:
    """Reconstruct one stock's first shadow trade from saved bars."""

    events: list[ShadowEvent] = []
    completed_trade: ShadowTrade | None = None
    open_position: OpenShadowPosition | None = None
    pending_buy_reason = ""
    pending_sell_reason = ""
    buy_price = 0.0
    bought_at: datetime | None = None
    stock_is_owned = False

    for index, shadow_bar in enumerate(shadow_bars):
        if pending_buy_reason:
            stock_is_owned = True
            buy_price = shadow_bar.open_price
            bought_at = shadow_bar.observed_at
            events.append(
                ShadowEvent(
                    observed_at=shadow_bar.observed_at,
                    symbol=symbol,
                    action="BUY_FILLED",
                    price=buy_price,
                    reason="Filled at the next minute's opening price.",
                )
            )
            pending_buy_reason = ""

        if pending_sell_reason:
            if bought_at is None:
                raise ValueError(f"{symbol} has a sell fill without a buy fill.")

            sell_price = shadow_bar.open_price
            events.append(
                ShadowEvent(
                    observed_at=shadow_bar.observed_at,
                    symbol=symbol,
                    action="SELL_FILLED",
                    price=sell_price,
                    reason="Filled at the next minute's opening price.",
                )
            )
            completed_trade = ShadowTrade(
                symbol=symbol,
                bought_at=bought_at,
                buy_price=buy_price,
                sold_at=shadow_bar.observed_at,
                sell_price=sell_price,
                return_percent=calculate_return_percent(buy_price, sell_price),
                sell_reason=pending_sell_reason,
            )

            return events, completed_trade, open_position

        if shadow_bar.observed_at < session_started_at:
            continue

        if not stock_is_owned:
            if index < settings.wave_window_prices:
                continue

            previous_bars = shadow_bars[index - settings.wave_window_prices : index]
            previous_high = max(bar.close_price for bar in previous_bars)
            recent_low = min(bar.close_price for bar in previous_bars)
            wave_rise_percent = (shadow_bar.close_price / recent_low - 1) * 100

            if (
                shadow_bar.close_price > previous_high
                and wave_rise_percent >= settings.minimum_wave_rise_percent
            ):
                pending_buy_reason = (
                    f"The price made a new {settings.wave_window_prices}-minute high "
                    f"after rising {wave_rise_percent:.2f}% from its recent low."
                )
                events.append(
                    ShadowEvent(
                        observed_at=shadow_bar.observed_at,
                        symbol=symbol,
                        action="BUY_SIGNAL",
                        price=shadow_bar.close_price,
                        reason=pending_buy_reason,
                    )
                )

            continue

        stop_price = buy_price * (1 - settings.maximum_loss_percent / 100)

        if shadow_bar.close_price <= stop_price:
            pending_sell_reason = (
                f"The price reached {settings.maximum_loss_percent:.2f}% below the buy price."
            )
        elif index >= settings.wave_window_prices:
            previous_bars = shadow_bars[index - settings.wave_window_prices : index]
            previous_low = min(bar.close_price for bar in previous_bars)

            if shadow_bar.close_price < previous_low:
                pending_sell_reason = (
                    f"The price broke below its previous {settings.wave_window_prices}-minute low."
                )

        if shadow_bar.observed_at.time() >= time(hour=15, minute=59):
            pending_sell_reason = "The regular market session is closing."

        if pending_sell_reason:
            events.append(
                ShadowEvent(
                    observed_at=shadow_bar.observed_at,
                    symbol=symbol,
                    action="SELL_SIGNAL",
                    price=shadow_bar.close_price,
                    reason=pending_sell_reason,
                )
            )

    if stock_is_owned and bought_at is not None and shadow_bars:
        open_position = OpenShadowPosition(
            symbol=symbol,
            bought_at=bought_at,
            buy_price=buy_price,
            latest_price=shadow_bars[-1].close_price,
        )

    return events, completed_trade, open_position


def replay_shadow_session(
    shadow_bars: list[ShadowBar],
    session_started_at: datetime,
    settings: ShadowSettings,
) -> ShadowResult:
    """Reconstruct every hypothetical decision from all collected bars."""

    bars_by_symbol: dict[str, list[ShadowBar]] = {}

    for shadow_bar in shadow_bars:
        bars_by_symbol.setdefault(shadow_bar.symbol, []).append(shadow_bar)

    events: list[ShadowEvent] = []
    trades: list[ShadowTrade] = []
    open_positions: list[OpenShadowPosition] = []

    for symbol in settings.symbols:
        symbol_bars = bars_by_symbol.get(symbol, [])
        symbol_bars.sort(key=lambda bar: bar.observed_at)
        symbol_events, completed_trade, open_position = replay_symbol(
            symbol=symbol,
            shadow_bars=symbol_bars,
            session_started_at=session_started_at,
            settings=settings,
        )
        events.extend(symbol_events)

        if completed_trade:
            trades.append(completed_trade)

        if open_position:
            open_positions.append(open_position)

    events.sort(key=lambda event: (event.observed_at, event.symbol, event.action))
    trades.sort(key=lambda trade: (trade.sold_at, trade.symbol))
    open_positions.sort(key=lambda position: position.symbol)

    return ShadowResult(
        events=events,
        trades=trades,
        open_positions=open_positions,
    )
