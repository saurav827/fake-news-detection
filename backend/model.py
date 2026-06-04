"""Model loading and prediction helpers."""

from functools import lru_cache
from pathlib import Path
import re
import warnings

import joblib
import numpy as np

from src.preprocessing import highlight_suspicious_words, preprocess_text


ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"

MODEL_OPTIONS = {
    "current": "Current Saved Model",
    "logistic": "Logistic Regression",
    "multinomial_nb": "MultinomialNB",
    "bernoulli_nb": "BernoulliNB",
    "gaussian_nb": "GaussianNB",
    "random_forest": "Random Forest",
    "decision_tree": "Decision Tree",
    "extra_trees": "Extra Trees",
    "gradient_boosting": "Gradient Boosting",
    "adaboost": "AdaBoost",
    "svm": "SVM",
    "linear_svc": "LinearSVC",
    "knn": "KNN",
    "sgd": "SGD Classifier",
    "passive_aggressive": "Passive Aggressive",
    "ridge": "Ridge Classifier",
    "perceptron": "Perceptron",
    "bagging": "Bagging Classifier",
    "voting": "Voting Classifier",
    "stacking": "Stacking Classifier",
    "dummy": "Dummy Classifier",
}

DENSE_MODEL_KEYS = {"gaussian_nb", "gradient_boosting", "adaboost"}

# Threshold for classifying as Real (class 1). Lowering this value makes
# the model more willing to predict Real for legitimate-sounding text.
# 0.38 was chosen empirically to balance REAL vs FAKE predictions on
# short factual sentences that the model sees as borderline.
REAL_THRESHOLD = 0.38


@lru_cache(maxsize=1)
def load_models():
    """Load saved TF-IDF vectorizers and classifiers once per process."""
    loaded = {}
    for lang in ("english", "hindi"):
        model_path = MODELS / f"{lang}_model.pkl"
        vectorizer_path = MODELS / f"{lang}_vectorizer.pkl"
        if model_path.exists() and vectorizer_path.exists():
            loaded[lang] = {
                "model": joblib.load(model_path),
                "vectorizer": joblib.load(vectorizer_path),
            }
    if not loaded:
        raise FileNotFoundError("No saved model/vectorizer files found in models/")
    return loaded


def _optional_model_path(language, model_key):
    """Return saved optional model path if it exists."""
    paths = [MODELS / f"{language}_{model_key}.pkl"]
    if language == "english":
        paths.append(MODELS / f"{model_key}.pkl")
    for path in paths:
        if path.exists():
            return path
    return None


@lru_cache(maxsize=64)
def _load_optional_model(language, model_key):
    path = _optional_model_path(language, model_key)
    if not path:
        return None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            return joblib.load(path)
        except Exception:
            return None


def _is_compatible(model, feature_count):
    expected = getattr(model, "n_features_in_", None)
    return expected is None or expected == feature_count


def get_available_models(language="english"):
    """Return models that are ready to use for the selected language."""
    language = (language or "english").lower()
    models = load_models()
    if language not in models:
        return []

    feature_count = len(models[language]["vectorizer"].get_feature_names_out())
    choices = [{"key": "current", "name": MODEL_OPTIONS["current"]}]

    for key, name in MODEL_OPTIONS.items():
        if key == "current":
            continue
        model = _load_optional_model(language, key)
        if model is not None and _is_compatible(model, feature_count):
            choices.append({"key": key, "name": name})
    return choices


def _probabilities(model, matrix):
    if hasattr(model, "predict_proba"):
        return model.predict_proba(matrix)[0]
    if hasattr(model, "decision_function"):
        score = np.ravel(model.decision_function(matrix))[0]
        real = 1 / (1 + np.exp(-score))
        return np.array([1 - real, real])
    return np.array([0.5, 0.5])


def _top_terms(vectorizer, matrix, limit=6):
    try:
        names = vectorizer.get_feature_names_out()
        row = matrix.toarray()[0]
        indexes = row.argsort()[::-1]
        return [names[i] for i in indexes if row[i] > 0][:limit]
    except Exception:
        return []


def extract_keywords(text, language, vectorizer=None, matrix=None):
    """Return simple keyword explanation from suspicious words + TF-IDF terms."""
    suspicious = highlight_suspicious_words(text, language)
    tfidf_terms = _top_terms(vectorizer, matrix) if vectorizer is not None else []
    keywords = []
    for word in suspicious + tfidf_terms:
        word = re.sub(r"\s+", " ", str(word)).strip()
        if word and word.lower() not in {k.lower() for k in keywords}:
            keywords.append(word)
    return keywords[:8]


def predict(text, language="english", model_key="logistic"):
    """Predict Fake/Real using existing TF-IDF + saved model logic.

    Uses Logistic Regression by default with a tuned probability threshold
    so that legitimate news text is not always classified as Fake.
    """
    language = (language or "english").lower()
    model_key = (model_key or "logistic").lower()
    if model_key not in MODEL_OPTIONS:
        model_key = "logistic"
    models = load_models()
    if language not in models:
        raise ValueError(f"Unsupported language: {language}")

    clean = (text or "").strip()
    if len(clean) < 5:
        raise ValueError("Please provide at least 5 characters of news text.")

    bundle = models[language]
    processed = preprocess_text(clean, language)
    matrix = bundle["vectorizer"].transform([processed])

    # Try to load the requested model; fall back to the saved default
    selected_model = bundle["model"]
    if model_key != "current":
        optional = _load_optional_model(language, model_key)
        if optional is not None and _is_compatible(optional, matrix.shape[1]):
            selected_model = optional
        elif model_key != "logistic":
            # If an explicitly requested model is missing, report the error
            raise ValueError("Selected model is not trained yet. Run train_models.py first.")
        # else: logistic not found → silently use the saved default model

    model_matrix = matrix.toarray() if model_key in DENSE_MODEL_KEYS else matrix
    probs = _probabilities(selected_model, model_matrix)

    # Threshold-based classification for balanced predictions
    classes = list(getattr(selected_model, "classes_", [0, 1]))
    real_idx = classes.index(1) if 1 in classes else 1
    real_prob = float(probs[real_idx]) if real_idx < len(probs) else 0.5
    label = 1 if real_prob >= REAL_THRESHOLD else 0

    confidence = float(max(real_prob, 1.0 - real_prob) * 100)

    return {
        "prediction": "Real" if label == 1 else "Fake",
        "confidence": round(confidence, 2),
        "keywords": extract_keywords(clean, language, bundle["vectorizer"], matrix),
        "model": MODEL_OPTIONS.get(model_key, model_key),
        "model_key": model_key,
    }
