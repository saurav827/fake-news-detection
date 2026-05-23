"""Utilities for reading saved model comparison reports safely."""

import json
import os


DEFAULT_REPORT_PATH = os.path.join("models", "model_comparison_results.json")


def load_model_comparison_results(path=DEFAULT_REPORT_PATH):
    """Load the saved research comparison JSON without retraining anything."""
    try:
        if not os.path.exists(path):
            return {"ok": False, "error": f"Comparison report not found: {path}"}
        with open(path, "r", encoding="utf-8") as report_file:
            return {"ok": True, "report": json.load(report_file), "path": path}
    except Exception as exc:
        return {"ok": False, "error": f"Could not load comparison report: {exc}"}


def get_language_report(report, language):
    return (report or {}).get("languages", {}).get(language, {})


def dataset_stats(report, language):
    language_report = get_language_report(report, language)
    return language_report.get("dataset", {})


def model_comparison_rows(report, language):
    """Return sorted model metric rows for Streamlit tables."""
    language_report = get_language_report(report, language)
    best_model = language_report.get("best_model_by_f1_score", "")
    rows = []
    for model_name, metrics in language_report.get("models", {}).items():
        rows.append(
            {
                "Model": model_name,
                "Status": metrics.get("status", "Unknown"),
                "Accuracy": _percent(metrics.get("accuracy")),
                "Precision": _percent(metrics.get("precision")),
                "Recall": _percent(metrics.get("recall")),
                "F1-score": _percent(metrics.get("f1_score")),
                "Best": "Yes" if model_name == best_model else "",
                "_accuracy_value": _number(metrics.get("accuracy")),
                "_f1_value": _number(metrics.get("f1_score")),
            }
        )

    rows.sort(key=lambda row: row["_f1_value"], reverse=True)
    return rows


def chart_metric_rows(report, language):
    rows = []
    for row in model_comparison_rows(report, language):
        rows.append(
            {
                "Model": row["Model"],
                "Accuracy": round(row["_accuracy_value"] * 100, 2),
                "F1-score": round(row["_f1_value"] * 100, 2),
            }
        )
    return rows


def best_model_summary(report, language):
    language_report = get_language_report(report, language)
    best_model = language_report.get("best_model_by_f1_score", "Not available")
    metrics = language_report.get("models", {}).get(best_model, {})
    return {
        "model": best_model,
        "accuracy": _percent(metrics.get("accuracy")),
        "f1_score": _percent(metrics.get("f1_score")),
        "note": language_report.get("academic_note", ""),
    }


def confusion_matrix(report, language):
    """Return a stored confusion matrix only if the JSON contains one."""
    language_report = get_language_report(report, language)
    return language_report.get("confusion_matrix") or language_report.get("best_confusion_matrix")


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _percent(value):
    if value is None:
        return "N/A"
    return f"{_number(value) * 100:.2f}%"
