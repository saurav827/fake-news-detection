import unittest

from helpers.trust_signals import analyze_trust_signals
from helpers.url_analyzer import extract_article_text, is_valid_article_url
from research.dashboard import (
    best_model_summary,
    load_model_comparison_results,
    model_comparison_rows,
)


class ResearchHelperTests(unittest.TestCase):
    def test_invalid_url_fails_safely(self):
        self.assertFalse(is_valid_article_url("not-a-url"))
        result = extract_article_text("not-a-url")

        self.assertFalse(result["ok"])
        self.assertIn("error", result)

    def test_trust_signals_detect_caps_and_urgency(self):
        result = analyze_trust_signals("BREAKING!!! SHARE NOW this shocking claim", "english")

        self.assertGreaterEqual(result["summary"]["risk_indicator_count"], 1)
        self.assertGreaterEqual(result["summary"]["exclamation_count"], 3)

    def test_model_comparison_json_can_be_read(self):
        state = load_model_comparison_results()
        if not state.get("ok"):
            self.skipTest(state.get("error", "Comparison report unavailable"))

        report = state["report"]
        english_rows = model_comparison_rows(report, "english")
        hindi_best = best_model_summary(report, "hindi")

        self.assertTrue(english_rows)
        self.assertIn("model", hindi_best)
        self.assertIn("f1_score", hindi_best)


if __name__ == "__main__":
    unittest.main()
