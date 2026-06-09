"""Compact premium styling for B.Tech project - clean, realistic, modern."""

import streamlit as st


def apply_styles():
    """Apply premium academic styling with Outift & Inter fonts."""
    st.markdown(
        """
        <style>
            /* Import Premium Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

            /* Global Styles */
            .stApp {
                background-color: #f8fafc;
                font-family: 'Inter', sans-serif;
            }

            .block-container {
                max-width: 900px;
                padding-top: 1.5rem;
                padding-bottom: 2rem;
                padding-left: 1.5rem;
                padding-right: 1.5rem;
            }

            /* Custom Typography */
            h1 {
                font-family: 'Outfit', sans-serif;
                color: #0f172a;
                font-size: 2.2rem;
                font-weight: 700;
                margin-top: 0rem;
                margin-bottom: 0.5rem;
                letter-spacing: -0.025em;
            }

            h2 {
                font-family: 'Outfit', sans-serif;
                color: #1e293b;
                font-size: 1.4rem;
                font-weight: 600;
                margin-top: 1rem;
                margin-bottom: 0.5rem;
                letter-spacing: -0.02em;
            }

            h3 {
                font-family: 'Outfit', sans-serif;
                color: #334155;
                font-size: 1.15rem;
                font-weight: 600;
                margin-top: 0.8rem;
                margin-bottom: 0.4rem;
            }

            p {
                margin-bottom: 0.8rem;
                line-height: 1.5;
                color: #475569;
                font-size: 0.95rem;
            }

            /* Main Header Banner */
            .project-header {
                background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
                border: 1px solid #bfdbfe;
                border-radius: 12px;
                padding: 1.25rem 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
            }
            
            .project-badge {
                display: inline-block;
                background-color: #3b82f6;
                color: white;
                font-size: 0.75rem;
                font-weight: 600;
                padding: 0.2rem 0.6rem;
                border-radius: 9999px;
                margin-bottom: 0.5rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            /* Metric Cards */
            div[data-testid="stMetric"] {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 0.9rem 1.1rem;
                box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            div[data-testid="stMetric"]:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
            }

            div[data-testid="stMetricLabel"] {
                font-weight: 500 !important;
                color: #64748b !important;
                font-size: 0.85rem !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            div[data-testid="stMetricValue"] {
                font-family: 'Outfit', sans-serif;
                font-size: 1.8rem !important;
                font-weight: 700 !important;
                color: #0f172a !important;
            }

            /* Form Elements styling */
            div[data-testid="stTextArea"] textarea {
                border-radius: 8px !important;
                border: 1px solid #cbd5e1 !important;
                background-color: #ffffff !important;
                font-size: 0.95rem !important;
                color: #0f172a !important;
                padding: 0.8rem !important;
                transition: border-color 0.2s ease, box-shadow 0.2s ease;
            }

            div[data-testid="stTextArea"] textarea:focus {
                border-color: #3b82f6 !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
            }

            div[data-testid="stTextInput"] input {
                border-radius: 8px !important;
                border: 1px solid #cbd5e1 !important;
                padding: 0.5rem 0.8rem !important;
            }

            /* Premium Buttons styling */
            div[data-testid="stButton"] button {
                border-radius: 8px !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                padding: 0.6rem 1.2rem !important;
                transition: all 0.2s ease !important;
            }

            /* Target Check button as Primary */
            div[data-testid="stButton"] button[kind="primary"] {
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
                border: none !important;
                color: #ffffff !important;
                box-shadow: 0 2px 4px 0 rgba(37, 99, 235, 0.2) !important;
            }

            div[data-testid="stButton"] button[kind="primary"]:hover {
                background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
                box-shadow: 0 4px 6px 0 rgba(37, 99, 235, 0.3) !important;
                transform: translateY(-1px);
            }

            /* Result Boxes (Real/Fake highlights) */
            .result-box {
                border-radius: 12px;
                padding: 1.2rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.02);
                border: 1px solid #e2e8f0;
                transition: transform 0.2s ease;
            }

            .result-box:hover {
                transform: translateY(-1px);
            }

            .result-real {
                background-color: #f0fdf4;
                border-left: 6px solid #16a34a;
                border-color: #bbf7d0;
            }

            .result-real .result-title {
                color: #15803d;
            }

            .result-fake {
                background-color: #fef2f2;
                border-left: 6px solid #dc2626;
                border-color: #fecaca;
            }

            .result-fake .result-title {
                color: #b91c1c;
            }

            .result-title {
                font-family: 'Outfit', sans-serif;
                font-size: 1.35rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                letter-spacing: -0.01em;
            }

            .result-info {
                display: flex;
                flex-wrap: wrap;
                gap: 1rem;
                margin-top: 0.4rem;
                font-size: 0.9rem;
                color: #475569;
            }

            .result-info b {
                color: #0f172a;
            }

            /* Progress Bar custom style */
            div[data-testid="stProgress"] > div > div > div > div {
                background-color: #3b82f6 !important;
            }

            /* Sidebar custom design */
            [data-testid="stSidebar"] {
                background-color: #ffffff;
                border-right: 1px solid #e2e8f0;
                width: 260px !important;
            }

            [data-testid="stSidebar"] h2 {
                font-size: 1.25rem;
                margin-top: 0.5rem;
            }

            .sidebar-card {
                padding: 0.8rem;
                border-radius: 8px;
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                margin-bottom: 0.8rem;
            }

            .sidebar-card span {
                display: block;
                font-size: 0.85rem;
                color: #475569;
                margin-bottom: 0.25rem;
            }

            /* Footer Styling */
            .footer {
                text-align: center;
                padding-top: 1.5rem;
                margin-top: 2rem;
                border-top: 1px solid #e2e8f0;
                color: #94a3b8;
                font-size: 0.8rem;
            }

            /* Dividers */
            hr {
                margin: 1.2rem 0 !important;
                border: none;
                border-top: 1px solid #e2e8f0;
            }

            /* Dataframe styling */
            div[data-testid="stDataFrame"] {
                border: 1px solid #e2e8f0 !important;
                border-radius: 8px !important;
                overflow: hidden !important;
                box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            }

            /* Responsive tweaks */
            @media (max-width: 768px) {
                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
                h1 {
                    font-size: 1.8rem;
                }
                h2 {
                    font-size: 1.2rem;
                }
                .result-title {
                    font-size: 1.15rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_premium_styles():
    """Keep compatibility name."""
    apply_styles()

