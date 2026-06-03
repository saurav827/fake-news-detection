"""Simple Streamlit styling for the project UI."""

import streamlit as st


def apply_styles():
    """Add a clean student-project look without heavy design code."""
    st.markdown(
        """
        <style>
            .stApp {
                background: #f7f9fc;
            }

            .block-container {
                max-width: 1120px;
                padding-top: 1.25rem;
                padding-bottom: 2rem;
                padding-left: 1.25rem;
                padding-right: 1.25rem;
            }

            h1, h2, h3 {
                color: #1f2937;
                letter-spacing: 0;
            }

            .small-note {
                color: #6b7280;
                font-size: 0.95rem;
                margin-top: -0.5rem;
                margin-bottom: 1.2rem;
            }

            div[data-testid="stSelectbox"] {
                margin-bottom: 0.35rem;
            }

            div[data-testid="stTextArea"],
            div[data-testid="stTextInput"] {
                margin-bottom: 0.75rem;
            }

            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px 14px;
            }

            div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stMetric"]) {
                gap: 0.85rem;
            }

            div[data-testid="stChart"] {
                margin-top: 0.4rem;
                padding-top: 0.35rem;
            }

            .chart-title {
                color: #374151;
                font-weight: 600;
                margin-top: 1rem;
                margin-bottom: 0.25rem;
            }

            .result-box {
                border-radius: 8px;
                border: 1px solid #d1d5db;
                padding: 18px;
                margin: 16px 0;
                background: #ffffff;
            }

            .result-real {
                border-left: 6px solid #16a34a;
                background: #f0fdf4;
            }

            .result-fake {
                border-left: 6px solid #dc2626;
                background: #fef2f2;
            }

            .result-title {
                font-size: 1.45rem;
                font-weight: 700;
                margin-bottom: 6px;
            }

            .status-ok {
                color: #15803d;
                font-weight: 600;
            }

            .status-bad {
                color: #b91c1c;
                font-weight: 600;
            }

            .footer {
                color: #6b7280;
                font-size: 0.9rem;
                text-align: center;
                margin-top: 2rem;
                padding-top: 1rem;
                border-top: 1px solid #e5e7eb;
            }

            [data-testid="stSidebar"] {
                background: #ffffff;
            }

            button {
                border-radius: 8px !important;
            }

            @media (max-width: 768px) {
                .block-container {
                    padding-left: 0.9rem;
                    padding-right: 0.9rem;
                }

                .result-title {
                    font-size: 1.25rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_premium_styles():
    """Old import name kept so older files do not break."""
    apply_styles()
