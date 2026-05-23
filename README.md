# Multilingual Fake News Detection System

## Short Overview

A Streamlit-based machine learning web app that analyzes English and Hindi news text using preprocessing, TF-IDF features, and trained ML models.

This project is designed as an academic final-year demonstration. It helps users check whether a news statement is likely to be real or fake, while also showing confidence and probability details for better interpretation.

## Live Demo

The deployed Streamlit app is available here:

https://fake-news-detection-xu5z482pv3s9pp78yxpbpc.streamlit.app

## Features

- English and Hindi text support
- Fake/Real news prediction
- Confidence score
- Probability breakdown
- Detection tips
- Academic demo disclaimer
- Professional Streamlit UI
- 10+ traditional ML model comparison for research
- URL article text extraction that feeds the existing text predictor
- TF-IDF word importance view for explainability
- Trust and heuristic indicators for reviewer awareness
- JSON-backed research dashboard for dataset/model comparison
- Image/video upload prototype for future multimodal verification planning

## Tech Stack

- Python
- Streamlit
- scikit-learn
- TF-IDF
- Logistic Regression or trained ML classifier
- joblib/numpy
- HTML/CSS styling through Streamlit markdown

## Project Structure

```text
fake-news-detection/
|-- app.py
|-- backend/
|-- frontend/
|-- helpers/
|-- research/
|-- models/
|-- data/
|-- src/
|-- tests/
|-- screenshots/
|-- requirements.txt
|-- runtime.txt
|-- README.md
```

## Safe Modular Architecture

```text
User text or extracted URL article
        |
        v
Existing Streamlit input box
        |
        v
Existing preprocessing + saved TF-IDF vectorizer + saved sklearn model
        |
        v
Prediction result, confidence, XAI terms, and heuristic trust indicators

Research-only side modules:
helpers/url_analyzer.py       -> extracts article text safely
helpers/xai.py                -> reads existing vectorizer/model for term importance
helpers/trust_signals.py      -> informational heuristics only
research/dashboard.py         -> reads models/model_comparison_results.json
research/ml_enhancements.py   -> optional model availability list only
```

The deployed prediction path is preserved. New modules do not retrain models, do not overwrite `.pkl` files, and do not replace the active classifier automatically.

## Workflow

1. Enter text manually, or use the URL Article Analyzer to extract article text into the same input box.
2. Select English or Hindi so the existing saved language-specific artifacts are used.
3. Run the existing prediction pipeline.
4. Review confidence, probability, suspicious words, XAI term importance, and heuristic trust indicators.
5. Use the research dashboard to discuss dataset statistics and model comparison results during academic evaluation.

## How to Run Locally

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

Run the Streamlit app:

```powershell
streamlit run app.py
```

After the command starts successfully, open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Screenshots

The following screenshots are included for project demonstration:

- `screenshots/01_home_ui.png`
- `screenshots/02_input_section.png`
- `screenshots/03_real_result.png`
- `screenshots/04_fake_result.png`

## Dataset Sources

The project datasets are prepared from public fake-news datasets for academic research and demonstration.

- English dataset: WELFake public dataset from Kaggle.
- Hindi/Indian-compatible dataset: IFND, an Indian fake news dataset, used where labels are clearly marked as `true` or `fake`.

During import, labels are normalized to `fake` and `real`, empty or very short rows are removed, duplicate text rows are dropped, and class balancing is applied where possible. The prepared files are kept at a reasonable size for laptop usage and Streamlit-based demonstration:

- `data/english_news.csv`: maximum 5000 rows.
- `data/hindi_news.csv`: maximum 3000 rows.

The original downloaded zip files are kept under `data/external/`. Local backups of the previous project CSV files are saved as:

- `data/english_news_backup.csv`
- `data/hindi_news_backup.csv`

These datasets are used for academic/demo work only. Dataset quality, size, and label reliability directly affect model performance, so no real-world 100% accuracy is claimed.

## Model Explanation

The system uses a standard text classification pipeline for fake news detection.

First, the input news text is cleaned through text preprocessing. This includes basic cleaning steps such as removing unnecessary spaces, symbols, links, and other noisy text patterns that may affect model prediction.

After preprocessing, the cleaned text is converted into numerical features using TF-IDF vectorization. TF-IDF gives importance to words based on how frequently they appear in a text and how meaningful they are across the dataset.

The generated TF-IDF features are passed to a trained classification model, such as Logistic Regression or another saved machine learning classifier. The model predicts whether the entered news text is more likely to be Real or Fake.

The app also displays a confidence score and a probability breakdown so that the prediction can be interpreted more clearly. These values should be treated as a screening signal, not as final proof.

Separate saved artifacts are used for English and Hindi. Each language has its own trained model and vectorizer so the app can handle both language inputs more appropriately.

## Explainability and Trust Indicators

The app includes an XAI view based on the existing TF-IDF vectorizer and saved sklearn model. For compatible linear or Naive Bayes models, the app displays the most influential terms for the current prediction. For other sklearn models, it falls back safely to available TF-IDF or feature-importance information.

The trust indicator section checks simple reviewer signals such as excessive ALL CAPS, repeated exclamation marks, urgency language, suspicious wording, and lightweight sentiment tone. These indicators are informational only and are not treated as a separate fake-news classifier.

## URL Article Analyzer

