"""Simple Streamlit frontend for Fake News Detection."""

import os

import pandas as pd
import requests
import streamlit as st

from frontend.styles import apply_styles


API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")


def get_error_message(response):
    """Get a readable error message from the API."""
    try:
        return response.json().get("detail", "Request failed")
    except Exception:
        return "Request failed. Please check the backend server."


def api_get(path):
    """Read data from FastAPI."""
    response = requests.get(f"{API_URL}{path}", timeout=20)
    if response.status_code >= 400:
        raise RuntimeError(get_error_message(response))
    return response.json()


def api_post(path, data):
    """Send prediction request to FastAPI."""
    response = requests.post(f"{API_URL}{path}", json=data, timeout=60)
    if response.status_code >= 400:
        raise RuntimeError(get_error_message(response))
    return response.json()


def api_is_running():
    """Check if the backend is reachable."""
    try:
        api_get("/")
        return True
    except Exception:
        return False


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
    """Display prediction in a clear result box."""
    is_real = result["prediction"] == "Real"
    box_class = "result-real" if is_real else "result-fake"
    label = "Real News" if is_real else "Fake News"
    confidence = float(result["confidence"])

    st.markdown(
        f"""
        <div class="result-box {box_class}">
            <div class="result-title">{label}</div>
            <div>Confidence: <b>{confidence:.2f}%</b></div>
            <div>Model: <b>{result.get("model", "Current Saved Model")}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(min(confidence / 100, 1.0))

    keywords = result.get("keywords", [])
    if keywords:
        st.info("Keywords: " + ", ".join(keywords))
    else:
        st.info("No strong keywords found.")


def show_history():
    """Show recent prediction history."""
    st.subheader("Prediction History")
    try:
        rows = api_get("/history")
        if not rows:
            st.info("No predictions yet.")
            return

        data = pd.DataFrame(rows)
        data["text"] = data["text"].str.slice(0, 120)
        data = data.rename(
            columns={
                "text": "News Text",
                "result": "Result",
                "confidence": "Confidence",
                "timestamp": "Time",
            }
        )
        st.dataframe(data, use_container_width=True)
    except Exception as exc:
        st.warning(f"Could not load history: {exc}")


def show_stats():
    """Show simple project statistics."""
    st.subheader("Project Stats")
    try:
        stats = api_get("/stats")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", stats["total"])
        col2.metric("Fake", stats["fake"])
        col3.metric("Real", stats["real"])

        chart = pd.DataFrame(
            {"Count": [stats["fake"], stats["real"]]},
            index=["Fake", "Real"],
        )
        if stats["total"] > 0:
            st.markdown("<div class='chart-title'>Result Chart</div>", unsafe_allow_html=True)
            st.bar_chart(chart)
        else:
            st.info("No chart data yet. Run a prediction first.")
    except Exception as exc:
        st.warning(f"Could not load stats: {exc}")


def footer():
    st.markdown(
        "<div class='footer'>Final year project demo | FastAPI + Streamlit + SQLite + TF-IDF model</div>",
        unsafe_allow_html=True,
    )


def clear_inputs():
    """Clear input fields."""
    st.session_state["news_text"] = ""
    st.session_state["news_url"] = ""


def main():
    st.set_page_config(page_title="Fake News Detector", page_icon=":newspaper:", layout="wide")
    apply_styles()

    with st.sidebar:
        st.title("Menu")
        page = st.radio("Go to", ["Predict", "History", "Stats"], label_visibility="collapsed")
        st.divider()
        st.caption("Backend API")
        st.code(API_URL)
        if api_is_running():
            st.markdown("<span class='status-ok'>Backend connected</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='status-bad'>Backend not connected</span>", unsafe_allow_html=True)
        st.caption("This app is for educational use. Always verify important news.")

    st.title("Fake News Detection")
    st.markdown(
        "<p class='small-note'>Paste news text or an article URL and check it using the saved ML model.</p>",
        unsafe_allow_html=True,
    )

    if page == "Predict":
        lang_col, model_col = st.columns([1, 2])
        language = lang_col.selectbox("Language", ["english", "hindi"])
        model_options = get_model_options(language)
        selected_model = model_col.selectbox("ML Model", list(model_options.keys()))
        model_col.caption(f"Available models: {len(model_options)}")
        text = st.text_area(
            "News Text",
            height=180,
            placeholder="Paste headline or article text here",
            key="news_text",
        )
        url = st.text_input("Article URL", placeholder="https://example.com/news", key="news_url")

        col1, col2 = st.columns([1, 1])
        predict_clicked = col1.button("Check News", type="primary", use_container_width=True)
        col2.button("Clear", use_container_width=True, on_click=clear_inputs)

        if predict_clicked:
            if not text.strip() and not url.strip():
                st.warning("Please enter news text or a URL.")
            else:
                with st.spinner("Checking news..."):
                    try:
                        result = api_post(
                            "/predict",
                            {
                                "text": text,
                                "url": url,
                                "language": language,
                                "model": model_options[selected_model],
                            },
                        )
                        show_result(result)
                    except Exception as exc:
                        st.error(f"Prediction failed: {exc}")

        st.divider()
        show_stats()

    elif page == "History":
        show_history()

    else:
        show_stats()

    footer()


if __name__ == "__main__":
    main()
