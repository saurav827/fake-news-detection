"""Lightweight trust and heuristic indicators for article text."""

import re


URGENCY_PHRASES = {
    "english": [
        "breaking",
        "urgent",
        "share now",
        "must read",
        "act now",
        "forward this",
        "do not ignore",
        "before it is deleted",
    ],
    "hindi": [
        "breaking",
        "urgent",
        "share",
        "forward",
        "abhi",
        "turant",
    ],
}

SUSPICIOUS_PHRASES = {
    "english": [
        "shocking truth",
        "secret plan",
        "media will not show",
        "doctors hate",
        "you will not believe",
        "viral claim",
        "anonymous sources",
    ],
    "hindi": [
        "viral",
        "shocking",
        "secret",
        "anonymous",
    ],
}

POSITIVE_WORDS = {
    "confirmed",
    "verified",
    "official",
    "evidence",
    "report",
    "announced",
    "approved",
    "support",
    "safe",
}

NEGATIVE_WORDS = {
    "shocking",
    "danger",
    "panic",
    "fake",
    "fraud",
    "scam",
    "hate",
    "threat",
    "exposed",
    "secret",
    "attack",
}


def _matches_phrases(text_lower, phrases):
    return [phrase for phrase in phrases if phrase in text_lower]


def _sentiment_summary(text):
    tokens = re.findall(r"[a-zA-Z]+", (text or "").lower())
    if not tokens:
        return {"label": "Neutral", "score": 0.0, "positive_hits": 0, "negative_hits": 0}

    positive_hits = sum(1 for token in tokens if token in POSITIVE_WORDS)
    negative_hits = sum(1 for token in tokens if token in NEGATIVE_WORDS)
    score = (positive_hits - negative_hits) / max(1, len(tokens))

    if score > 0.015:
        label = "Positive / factual tone"
    elif score < -0.015:
        label = "Negative / emotionally loaded tone"
    else:
        label = "Neutral"

    return {
        "label": label,
        "score": round(score, 4),
        "positive_hits": positive_hits,
        "negative_hits": negative_hits,
    }


def analyze_trust_signals(text, language="english"):
    """Return heuristic indicators only; these are not model predictions."""
    safe_text = text or ""
    text_lower = safe_text.lower()
    language = (language or "english").lower()

    signals = []
    words = re.findall(r"\b\w+\b", safe_text)
    latin_words = re.findall(r"\b[A-Za-z]{3,}\b", safe_text)
    all_caps_words = [word for word in latin_words if word.isupper()]
    all_caps_ratio = len(all_caps_words) / max(1, len(latin_words))

    if len(all_caps_words) >= 4 or all_caps_ratio >= 0.25:
        signals.append(
            {
                "signal": "Excessive ALL CAPS",
                "severity": "Medium",
                "detail": f"{len(all_caps_words)} uppercase words detected.",
            }
        )

    exclamation_count = safe_text.count("!")
    if exclamation_count >= 3 or re.search(r"!{2,}", safe_text):
        signals.append(
            {
                "signal": "Repeated exclamation marks",
                "severity": "Low",
                "detail": f"{exclamation_count} exclamation marks detected.",
            }
        )

    urgency_hits = _matches_phrases(text_lower, URGENCY_PHRASES.get(language, []))
    if urgency_hits:
        signals.append(
            {
                "signal": "Urgency language",
                "severity": "Medium",
                "detail": ", ".join(urgency_hits[:5]),
            }
        )

    suspicious_hits = _matches_phrases(text_lower, SUSPICIOUS_PHRASES.get(language, []))
    if suspicious_hits:
        signals.append(
            {
                "signal": "Suspicious wording",
                "severity": "Medium",
                "detail": ", ".join(suspicious_hits[:5]),
            }
        )

    sentiment = _sentiment_summary(safe_text)
    if sentiment["label"] != "Neutral":
        signals.append(
            {
                "signal": "Sentiment tone",
                "severity": "Info",
                "detail": sentiment["label"],
            }
        )

    return {
        "signals": signals,
        "summary": {
            "word_count": len(words),
            "all_caps_words": len(all_caps_words),
            "exclamation_count": exclamation_count,
            "sentiment": sentiment,
            "risk_indicator_count": len(signals),
        },
    }
