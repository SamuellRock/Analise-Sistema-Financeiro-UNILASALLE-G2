"""Theme and visual configuration for the Streamlit dashboard."""

from __future__ import annotations

import streamlit as st


def configure_page() -> None:
    """Configure the base Streamlit page settings."""
    st.set_page_config(
        page_title="Dashboard Financeiro Brasil",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_theme() -> None:
    """Apply the visual system for the dashboard."""
    st.markdown(
        """
        <style>
            :root {
                --bg-color: #F3F6FA;
                --surface-color: #FFFFFF;
                --surface-muted: #F8FBFF;
                --border-color: #E2E8F0;
                --primary-color: #2563EB;
                --primary-dark: #1E3A8A;
                --primary-mid: #3B82F6;
                --primary-soft: #DBEAFE;
                --text-color: #0F172A;
                --text-muted: #64748B;
                --success-color: #10B981;
                --danger-color: #EF4444;
                --shadow-soft: 0 12px 30px rgba(15, 23, 42, 0.08);
                --radius-lg: 28px;
                --radius-md: 18px;
                --radius-sm: 12px;
            }

            html, body, [class*="css"] {
                color: var(--text-color);
                font-family: "Trebuchet MS", "Segoe UI", sans-serif;
            }

            [data-testid="stAppViewContainer"] {
                background: linear-gradient(180deg, #F8FBFF 0%, var(--bg-color) 14%, var(--bg-color) 100%);
            }

            [data-testid="stHeader"] {
                background: rgba(243, 246, 250, 0.88);
            }

            [data-testid="stSidebar"] {
                background: var(--surface-color);
                border-right: 1px solid var(--border-color);
            }

            [data-testid="stSidebar"] > div:first-child {
                padding-top: 1.2rem;
            }

            [data-testid="stSidebar"] * {
                color: var(--text-color);
            }

            .block-container {
                max-width: 1500px;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }

            .dashboard-hero {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 251, 255, 0.94) 100%);
                border: 1px solid rgba(219, 234, 254, 0.95);
                border-radius: var(--radius-lg);
                box-shadow: var(--shadow-soft);
                margin-bottom: 1.5rem;
                padding: 1.75rem 1.9rem;
            }

            .dashboard-eyebrow {
                color: var(--primary-color);
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                margin-bottom: 0.55rem;
                text-transform: uppercase;
            }

            .dashboard-title {
                color: var(--text-color);
                font-size: 2.15rem;
                font-weight: 800;
                line-height: 1.1;
                margin: 0;
            }

            .dashboard-subtitle {
                color: var(--text-muted);
                font-size: 1rem;
                line-height: 1.65;
                margin: 0.8rem 0 0;
                max-width: 70rem;
            }

            .dashboard-note {
                background: rgba(255, 255, 255, 0.86);
                border: 1px solid rgba(37, 99, 235, 0.12);
                border-radius: 16px;
                color: var(--text-muted);
                font-size: 0.92rem;
                line-height: 1.55;
                margin-top: 1rem;
                padding: 0.95rem 1rem;
            }

            .section-heading {
                color: var(--text-color);
                font-size: 1.08rem;
                font-weight: 800;
                margin: 0.2rem 0;
            }

            .section-description {
                color: var(--text-muted);
                font-size: 0.94rem;
                line-height: 1.6;
                margin-bottom: 0.95rem;
            }

            .sidebar-brand {
                background: linear-gradient(180deg, rgba(37, 99, 235, 0.08) 0%, rgba(219, 234, 254, 0.16) 100%);
                border: 1px solid rgba(37, 99, 235, 0.12);
                border-radius: 18px;
                margin-bottom: 1rem;
                padding: 1rem 1rem 0.95rem;
            }

            .sidebar-title {
                color: var(--text-color);
                font-size: 1.15rem;
                font-weight: 800;
                margin-bottom: 0.15rem;
            }

            .sidebar-subtitle {
                color: var(--text-muted);
                font-size: 0.88rem;
                line-height: 1.45;
            }

            .sidebar-section-title {
                color: var(--primary-dark);
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                margin: 1rem 0 0.5rem;
                text-transform: uppercase;
            }

            .sidebar-menu {
                background: var(--surface-muted);
                border: 1px solid rgba(37, 99, 235, 0.08);
                border-radius: 16px;
                padding: 0.85rem 0.9rem;
            }

            .sidebar-menu-item {
                align-items: center;
                color: var(--text-color);
                display: flex;
                font-size: 0.92rem;
                gap: 0.45rem;
                margin-bottom: 0.45rem;
            }

            .sidebar-menu-item:last-child {
                margin-bottom: 0;
            }

            .sidebar-menu-bullet {
                align-items: center;
                background: var(--primary-soft);
                border-radius: 999px;
                color: var(--primary-dark);
                display: inline-flex;
                font-size: 0.72rem;
                font-weight: 800;
                height: 1.2rem;
                justify-content: center;
                width: 1.2rem;
            }

            .sidebar-copy {
                color: var(--text-muted);
                font-size: 0.88rem;
                line-height: 1.55;
                margin-bottom: 0.55rem;
            }

            .sidebar-divider {
                border-top: 1px solid var(--border-color);
                margin: 1rem 0;
            }

            .sidebar-caption {
                color: var(--text-muted);
                font-size: 0.82rem;
                line-height: 1.5;
                margin-bottom: 0.6rem;
            }

            .kpi-card {
                background: var(--surface-color);
                border: 1px solid var(--border-color);
                border-radius: var(--radius-md);
                box-shadow: var(--shadow-soft);
                min-height: 170px;
                padding: 1rem 1.05rem;
            }

            .kpi-card--primary {
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-mid) 100%);
                border-color: transparent;
                color: #FFFFFF;
            }

            .kpi-card--primary .kpi-label,
            .kpi-card--primary .kpi-value,
            .kpi-card--primary .kpi-caption,
            .kpi-card--primary .kpi-support {
                color: #FFFFFF;
            }

            .kpi-label {
                color: var(--text-muted);
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.02em;
                margin-bottom: 0.7rem;
                text-transform: uppercase;
            }

            .kpi-value {
                color: var(--text-color);
                font-size: 2rem;
                font-weight: 800;
                letter-spacing: -0.03em;
                line-height: 1.1;
                margin-bottom: 0.45rem;
            }

            .kpi-caption {
                color: var(--text-color);
                font-size: 0.95rem;
                font-weight: 600;
                line-height: 1.35;
                margin-bottom: 0.45rem;
            }

            .kpi-support {
                color: var(--text-muted);
                font-size: 0.84rem;
                line-height: 1.45;
            }

            .kpi-badge {
                align-items: center;
                background: rgba(37, 99, 235, 0.1);
                border-radius: 999px;
                color: var(--primary-dark);
                display: inline-flex;
                font-size: 0.76rem;
                font-weight: 700;
                margin-top: 0.7rem;
                padding: 0.22rem 0.55rem;
            }

            .kpi-card--primary .kpi-badge {
                background: rgba(255, 255, 255, 0.18);
                color: #FFFFFF;
            }

            .table-title {
                color: var(--text-color);
                font-size: 1.05rem;
                font-weight: 800;
                margin-bottom: 0.2rem;
            }

            .table-description {
                color: var(--text-muted);
                font-size: 0.9rem;
                line-height: 1.55;
                margin-bottom: 0.75rem;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 0.45rem;
                margin-bottom: 1rem;
            }

            .stTabs [data-baseweb="tab"] {
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid var(--border-color);
                border-radius: 999px;
                color: var(--text-muted);
                height: 2.75rem;
                padding: 0 1rem;
            }

            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-mid) 100%);
                border-color: transparent;
                color: #FFFFFF;
            }

            .stPlotlyChart,
            div[data-testid="stDataFrame"],
            div[data-testid="stMetric"] {
                background: var(--surface-color);
                border: 1px solid var(--border-color);
                border-radius: var(--radius-md);
                box-shadow: var(--shadow-soft);
                padding: 0.35rem;
            }

            div[data-testid="stDataFrame"] {
                padding: 0.55rem;
            }

            div[data-testid="stMetric"] {
                padding: 1rem 1.1rem;
            }

            [data-testid="stMetricValue"] {
                color: var(--text-color);
                font-size: 1.55rem;
                font-weight: 800;
            }

            [data-testid="stMetricLabel"] {
                color: var(--text-muted);
                font-size: 0.92rem;
                font-weight: 600;
            }

            .stButton > button,
            .stDownloadButton > button {
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-mid) 100%);
                border: none;
                border-radius: 12px;
                box-shadow: 0 10px 20px rgba(37, 99, 235, 0.18);
                color: #FFFFFF;
                font-weight: 700;
                padding: 0.65rem 1rem;
            }

            .stButton > button:hover,
            .stDownloadButton > button:hover {
                filter: brightness(1.02);
            }

            .stMultiSelect [data-baseweb="select"],
            .stSelectbox [data-baseweb="select"] {
                background: var(--surface-color);
                border-radius: 12px;
            }

            .stMultiSelect [data-baseweb="tag"] {
                background: var(--primary-soft);
                color: var(--primary-dark);
            }

            .stAlert {
                border-radius: 14px;
            }

            .stCaption,
            .stMarkdown p {
                color: var(--text-color);
            }

            @media (max-width: 991px) {
                .dashboard-title {
                    font-size: 1.8rem;
                }

                .dashboard-hero {
                    padding: 1.35rem 1.2rem;
                }

                .kpi-card {
                    min-height: 150px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
