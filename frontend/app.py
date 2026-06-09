"""Simple Streamlit frontend for Fake News Detection."""

import os

import pandas as pd
import requests
import streamlit as st

from frontend.styles import apply_styles


API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

# Detect if we should fall back to in-process mode when local FastAPI is down
IN_PROCESS_MODE = False
try:
    response = requests.get(f"{API_URL}/", timeout=1.5)
    if response.status_code != 200:
        IN_PROCESS_MODE = True
except Exception:
    IN_PROCESS_MODE = True

if IN_PROCESS_MODE:
    from backend.model import predict as local_predict, get_available_models as local_get_available_models
    from backend.db import (
        get_history as local_get_history,
        get_stats as local_get_stats,
        save_prediction as local_save_prediction,
        init_db as _init_db,
    )
    # Auto-create DB + predictions table on first startup (critical for Streamlit Cloud)
    _init_db()


def get_error_message(response):
    """Get a readable error message from the API."""
    try:
        return response.json().get("detail", "Request failed")
    except Exception:
        return "Request failed. Please check the backend server."


def api_get(path):
    """Read data from FastAPI (or local DB if in-process)."""
    if not IN_PROCESS_MODE:
        response = requests.get(f"{API_URL}{path}", timeout=20)
        if response.status_code >= 400:
            raise RuntimeError(get_error_message(response))
        return response.json()
    else:
        # Standalone routing
        if path == "/":
            return {"status": "ok", "service": "Fake News Detection (In-Process)"}
        elif path == "/history":
            return local_get_history(50)
        elif path == "/stats":
            return local_get_stats()
        elif path.startswith("/models"):
            lang = "english"
            if "language=" in path:
                lang = path.split("language=")[-1].split("&")[0]
            return local_get_available_models(lang)
        raise RuntimeError(f"Endpoint not supported in-process: {path}")


def api_post(path, data):
    """Send prediction request to FastAPI (or predict locally if in-process)."""
    if not IN_PROCESS_MODE:
        response = requests.post(f"{API_URL}{path}", json=data, timeout=60)
        if response.status_code >= 400:
            raise RuntimeError(get_error_message(response))
        return response.json()
    else:
        # Standalone routing
        if path == "/predict":
            text = data.get("text", "")
            url = data.get("url", "")
            language = data.get("language", "english")
            model_key = data.get("model", "current")
            
            if url:
                from helpers.url_analyzer import extract_article_text
                article = extract_article_text(url)
                if not article.get("ok"):
                    raise RuntimeError(article.get("error", "URL extraction failed"))
                text = article["text"]
                
            if not text.strip():
                raise RuntimeError("Send text or a valid article URL.")
                
            res = local_predict(text, language, model_key)
            local_save_prediction(text[:5000], res["prediction"], res["confidence"])
            return res
            
        elif path == "/explain":
            from helpers.ai_explainer import generate_ai_explanation
            return generate_ai_explanation(
                data.get("text", ""),
                data.get("prediction", ""),
                data.get("confidence", 0.0),
                data.get("keywords", [])
            )
        raise RuntimeError(f"Endpoint not supported in-process: {path}")


def api_is_running():
    """Check if the backend is reachable."""
    if not IN_PROCESS_MODE:
        try:
            requests.get(f"{API_URL}/", timeout=1.5)
            return True
        except Exception:
            return False
    return True


def get_model_options(language):
    """Load trained model choices for dropdown."""
    try:
        models = api_get(f"/models?language={language}")
        options = {item["name"]: item["key"] for item in models}
        if "Current Saved Model" in options:
            ordered = {"Current Saved Model": options.pop("Current Saved Model")}
            ordered.update(dict(sorted(options.items())))
            return ordered
        return dict(sorted(options.items()))
    except Exception:
        return {"Current Saved Model": "current"}


