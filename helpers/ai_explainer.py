"""Optional AI explanation helper using OpenRouter free model."""

import os

import requests


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openrouter/free"


def is_ai_explainer_enabled():
    """Return True only when the optional API key is configured."""
    return bool(os.getenv("OPENROUTER_API_KEY"))


def _build_prompt(text, prediction, confidence, keywords):
    keyword_text = ", ".join(keywords or []) or "No keywords returned by model"
    short_text = (text or "").strip()[:1800]
    return f"""
Explain this fake news detection result in simple student-project language.

Prediction: {prediction}
Confidence: {confidence}%
Model keywords: {keyword_text}
News text:
{short_text}

Give 3 to 5 short bullet points covering:
- why it may be predicted as fake or real
- suspicious keywords
- emotional language
- possible misleading patterns

Do not claim the result is final proof. Keep it concise.
""".strip()


def generate_ai_explanation(text, prediction, confidence, keywords=None):
    """Generate an optional explanation without changing the ML prediction."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {
            "ok": False,
            "enabled": False,
            "explanation": "",
            "message": "AI explanation skipped because OPENROUTER_API_KEY is not set.",
        }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You explain ML fake news predictions clearly and cautiously.",
            },
            {
                "role": "user",
                "content": _build_prompt(text, prediction, confidence, keywords),
            },
        ],
        "temperature": 0.3,
        "max_tokens": 220,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        return {
            "ok": True,
            "enabled": True,
            "model": OPENROUTER_MODEL,
            "explanation": content,
        }
    except Exception as exc:
        return {
            "ok": False,
            "enabled": True,
            "explanation": "",
            "message": f"AI explanation failed safely: {exc}",
        }
