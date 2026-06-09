"""
Test Script for Fake News Detection System.
Verifies predictions and confidence scores on target examples.
"""

import sys
import os

# Insert workspace root in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.model import predict

def run_tests():
    real_examples = [
        "ISRO successfully launched Chandrayaan-3 mission from Sriharikota with advanced lunar exploration technology.",
        "The Reserve Bank of India introduced new digital banking reforms.",
        "India won the cricket match against Australia in Mumbai."
    ]

    fake_examples = [
        "Scientists confirmed humans become invisible after drinking a secret chemical discovered on Mars.",
        "Aliens officially opened a university in Bihar.",
        "NASA announced the moon is made entirely of gold."
    ]

    print("=" * 60)
    print("TESTING REAL EXAMPLES (Target: Real, Confidence: 90% - 99%)")
    print("=" * 60)
    all_ok = True
    for text in real_examples:
        res = predict(text, language="english", model_key="current")
        print(f"Text: {text}")
        print(f"Prediction: {res['prediction']} | Confidence: {res['confidence']}% | Model: {res['model']}")
        if res["prediction"] != "Real" or res["confidence"] < 90.0:
            print(">>> [FAIL] Target expectations not met!")
            all_ok = False
        else:
            print("[PASS]")
        print("-" * 60)

    print("=" * 60)
    print("TESTING FAKE EXAMPLES (Target: Fake, Confidence: 90% - 99%)")
    print("=" * 60)
    for text in fake_examples:
        res = predict(text, language="english", model_key="current")
        print(f"Text: {text}")
        print(f"Prediction: {res['prediction']} | Confidence: {res['confidence']}% | Model: {res['model']}")
        if res["prediction"] != "Fake" or res["confidence"] < 90.0:
            print(">>> [FAIL] Target expectations not met!")
            all_ok = False
        else:
            print("[PASS]")
        print("-" * 60)

    if all_ok:
        print("\nALL TARGET TEST CASES PASSED WITH 90%+ CONFIDENCE!")
        sys.exit(0)
    else:
        print("\nSOME TEST CASES FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
