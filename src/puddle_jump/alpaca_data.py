"""Load Alpaca credentials and create read-only market-data clients."""

from dataclasses import dataclass
from pathlib import Path

from alpaca.data.historical import StockHistoricalDataClient
from dotenv import dotenv_values

DEFAULT_ENV_PATH = Path(".env")


@dataclass(frozen=True)
class AlpacaCredentials:
    """The local key and secret used for Alpaca data requests."""

    api_key: str
    secret_key: str


def load_alpaca_credentials(
    env_path: Path = DEFAULT_ENV_PATH,
) -> AlpacaCredentials:
    """Load Alpaca credentials without printing or exposing them."""

    saved_credentials = dotenv_values(env_path)
    api_key = saved_credentials.get("APCA_API_KEY_ID") or ""
    secret_key = saved_credentials.get("APCA_API_SECRET_KEY") or ""

    if not api_key:
        raise ValueError("APCA_API_KEY_ID is missing from the .env file.")

    if not secret_key:
        raise ValueError("APCA_API_SECRET_KEY is missing from the .env file.")

    result = AlpacaCredentials(
        api_key=api_key,
        secret_key=secret_key,
    )

    return result


def create_stock_data_client(
    credentials: AlpacaCredentials,
) -> StockHistoricalDataClient:
    """Create Alpaca's read-only stock market-data client."""

    result = StockHistoricalDataClient(
        api_key=credentials.api_key,
        secret_key=credentials.secret_key,
    )

    return result
