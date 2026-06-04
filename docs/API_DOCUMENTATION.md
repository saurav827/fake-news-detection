# Fake News Detection API

The backend is built with **FastAPI** and provides predictions via REST endpoints.

## Base URL
`http://localhost:8000` (or the deployed URL)

---

## Endpoints

### 1. Predict News (`POST /predict`)
Predicts whether a given news text or article URL is Real or Fake.

**Request Body (JSON):**
```json
{
  "text": "The government announced a new infrastructure project.",
  "url": null,
  "language": "english",
  "model": "logistic"
}
```

**Response (JSON):**
```json
{
  "prediction": "Real",
  "confidence": 85.5,
  "keywords": ["government", "infrastructure", "project"],
  "model": "Logistic Regression",
  "model_key": "logistic"
}
```

---

### 2. Get Prediction History (`GET /history`)
Returns the last `limit` predictions stored in the database.

**Query Parameters:**
- `limit` (int, default: 50): Number of records to return.

**Response (JSON):**
```json
[
  {
    "text": "The government announced a new infrastructure project.",
    "result": "Real",
    "confidence": 85.5,
    "timestamp": "2026-06-03 14:32:00"
  }
]
```

---

### 3. Get Statistics (`GET /stats`)
Returns the total counts of predictions.

**Response (JSON):**
```json
{
  "total": 150,
  "fake": 45,
  "real": 105
}
```
