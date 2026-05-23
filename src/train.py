"""
Safe research training script for the Multilingual Fake News Detection System.

This script compares traditional machine learning models on the existing
English and Hindi CSV datasets. It is intended for academic comparison only.

Important safety behavior:
- It does not overwrite deployed model files such as english_model.pkl,
  hindi_model.pkl, english_vectorizer.pkl, or hindi_vectorizer.pkl.
- It saves comparison metrics separately in models/model_comparison_results.json.
- Optional research model artifacts use clear research_* filenames.
"""

import argparse
import math
import os
import sys
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import (
    AdaBoostClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import (
    LogisticRegression,
    PassiveAggressiveClassifier,
    SGDClassifier,
)
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model_utils import save_model_comparison_results
from preprocessing import preprocess_text

warnings.filterwarnings("ignore")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
RANDOM_STATE = 42
SMALL_DATASET_LIMIT = 1000


class FakeNewsResearchComparison:
    """Train and compare research models without changing deployed artifacts."""

    def __init__(self, language="english", max_features=5000):
        self.language = language
        self.max_features = max_features
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=2,
            max_df=0.8,
            ngram_range=(1, 2),
            stop_words="english" if language == "english" else None,
        )
        self.models = {
            "Logistic Regression": LogisticRegression(
                max_iter=1000,
                random_state=RANDOM_STATE,
            ),
            "Multinomial NB": MultinomialNB(),
            "Complement NB": ComplementNB(),
            "Bernoulli NB": BernoulliNB(),
            "Linear SVM": LinearSVC(random_state=RANDOM_STATE),
            "SGD": SGDClassifier(max_iter=1000, random_state=RANDOM_STATE, tol=1e-3),
            "Passive Aggressive Classifier": PassiveAggressiveClassifier(
                max_iter=1000,
                random_state=RANDOM_STATE,
                tol=1e-3,
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=100,
                random_state=RANDOM_STATE,
            ),
            "Extra Trees": ExtraTreesClassifier(
                n_estimators=100,
                random_state=RANDOM_STATE,
            ),
            "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE),
            "KNN": KNeighborsClassifier(n_neighbors=3),
            "AdaBoost": AdaBoostClassifier(random_state=RANDOM_STATE),
            "Gradient Boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
        }
        self.trained_models = {}
        self.comparison_results = {}
        self.split_info = {}

    def load_data(self, csv_file):
        """Load text and labels from a project CSV dataset."""
        print(f"\nLoading {self.language} dataset from {csv_file}...")
        df = pd.read_csv(csv_file)

        if "label" not in df.columns:
            raise ValueError(f"{csv_file} must contain a 'label' column.")

        if "title" in df.columns and "text" in df.columns:
            full_text = df["title"].fillna("") + " " + df["text"].fillna("")
        elif "text" in df.columns:
            full_text = df["text"].fillna("")
        else:
            raise ValueError(f"{csv_file} must contain a 'text' column.")

        texts = full_text.astype(str).values
        labels = df["label"].values
        print(f"Loaded {len(texts)} samples")
        return texts, labels

    def preprocess_data(self, texts):
        """Apply the project preprocessing pipeline to all texts."""
        print(f"Preprocessing {len(texts)} texts for {self.language}...")
        processed_texts = []

        for text in texts:
            if pd.isna(text) or str(text).strip() == "":
                processed_texts.append("")
            else:
                processed_texts.append(preprocess_text(str(text), self.language))

        print("Preprocessing complete.")
        return processed_texts

    def _get_class_distribution(self, labels):
        unique_labels, counts = np.unique(labels, return_counts=True)
        return {
            str(label): int(count)
            for label, count in zip(unique_labels, counts)
        }

    def _can_stratify(self, labels, test_size):
        unique_labels, counts = np.unique(labels, return_counts=True)
        if len(unique_labels) < 2 or np.any(counts < 2):
            return False

        total_samples = len(labels)
        test_count = math.ceil(total_samples * test_size)
        train_count = total_samples - test_count
        return test_count >= len(unique_labels) and train_count >= len(unique_labels)

    def train_and_compare(self, texts, labels, test_size=0.2):
        """Train each research model and return comparison metrics."""
        if len(texts) < 2:
            raise ValueError("At least two samples are required for train/test comparison.")

        print("\n" + "=" * 68)
        print(f"RESEARCH MODEL COMPARISON FOR {self.language.upper()}")
        print("=" * 68)

        labels = np.asarray(labels)
        stratify_labels = labels if self._can_stratify(labels, test_size) else None

        X_train, X_test, y_train, y_test = train_test_split(
            texts,
            labels,
            test_size=test_size,
            random_state=RANDOM_STATE,
            stratify=stratify_labels,
        )

        print("Converting texts to TF-IDF vectors...")
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        print(f"TF-IDF train matrix shape: {X_train_tfidf.shape}")

        self.split_info = {
            "total_samples": int(len(texts)),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "test_size": test_size,
            "random_state": RANDOM_STATE,
            "stratified_split": stratify_labels is not None,
            "class_distribution": self._get_class_distribution(labels),
            "small_dataset_warning": (
                "Results are for academic comparison only because the dataset is small."
                if len(texts) < SMALL_DATASET_LIMIT
                else ""
            ),
        }

        for model_name, model in self.models.items():
            print(f"Training {model_name}...")
            try:
                model.fit(X_train_tfidf, y_train)
                y_pred = model.predict(X_test_tfidf)

                self.trained_models[model_name] = model
                self.comparison_results[model_name] = {
                    "status": "Success",
                    "accuracy": float(accuracy_score(y_test, y_pred)),
                    "precision": float(
                        precision_score(
                            y_test,
                            y_pred,
                            average="weighted",
                            zero_division=0,
                        )
                    ),
                    "recall": float(
                        recall_score(
                            y_test,
                            y_pred,
                            average="weighted",
                            zero_division=0,
                        )
                    ),
                    "f1_score": float(
                        f1_score(
                            y_test,
                            y_pred,
                            average="weighted",
                            zero_division=0,
                        )
                    ),
                }
            except Exception as exc:
                print(f"{model_name} failed: {exc}")
                self.comparison_results[model_name] = {
                    "status": "Failed",
                    "accuracy": None,
                    "precision": None,
                    "recall": None,
                    "f1_score": None,
                    "error": str(exc),
                }

        return self.build_report()

    def build_report(self):
        """Build a serializable report for this language."""
        successful_results = {
            name: metrics
            for name, metrics in self.comparison_results.items()
            if metrics.get("status") == "Success"
        }
        best_by_f1 = (
            max(successful_results, key=lambda name: successful_results[name]["f1_score"])
            if successful_results
            else None
        )

        return {
            "language": self.language,
            "dataset": self.split_info,
            "tfidf": {
                "max_features": self.max_features,
                "min_df": self.vectorizer.min_df,
                "max_df": self.vectorizer.max_df,
                "ngram_range": list(self.vectorizer.ngram_range),
                "fitted_features": int(len(self.vectorizer.get_feature_names_out())),
            },
            "metric_average": "weighted",
            "models": self.comparison_results,
            "best_model_by_f1_score": best_by_f1,
            "academic_note": (
                "No 100% accuracy is guaranteed. The best model depends on dataset "
                "quality, dataset size, preprocessing, and evaluation split."
            ),
        }

    def save_research_artifacts(self, model_dir=MODELS_DIR):
        """Save optional research artifacts with separate non-deployment names."""
        os.makedirs(model_dir, exist_ok=True)

        vectorizer_path = os.path.join(
            model_dir,
            f"research_{self.language}_tfidf_vectorizer.pkl",
        )
        joblib.dump(self.vectorizer, vectorizer_path)
        print(f"Research vectorizer saved: {vectorizer_path}")

        for model_name, model in self.trained_models.items():
            safe_name = (
                model_name.lower()
                .replace("/", "")
                .replace(" ", "_")
                .replace("-", "_")
            )
            model_path = os.path.join(
                model_dir,
                f"research_{self.language}_{safe_name}.pkl",
            )
            joblib.dump(model, model_path)
            print(f"Research model saved: {model_path}")


