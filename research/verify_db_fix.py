"""
DB Fix Verification Script.
Simulates a fresh Streamlit Cloud deployment with no existing database.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simulate fresh deployment: remove existing DB
db_path = os.path.join("database", "predictions.db")
if os.path.exists(db_path):
    os.remove(db_path)
    print("Deleted existing DB to simulate fresh Streamlit Cloud container...")

from backend.db import init_db, save_prediction, get_history, get_stats

print("Step 1: Calling init_db()...")
init_db()
print("  init_db() success - table created from scratch")

print("Step 2: Saving test predictions...")
save_prediction("Aliens opened a university in Bihar yesterday.", "Fake", 95.0)
save_prediction("ISRO launched Chandrayaan-3 successfully from Sriharikota.", "Real", 97.3)
save_prediction("Scientists say water gives immortality.", "Fake", 95.0)
print("  save_prediction() x3 success")

print("Step 3: Reading history...")
h = get_history()
print("  History rows:", len(h))

print("Step 4: Reading stats...")
s = get_stats()
print("  Stats => total={}, fake={}, real={}".format(s["total"], s["fake"], s["real"]))

print()
if s["total"] == 3 and s["fake"] == 2 and s["real"] == 1 and len(h) == 3:
    print("ALL CHECKS PASSED - DB fix is working correctly!")
    print("Deployment is safe. Streamlit Cloud will auto-create the DB on startup.")
    sys.exit(0)
else:
    print("FAIL - unexpected result")
    sys.exit(1)
