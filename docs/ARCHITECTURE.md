# System Architecture

The Fake News Detection System follows a standard 3-tier architecture.

## 1. Frontend (Streamlit)
- **Framework**: Streamlit
- **Language**: Python
- **Purpose**: Provides a clean, interactive user interface for inputting text/URLs and viewing predictions, history, and statistics.
- **Key Files**: `frontend/app.py`, `frontend/ui.py`, `frontend/styles.py`

## 2. Backend (FastAPI)
- **Framework**: FastAPI
- **Language**: Python
- **Purpose**: Serves as the API layer connecting the UI to the ML models. Handles requests, processes text, calls the model, and logs to SQLite.
- **Key Files**: `backend/main.py`, `backend/predictor.py`, `backend/db.py`

## 3. Database (SQLite)
- **Engine**: SQLite3
- **Purpose**: A lightweight file-based database (`database/predictions.db`) to store prediction history and metadata.

## 4. Machine Learning Pipeline
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Classification**: Logistic Regression (Default), with support for other scikit-learn classifiers.
- **Flow**: Text -> Preprocessing (cleaning) -> TF-IDF Vectorization -> ML Model Prediction -> Probability Thresholding -> Result.
- **Key Files**: `src/preprocessing.py`, `backend/model.py`, `models/*.pkl`

## Workflow Diagram

1. User enters text in **Streamlit UI**.
2. **UI** sends a POST request to **FastAPI `/predict`**.
3. **FastAPI** calls `backend.model.predict()`.
4. Text is cleaned via `src.preprocessing.preprocess_text()`.
5. Preprocessed text is vectorized using the pre-trained TF-IDF vectorizer.
6. The vector is passed to the ML model for classification.
7. Result and confidence score are saved to SQLite (`database/predictions.db`).
8. The result is returned to the UI and displayed to the user.
