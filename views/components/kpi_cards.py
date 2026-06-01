"""KPI card rendering helpers."""

from __future__ import annotations

import streamlit as st

from src.utils.helpers import formatar_moeda_brl, formatar_numero, formatar_percentual


def render_kpi_cards(kpis: dict) -> None:
    """Render the KPI cards using Streamlit metrics."""
    top_cols = st.columns(3)
    bottom_cols = st.columns(3)
    extra_cols = st.columns(2)

    top_cols[0].metric("Volume total de credito", formatar_moeda_brl(kpis["volume_total_credito"]))
    top_cols[1].metric("Taxa media de juros", formatar_percentual(kpis["taxa_media_juros"]))
    top_cols[2].metric("Inadimplencia media", formatar_percentual(kpis["inadimplencia_media"]))

    bottom_cols[0].metric("Total de clientes", formatar_numero(kpis["total_clientes"]))
    bottom_cols[1].metric("Credito medio por cliente", formatar_moeda_brl(kpis["credito_medio_por_cliente"]))
    bottom_cols[2].metric(
        "Percentual de operacoes criticas",
        formatar_percentual(kpis["percentual_operacoes_criticas"]),
    )

    extra_cols[0].metric("Renda media geral", formatar_moeda_brl(kpis["renda_media_geral"]))
    extra_cols[1].metric("Prazo medio de pagamento", formatar_numero(kpis["prazo_medio_pagamento"]))
