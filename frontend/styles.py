import streamlit as st


def apply_premium_styles():
    """Apply clean, presentation-ready styling to the Streamlit app."""
    st.markdown(
        """
        <style>
            :root {
                --navy: #07182f;
                --navy-soft: #0f2f57;
                --cyan: #06b6d4;
                --bg: #f5f7fb;
                --card: #ffffff;
                --text: #172033;
                --muted: #5b677a;
                --border: #dbe3ef;
                --green-bg: #ecfdf5;
                --green-text: #065f46;
                --green-border: #22c55e;
                --red-bg: #fef2f2;
                --red-text: #991b1b;
                --red-border: #ef4444;
                --amber-bg: #fffbeb;
                --amber-text: #78350f;
                --amber-border: #f59e0b;
            }

            .stApp {
                background: var(--bg);
                color: var(--text);
            }

            .block-container {
                max-width: 1160px;
                padding-top: 1.25rem;
                padding-bottom: 2.5rem;
            }

            h1, h2, h3, h4, h5, h6 {
                color: var(--text);
                font-family: Arial, sans-serif;
                letter-spacing: 0;
            }

            p, li, label, div {
                letter-spacing: 0;
            }

            .main-header {
                padding: 36px 36px 34px;
                border-radius: 8px;
                background:
                    linear-gradient(135deg, rgba(6, 182, 212, 0.24), rgba(6, 182, 212, 0) 38%),
                    linear-gradient(135deg, var(--navy), var(--navy-soft));
                border: 1px solid rgba(6, 182, 212, 0.35);
                box-shadow: 0 18px 42px rgba(7, 24, 47, 0.18);
                margin-bottom: 16px;
                position: relative;
                overflow: hidden;
            }

            .header-topline {
                align-items: center;
                display: flex;
                gap: 12px;
                justify-content: space-between;
                margin-bottom: 8px;
            }

            .header-kicker {
                color: #99f6e4;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }

            .header-status {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(153, 246, 228, 0.38);
                border-radius: 999px;
                color: #ccfbf1;
                font-size: 12px;
                font-weight: 700;
                padding: 6px 10px;
                white-space: nowrap;
            }

            .main-header h1 {
                color: #ffffff !important;
                margin: 0 0 10px;
                font-size: 40px;
                font-weight: 800;
                line-height: 1.15;
            }

            .main-header p {
                color: #dbeafe;
                font-size: 16px;
                line-height: 1.6;
                max-width: 780px;
                margin: 0;
            }

            .header-meta {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 18px;
            }

            .header-meta span {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(219, 234, 254, 0.22);
                border-radius: 999px;
                color: #e0f2fe;
                font-size: 12px;
                font-weight: 700;
                padding: 7px 10px;
            }

            .disclaimer-card {
                background: var(--amber-bg);
                border: 1px solid #fcd34d;
                border-left: 5px solid var(--amber-border);
                border-radius: 8px;
                color: var(--amber-text);
                margin: 16px 0 18px;
                padding: 14px 16px;
            }

            .disclaimer-card strong {
                display: block;
                font-size: 15px;
                margin-bottom: 4px;
            }

            .disclaimer-card p {
                margin: 0;
                line-height: 1.55;
                font-size: 14px;
            }

            .disclaimer-card p + p {
                margin-top: 6px;
            }

            .section-title {
                color: var(--text);
                font-size: 21px;
                font-weight: 700;
                margin: 0 0 8px;
            }

            .section-subtitle {
                color: var(--text);
                font-size: 17px;
                font-weight: 700;
                margin: 20px 0 10px;
            }

            .section-heading {
                margin: 0 0 14px;
            }

            .section-heading h2 {
                color: var(--text);
                font-size: 24px;
                line-height: 1.25;
                margin: 0 0 6px;
            }

            .section-heading p {
                color: var(--muted);
                font-size: 15px;
                line-height: 1.6;
                margin: 0;
                max-width: 820px;
            }

            .compact-heading {
                margin-top: 20px;
            }

            .section-divider {
                border-top: 1px solid var(--border);
                margin: 28px 0 18px;
            }

            .info-box {
                background-color: #ffffff;
                padding: 14px 16px;
                border-radius: 8px;
                color: var(--muted);
                margin-bottom: 14px;
                border: 1px solid var(--border);
                border-left: 4px solid var(--cyan);
                line-height: 1.55;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            }

            .workflow-section {
                margin: 18px 0 14px;
            }

            .workflow-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 12px;
            }

            .workflow-step {
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 8px;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
                min-height: 142px;
                padding: 16px;
            }

            .step-number {
                color: var(--cyan);
                display: block;
                font-size: 12px;
                font-weight: 800;
                margin-bottom: 8px;
                text-transform: uppercase;
            }

            .workflow-step strong {
                color: var(--text);
                display: block;
                font-size: 15px;
                margin-bottom: 7px;
            }

            .workflow-step p {
                color: var(--muted);
                font-size: 13px;
                line-height: 1.55;
                margin: 0;
            }

            .feature-section {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 12px;
                margin: 16px 0 0;
            }

            .feature-card {
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 8px;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
                min-height: 150px;
                padding: 16px;
            }

            .feature-card h3 {
                color: var(--text);
                font-size: 16px;
                line-height: 1.3;
                margin: 10px 0 8px;
            }

            .feature-card p {
                color: var(--muted);
                font-size: 13px;
                line-height: 1.55;
                margin: 0;
            }

            .feature-tag,
            .status-badge {
                border-radius: 999px;
                display: inline-block;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 0.02em;
                line-height: 1;
                padding: 6px 8px;
                text-transform: uppercase;
                white-space: nowrap;
            }

            .feature-tag.implemented,
            .status-badge.implemented {
                background: #ecfdf5;
                border: 1px solid #bbf7d0;
                color: #047857;
            }

            .feature-tag.research,
            .status-badge.research {
                background: #eff6ff;
                border: 1px solid #bfdbfe;
                color: #1d4ed8;
            }

            .feature-tag.future,
            .status-badge.future {
                background: #f8fafc;
                border: 1px solid #cbd5e1;
                color: #475569;
            }

            .input-note {
                color: var(--muted);
                font-size: 14px;
                margin: 0 0 14px;
            }

            div[data-testid="stForm"] {
                background-color: var(--card);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 20px 20px 22px;
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.07);
            }

            textarea {
                border-radius: 8px !important;
                border: 1px solid #cbd5e1 !important;
                color: var(--text) !important;
            }

            textarea:focus {
                border-color: var(--cyan) !important;
                box-shadow: 0 0 0 1px var(--cyan) !important;
            }

            div[role="radiogroup"] label {
                background: #f8fafc;
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 8px 12px;
            }

            button {
                border-radius: 8px !important;
                font-weight: 600 !important;
            }

            div[data-testid="stFormSubmitButton"] button {
                min-height: 44px;
            }

            div[data-testid="stFormSubmitButton"] button[kind*="primary" i],
            div[data-testid="stFormSubmitButton"] button[data-testid*="primary" i],
            div[data-testid="stButton"] button[kind*="primary" i],
            div[data-testid="stButton"] button[data-testid*="primary" i],
            button[kind*="primary" i],
            button[data-testid*="primary" i] {
                background: #0891b2 !important;
                background-image: linear-gradient(135deg, #0e7490, var(--cyan)) !important;
                background-color: #0891b2 !important;
                border: 1px solid #0e7490 !important;
                color: #ffffff !important;
                box-shadow: 0 8px 18px rgba(8, 145, 178, 0.22) !important;
            }

            div[data-testid="stFormSubmitButton"] button[kind*="primary" i]:hover,
            div[data-testid="stFormSubmitButton"] button[data-testid*="primary" i]:hover,
            div[data-testid="stButton"] button[kind*="primary" i]:hover,
            div[data-testid="stButton"] button[data-testid*="primary" i]:hover,
            button[kind*="primary" i]:hover,
            button[data-testid*="primary" i]:hover,
            div[data-testid="stFormSubmitButton"] button[kind*="primary" i]:focus,
            div[data-testid="stFormSubmitButton"] button[data-testid*="primary" i]:focus,
            div[data-testid="stButton"] button[kind*="primary" i]:focus,
            div[data-testid="stButton"] button[data-testid*="primary" i]:focus,
            button[kind*="primary" i]:focus,
            button[data-testid*="primary" i]:focus,
            div[data-testid="stFormSubmitButton"] button[kind*="primary" i]:active,
            div[data-testid="stFormSubmitButton"] button[data-testid*="primary" i]:active,
            div[data-testid="stButton"] button[kind*="primary" i]:active,
            div[data-testid="stButton"] button[data-testid*="primary" i]:active,
            button[kind*="primary" i]:active,
            button[data-testid*="primary" i]:active {
                background: #0e7490 !important;
                background-image: linear-gradient(135deg, #155e75, #0891b2) !important;
                background-color: #0e7490 !important;
                border-color: #155e75 !important;
                color: #ffffff !important;
            }

            div[data-testid="stFormSubmitButton"] button[kind*="secondary" i],
            div[data-testid="stFormSubmitButton"] button[data-testid*="secondary" i],
            div[data-testid="stButton"] button[kind*="secondary" i],
            div[data-testid="stButton"] button[data-testid*="secondary" i],
            button[kind*="secondary" i],
            button[data-testid*="secondary" i] {
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #cbd5e1 !important;
                color: #334155 !important;
                box-shadow: none !important;
            }

            div[data-testid="stFormSubmitButton"] button[kind*="secondary" i]:hover,
            div[data-testid="stFormSubmitButton"] button[data-testid*="secondary" i]:hover,
            div[data-testid="stButton"] button[kind*="secondary" i]:hover,
            div[data-testid="stButton"] button[data-testid*="secondary" i]:hover,
            button[kind*="secondary" i]:hover,
            button[data-testid*="secondary" i]:hover {
                background: #f8fafc !important;
                background-color: #f8fafc !important;
                border-color: #94a3b8 !important;
                color: #0f172a !important;
            }

            .guide-card {
                background-color: var(--card);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
            }

            .guide-card h3 {
                font-size: 20px;
                margin: 0 0 8px;
            }

            .guide-card p {
                color: var(--muted);
                font-size: 14px;
                line-height: 1.55;
                margin: 0 0 14px;
            }

            .guide-card h4 {
                font-size: 15px;
                margin: 15px 0 7px;
                color: var(--text);
            }

            .guide-card ul {
                margin: 0 0 8px 18px;
                padding: 0;
                color: var(--muted);
                line-height: 1.55;
                font-size: 14px;
            }

            .research-section {
                margin-top: 8px;
            }

            .research-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 14px;
                margin-bottom: 14px;
            }

            .research-card {
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 18px 20px;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            }

            .research-card > .status-badge {
                margin-bottom: 10px;
            }

            .research-card h3 {
                color: var(--text);
                font-size: 18px;
                margin: 0 0 10px;
            }

            .research-card h4 {
                color: var(--text);
                font-size: 15px;
                margin: 18px 0 8px;
            }

            .research-card p {
                color: var(--muted);
                font-size: 14px;
                line-height: 1.6;
                margin: 0 0 10px;
            }

            .research-card ul {
                color: var(--muted);
                font-size: 14px;
                line-height: 1.6;
                margin: 0 0 0 18px;
                padding: 0;
            }

            .research-table-card {
                margin-bottom: 14px;
            }

            .research-table-wrap {
                overflow-x: auto;
            }

            .research-table {
                border-collapse: collapse;
                min-width: 760px;
                width: 100%;
                font-size: 14px;
            }

            .research-table th,
            .research-table td {
                border: 1px solid var(--border);
                padding: 10px 12px;
                text-align: left;
                vertical-align: top;
            }

            .research-table th {
                background: #f8fafc;
                color: var(--text);
                font-weight: 700;
            }

            .research-table td {
                color: var(--muted);
                line-height: 1.45;
            }

            .metrics-table th:not(:first-child),
            .metrics-table td:not(:first-child) {
                text-align: right;
                white-space: nowrap;
            }

            .result-note {
                background: #f8fafc;
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 10px 12px;
            }

            .research-table .best-result-row td {
                background: #ecfdf5;
                color: #065f46;
                font-weight: 700;
            }

            .prototype-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 12px;
                margin: 12px 0 16px;
            }

            .prototype-card {
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 8px;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
                min-height: 150px;
                padding: 16px;
            }

            .prototype-card h3 {
                color: var(--text);
                font-size: 15px;
                line-height: 1.35;
                margin: 10px 0 8px;
            }

            .prototype-card p {
                color: var(--muted);
                font-size: 13px;
                line-height: 1.55;
                margin: 0;
            }

            .multimodal-section {
                margin-top: 8px;
            }

            .upload-shell {
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 8px;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
                margin-top: 14px;
                padding: 18px 20px;
            }

            .upload-shell strong {
                color: var(--text);
                display: block;
                font-size: 15px;
                margin-bottom: 5px;
            }

            .upload-shell p {
                color: var(--muted);
                font-size: 14px;
                line-height: 1.55;
                margin: 0;
            }

            .upload-result {
                background: #f8fafc;
                border: 1px solid var(--border);
                border-left: 4px solid var(--cyan);
                border-radius: 8px;
                margin-top: 12px;
                padding: 14px 16px;
            }

            .upload-result strong {
                color: var(--text);
                display: block;
                font-size: 15px;
                margin-bottom: 4px;
            }

            .upload-result p {
                color: var(--muted);
                font-size: 14px;
                line-height: 1.55;
                margin: 0 0 10px;
            }

            .upload-meta {
                display: grid;
                gap: 6px;
            }

            .upload-meta span {
                color: var(--text);
                font-size: 13px;
                line-height: 1.45;
            }

            .wide-card {
                grid-column: span 3;
                min-height: 118px;
            }

            .accuracy-note {
                background: #ffffff;
                border: 1px solid var(--border);
                border-left: 4px solid var(--cyan);
                border-radius: 8px;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
                margin-top: 16px;
                padding: 18px 20px;
            }

            .accuracy-note h3 {
                color: var(--text);
                font-size: 18px;
                margin: 0 0 8px;
            }

            .accuracy-note p {
                color: var(--muted);
                font-size: 14px;
                line-height: 1.6;
                margin: 0;
                max-width: 900px;
            }

            .academic-note {
                background: #f8fafc;
                border: 1px solid var(--border);
                border-left: 4px solid var(--cyan);
                border-radius: 8px;
                color: var(--text);
                font-size: 14px;
                line-height: 1.6;
                margin-top: 14px;
                padding: 14px 16px;
            }

            .compact-note {
                margin-top: 12px;
            }

            .real-news-box,
            .fake-news-box {
                padding: 24px 26px;
                border-radius: 8px;
                margin: 12px 0 18px;
                border: 1px solid;
                box-shadow: 0 10px 26px rgba(15, 23, 42, 0.07);
            }

            .real-news-box {
                background-color: var(--green-bg);
                color: var(--green-text);
                border-color: var(--green-border);
            }

            .fake-news-box {
                background-color: var(--red-bg);
                color: var(--red-text);
                border-color: var(--red-border);
            }

            .result-label {
                font-size: 28px;
                font-weight: 800;
                line-height: 1.2;
            }

            .result-caption {
                margin-top: 8px;
                font-size: 15px;
                font-weight: 600;
            }

            .result-helper {
                font-size: 14px;
                line-height: 1.55;
                margin-top: 10px;
                max-width: 760px;
            }

            .suspicious-keywords {
                background-color: var(--amber-bg);
                padding: 12px 14px;
                border-radius: 8px;
                border: 1px solid #fcd34d;
                border-left: 4px solid var(--amber-border);
                margin-top: 16px;
                color: var(--amber-text);
            }

            .suspicious-keywords p {
                font-size: 13px;
                margin: 6px 0 0;
            }

            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 14px 16px;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            }

            div[data-testid="stMetricLabel"] {
                color: var(--muted);
            }

            div[data-testid="stMetricValue"] {
                color: var(--text);
                font-weight: 800;
            }

            .footer {
                text-align: center;
                color: var(--muted);
                margin-top: 36px;
                font-size: 14px;
                padding: 16px 12px 4px;
                line-height: 1.5;
            }

            [data-testid="stSidebar"] {
                background-color: #ffffff;
                border-right: 1px solid var(--border);
            }

            .sidebar-panel {
                background: #f8fafc;
                border: 1px solid var(--border);
                border-radius: 8px;
                margin-bottom: 12px;
                padding: 14px;
            }

            .sidebar-panel h2,
            .sidebar-heading {
                color: var(--navy);
                font-size: 18px;
                font-weight: 800;
                margin: 0 0 8px;
            }

            .sidebar-panel p {
                color: var(--muted);
                font-size: 13px;
                line-height: 1.55;
                margin: 0 0 12px;
            }

            .sidebar-list {
                display: grid;
                gap: 7px;
            }

            .sidebar-list span {
                background: #ffffff;
                border: 1px solid var(--border);
                border-radius: 8px;
                color: var(--text);
                display: block;
                font-size: 13px;
                padding: 8px 10px;
            }

            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: var(--navy);
            }

            div[data-testid="stAlert"] {
                border-radius: 8px;
            }

            hr {
                border-color: var(--border);
                margin: 1.25rem 0;
            }

            @media (max-width: 780px) {
                .header-topline {
                    align-items: flex-start;
                    flex-direction: column;
                }

                .main-header {
                    padding: 28px 22px 26px;
                }

                .main-header h1 {
                    font-size: 30px;
                }

                .workflow-grid,
                .feature-section,
                .prototype-grid {
                    grid-template-columns: 1fr;
                }

                .research-grid {
                    grid-template-columns: 1fr;
                }

                .section-heading h2 {
                    font-size: 21px;
                }

                .wide-card {
                    grid-column: span 1;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
