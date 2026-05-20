# Multilingual Fake News Detection System

## Short Overview

A Streamlit-based machine learning web app that analyzes English and Hindi news text using preprocessing, TF-IDF features, and trained ML models.

This project is designed as an academic final-year demonstration. It helps users check whether a news statement is likely to be real or fake, while also showing confidence and probability details for better interpretation.

## Features

- English and Hindi text support
- Fake/Real news prediction
- Confidence score
- Probability breakdown
- Detection tips
- Academic demo disclaimer
- Professional Streamlit UI

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
|-- models/
|-- data/
|-- src/
|-- tests/
|-- screenshots/
|-- requirements.txt
|-- runtime.txt
|-- README.md
```

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

## Model Explanation

The system uses a standard text classification pipeline for fake news detection.

First, the input news text is cleaned through text preprocessing. This includes basic cleaning steps such as removing unnecessary spaces, symbols, links, and other noisy text patterns that may affect model prediction.

After preprocessing, the cleaned text is converted into numerical features using TF-IDF vectorization. TF-IDF gives importance to words based on how frequently they appear in a text and how meaningful they are across the dataset.

The generated TF-IDF features are passed to a trained classification model, such as Logistic Regression or another saved machine learning classifier. The model predicts whether the entered news text is more likely to be Real or Fake.

The app also displays a confidence score and a probability breakdown so that the prediction can be interpreted more clearly. These values should be treated as a screening signal, not as final proof.

Separate saved artifacts are used for English and Hindi. Each language has its own trained model and vectorizer so the app can handle both language inputs more appropriately.

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
- Add image/video fake news detection.
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
