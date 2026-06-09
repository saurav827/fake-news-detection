# B.Tech Project Viva Preparation Guide
## Project: Multilingual Fake News Detection System using Machine Learning

This guide contains essential technical details, architecture overview, and typical questions that examiners ask during project reviews.

---

### 1. Key Project Architecture
- **Backend**: FastAPI (Python). Provides high-performance, asynchronous REST endpoints (`/predict`, `/history`, `/stats`, `/models`).
- **Frontend**: Streamlit. Light and clean sidebar navigation, simple prediction text area, prediction history dataframes, and a stats dashboard.
- **Database**: SQLite (`database/predictions.db`). A lightweight relational database that stores the prediction logs (text, result, confidence, timestamp).
- **Core ML Pipeline**:
  1. **Preprocessing**: Lowercasing, cleaning URLs/HTML tags/emojis, removing punctuation, filtering stopwords, and Snowball Stemming (for English).
  2. **Feature Extraction**: TF-IDF Vectorizer (`models/vectorizer.pkl`) with n-gram range (1, 2) and sublinear TF scaling.
  3. **Classification**: Linear SVM and SGD Classifiers (calibrated to output stable probabilities) selected as the best lightweight models.

---

### 2. Common Viva Questions & Answers

#### Q1: Why did you choose Support Vector Machines (SVM) / SGD Classifier over Deep Learning models (like LSTM or BERT)?
**Answer**: Deep learning models are computationally heavy, require GPUs for fast inference, and generate large model files (often hundreds of megabytes). For a lightweight, beginner-friendly system that runs on standard laptops during demonstrations, traditional ML models (like Linear SVM or Logistic Regression) combined with TF-IDF are fast (inference < 10ms), resource-efficient, and still achieve high accuracy (93%-95%+).

#### Q2: What is TF-IDF? How does it work?
**Answer**: TF-IDF stands for **Term Frequency-Inverse Document Frequency**. It is a numerical statistic intended to reflect how important a word is to a document in a collection or corpus.
- **Term Frequency (TF)**: Number of times a word appears in a document / total words in document.
- **Inverse Document Frequency (IDF)**: Log(total documents / documents containing the word).
- **TF-IDF Score**: $TF \times IDF$. High score means a word is frequent in the current text but rare across other texts, indicating high semantic importance.

#### Q3: Why did you use `CalibratedClassifierCV`?
**Answer**: Traditional classifiers like SVM or Passive Aggressive find a decision boundary but do not naturally output probabilities (confidence scores). `CalibratedClassifierCV` wraps the classifier and uses cross-validation (with Platt scaling or Isotonic regression) to output well-calibrated class probabilities, which we display as the "prediction confidence".

#### Q4: How did you clean the dataset?
**Answer**: 
1. Removed duplicates and rows with missing text/labels.
2. Normalized labels (mapped various formats of `true`/`1` to `1` and `false`/`0` to `0`).
3. Cleaned text by stripping HTML tags, emojis, emails, and URLs.
4. Balanced the dataset to have an equal number of fake and real samples (50/50 split) to prevent bias.

#### Q5: How does the multilingual aspect work?
**Answer**: We train separate models and vectorizers for English (`best_model.pkl` and `vectorizer.pkl`) and Hindi (`hindi_model.pkl` and `hindi_vectorizer.pkl`). Depending on the language selected in the dropdown, the backend routes the text through the correct preprocessing function and loads the corresponding language model artifacts.

---

### 3. Quick Command Summary for Examiners
1. **To run the backend**:
   `python -m uvicorn backend.main:app --reload`
2. **To run the frontend**:
   `streamlit run app.py`
3. **App URL**: `http://localhost:8501`
