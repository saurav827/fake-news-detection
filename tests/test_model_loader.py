import os
import unittest

from backend.model_loader import load_models


class ModelLoaderTests(unittest.TestCase):
    def test_load_models_returns_saved_models(self):
        required_files = [
            "models/english_model.pkl",
            "models/english_vectorizer.pkl",
            "models/hindi_model.pkl",
            "models/hindi_vectorizer.pkl",
        ]
        missing_files = [path for path in required_files if not os.path.exists(path)]
        if missing_files:
            self.skipTest(f"Missing saved model files: {missing_files}")

        models = load_models()

        self.assertIsInstance(models, dict)
        self.assertIn("english_model", models)
        self.assertIn("english_vectorizer", models)
        self.assertIn("hindi_model", models)
        self.assertIn("hindi_vectorizer", models)


if __name__ == "__main__":
    unittest.main()
