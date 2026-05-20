import unittest

from backend.model_loader import load_models
from backend.predictor import predict_fake_news


class PredictorTests(unittest.TestCase):
    def test_predict_fake_news_returns_expected_fields(self):
        models = load_models()
        if not models or "english_model" not in models:
            self.skipTest("English model files are not available")

        result = predict_fake_news(
            "Government officials announced a new public health policy today.",
            "english",
            models,
        )

        self.assertIsInstance(result, dict)
        self.assertIn("prediction", result)
        self.assertIn("confidence", result)
        self.assertIn("fake_probability", result)
        self.assertIn("real_probability", result)
        self.assertGreaterEqual(result["confidence"], 0)
        self.assertLessEqual(result["confidence"], 100)

    def test_predict_fake_news_returns_none_for_missing_language_model(self):
        result = predict_fake_news("Some news text", "marathi", {})

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
