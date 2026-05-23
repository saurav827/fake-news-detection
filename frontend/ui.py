import streamlit as st

from config import THRESHOLDS
from helpers.trust_signals import analyze_trust_signals
from helpers.url_analyzer import extract_article_text
from helpers.xai import get_tfidf_word_importance
from research.dashboard import (
    best_model_summary,
    chart_metric_rows,
    confusion_matrix,
    dataset_stats,
    load_model_comparison_results,
    model_comparison_rows,
)
from research.ml_enhancements import optional_boosting_candidates


def render_header():
    """Render the main header of the application."""
    st.markdown(
        """
        <div class="main-header">
            <div class="header-topline">
                <div class="header-kicker">Final Year Machine Learning Project</div>
                <div class="header-status">Deployed Streamlit App</div>
            </div>
            <h1>Multilingual Fake News Detection System</h1>
            <p>
                An academic demonstration that analyzes English and Hindi news text
                using preprocessing, TF-IDF features, and trained machine learning models.
            </p>
            <div class="header-meta">
                <span>English and Hindi</span>
                <span>TF-IDF Features</span>
                <span>ML Classification</span>
                <span>Confidence Review</span>
            </div>
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


def render_project_workflow():
    """Render the top-level workflow for the app."""
    st.markdown(
        """
        <div class="workflow-section">
            <div class="section-heading">
                <h2>Project Workflow</h2>
                <p>A simple screening flow for academic demonstration and viva discussion.</p>
            </div>
            <div class="workflow-grid">
                <div class="workflow-step">
                    <span class="step-number">Step 1</span>
                    <strong>Enter news text</strong>
                    <p>Paste a headline, claim, or short article excerpt.</p>
                </div>
                <div class="workflow-step">
                    <span class="step-number">Step 2</span>
                    <strong>Select language</strong>
                    <p>Choose English or Hindi so the matching model is used.</p>
                </div>
                <div class="workflow-step">
                    <span class="step-number">Step 3</span>
                    <strong>Run prediction</strong>
                    <p>Submit the text for preprocessing, TF-IDF, and classification.</p>
                </div>
                <div class="workflow-step">
                    <span class="step-number">Step 4</span>
                    <strong>Review output</strong>
                    <p>Check confidence, probabilities, and credibility tips.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards():
    """Render concise feature cards for the project capabilities."""
    st.markdown(
        """
        <div class="feature-section">
            <div class="feature-card">
                <span class="feature-tag implemented">Implemented</span>
                <h3>Text Detection</h3>
                <p>Supports English and Hindi news text through separate saved artifacts.</p>
            </div>
            <div class="feature-card">
                <span class="feature-tag research">Implemented for research</span>
                <h3>10+ Model Comparison</h3>
                <p>Compares traditional sklearn models using TF-IDF and the current datasets.</p>
            </div>
            <div class="feature-card">
                <span class="feature-tag future">Prototype</span>
                <h3>Image Upload</h3>
                <p>Accepts image files for a future verification workflow preview.</p>
            </div>
            <div class="feature-card">
                <span class="feature-tag future">Prototype</span>
                <h3>Video Upload</h3>
                <p>Accepts MP4 files for prototype media-review checklist display.</p>
            </div>
            <div class="feature-card">
                <span class="feature-tag future">Future Scope</span>
                <h3>Multimodal Detection</h3>
                <p>Planned combination of text, media checks, and source credibility.</p>
            </div>
            <div class="feature-card">
                <span class="feature-tag implemented">Implemented</span>
                <h3>Deployed web app</h3>
                <p>Runs as a Streamlit application suitable for project demonstration.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render the sidebar with about info and settings."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-panel">
                <h2>Project Overview</h2>
                <p>
                    A text-based fake news screening system built for final-year
                    academic demonstration and external viva.
                </p>
                <div class="sidebar-list">
                    <span>English and Hindi support</span>
                    <span>Text cleaning and TF-IDF</span>
                    <span>Saved ML model inference</span>
                    <span>Confidence and probability display</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("<div class='sidebar-heading'>Review Setting</div>", unsafe_allow_html=True)
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=THRESHOLDS["confidence_min"],
            max_value=THRESHOLDS["confidence_max"],
            value=THRESHOLDS["confidence_default"],
            help="Predictions below this level should be reviewed more carefully.",
        )
        return confidence_threshold


def render_url_article_analyzer(text_session_key):
    """Render a safe URL extractor that fills the existing news input box."""
    with st.expander("URL Article Analyzer"):
        st.caption(
            "Paste an article URL to extract readable text, then reuse the existing text prediction pipeline."
        )
        url = st.text_input(
            "Article URL",
            placeholder="https://example.com/news/article",
            key="article_url_input",
        )
        analyze_url = st.button("Extract Article Text", width="stretch")

        if analyze_url:
            with st.spinner("Extracting article text safely..."):
                result = extract_article_text(url)

            if result.get("ok"):
                st.session_state[text_session_key] = result["text"]
                st.success("Article text extracted and copied into the news input box.")
                metric_cols = st.columns(3)
                metric_cols[0].metric("Words", result.get("word_count", 0))
                metric_cols[1].metric("Characters", result.get("char_count", 0))
                metric_cols[2].metric("Extractor", result.get("source", "Safe parser"))
                if result.get("title"):
                    st.markdown(f"**Article title:** {result['title']}")
                st.text_area(
                    "Extracted preview",
                    value=result["text"][:1500],
                    height=160,
                    disabled=True,
                )
            else:
                st.warning(result.get("error", "Could not extract article text from this URL."))


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


def render_advanced_research_scope():
    """Render JSON-backed research comparison and future scope."""
    st.divider()
    st.subheader("Advanced Research Dashboard")
    st.caption("Saved comparison results are loaded from JSON. No retraining or model replacement is performed here.")

    report_state = load_model_comparison_results()
    if not report_state.get("ok"):
        st.warning(report_state.get("error", "Research comparison report is unavailable."))
        return

    report = report_state["report"]
    tab_overview, tab_english, tab_hindi, tab_confusion, tab_optional = st.tabs(
        ["Overview", "English", "Hindi", "Confusion Matrix", "Optional ML"]
    )

    with tab_overview:
        st.markdown("**Research file**")
        st.code(report_state.get("path", "models/model_comparison_results.json"))
        st.info(report.get("safety_note", "Research results are separate from deployed artifacts."))
        overview_cols = st.columns(2)
        for column, language in zip(overview_cols, ["english", "hindi"]):
            with column:
                best = best_model_summary(report, language)
                stats = dataset_stats(report, language)
                st.markdown(f"**{language.capitalize()} best model by F1-score**")
                st.metric(best["model"], best["f1_score"], help=best["note"])
                st.caption(
                    f"Dataset: {stats.get('total_samples', 'N/A')} samples, "
                    f"{stats.get('train_samples', 'N/A')} train, "
                    f"{stats.get('test_samples', 'N/A')} test."
                )

    for selected_tab, language in [(tab_english, "english"), (tab_hindi, "hindi")]:
        with selected_tab:
            stats = dataset_stats(report, language)
            metric_cols = st.columns(4)
            metric_cols[0].metric("Total Samples", stats.get("total_samples", "N/A"))
            metric_cols[1].metric("Train Samples", stats.get("train_samples", "N/A"))
            metric_cols[2].metric("Test Samples", stats.get("test_samples", "N/A"))
            metric_cols[3].metric("Test Size", stats.get("test_size", "N/A"))

            class_distribution = stats.get("class_distribution", {})
            st.caption(
                f"Class distribution: fake={class_distribution.get('fake', 'N/A')}, "
                f"real={class_distribution.get('real', 'N/A')}"
            )

            best = best_model_summary(report, language)
            st.success(
                f"Best {language.capitalize()} model by F1-score: {best['model']} "
                f"(Accuracy {best['accuracy']}, F1 {best['f1_score']})."
            )

            rows = model_comparison_rows(report, language)
            display_rows = [
                {key: value for key, value in row.items() if not key.startswith("_")}
                for row in rows
            ]
            st.dataframe(display_rows, width="stretch", hide_index=True)

            chart_rows = chart_metric_rows(report, language)
            if chart_rows:
                try:
                    import pandas as pd

                    chart_frame = pd.DataFrame(chart_rows).set_index("Model")
                    st.bar_chart(chart_frame[["Accuracy", "F1-score"]])
                except Exception:
                    st.table(chart_rows)

    with tab_confusion:
        st.caption("A confusion matrix is displayed only when it is stored in the saved JSON report.")
        for language in ["english", "hindi"]:
            st.markdown(f"**{language.capitalize()} confusion matrix**")
            matrix = confusion_matrix(report, language)
            if matrix:
                st.table(matrix)
            else:
                st.info(
                    "No confusion matrix is stored in the current comparison JSON. "
                    "The app will not retrain models during deployment to generate one."
                )

    with tab_optional:
        st.caption(
            "Optional boosting models can be evaluated in a separate research script. "
            "They are never used to replace deployed models automatically."
        )
        st.dataframe(optional_boosting_candidates(), width="stretch", hide_index=True)

    with st.expander("Why not 100% accuracy?"):
        st.markdown(
            """
            - Fake news detection depends on dataset quality.
            - Real-world news changes over time.
            - Small academic datasets have limited generalization.
            - Larger verified datasets and transformer/multimodal models can improve performance.
            - No model should be treated as a final fact-checking authority.
            """
        )


def _file_size_category(size_bytes):
    """Return a simple non-ML file size category for prototype review."""
    size_mb = size_bytes / (1024 * 1024)
    if size_mb < 2:
        return "Small"
    if size_mb <= 20:
        return "Medium"
    return "Large"


def _render_uploaded_media_details(uploaded_file, related_text_available):
    """Show safe media metadata and manual verification checklist."""
    file_type = uploaded_file.type or "Unknown type"
    file_size_kb = uploaded_file.size / 1024
    size_category = _file_size_category(uploaded_file.size)

    st.success(
        "Prototype upload received. This version does not perform real image/video fake detection yet."
    )
    st.markdown(f"**File name:** {uploaded_file.name}")
    st.markdown(f"**File type:** {file_type}")
    st.markdown(f"**File size:** {file_size_kb:.2f} KB")
    st.markdown(f"**File size category:** {size_category}")
    st.markdown(
        f"**Related news text provided:** {'Yes' if related_text_available else 'No'}"
    )
    st.markdown(
        """
        **Prototype risk checklist**
        - Verify the original source.
        - Check publication date and context.
        - Confirm author or publisher details.
        - Use reverse image search for reused media.
        - Review metadata if available.
        - Cross-check the claim with trusted news sources.
        """
    )


def render_multimodal_prototype_scope(news_text="", text_result=None):
    """Render planned multimodal scope with native Streamlit components."""
    st.divider()
    st.subheader("Multimodal Prototype Scope")
    st.caption(
        "Planned image and video support is shown as future scope only. The deployed version does not perform real image/video fake news detection."
    )

    multimodal_cols = st.columns(4)
    multimodal_cards = [
        (
            "News screenshot analysis prototype",
            "Future idea: OCR can extract text from news screenshots and send extracted text to the text model.",
        ),
        (
            "Image verification prototype",
            "Future idea: reverse image search, metadata check, and manipulation detection can help identify misleading images.",
        ),
        (
            "Video/deepfake verification prototype",
            "Future idea: video frame analysis, audio mismatch detection, metadata review, and deepfake models can be added later.",
        ),
        (
            "Multimodal fake news detection",
            "Future idea: combine text + image + video + source credibility score for stronger verification.",
        ),
    ]

    for column, (title, description) in zip(multimodal_cols, multimodal_cards):
        with column:
            st.markdown(f"**{title}**")
            st.markdown(description)
            st.caption("Future scope only")

    st.info(
        "This is a multimodal prototype. Uploaded media is not classified by a trained image/video model in this version."
    )
    st.markdown("**Optional upload UI mockup**")
    st.caption(
        "This uploader demonstrates the planned workflow only. Uploaded files are not analyzed in this version."
    )

    image_file = st.file_uploader(
        "Image upload prototype",
        type=["png", "jpg", "jpeg"],
        help="Prototype only. This version does not analyze image content.",
        key="prototype_image_upload",
    )
    video_file = st.file_uploader(
        "Video upload prototype",
        type=["mp4"],
        help="Prototype only. This version does not analyze image or video content.",
        key="prototype_video_upload",
    )

    related_text_available = bool(news_text and news_text.strip())
    uploaded_files = [file for file in (image_file, video_file) if file is not None]

    for uploaded_file in uploaded_files:
        _render_uploaded_media_details(uploaded_file, related_text_available)

    if uploaded_files and text_result:
        text_label = "Likely Real News" if text_result["is_real"] else "Likely Fake News"
        st.subheader("Combined Prototype Summary")
        st.markdown(f"**Text model result:** {text_label}")
        st.markdown(f"**Text confidence:** {text_result['confidence']:.1f}%")
        st.markdown(
            """
            **Media verification checklist:** source, date, author, reverse image
            search, metadata review, and cross-checking with trusted sources.
            """
        )
        st.warning("Final note: Needs manual verification.")
    elif uploaded_files and related_text_available:
        st.info(
            "Related news text is present. Run the text prediction to show a combined prototype summary."
        )

    st.info(
        "Image and video fake news detection requires separate multimodal datasets and specialized models. This deployed version focuses on text-based screening."
    )


def render_trust_indicators(news_text, language_code):
    """Render non-predictive heuristic trust indicators."""
    try:
        analysis = analyze_trust_signals(news_text, language_code)
        summary = analysis["summary"]
        st.markdown("<div class='section-subtitle'>Trust and Heuristic Signals</div>", unsafe_allow_html=True)
        cols = st.columns(4)
        cols[0].metric("Heuristic Flags", summary["risk_indicator_count"])
        cols[1].metric("ALL CAPS Words", summary["all_caps_words"])
        cols[2].metric("Exclamation Marks", summary["exclamation_count"])
        cols[3].metric("Sentiment", summary["sentiment"]["label"])

        st.caption(
            "These are lightweight indicators for reviewer awareness only. They are not used as final truth labels."
        )
        if analysis["signals"]:
            st.table(analysis["signals"])
        else:
            st.info("No strong heuristic warning signs were detected in this text.")
    except Exception as exc:
        st.info(f"Trust indicators are unavailable for this input: {exc}")


def render_xai_word_importance(news_text, language_code, models):
    """Render TF-IDF word importance from the existing vectorizer/model."""
    try:
        explanation = get_tfidf_word_importance(news_text, language_code, models)
        st.markdown("<div class='section-subtitle'>Explainable AI: TF-IDF Word Importance</div>", unsafe_allow_html=True)
        if not explanation.get("ok"):
            st.info(explanation.get("error", "No explanation is available for this prediction."))
            return

        rows = [
            {
                "Term": row["term"],
                "Impact": round(row["impact"], 4),
                "Direction": row["direction"],
                "TF-IDF": round(row["tfidf"], 4),
            }
            for row in explanation["terms"]
        ]
        st.caption(f"Explanation method: {explanation.get('method', 'TF-IDF fallback')}")
        try:
            import pandas as pd

            chart_frame = pd.DataFrame(rows).set_index("Term")
            st.bar_chart(chart_frame[["Impact"]])
        except Exception:
            pass
        st.dataframe(rows, width="stretch", hide_index=True)
    except Exception as exc:
        st.info(f"XAI explanation is unavailable for this input: {exc}")


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

    render_trust_indicators(news_text, language_code)
    render_xai_word_importance(news_text, language_code, models)

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
