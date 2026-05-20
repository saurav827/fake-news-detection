"""
Streamlit Web Application for Multilingual Fake News Detection System.

Run with: streamlit run app.py
"""

import streamlit as st

from backend.model_loader import load_models
from backend.predictor import predict_fake_news
from config import DEMO_WARNING, LANGUAGES, UI_CONFIG
from frontend.styles import apply_premium_styles
from frontend.ui import (
    render_disclaimer,
    render_detection_guide,
    render_footer,
    render_header,
    render_results,
    render_sidebar,
)


NEWS_TEXT_KEY = "news_text_input"


def clear_news_text():
    """Clear the current input text from Streamlit session state."""
    st.session_state[NEWS_TEXT_KEY] = ""


def main():
    """Run the Streamlit application."""
    st.set_page_config(
        page_title=UI_CONFIG["page_title"],
        page_icon=UI_CONFIG["page_icon"],
        layout=UI_CONFIG["layout"],
        initial_sidebar_state=UI_CONFIG["initial_sidebar_state"],
    )

    apply_premium_styles()

    render_header()
    render_disclaimer(DEMO_WARNING)

    confidence_threshold = render_sidebar()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            "<div class='section-title'>News Input</div>"
            "<div class='info-box'>Paste a news headline, short claim, or article excerpt. "
            "Select the matching language so the correct saved model is used for analysis.</div>",
            unsafe_allow_html=True,
        )

        with st.form("prediction_form"):
            language = st.radio(
                "Language Selection",
                options=[language.capitalize() for language in LANGUAGES],
                horizontal=True,
            )
            language_code = language.lower()

            news_text = st.text_area(
                "News Input Box",
                height=200,
                placeholder="Paste the news text here for analysis...",
                label_visibility="collapsed",
                key=NEWS_TEXT_KEY,
            )

            button_col1, button_col2 = st.columns([1, 1])
            with button_col1:
                check_button = st.form_submit_button(
                    "Check News",
                    use_container_width=True,
                    type="primary",
                )
            with button_col2:
                clear_button = st.form_submit_button(
                    "Clear Text",
                    use_container_width=True,
                    type="secondary",
                    on_click=clear_news_text,
                )

    with col2:
        render_detection_guide()

    if clear_button:
        st.info("Input cleared. Enter fresh text to run another screening.")

    elif check_button and news_text.strip():
        models = load_models()

        if models is None or f"{language_code}_model" not in models:
            st.error(f"{language} model files were not found.")
            st.info("Keep the saved model and vectorizer files inside the models folder.")
            return

        with st.spinner("Analyzing news..."):
            result = predict_fake_news(news_text, language_code, models)

        if result:
            render_results(result, models, language_code, confidence_threshold, news_text)
        else:
            st.error("Error making prediction. Please try again.")

    elif check_button and not news_text.strip():
        st.warning("Please enter some news text before checking.")

    render_footer()


if __name__ == "__main__":
    main()
