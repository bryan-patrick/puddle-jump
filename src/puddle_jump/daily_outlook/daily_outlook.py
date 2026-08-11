"""Create, validate, write, and read daily stock outlooks."""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class DailyOutlook:
    """One news-based outlook for one stock."""

    symbol: str
    score: float
    label: str
    explanation: str
    sources: list[str]
    recorded_at: datetime


def get_outlook_label(score: float) -> str:
    """Turn an outlook score into a plain label."""
    result = "neutral"

    if score < 0:
        result = "bad"

    if score > 0:
        result = "good"

    return result


def check_daily_outlook(outlook: DailyOutlook) -> None:
    """Reject a daily outlook with missing or inconsistent values."""
    if not outlook.symbol:
        raise ValueError("A daily outlook needs a stock symbol.")

    if outlook.symbol != outlook.symbol.upper():
        raise ValueError("A daily outlook stock symbol must be uppercase.")

    if not -1 <= outlook.score <= 1:
        raise ValueError("A daily outlook score must be between -1 and 1.")

    expected_label = get_outlook_label(outlook.score)

    if outlook.label != expected_label:
        raise ValueError(f"A score of {outlook.score} must use the label {expected_label}.")

    if not outlook.explanation.strip():
        raise ValueError("A daily outlook needs an explanation.")

    if not outlook.sources:
        raise ValueError("A daily outlook needs at least one source.")

    for source in outlook.sources:
        if not source.strip():
            raise ValueError("Daily outlook sources cannot be empty.")

    if outlook.recorded_at.utcoffset() is None:
        raise ValueError("A daily outlook timestamp must include a timezone.")


def create_daily_outlook(
    symbol: str,
    score: float,
    explanation: str,
    sources: list[str],
    recorded_at: datetime,
) -> DailyOutlook:
    """Create and validate one daily stock outlook."""
    result = DailyOutlook(
        symbol=symbol,
        score=score,
        label=get_outlook_label(score),
        explanation=explanation,
        sources=sources,
        recorded_at=recorded_at,
    )

    check_daily_outlook(result)
    return result


def write_daily_outlook(
    outlooks: list[DailyOutlook],
    outlook_path: Path,
    replace_existing: bool = True,
) -> None:
    """Write daily stock outlooks to a readable JSON file."""
    saved_outlooks: list[dict[str, object]] = []

    for outlook in outlooks:
        check_daily_outlook(outlook)

        saved_outlook = {
            "symbol": outlook.symbol,
            "score": outlook.score,
            "label": outlook.label,
            "explanation": outlook.explanation,
            "sources": outlook.sources,
            "recorded_at": outlook.recorded_at.isoformat(),
        }
        saved_outlooks.append(saved_outlook)

    saved_file = {"outlooks": saved_outlooks}

    write_mode = "w"

    if not replace_existing:
        write_mode = "x"

    with outlook_path.open(write_mode, encoding="utf-8") as outlook_file:
        json.dump(saved_file, outlook_file, indent=2)
        outlook_file.write("\n")


def read_daily_outlook(outlook_path: Path) -> list[DailyOutlook]:
    """Read and validate daily stock outlooks from JSON."""
    result: list[DailyOutlook] = []

    with outlook_path.open(encoding="utf-8") as outlook_file:
        saved_file = json.load(outlook_file)

    for saved_outlook in saved_file["outlooks"]:
        outlook = DailyOutlook(
            symbol=saved_outlook["symbol"],
            score=saved_outlook["score"],
            label=saved_outlook["label"],
            explanation=saved_outlook["explanation"],
            sources=saved_outlook["sources"],
            recorded_at=datetime.fromisoformat(saved_outlook["recorded_at"]),
        )
        check_daily_outlook(outlook)
        result.append(outlook)

    return result
