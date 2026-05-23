"""Explainable TF-IDF term importance helpers."""

from src.preprocessing import preprocess_text


def _feature_names(vectorizer):
    if hasattr(vectorizer, "get_feature_names_out"):
        return vectorizer.get_feature_names_out()
    return vectorizer.get_feature_names()


def _linear_coefficients(model):
    if not hasattr(model, "coef_"):
        return None

    coefficients = model.coef_
    if getattr(coefficients, "ndim", 1) == 1:
        return coefficients
    if coefficients.shape[0] == 1:
        return coefficients[0]
    return coefficients[1] - coefficients[0]


def _nb_coefficients(model):
    if not hasattr(model, "feature_log_prob_"):
        return None

    feature_log_prob = model.feature_log_prob_
    if feature_log_prob.shape[0] < 2:
        return feature_log_prob[0]
    return feature_log_prob[1] - feature_log_prob[0]


def get_tfidf_word_importance(text, language, models, top_n=12):
    """Compute local TF-IDF term contributions using the saved model/vectorizer."""
    try:
        model = models.get(f"{language}_model")
        vectorizer = models.get(f"{language}_vectorizer")
        if model is None or vectorizer is None:
            return {"ok": False, "error": "Model or vectorizer is unavailable.", "terms": []}

        processed_text = preprocess_text(text or "", language)
        matrix = vectorizer.transform([processed_text])
        if matrix.nnz == 0:
            return {"ok": False, "error": "No known TF-IDF terms were found.", "terms": []}

        names = _feature_names(vectorizer)
        coefficients = _linear_coefficients(model)
        method = "linear_model_coefficients"
        if coefficients is None:
            coefficients = _nb_coefficients(model)
            method = "naive_bayes_log_probability_difference"

        feature_importances = getattr(model, "feature_importances_", None)
        rows = []
        coo = matrix.tocoo()
        for _, feature_index, tfidf_value in zip(coo.row, coo.col, coo.data):
            word = names[feature_index]
            if coefficients is not None:
                contribution = float(tfidf_value * coefficients[feature_index])
                direction = "Real-leaning" if contribution >= 0 else "Fake-leaning"
            elif feature_importances is not None:
                contribution = float(tfidf_value * feature_importances[feature_index])
                direction = "High model importance"
                method = "tree_feature_importance"
            else:
                contribution = float(tfidf_value)
                direction = "TF-IDF weight only"
                method = "tfidf_weight_fallback"

            rows.append(
                {
                    "term": word,
                    "impact": abs(contribution),
                    "signed_impact": contribution,
                    "tfidf": float(tfidf_value),
                    "direction": direction,
                }
            )

        rows.sort(key=lambda row: row["impact"], reverse=True)
        return {
            "ok": True,
            "method": method,
            "processed_text": processed_text,
            "terms": rows[:top_n],
        }
    except Exception as exc:
        return {"ok": False, "error": f"XAI explanation failed safely: {exc}", "terms": []}
