import os, sys
sys.path.append(os.getcwd())
from backend.database import init_db, insert_prediction, fetch_predictions, fetch_stats

init_db()
insert_prediction('Test news', 'FAKE NEWS ✗', 'english')
print('Predictions:', fetch_predictions())
print('Stats:', fetch_stats())
