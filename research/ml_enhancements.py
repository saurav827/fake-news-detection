"""Optional sklearn-compatible research model candidates.

These helpers describe optional models only. They do not train models, save
artifacts, or replace the deployed prediction pipeline.
"""


def optional_boosting_candidates():
    candidates = []
    optional_imports = [
        ("XGBoost", "xgboost", "XGBClassifier"),
        ("LightGBM", "lightgbm", "LGBMClassifier"),
        ("CatBoost", "catboost", "CatBoostClassifier"),
    ]

    for display_name, module_name, class_name in optional_imports:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            status = "Available locally"
        except Exception:
            status = "Optional dependency not installed"

        candidates.append(
            {
                "Model": display_name,
                "Status": status,
                "Safety": "Research comparison only; never auto-replaces deployed .pkl files.",
            }
        )

    return candidates
