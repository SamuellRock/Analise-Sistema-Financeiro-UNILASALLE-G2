"""Tabular rendering helpers for the Streamlit dashboard."""

from __future__ import annotations

from io import BytesIO

import pandas as pd
import streamlit as st


def render_table(df: pd.DataFrame, title: str, use_container_width: bool = True) -> None:
    """Render a table with a title."""
    st.markdown(f"**{title}**")
    st.dataframe(df, use_container_width=use_container_width, hide_index=True)


def render_download_button(df: pd.DataFrame, label: str = "Baixar CSV filtrado") -> None:
    """Render a simple CSV download button for the filtered dataset."""
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=BytesIO(csv_bytes),
        file_name="dados_filtrados_dashboard.csv",
        mime="text/csv",
    )
