import unittest

from src.preprocessing import preprocess_text


class PreprocessingTests(unittest.TestCase):
    def test_english_preprocessing_removes_noise(self):
        text = "This is FAKE news!!! Visit https://example.com now."

        processed = preprocess_text(text, "english")

        self.assertIn("fake", processed)
        self.assertIn("news", processed)
        self.assertNotIn("https", processed)
        self.assertNotIn("example", processed)

    def test_hindi_preprocessing_runs_without_downloads(self):
        text = "यह झूठी खबर है। https://example.com देखें।"

        processed = preprocess_text(text, "hindi")

        self.assertIsInstance(processed, str)
        self.assertNotIn("https", processed)


if __name__ == "__main__":
    unittest.main()
