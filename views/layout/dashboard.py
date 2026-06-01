"""Main dashboard assembly for the Streamlit application."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.kpis.kpi_calculations import (
    calculate_general_kpis,
    calculate_monthly_summary,
    calculate_ranking_by_modality,
    calculate_ranking_by_region,
    calculate_ranking_by_sector,
    calculate_ranking_by_uf,
    calculate_risk_summary,
)
from src.utils.helpers import formatar_moeda_brl, formatar_percentual
from views.components.charts import (
    create_credit_by_modality_chart,
    create_credit_by_region_chart,
    create_credit_by_uf_chart,
    create_credit_evolution_chart,
    create_inadimplencia_by_modality_chart,
    create_inadimplencia_evolution_chart,
    create_juro_vs_inadimplencia_scatter,
    create_risk_distribution_chart,
    create_taxa_juros_evolution_chart,
    create_temporal_heatmap,
)
from views.components.filters import apply_dashboard_filters, render_filters
from views.components.kpi_cards import render_kpi_cards
from views.components.tables import render_download_button, render_table


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_PATH = PROJECT_ROOT / "database" / "processed" / "dados_tratados.csv"


@st.cache_data(show_spinner=False)
def load_dashboard_data() -> pd.DataFrame:
    """Load the processed dashboard dataset with Streamlit cache."""
    return pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["data"])


def _render_intro() -> None:
    st.markdown(
        """
        <div class="dashboard-hero">
            <div class="dashboard-eyebrow">Feito por: Samuel Elias da Silva Rocha</div>
            <h1 class="dashboard-title">Dashboard Financeiro Brasil</h1>
            <p class="dashboard-subtitle">
                Analise exploratoria de credito, inadimplencia, juros e risco com base simulada entre 2015 e 2024.
                O foco e combinar leitura academica com uma visao executiva limpa e comparavel entre recortes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_section_header(title: str, description: str) -> None:
    st.markdown(f'<div class="section-heading">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-description">{description}</div>', unsafe_allow_html=True)


def _render_overview_tab(filtered_df: pd.DataFrame) -> None:
    kpis = calculate_general_kpis(filtered_df)
    regiao_df = calculate_ranking_by_region(filtered_df)
    modalidade_df = calculate_ranking_by_modality(filtered_df)

    _render_section_header(
        "Painel executivo",
        "Os indicadores abaixo sintetizam escala, custo, risco e perfil da carteira no recorte selecionado.",
    )
    render_kpi_cards(kpis)

    st.markdown(
        f"""
        No recorte filtrado, a carteira observada acumula {formatar_moeda_brl(kpis['volume_total_credito'])},
        com taxa media de juros de {formatar_percentual(kpis['taxa_media_juros'])} e inadimplencia media de
        {formatar_percentual(kpis['inadimplencia_media'])}. A combinacao entre distribuicao regional e modalidades
        ajuda a identificar onde o volume se concentra e como o mix de negocio muda entre os segmentos.
        """
    )

    _render_section_header(
        "Distribuicao territorial e mix de credito",
        "Compare a concentracao de volume por regiao e o peso relativo das modalidades de credito no mesmo recorte.",
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_credit_by_region_chart(regiao_df),
            width="stretch",
            key="overview_credit_region",
        )
    with col2:
        st.plotly_chart(
            create_credit_by_modality_chart(modalidade_df),
            width="stretch",
            key="overview_credit_modality",
        )

    render_table(
        regiao_df[["regiao", "volume_total_credito", "inadimplencia_media", "taxa_media_juros", "percentual_operacoes_criticas"]],
        "Tabela agregada por regiao",
        "Resumo tabular para confrontar volume, custo e risco medio entre as grandes regioes.",
    )


def _render_temporal_tab(filtered_df: pd.DataFrame) -> None:
    monthly_df = calculate_monthly_summary(filtered_df)
    _render_section_header(
        "Leitura temporal",
        "A evolucao mensal mostra oscilacoes no volume, no custo do credito e na pressao de inadimplencia ao longo do periodo.",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_credit_evolution_chart(monthly_df),
            width="stretch",
            key="temporal_credit_evolution",
        )
    with col2:
        st.plotly_chart(
            create_inadimplencia_evolution_chart(monthly_df),
            width="stretch",
            key="temporal_default_evolution",
        )

    _render_section_header(
        "Pressao de custo e sazonalidade",
        "A combinacao entre juros medios e heatmap facilita a identificacao de picos, sazonalidade e mudancas de ritmo.",
    )
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(
            create_taxa_juros_evolution_chart(monthly_df),
            width="stretch",
            key="temporal_interest_evolution",
        )
    with col4:
        st.plotly_chart(
            create_temporal_heatmap(monthly_df),
            width="stretch",
            key="temporal_credit_heatmap",
        )