def run_language_comparison(language, csv_filename, args):
    csv_path = os.path.join(DATA_DIR, csv_filename)
    if not os.path.exists(csv_path):
        print(f"Dataset not found: {csv_path}. Skipping {language}.")
        return None

    comparison = FakeNewsResearchComparison(
        language=language,
        max_features=args.max_features,
    )
    texts, labels = comparison.load_data(csv_path)
    processed_texts = comparison.preprocess_data(texts)
    report = comparison.train_and_compare(
        processed_texts,
        labels,
        test_size=args.test_size,
    )

    if args.save_research_artifacts:
        comparison.save_research_artifacts()

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Safely compare traditional ML models for fake news detection."
    )
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--max-features", type=int, default=5000)
    parser.add_argument(
        "--save-research-artifacts",
        action="store_true",
        help="Optionally save research_* model files without replacing deployed models.",
    )
    args = parser.parse_args()

    print("\n" + "=" * 68)
    print("MULTILINGUAL FAKE NEWS DETECTION SYSTEM")
    print("Safe Research Model Comparison")
    print("=" * 68)
    print("Deployment model files will not be overwritten by this script.\n")

    report = {
        "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "purpose": "Academic comparison of 10+ sklearn text models using existing CSV datasets and TF-IDF features.",
        "safety_note": (
            "This report is separate from deployed prediction artifacts. Existing "
            "english_model.pkl, hindi_model.pkl, english_vectorizer.pkl, and "
            "hindi_vectorizer.pkl are not replaced."
        ),
        "future_multimodal_prototype_plan": [
            "Image upload prototype for png, jpg, and jpeg files",
            "Video upload prototype for mp4 files",
            "OCR-based text extraction from news screenshots",
            "Image manipulation detection",
            "Reverse image verification",
            "Video/deepfake detection",
            "Multimodal detection using text + image + video",
        ],
        "languages": {},
    }

    language_files = {
        "english": "english_news.csv",
        "hindi": "hindi_news.csv",
    }

    for language, csv_filename in language_files.items():
        language_report = run_language_comparison(language, csv_filename, args)
        if language_report:
            report["languages"][language] = language_report

    output_path = save_model_comparison_results(report)

    print("\nModel comparison complete.")
    print(f"Comparison report saved separately: {output_path}")
    print("Original deployed model files were not overwritten.")
    print("=" * 68 + "\n")


if __name__ == "__main__":
    main()
