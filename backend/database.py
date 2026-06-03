"""Compatibility wrappers around the production SQLite layer."""

from backend.db import get_history, get_stats, init_db, save_prediction


def insert_prediction(news_text, prediction, language=None, confidence=0):
    save_prediction(news_text, prediction, confidence)


def fetch_predictions(limit=100):
    return get_history(limit)


def fetch_stats():
    stats = get_stats()
    stats["by_language"] = {}
    return stats