def show_result(result):
    """Display prediction in a compact result box."""
    is_real = result["prediction"] == "Real"
    box_class = "result-real" if is_real else "result-fake"
    label = "✓ REAL NEWS" if is_real else "✗ FAKE NEWS"
    confidence = float(result["confidence"])

    st.markdown(
        f"""
        <div class="result-box {box_class}">
            <div class="result-title">{label}</div>
            <div class="result-info">
                <span><b>Confidence Score:</b> {confidence:.1f}%</span>
                <span>•</span>
                <span><b>Classification Model:</b> {result.get("model", "Saved Model")}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(min(confidence / 100, 1.0))

    keywords = result.get("keywords", [])
    if keywords:
        st.caption("📌 Keywords: " + ", ".join(keywords[:5]))
    else:
        st.caption("No strong keywords detected.")


def show_ai_explanation(text, result):
    """Show AI explanation button for prediction."""
    if st.button("📝 AI Explanation", use_container_width=True):
        with st.spinner("Generating..."):
            try:
                explanation = api_post(
                    "/explain",
                    {
                        "text": text,
                        "prediction": result["prediction"],
                        "confidence": result["confidence"],
                        "keywords": result.get("keywords", []),
                    },
                )
                if explanation.get("ok"):
                    st.info(explanation["explanation"])
                else:
                    st.warning("Explanation unavailable.")
            except Exception:
                st.warning("Could not generate explanation.")


def show_history():
    """Show recent prediction history - compact."""
    st.subheader("History", divider="gray")
    try:
        rows = api_get("/history")
        if not rows:
            st.info("No predictions yet.")
            return

        data = pd.DataFrame(rows)
        data["text"] = data["text"].str.slice(0, 100)
        data = data.rename(
            columns={
                "text": "Text",
                "result": "Result",
                "confidence": "Confidence",
                "timestamp": "Time",
            }
        )
        st.dataframe(data, use_container_width=True, height=300)
    except Exception as exc:
        st.warning(f"History unavailable: {exc}")


def show_stats():
    """Show simple project statistics - compact and clean."""
    st.subheader("Stats", divider="gray")
    try:
        stats = api_get("/stats")
        
        # Compact metrics row
        col1, col2, col3 = st.columns(3, gap="small")
        col1.metric("Total", stats["total"])
        col2.metric("Fake", stats["fake"])
        col3.metric("Real", stats["real"])

        # Compact chart
        if stats["total"] > 0:
            chart_data = pd.DataFrame(
                {"Count": [stats["fake"], stats["real"]]},
                index=["Fake", "Real"],
            )
            st.bar_chart(chart_data, height=160)
        else:
            st.caption("No predictions yet.")
    except Exception as exc:
        st.warning(f"Stats unavailable: {exc}")


def footer():
    st.markdown(
        "<div class='footer'>B.Tech Final Year Project | ML + Streamlit | TF-IDF + Logistic Regression</div>",
        unsafe_allow_html=True,
    )


def clear_inputs():
    """Clear input fields."""
    st.session_state["news_text"] = ""
    st.session_state["news_url"] = ""
    st.session_state.pop("last_prediction", None)
    st.session_state.pop("last_text", None)


def main():
    st.set_page_config(page_title="Fake News Detector", page_icon=":newspaper:", layout="wide")
    apply_styles()

    with st.sidebar:
        st.markdown("### Menu")
        page = st.radio("", ["Predict", "History", "Stats"], label_visibility="collapsed")
        st.divider()
        st.markdown("**API Status**", help="Backend connection check")
        if api_is_running():
            if IN_PROCESS_MODE:
                st.markdown(":green[✓ Connected (In-Process Mode)]")
            else:
                st.markdown(":green[✓ Connected (Local API)]")
        else:
            st.markdown(":red[✗ Not connected]")
        st.caption("Educational use only. Always verify with trusted sources.")

    st.markdown(
        """
        <div class="project-header">
            <span class="project-badge">Academic Project</span>
            <h1>Multilingual Fake News Detection System</h1>
            <p>An intelligent screening application to evaluate the credibility of news claims in English and Hindi using TF-IDF feature extraction and machine learning.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if page == "Predict":
        language = st.selectbox("Language", ["english", "hindi"])

        text = st.text_area(
            "News Text",
            height=150,
            placeholder="Paste headline or article text",
            key="news_text",
        )
        url = st.text_input("Article URL", placeholder="https://example.com", key="news_url")

        predict_clicked = st.button("Check News", type="primary", use_container_width=True)

        if predict_clicked:
            if not text.strip() and not url.strip():
                st.warning("Enter news text or URL.")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        result = api_post(
                            "/predict",
                            {
                                "text": text,
                                "url": url,
                                "language": language,
                            },
                        )
                        show_result(result)
                        st.session_state["last_prediction"] = result
                        st.session_state["last_text"] = text or url
                    except Exception as exc:
                        st.error(f"Error: {exc}")

        if st.session_state.get("last_prediction") and not predict_clicked:
            show_result(st.session_state["last_prediction"])

        st.divider()
        show_stats()

    elif page == "History":
        show_history()

    else:
        show_stats()

    footer()



if __name__ == "__main__":
    main()
