"""FastAPI app for Fake News Detection."""

from typing import Optional

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.db import get_history, get_stats, init_db, save_prediction
from backend.model import get_available_models, predict
from helpers.url_analyzer import extract_article_text


class PredictRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    language: str = "english"
    model: str = "current"
    selected_model: Optional[str] = None


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(title="Fake News Detection API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "service": "Fake News Detection API"}


@app.post("/predict")
def predict_news(payload: PredictRequest):
    text = (payload.text or "").strip()

    if payload.url:
        article = extract_article_text(payload.url)
        if not article.get("ok"):
            raise HTTPException(status_code=400, detail=article.get("error", "URL extraction failed"))
        text = article["text"]

    if not text:
        raise HTTPException(status_code=400, detail="Send text or a valid article URL.")

    try:
        result = predict(text, payload.language, payload.selected_model or payload.model)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    save_prediction(text[:5000], result["prediction"], result["confidence"])
    return result


@app.get("/history")
def history(limit: int = 50):
    return get_history(limit)


@app.get("/models")
def models(language: str = "english"):
    return get_available_models(language)


@app.get("/stats")
def stats():
    return get_stats()
