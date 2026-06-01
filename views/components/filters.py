"""Sidebar filters for the Streamlit dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st


FILTER_COLUMNS = [
    "ano",
    "mes",
    "regiao",
    "uf",
    "modalidade_credito",
    "setor_economico",
    "risco_credito",
    "faixa_inadimplencia",
    "faixa_juros",
]


FILTER_LABELS = {
    "ano": "Ano",
    "mes": "Mes",
    "regiao": "Regiao",
    "uf": "UF",
    "modalidade_credito": "Modalidade de credito",
    "setor_economico": "Setor economico",
    "risco_credito": "Risco de credito",
    "faixa_inadimplencia": "Faixa de inadimplencia",
    "faixa_juros": "Faixa de juros",
}


MENU_ITEMS = [
    "Visao Geral",
    "Evolucao Temporal",
    "Analise Regional",
    "Modalidades e Setores",
    "Risco e Inadimplencia",
    "Tabela Analitica",
]


def _normalize_selection(selection, default_values):
    return selection if selection else list(default_values)


def _render_sidebar_identity() -> None:
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-title">Sistema Financeiro BR</div>
            <div class="sidebar-subtitle">Analise de credito, risco, juros e distribuicao territorial da base simulada do projeto.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown('<div class="sidebar-section-title">Menu</div>', unsafe_allow_html=True)
    menu_markup = "".join(
        f'<div class="sidebar-menu-item"><span class="sidebar-menu-bullet">{index}</span><span>{item}</span></div>'
        for index, item in enumerate(MENU_ITEMS, start=1)
    )
    st.sidebar.markdown(f'<div class="sidebar-menu">{menu_markup}</div>', unsafe_allow_html=True)

    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)


def _render_sidebar_footer() -> None:
    st.sidebar.markdown('<div class="sidebar-section-title">Sobre a analise</div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        """
        <div class="sidebar-copy">
            A leitura do painel e exploratoria e academica. Os indicadores refletem apenas o recorte filtrado
            da base tratada entre 2015 e 2024.
        </div>
        <div class="sidebar-copy">
            O marcador <code>operacao_critica</code> continua sendo apenas um sinalizador amplo de atencao,
            sem substituir classificacoes formais de risco.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_filters(df: pd.DataFrame) -> dict[str, list]:
    """Render sidebar filters and return the selected values."""
    _render_sidebar_identity()

    st.sidebar.markdown('<div class="sidebar-section-title">Filtros</div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="sidebar-caption">Selecione os recortes desejados. Se nada for escolhido, o painel considera todos os valores disponiveis.</div>',
        unsafe_allow_html=True,
    )

    selections: dict[str, list] = {}
    for column in FILTER_COLUMNS:
        options = sorted(df[column].dropna().unique().tolist())
        selected = st.sidebar.multiselect(
            FILTER_LABELS[column],
            options=options,
            default=options,
        )
        selections[column] = _normalize_selection(selected, options)

    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    _render_sidebar_footer()
    return selections


def apply_dashboard_filters(df: pd.DataFrame, selections: dict[str, list]) -> pd.DataFrame:
    """Apply the sidebar filters to the dashboard DataFrame."""
    filtered_df = df.copy()
    for column, values in selections.items():
        if values:
            filtered_df = filtered_df.loc[filtered_df[column].isin(values)].copy()
    return filtered_df.reset_index(drop=True)
