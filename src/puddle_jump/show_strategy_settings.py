"""Show the settings for the initial trading strategy."""

from puddle_jump.strategy_settings import load_strategy_settings


def main() -> None:
    """Load and print the strategy settings."""
    settings = load_strategy_settings()

    print(f"Check prices every: {settings.check_prices_every_seconds} seconds")
    print(f"Rising prices needed to buy: {settings.rising_prices_needed_to_buy}")
    print(f"Falling prices needed to sell: {settings.falling_prices_needed_to_sell}")
    print(f"Minimum price rise: {settings.minimum_price_rise_percent}%")
    print(f"Minimum falling price drop: {settings.minimum_falling_price_drop_percent}%")
    print(f"Minimum news outlook: {settings.minimum_news_outlook}")
    print(f"Maximum fast drop: {settings.maximum_fast_drop_percent}%")
    print(f"Maximum loss: {settings.maximum_loss_percent}% below the buy price")
