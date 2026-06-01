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
    df = pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["data"])
    return df


def _render_intro() -> None:
    st.title("Analise do Sistema Financeiro e Credito no Brasil")
    st.markdown(
        """
        Este dashboard organiza os principais resultados do projeto academico a partir da base tratada
        e dos modulos analiticos ja estruturados. A proposta e permitir leitura executiva, exploracao
        por filtros e comparacao entre dimensoes temporais, territoriais, setoriais e de risco.
        """
    )
    st.markdown(
        """
        <div class="dashboard-note">
            <strong>Notas metodologicas:</strong> a base utilizada e simulada; <code>operacao_critica</code> deve ser lida como sinalizador exploratorio amplo;
            e correlacao nao implica causalidade.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_overview_tab(filtered_df: pd.DataFrame) -> None:
    kpis = calculate_general_kpis(filtered_df)
    render_kpi_cards(kpis)

    regiao_df = calculate_ranking_by_region(filtered_df)
    modalidade_df = calculate_ranking_by_modality(filtered_df)

    st.markdown(
        f"""
        No recorte filtrado, o dashboard resume uma carteira com volume total de {formatar_moeda_brl(kpis['volume_total_credito'])},
        taxa media de juros de {formatar_percentual(kpis['taxa_media_juros'])} e inadimplencia media de
        {formatar_percentual(kpis['inadimplencia_media'])}. Essa visao geral ajuda a localizar rapidamente
        escala, custo e pressao de risco no subconjunto analisado.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_credit_by_region_chart(regiao_df),
            use_container_width=True,
            key="overview_credit_region",
        )
    with col2:
        st.plotly_chart(
            create_credit_by_modality_chart(modalidade_df),
            use_container_width=True,
            key="overview_credit_modality",
        )

    render_table(
        regiao_df[["regiao", "volume_total_credito", "inadimplencia_media", "taxa_media_juros", "percentual_operacoes_criticas"]],
        "Tabela agregada por regiao",
    )


def _render_temporal_tab(filtered_df: pd.DataFrame) -> None:
    monthly_df = calculate_monthly_summary(filtered_df)
    st.markdown(
        """
        A aba temporal destaca que o comportamento do credito nao deve ser resumido a uma unica tendencia linear.
        O usuario pode observar oscilacoes de volume, custo e inadimplencia ao longo do tempo e comparar
        concentracoes mensais no recorte filtrado.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_credit_evolution_chart(monthly_df),
            use_container_width=True,
            key="temporal_credit_evolution",
        )
    with col2:
        st.plotly_chart(
            create_inadimplencia_evolution_chart(monthly_df),
            use_container_width=True,
            key="temporal_default_evolution",
        )

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(
            create_taxa_juros_evolution_chart(monthly_df),
            use_container_width=True,
            key="temporal_interest_evolution",
        )
    with col4:
        st.plotly_chart(
            create_temporal_heatmap(monthly_df),
            use_container_width=True,
            key="temporal_credit_heatmap",
        )


def _render_regional_tab(filtered_df: pd.DataFrame) -> None:
    regiao_df = calculate_ranking_by_region(filtered_df)
    uf_df = calculate_ranking_by_uf(filtered_df)
    st.markdown(
        """
        A leitura territorial permite separar escala financeira e risco territorial. Em varios recortes,
        as UFs e regioes de maior volume nao coincidem automaticamente com os maiores niveis medios de inadimplencia.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_credit_by_region_chart(regiao_df),
            use_container_width=True,
            key="regional_credit_region",
        )
    with col2:
        st.plotly_chart(
            create_credit_by_uf_chart(uf_df),
            use_container_width=True,
            key="regional_credit_uf",
        )

    regional_detail = regiao_df[
        ["regiao", "volume_total_credito", "inadimplencia_media", "taxa_media_juros", "percentual_operacoes_criticas"]
    ]
    render_table(regional_detail, "Tabela agregada por regiao")


def _render_business_tab(filtered_df: pd.DataFrame) -> None:
    modalidade_df = calculate_ranking_by_modality(filtered_df)
    setor_df = calculate_ranking_by_sector(filtered_df)
    st.markdown(
        """
        Modalidades e setores ajudam a entender o mix de negocio da carteira. O dashboard permite comparar
        volume, juros e inadimplencia para evitar leituras simplificadas baseadas em um unico ranking.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_credit_by_modality_chart(modalidade_df),
            use_container_width=True,
            key="business_credit_modality",
        )
    with col2:
        st.plotly_chart(
            create_inadimplencia_by_modality_chart(modalidade_df),
            use_container_width=True,
            key="business_default_modality",
        )

    render_table(
        setor_df[["setor_economico", "volume_total_credito", "inadimplencia_media", "taxa_media_juros", "percentual_operacoes_criticas"]],
        "Tabela agregada por setor",
    )


def _render_risk_tab(filtered_df: pd.DataFrame) -> None:
    risk_df = calculate_risk_summary(filtered_df)
    st.markdown(
        """
        Esta secao aprofunda a comparacao por risco de credito e reforca que correlacao nao implica causalidade.
        As relacoes entre juros, inadimplencia e risco devem ser lidas como associacoes exploratorias.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_risk_distribution_chart(risk_df),
            use_container_width=True,
            key="risk_distribution",
        )
    with col2:
        st.plotly_chart(
            create_juro_vs_inadimplencia_scatter(filtered_df),
            use_container_width=True,
            key="risk_interest_default_scatter",
        )

    render_table(
        risk_df[["risco_credito", "quantidade_registros", "volume_total_credito", "inadimplencia_media", "taxa_media_juros", "percentual_operacoes_criticas"]],
        "Resumo por risco de credito",
    )
    st.caption("`operacao_critica` permanece como sinalizador exploratorio amplo e nao deve ser interpretado como classificacao definitiva de risco.")


def _render_table_tab(filtered_df: pd.DataFrame) -> None:
    st.markdown(
        """
        A tabela analitica permite inspecionar o recorte filtrado da base tratada e baixar o CSV correspondente
        para apoio a leituras complementares.
        """
    )
    render_download_button(filtered_df)
    render_table(filtered_df, "Tabela analitica filtrada")


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
    st.subheader("Conclusao executiva")
    st.markdown(
        """
        O dashboard permite observar uma carteira de credito com escala relevante, distribuicao territorial desigual,
        diferencas importantes entre modalidades e setores e correlacoes fracas nas relacoes centrais ligadas a inadimplencia.
        A interface foi desenhada para apoiar leitura academica e executiva, sem extrapolar para inferencias causais
        que nao estejam sustentadas pela base simulada e pelos resultados do notebook.
        """
    )
