"""Create simple, repeatable outlooks from historical news headlines."""

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from puddle_jump.daily_outlook import DailyOutlook, create_daily_outlook
from puddle_jump.historical_inputs import HistoricalNews

DEFAULT_NEWS_WORDS_PATH = Path("config/news_words.json")


@dataclass(frozen=True)
class NewsWords:
    """Plain words and phrases that affect a headline's score."""

    positive: list[str]
    negative: list[str]


def load_news_words(words_path: Path = DEFAULT_NEWS_WORDS_PATH) -> NewsWords:
    """Load the small positive and negative headline word lists."""

    with words_path.open(encoding="utf-8") as words_file:
        saved_words = json.load(words_file)

    result = NewsWords(
        positive=saved_words["positive"],
        negative=saved_words["negative"],
    )

    if not result.positive or not result.negative:
        raise ValueError("News scoring needs positive and negative words.")

    positive_words = set(result.positive)
    negative_words = set(result.negative)

    if len(positive_words) != len(result.positive):
        raise ValueError("The positive news words contain a duplicate.")

    if len(negative_words) != len(result.negative):
        raise ValueError("The negative news words contain a duplicate.")

    if positive_words.intersection(negative_words):
        raise ValueError("A news word cannot be both positive and negative.")

    return result


def normalize_headline(headline: str) -> str:
    """Make headline phrase matching predictable without hiding the steps."""

    lowercase_headline = headline.lower()
    words_only_headline = re.sub(r"[^a-z0-9]+", " ", lowercase_headline)
    result = f" {words_only_headline.strip()} "

    return result


def headline_contains_phrase(headline: str, phrase: str) -> bool:
    """Return whether a whole word or phrase appears in a headline."""

    normalized_headline = normalize_headline(headline)
    normalized_phrase = normalize_headline(phrase).strip()
    result = f" {normalized_phrase} " in normalized_headline

    return result


def score_headline(headline: str, words: NewsWords) -> int:
    """Score one headline as positive, negative, or neutral."""

    has_positive_word = False
    has_negative_word = False

    for positive_word in words.positive:
        if headline_contains_phrase(headline, positive_word):
            has_positive_word = True
            break

    for negative_word in words.negative:
        if headline_contains_phrase(headline, negative_word):
            has_negative_word = True
            break

    result = 0

    if has_positive_word and not has_negative_word:
        result = 1
    elif has_negative_word and not has_positive_word:
        result = -1

    return result


def create_news_outlook(
    symbol: str,
    news_items: list[HistoricalNews],
    recorded_at: datetime,
    words: NewsWords,
) -> DailyOutlook | None:
    """Create one outlook from news published before the recorded time."""

    matching_news: list[HistoricalNews] = []

    for news in news_items:
        if symbol in news.symbols and news.created_at <= recorded_at:
            matching_news.append(news)

    if not matching_news:
        return None

    headline_score_total = 0
    positive_headlines = 0
    negative_headlines = 0

    for news in matching_news:
        headline_score = score_headline(news.headline, words)
        headline_score_total += headline_score

        if headline_score > 0:
            positive_headlines += 1
        elif headline_score < 0:
            negative_headlines += 1

    neutral_headlines = len(matching_news) - positive_headlines - negative_headlines
    score = round(headline_score_total / len(matching_news), 4)
    explanation = (
        f"Premarket headlines: {positive_headlines} positive, "
        f"{negative_headlines} negative, and {neutral_headlines} neutral."
    )
    sources: list[str] = []

    for news in matching_news:
        sources.append(news.url)

    result = create_daily_outlook(
        symbol=symbol,
        score=score,
        explanation=explanation,
        sources=sources,
        recorded_at=recorded_at,
    )

    return result


def create_news_outlooks(
    symbols: list[str],
    news_items: list[HistoricalNews],
    recorded_at: datetime,
    words: NewsWords,
) -> dict[str, DailyOutlook]:
    """Create every outlook supported by premarket news."""

    result: dict[str, DailyOutlook] = {}

    for symbol in symbols:
        outlook = create_news_outlook(symbol, news_items, recorded_at, words)

        if outlook is not None:
            result[symbol] = outlook

    return result
