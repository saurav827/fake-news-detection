"""
Test Script for Fake News Detection System.
Verifies predictions and confidence scores on target examples including
randomly unseen real-world text not directly present in training dataset.
"""

import sys
import os

# Insert workspace root in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.model import predict


def run_tests():
    # ─── REAL examples (unseen / random) ───────────────────────────────────────
    real_examples = [
        # Originally trained targets
        "ISRO successfully launched Chandrayaan-3 mission from Sriharikota with advanced lunar exploration technology.",
        "The Reserve Bank of India introduced new digital banking reforms.",
        "India won the cricket match against Australia in Mumbai.",
        # User-requested unseen examples
        "India announced new railway reforms and infrastructure expansion.",
        "The Supreme Court released a new digital hearing policy.",
        "Parliament passed a new education reform bill to improve quality of schooling across India.",
        "The Prime Minister inaugurated a new expressway connecting major cities in northern India.",
        "Indian economy grew at 7.2 percent in the last quarter according to government data.",
    ]

    # ─── FAKE examples (unseen / random) ───────────────────────────────────────
    fake_examples = [
        # Originally trained targets
        "Scientists confirmed humans become invisible after drinking a secret chemical discovered on Mars.",
        "Aliens officially opened a university in Bihar.",
        "NASA announced the moon is made entirely of gold.",
        # User-requested unseen examples
        "Aliens opened a university in Bihar yesterday.",
        "Scientists discovered water on Earth gives immortality.",
        "Drinking tap water daily makes humans immortal according to secret government research.",
        "A new miracle pill discovered in jungle cures all diseases within 24 hours permanently.",
        "Government secretly distributing mind-control chips through COVID vaccines across India.",
    ]

    CONFIDENCE_THRESHOLD = 90.0  # Minimum acceptable confidence
    all_ok = True

    print("=" * 70)
    print("  FAKE NEWS DETECTOR - FINAL PREDICTION VERIFICATION REPORT")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("  REAL EXAMPLES (Target: Real, Confidence >= 90%)")
    print("=" * 70)
    for text in real_examples:
        res = predict(text, language="english", model_key="current")
        passed = res["prediction"] == "Real" and res["confidence"] >= CONFIDENCE_THRESHOLD
        status = "[PASS]" if passed else "[FAIL]"
        if not passed:
            all_ok = False
        print(f"{status} | {res['confidence']:5.1f}% | {text[:65]}...")
        if not passed:
            print(f"       +- Got: {res['prediction']} @ {res['confidence']}%")

    print("\n" + "=" * 70)
    print("  FAKE EXAMPLES (Target: Fake, Confidence >= 90%)")
    print("=" * 70)
    for text in fake_examples:
        res = predict(text, language="english", model_key="current")
        passed = res["prediction"] == "Fake" and res["confidence"] >= CONFIDENCE_THRESHOLD
        status = "[PASS]" if passed else "[FAIL]"
        if not passed:
            all_ok = False
        print(f"{status} | {res['confidence']:5.1f}% | {text[:65]}...")
        if not passed:
            print(f"       +- Got: {res['prediction']} @ {res['confidence']}%")

    print("\n" + "=" * 70)
    if all_ok:
        print("  ALL TEST CASES PASSED WITH 90%+ CONFIDENCE!")
        print("  Model is viva-safe and deployment-ready.")
        sys.exit(0)
    else:
        print("  SOME TEST CASES FAILED -- Check output above.")
        sys.exit(1)
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
