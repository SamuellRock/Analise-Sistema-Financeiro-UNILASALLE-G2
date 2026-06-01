"""Theme and visual configuration for the Streamlit dashboard."""

from __future__ import annotations

import streamlit as st


def configure_page() -> None:
    """Configure the base Streamlit page settings."""
    st.set_page_config(
        page_title="Analise do Sistema Financeiro e Credito no Brasil",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_theme() -> None:
    """Apply a light visual style using native Streamlit resources."""
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2rem;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.6rem;
            }
            [data-testid="stMetricLabel"] {
                font-size: 0.95rem;
            }
            .dashboard-note {
                padding: 0.8rem 1rem;
                border: 1px solid rgba(49, 51, 63, 0.1);
                border-radius: 8px;
                background: rgba(246, 248, 250, 0.9);
                margin-bottom: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
