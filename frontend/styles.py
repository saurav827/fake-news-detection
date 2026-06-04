"""Compact styling for B.Tech project - clean, realistic, minimal."""

import streamlit as st


def apply_styles():
    """Clean student-project styling with compact layout."""
    st.markdown(
        """
        <style>
            /* Main container - compact width */
            .stApp {
                background: #f5f6f7;
            }

            .block-container {
                max-width: 850px;
                padding-top: 0.8rem;
                padding-bottom: 1.2rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            /* Headings - clean and minimal */
            h1 {
                color: #1a1a1a;
                font-size: 1.8rem;
                margin-top: 0.3rem;
                margin-bottom: 0.4rem;
                line-height: 1.3;
            }

            h2 {
                color: #1a1a1a;
                font-size: 1.2rem;
                margin-top: 0.5rem;
                margin-bottom: 0.3rem;
                font-weight: 600;
            }

            h3 {
                color: #2a2a2a;
                font-size: 1rem;
                margin-top: 0.3rem;
                margin-bottom: 0.2rem;
                font-weight: 600;
            }

            p {
                margin-bottom: 0.6rem;
                line-height: 1.4;
                color: #444;
                font-size: 0.95rem;
            }

            /* Form elements - compact spacing */
            div[data-testid="stSelectbox"],
            div[data-testid="stRadio"],
            div[data-testid="stCheckbox"] {
                margin-bottom: 0.3rem;
            }

            div[data-testid="stTextArea"],
            div[data-testid="stTextInput"],
            div[data-testid="stSlider"] {
                margin-bottom: 0.4rem;
            }

            /* Vertical spacing between elements */
            div[data-testid="stVerticalBlock"] > div {
                margin-bottom: 0.2rem !important;
            }

            /* Labels for form elements */
            label {
                font-size: 0.92rem !important;
                margin-bottom: 0.2rem !important;
            }

            /* Metrics - compact cards */
            div[data-testid="stMetric"] {
                background: #fff;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 7px 9px;
                margin: 0 !important;
            }

            div[data-testid="stMetricDeltaContainer"] {
                font-size: 0.75rem !important;
            }

            div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stMetric"]) {
                gap: 0.3rem !important;
            }

            /* Charts - reduced height */
            div[data-testid="stChart"] {
                margin-top: 0rem !important;
                margin-bottom: 0rem !important;
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                height: auto !important;
                max-height: 200px;
            }

            [data-testid="stChart"] > div {
                margin-bottom: 0 !important;
            }

            /* Columns - optimal spacing */
            [data-testid="stHorizontalBlock"] {
                gap: 0.3rem !important;
            }

            .chart-title {
                color: #2a2a2a;
                font-weight: 600;
                font-size: 0.95rem;
                margin-top: 0.4rem;
                margin-bottom: 0.2rem;
            }

            /* Result boxes - compact */
            .result-box {
                border-radius: 6px;
                border: 1px solid #ddd;
                padding: 8px;
                margin: 0.4rem 0;
                background: #fff;
            }

            .result-real {
                border-left: 5px solid #16a34a;
                background: #f0fdf4;
            }

            .result-fake {
                border-left: 5px solid #dc2626;
                background: #fef2f2;
            }

            .result-title {
                font-size: 1.2rem;
                font-weight: 700;
                margin-bottom: 0.3rem;
            }

            .status-ok {
                color: #15803d;
                font-weight: 600;
            }

            .status-bad {
                color: #b91c1c;
                font-weight: 600;
            }

            /* Sidebar - compact */
            [data-testid="stSidebar"] {
                background: #fff;
                width: 250px;
            }

            .sidebar-panel {
                margin-bottom: 0.6rem;
            }

            .sidebar-heading {
                font-weight: 600;
                color: #1a1a1a;
                font-size: 0.9rem;
                margin: 0.4rem 0 0.3rem 0;
            }

            .sidebar-list {
                display: flex;
                flex-direction: column;
                gap: 0.2rem;
                font-size: 0.85rem;
                color: #555;
            }

            /* Buttons - simple and compact */
            button {
                border-radius: 6px !important;
                font-size: 0.92rem !important;
                padding: 0.4rem 0.8rem !important;
            }

            /* Divider - minimal */
            hr {
                margin: 0.4rem 0 !important;
                border: none;
                border-top: 1px solid #e5e7eb;
            }

            /* Caption - smaller text */
            .stCaption {
                font-size: 0.8rem !important;
                margin-top: 0.2rem !important;
                margin-bottom: 0.2rem !important;
            }

            /* Disclaimer - compact */
            .disclaimer-card {
                background: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 8px 10px;
                border-radius: 4px;
                margin-bottom: 0.6rem;
                font-size: 0.9rem;
            }

            .disclaimer-card p {
                margin-bottom: 0.2rem;
            }

            /* Section divider */
            .section-divider {
                height: 1px;
                background: #e5e7eb;
                margin: 0.6rem 0;
            }

            .section-title {
                font-size: 1rem;
                font-weight: 600;
                color: #1a1a1a;
                margin: 0.5rem 0 0.3rem 0;
            }

            .info-box {
                background: #f0f4f8;
                border-left: 3px solid #3b82f6;
                padding: 7px 9px;
                border-radius: 4px;
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            }

            /* Info/Warning boxes */
            [data-testid="stAlert"] {
                margin-bottom: 0.4rem !important;
                padding: 0.6rem 0.8rem !important;
            }

            /* Footer - minimal */
            .footer {
                color: #777;
                font-size: 0.8rem;
                text-align: center;
                margin-top: 1rem;
                padding-top: 0.6rem;
                border-top: 1px solid #e5e7eb;
            }

            /* Guide card */
            .guide-card {
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 0.9rem;
            }

            .guide-card h3 {
                margin-top: 0.3rem;
            }

            .guide-card h4 {
                margin-top: 0.4rem;
                margin-bottom: 0.2rem;
                font-size: 0.9rem;
            }

            .guide-card ul {
                margin-left: 1.2rem;
                margin-bottom: 0.2rem;
                font-size: 0.9rem;
                padding: 0;
            }

            .guide-card li {
                margin-bottom: 0.15rem;
            }

            /* Caption - smaller */
            .stCaption {
                font-size: 0.85rem !important;
            }

            /* Tabs - compact */
            [data-testid="stTabs"] {
                margin-top: 0.3rem;
            }

            /* Expander - compact */
            [data-testid="stExpander"] {
                margin-bottom: 0.4rem;
            }

            /* Mobile responsiveness */
            @media (max-width: 768px) {
                .block-container {
                    padding-left: 0.8rem;
                    padding-right: 0.8rem;
                    max-width: 100%;
                }

                h1 {
                    font-size: 1.4rem;
                }

                h2 {
                    font-size: 1rem;
                }

                .result-title {
                    font-size: 1.05rem;
                }

                div[data-testid="stChart"] {
                    max-height: 160px;
                }

                [data-testid="stSidebar"] {
                    width: 220px;
                }
            }

            @media (max-width: 480px) {
                .block-container {
                    padding-left: 0.6rem;
                    padding-right: 0.6rem;
                }

                h1 {
                    font-size: 1.2rem;
                    margin-bottom: 0.3rem;
                }

                h2 {
                    font-size: 0.95rem;
                }

                .result-title {
                    font-size: 1rem;
                }

                button {
                    font-size: 0.85rem !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_premium_styles():
    """Old import name kept for backward compatibility."""
    apply_styles()
