"""KPI card rendering helpers."""

from __future__ import annotations

import streamlit as st

from src.utils.helpers import formatar_moeda_brl, formatar_numero, formatar_percentual


def _render_card(column, label: str, value: str, caption: str, support: str, primary: bool = False) -> None:
    card_class = "kpi-card kpi-card--primary" if primary else "kpi-card"
    badge = "Carteira filtrada" if primary else "Indicador sintetico"
    column.markdown(
        f"""
        <div class="{card_class}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-caption">{caption}</div>
            <div class="kpi-support">{support}</div>
            <div class="kpi-badge">{badge}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_cards(kpis: dict) -> None:
    """Render KPI cards with a more editorial visual treatment."""
    cards = [
        {
            "label": "Volume total de credito",
            "value": formatar_moeda_brl(kpis["volume_total_credito"]),
            "caption": "Montante agregado no recorte filtrado",
            "support": "Resume a escala financeira observada na base tratada.",
            "primary": True,
        },
        {
            "label": "Taxa media de juros",
            "value": formatar_percentual(kpis["taxa_media_juros"]),
            "caption": "Custo medio do credito selecionado",
            "support": "Ajuda a comparar precificacao e pressao de custo entre recortes.",
        },
        {
            "label": "Inadimplencia media",
            "value": formatar_percentual(kpis["inadimplencia_media"]),
            "caption": "Nivel medio de atraso no painel",
            "support": "Leitura sintetica do risco observado na carteira filtrada.",
        },
        {
            "label": "Total de clientes",
            "value": formatar_numero(kpis["total_clientes"]),
            "caption": "Base de clientes contemplada",
            "support": "Mostra a abrangencia do recorte analisado no dashboard.",
        },
        {
            "label": "Credito medio por cliente",
            "value": formatar_moeda_brl(kpis["credito_medio_por_cliente"]),
            "caption": "Ticket medio da carteira",
            "support": "Relaciona o volume consolidado ao total de clientes atendidos.",
        },
        {
            "label": "Renda media geral",
            "value": formatar_moeda_brl(kpis["renda_media_geral"]),
            "caption": "Perfil medio de renda",
            "support": "Apoia a leitura do contexto socioeconomico do recorte atual.",
        },
        {
            "label": "Prazo medio de pagamento",
            "value": formatar_numero(kpis["prazo_medio_pagamento"]),
            "caption": "Horizonte medio dos contratos",
            "support": "Importante para interpretar liquidez e ciclo financeiro.",
        },
        {
            "label": "Operacoes criticas",
            "value": formatar_percentual(kpis["percentual_operacoes_criticas"]),
            "caption": "Participacao de registros sinalizados",
            "support": "Mantem o marcador exploratorio sem alterar a logica original.",
        },
    ]

    for start in range(0, len(cards), 4):
        row_columns = st.columns(4)
        for column, card in zip(row_columns, cards[start : start + 4]):
            _render_card(column=column, **card)