The URL analyzer is a helper module that extracts readable article text with optional `newspaper3k` support and a BeautifulSoup/standard-library fallback. Invalid URLs, timeouts, non-HTML pages, and extraction failures are handled safely. Extracted text is copied into the existing Streamlit text input and then analyzed by the same deployed model pipeline.

## Model Comparison

The deployed Streamlit app remains stable because it continues to use the existing saved model and vectorizer artifacts for live prediction. The research comparison code is separate from the deployed prediction flow and does not automatically replace the working model files.

For academic evaluation, the project includes a safe comparison layer for 10+ traditional machine learning models:

- Logistic Regression
- Multinomial NB
- Complement NB
- Bernoulli NB
- Linear SVM
- SGD
- Passive Aggressive Classifier
- Random Forest
- Extra Trees
- Decision Tree
- KNN
- AdaBoost
- Gradient Boosting

All comparison models use TF-IDF vectorization on the existing English and Hindi CSV datasets. The comparison output is designed to be saved separately as `models/model_comparison_results.json`, including accuracy, precision, recall, F1-score, train/test split information, dataset size, and model status. If a research model fails during comparison, the script records it as `Failed` instead of replacing deployed files or stopping the whole comparison.

The Streamlit research dashboard reads `models/model_comparison_results.json` at runtime. If a confusion matrix is not stored in that JSON file, the dashboard clearly reports it as unavailable instead of retraining during deployment or inventing values.

### English Model Results

Dataset size: 25 samples  
Train/Test split: 20 training samples and 5 testing samples, using an 80/20 split.

| Model | Accuracy | Precision | Recall | F1-score |
| --- | ---: | ---: | ---: | ---: |
| Logistic Regression | 60.00% | 36.00% | 60.00% | 45.00% |
| Multinomial Naive Bayes | 60.00% | 36.00% | 60.00% | 45.00% |
| Linear SVM | 60.00% | 36.00% | 60.00% | 45.00% |
| Random Forest | 60.00% | 36.00% | 60.00% | 45.00% |
| Passive Aggressive Classifier | 60.00% | 36.00% | 60.00% | 45.00% |

English results are limited due to the very small dataset size.

### Hindi Model Results

Dataset size: 40 samples  
Train/Test split: 32 training samples and 8 testing samples, using an 80/20 split.

| Model | Accuracy | Precision | Recall | F1-score |
| --- | ---: | ---: | ---: | ---: |
| Logistic Regression | 62.50% | 63.33% | 62.50% | 61.90% |
| Multinomial Naive Bayes | 50.00% | 50.00% | 50.00% | 50.00% |
| Linear SVM | 62.50% | 63.33% | 62.50% | 61.90% |
| Random Forest | 62.50% | 78.57% | 62.50% | 56.36% |
| Passive Aggressive Classifier | 75.00% | 75.00% | 75.00% | 75.00% |

Best Hindi result: Passive Aggressive Classifier with 75.00% accuracy.

No 100% accuracy is guaranteed. The best model depends on dataset quality, dataset size, preprocessing, and the evaluation split. Results are for academic comparison only because the dataset is small.

These results are for academic comparison only because the dataset is small. Higher accuracy requires a larger verified dataset.

The project also identifies image and video fake news detection as future work only. Possible prototype modules include OCR-based text extraction from news screenshots, image manipulation detection, reverse image verification, video/deepfake detection, and multimodal detection using text + image + video. These features require larger verified multimodal datasets and are not implemented in the deployed version.

## Multimodal Prototype Scope

The text fake news detection model is implemented and remains the active deployed prediction feature. The app also includes a safe image/video upload prototype for final-year project presentation.

The upload prototype can accept image files (`png`, `jpg`, `jpeg`) and video files (`mp4`) to show file name, file type, file size, and a manual verification checklist. It does not classify uploaded media with a trained image or video model.

Planned multimodal checks include:

- File size category
- File type review
- Whether related news text was provided
- Source checking
- Date and author verification
- Reverse image search
- Metadata review
- Cross-checking with trusted sources

Real image/video fake news accuracy requires multimodal datasets and specialized models. This project does not claim image/video fake detection accuracy, and no model guarantees 100% real-world accuracy.

## Limitations

- The project uses a small academic sample dataset.
- The prediction is only a screening signal.
- The system is not a final fact-checking authority.
- Users should verify important news with trusted sources before making decisions.
- Real-world fake news detection requires larger verified datasets, regular updates, and expert review.

## Future Scope

- Use a larger verified dataset.
- Compare Naive Bayes, SVM, and Random Forest models.
- Add Passive Aggressive Classifier.
- Build a BERT/Transformer-based model.
- Add image/video verification only after collecting verified multimodal datasets and training real multimodal models.
- Develop a browser extension or mobile app.

## Deployment

The project can be deployed on Streamlit Cloud.

Recommended deployment settings:

- Main file path: `app.py`
- Dependency file: `requirements.txt`
- Python runtime file: `runtime.txt`
- Runtime version: `python-3.11.9`

Keep the trained model files inside the `models/` folder during deployment so the app can load the saved artifacts without retraining.

## Academic Disclaimer

This application is created for academic demonstration and learning purposes. It should not be used as the only source for judging whether real-world news is true or false. Users should always cross-check news from reliable and trusted sources.

The project should be presented ethically: predictions may be wrong, labels depend on dataset quality, and no result should be used to target a person, community, publisher, or political group without independent fact-checking.
