"""Load the stocks Puddle Jump is allowed to consider."""

import json
from dataclasses import dataclass
from pathlib import Path

DEFAULT_STOCK_POOL_PATH = Path("config/stock_pool.json")


@dataclass(frozen=True)
class Stock:
    """One stock in the eligible stock pool."""

    symbol: str
    name: str
    sector: str
    group: str


def load_stock_pool(stock_pool_path: Path = DEFAULT_STOCK_POOL_PATH) -> list[Stock]:
    """Load the stock pool and reject missing or repeated symbols."""
    result: list[Stock] = []
    loaded_symbols: set[str] = set()

    with stock_pool_path.open(encoding="utf-8") as stock_pool_file:
        saved_stock_pool = json.load(stock_pool_file)

    for saved_stock in saved_stock_pool["stocks"]:
        symbol = saved_stock["symbol"]

        if not symbol:
            raise ValueError("Every stock in the pool needs a symbol.")

        if symbol in loaded_symbols:
            raise ValueError(f"The stock pool contains {symbol} more than once.")

        loaded_symbols.add(symbol)

        stock = Stock(
            symbol=symbol,
            name=saved_stock["name"],
            sector=saved_stock["sector"],
            group=saved_stock["group"],
        )

        result.append(stock)

    return result