def _render_regional_tab(filtered_df: pd.DataFrame) -> None:
    regiao_df = calculate_ranking_by_region(filtered_df)
    uf_df = calculate_ranking_by_uf(filtered_df)

    _render_section_header(
        "Escala territorial",
        "A comparacao entre regioes e UFs mostra onde o credito se concentra e como a exposicao territorial se distribui.",
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_credit_by_region_chart(regiao_df),
            width="stretch",
            key="regional_credit_region",
        )
    with col2:
        st.plotly_chart(
            create_credit_by_uf_chart(uf_df),
            width="stretch",
            key="regional_credit_uf",
        )

    regional_detail = regiao_df[
        ["regiao", "volume_total_credito", "inadimplencia_media", "taxa_media_juros", "percentual_operacoes_criticas"]
    ]
    render_table(
        regional_detail,
        "Tabela agregada por regiao",
        "Quadro sintese para comparar o equilibrio entre volume, juros e operacoes criticas em cada regiao.",
    )


def _render_business_tab(filtered_df: pd.DataFrame) -> None:
    modalidade_df = calculate_ranking_by_modality(filtered_df)
    setor_df = calculate_ranking_by_sector(filtered_df)

    _render_section_header(
        "Modalidades e setores",
        "O painel abaixo ajuda a entender o mix de negocio da carteira e as diferencas de desempenho entre segmentos.",
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_credit_by_modality_chart(modalidade_df),
            width="stretch",
            key="business_credit_modality",
        )
    with col2:
        st.plotly_chart(
            create_inadimplencia_by_modality_chart(modalidade_df),
            width="stretch",
            key="business_default_modality",
        )

    render_table(
        setor_df[["setor_economico", "volume_total_credito", "inadimplencia_media", "taxa_media_juros", "percentual_operacoes_criticas"]],
        "Tabela agregada por setor",
        "Visao tabular para aprofundar a leitura do mix setorial e seus niveis medios de risco.",
    )


def _render_risk_tab(filtered_df: pd.DataFrame) -> None:
    risk_df = calculate_risk_summary(filtered_df)

    _render_section_header(
        "Risco e inadimplencia",
        "Esta secao aprofunda a leitura por classe de risco e reforca a interpretacao exploratoria das associacoes observadas.",
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_risk_distribution_chart(risk_df),
            width="stretch",
            key="risk_distribution",
        )
    with col2:
        st.plotly_chart(
            create_juro_vs_inadimplencia_scatter(filtered_df),
            width="stretch",
            key="risk_interest_default_scatter",
        )

    render_table(
        risk_df[["risco_credito", "quantidade_registros", "volume_total_credito", "inadimplencia_media", "taxa_media_juros", "percentual_operacoes_criticas"]],
        "Resumo por risco de credito",
        "Tabela de apoio para comparar frequencia, volume e custo medio entre as faixas de risco.",
    )
    st.caption(
        "`operacao_critica` permanece como sinalizador exploratorio amplo e nao deve ser interpretado como classificacao definitiva de risco."
    )


def _render_table_tab(filtered_df: pd.DataFrame) -> None:
    _render_section_header(
        "Base filtrada para apoio analitico",
        "Use a tabela abaixo para inspecionar o recorte aplicado e baixar o CSV correspondente para leituras complementares.",
    )
    render_download_button(filtered_df)
    render_table(
        filtered_df,
        "Tabela analitica filtrada",
        "Visualizacao completa da base tratada apos a aplicacao dos filtros da sidebar.",
    )


def render_dashboard() -> None:
    """Render the full Streamlit dashboard."""
    _render_intro()
    df = load_dashboard_data()
    selections = render_filters(df)
    filtered_df = apply_dashboard_filters(df, selections)

    if filtered_df.empty:
        st.warning("Os filtros selecionados nao retornaram registros. Ajuste os filtros para continuar a analise.")
        st.stop()

    tabs = st.tabs(
        [
            "Visao Geral",
            "Evolucao Temporal",
            "Analise Regional",
            "Modalidades e Setores",
            "Risco e Inadimplencia",
            "Tabela Analitica",
        ]
    )

    with tabs[0]:
        _render_overview_tab(filtered_df)
    with tabs[1]:
        _render_temporal_tab(filtered_df)
    with tabs[2]:
        _render_regional_tab(filtered_df)
    with tabs[3]:
        _render_business_tab(filtered_df)
    with tabs[4]:
        _render_risk_tab(filtered_df)
    with tabs[5]:
        _render_table_tab(filtered_df)

    st.markdown("---")
    _render_section_header(
        "Conclusao executiva",
        "O dashboard foi organizado para apoiar uma leitura academica-profissional da carteira sem alterar dados, KPIs ou regras de filtro.",
    )
    st.markdown(
        """
        O painel evidencia uma carteira de credito com distribuicao territorial desigual, diferencas relevantes
        entre modalidades e setores e relacoes exploratorias entre juros, inadimplencia e risco. A estrutura visual
        privilegia leitura rapida, comparabilidade e consistencia, mantendo a integridade do pipeline analitico original.
        """
    )
