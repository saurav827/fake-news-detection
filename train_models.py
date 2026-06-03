"""Train optional ML models using the existing TF-IDF vectorizers."""

from pathlib import Path
import os
import warnings

import joblib
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, StackingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier, Perceptron
from sklearn.linear_model import RidgeClassifier, SGDClassifier
from sklearn.dummy import DummyClassifier
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier

from backend.model import MODEL_OPTIONS
from src.preprocessing import preprocess_text


ROOT = Path(__file__).resolve().parent
MODELS = ROOT / "models"
DATA = ROOT / "data"
MAX_ROWS = int(os.getenv("TRAIN_MAX_ROWS", "1200"))
SKIP_EXISTING = os.getenv("RETRAIN_MODELS", "0") != "1"


def optional_models():
    """Return model objects. Missing optional libraries are skipped."""
    return {
        "logistic": LogisticRegression(max_iter=1000),
        "multinomial_nb": MultinomialNB(),
        "bernoulli_nb": BernoulliNB(),
        "gaussian_nb": GaussianNB(),
        "random_forest": RandomForestClassifier(n_estimators=40, random_state=42),
        "decision_tree": DecisionTreeClassifier(random_state=42),
        "extra_trees": ExtraTreesClassifier(n_estimators=40, random_state=42),
        "gradient_boosting": GradientBoostingClassifier(random_state=42),
        "adaboost": AdaBoostClassifier(random_state=42),
        "svm": SVC(kernel="linear", random_state=42),
        "linear_svc": LinearSVC(random_state=42),
        "knn": KNeighborsClassifier(n_neighbors=5),
        "sgd": SGDClassifier(loss="log_loss", max_iter=1000, random_state=42),
        "passive_aggressive": PassiveAggressiveClassifier(max_iter=1000, random_state=42),
        "ridge": RidgeClassifier(),
        "perceptron": Perceptron(max_iter=1000, random_state=42),
        "bagging": BaggingClassifier(random_state=42),
        "voting": VotingClassifier(
            estimators=[
                ("lr", LogisticRegression(max_iter=1000)),
                ("nb", MultinomialNB()),
                ("dt", DecisionTreeClassifier(random_state=42)),
            ]
        ),
        "stacking": StackingClassifier(
            estimators=[
                ("lr", LogisticRegression(max_iter=1000)),
                ("nb", MultinomialNB()),
            ],
            final_estimator=LogisticRegression(max_iter=1000),
        ),
        "dummy": DummyClassifier(strategy="most_frequent"),
    }


def load_data(language):
    """Read news CSV and convert labels to 0/1."""
    path = DATA / f"{language}_news.csv"
    df = pd.read_csv(path).dropna(subset=["text", "label"]).head(MAX_ROWS)
    title = df["title"].fillna("").astype(str) if "title" in df else ""
    text = (title + " " + df["text"].fillna("").astype(str)).astype(str)
    y = df["label"].astype(str).str.lower().map({"fake": 0, "real": 1})
    valid = y.notna()
    return text[valid].tolist(), y[valid].astype(int).to_numpy()


def train_language(language):
    """Train all working optional models for one language."""
    vectorizer = joblib.load(MODELS / f"{language}_vectorizer.pkl")
    texts, y = load_data(language)
    processed = [preprocess_text(text, language) for text in texts]
    x_sparse = vectorizer.transform(processed)
    x_dense = None

    print(f"\nTraining {language} models on {len(y)} rows", flush=True)
    for key, model in optional_models().items():
        output_path = MODELS / f"{language}_{key}.pkl"
        if SKIP_EXISTING and output_path.exists():
            print(f"Already saved {MODEL_OPTIONS[key]}", flush=True)
            continue

        try:
            x_train = x_sparse
            if key in {"gaussian_nb", "gradient_boosting", "adaboost"}:
                x_dense = x_dense if x_dense is not None else x_sparse.toarray()
                x_train = x_dense

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model.fit(x_train, y)

            joblib.dump(model, output_path)
            if language == "english":
                joblib.dump(model, MODELS / f"{key}.pkl")
            print(f"Saved {MODEL_OPTIONS[key]}", flush=True)
        except Exception as exc:
            print(f"Skipped {MODEL_OPTIONS.get(key, key)}: {exc}", flush=True)


def main():
    MODELS.mkdir(exist_ok=True)
    for language in ("english", "hindi"):
        if (DATA / f"{language}_news.csv").exists() and (MODELS / f"{language}_vectorizer.pkl").exists():
            train_language(language)


if __name__ == "__main__":
    main()
