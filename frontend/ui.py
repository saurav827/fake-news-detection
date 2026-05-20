import streamlit as st

from config import THRESHOLDS


def render_header():
    """Render the main header of the application."""
    st.markdown(
        """
        <div class="main-header">
            <div class="header-kicker">Final Year Machine Learning Project</div>
            <h1>Multilingual Fake News Detection System</h1>
            <p>
                An academic demonstration that analyzes English and Hindi news text
                using preprocessing, TF-IDF features, and trained machine learning models.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer(message):
    """Render the project disclaimer as a styled warning card."""
    st.markdown(
        f"""
        <div class="disclaimer-card">
            <strong>Academic Demo Disclaimer</strong>
            <p>{message}</p>
            <p>This output is a screening result for demonstration and should not be treated as a final fact-checking authority.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render the sidebar with about info and settings."""
    with st.sidebar:
        st.header("Project Overview")
        st.write(
            """
            This system estimates whether a news statement is likely to be real
            or fake. It is built for academic demonstration, viva discussion,
            and quick model inference from saved training artifacts.

            **Core components**
            - English and Hindi text support
            - Text cleaning and feature extraction
            - Saved ML models for fast prediction
            - Confidence and probability display

            **Demo flow**
            1. Enter or paste news text.
            2. Select the language.
            3. Click **Check News**.
            4. Review the result with confidence.
            """
        )

        st.markdown("---")
        st.header("Review Setting")
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=THRESHOLDS["confidence_min"],
            max_value=THRESHOLDS["confidence_max"],
            value=THRESHOLDS["confidence_default"],
            help="Predictions below this level should be reviewed more carefully.",
        )
        return confidence_threshold


def render_detection_guide():
    """Render a compact guide for interpreting news quality."""
    st.markdown(
        """
        <div class="guide-card">
            <h3>Detection Tips</h3>
            <p>Use the model result as a first screening signal, then compare it with reliable sources.</p>
            <h4>Warning signs</h4>
            <ul>
                <li>Sensational or emotionally loaded wording</li>
                <li>Missing author, date, or source details</li>
                <li>Claims that cannot be verified elsewhere</li>
                <li>Unusual formatting, spelling, or grammar issues</li>
            </ul>
            <h4>Stronger credibility signs</h4>
            <ul>
                <li>Clear attribution and factual reporting</li>
                <li>Consistent details across trusted sources</li>
                <li>Balanced tone without exaggerated claims</li>
                <li>Transparent evidence or official references</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _progress_value(value):
    return max(0, min(100, int(round(value))))


def render_results(result, models, language_code, confidence_threshold, news_text):
    """Render the prediction results."""
    st.markdown("<div class='section-title'>Result Display</div>", unsafe_allow_html=True)

    result_class = "real-news-box" if result["is_real"] else "fake-news-box"
    result_label = "Likely Real News" if result["is_real"] else "Likely Fake News"
    result_note = (
        "For this demo screening, the text pattern is closer to the real-news examples learned by the model."
        if result["is_real"]
        else "For this demo screening, the text pattern is closer to the fake-news examples learned by the model."
    )
    st.markdown(
        f"""
        <div class="{result_class}">
            <div class="result-label">{result_label}</div>
            <div class="result-caption">Confidence score: {result["confidence"]:.1f}%</div>
            <div class="result-helper">{result_note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-subtitle'>Confidence Overview</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Overall Confidence", f"{result['confidence']:.1f}%")
    with col2:
        st.metric("Fake Probability", f"{result['fake_probability']:.1f}%")
    with col3:
        st.metric("Real Probability", f"{result['real_probability']:.1f}%")

    st.markdown("<div class='section-subtitle'>Probability Breakdown</div>", unsafe_allow_html=True)
    st.write(f"**Real News Probability:** {result['real_probability']:.1f}%")
    st.progress(_progress_value(result["real_probability"]))

    st.write(f"**Fake News Probability:** {result['fake_probability']:.1f}%")
    st.progress(_progress_value(result["fake_probability"]))

    if result["confidence"] < confidence_threshold:
        st.warning(
            f"Confidence is below the selected threshold ({confidence_threshold}%). "
            "Please verify this news with trusted sources before relying on it."
        )

    if result["suspicious_words"]:
        keywords_str = ", ".join(f"<strong>{word}</strong>" for word in result["suspicious_words"])
        st.markdown(
            f"""
            <div class="suspicious-keywords">
                <strong>Suspicious keywords detected:</strong> {keywords_str}
                <p>These words can appear in misleading news, but they should be verified with context.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Advanced Details"):
        st.write("**Original Text Length:**", len(news_text), "characters")
        st.write("**Processed Text Length:**", len(result["processed_text"]), "characters")
        st.write("**Language Used:**", language_code.capitalize())

        stats_key = f"{language_code}_stats"
        if stats_key in models:
            stats = models[stats_key]
            best_model_name = stats.get("best_model", "Logistic Regression")
            accuracy = stats.get("test_accuracy", 0) * 100
            st.write(f"**ML Model Used:** {best_model_name}")
            st.write(f"**Model Accuracy:** {accuracy:.2f}%")

        if st.checkbox("Show preprocessed text"):
            st.text_area("Preprocessed Text:", result["processed_text"], height=100)


def render_footer():
    """Render the application footer."""
    st.markdown("---")
    st.markdown(
        """
        <div class="footer">
            <p><strong>Multilingual Fake News Detection System</strong></p>
            <p>Prepared as a B.Tech CSE final-year academic project for demonstration and evaluation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
