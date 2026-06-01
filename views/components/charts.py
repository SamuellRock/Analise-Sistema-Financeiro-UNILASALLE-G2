"""Chart factory functions for the Streamlit dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def create_default_color_map() -> dict[str, str]:
    return {
        "Norte": "#2563eb",
        "Nordeste": "#0891b2",
        "Centro-Oeste": "#16a34a",
        "Sudeste": "#f59e0b",
        "Sul": "#dc2626",
        "Cartão": "#2563eb",
        "Credito pessoal": "#7c3aed",
        "Crédito pessoal": "#7c3aed",
        "Empresarial": "#0f766e",
        "Imobiliário": "#f59e0b",
        "Veículos": "#dc2626",
        "Baixo": "#16a34a",
        "Médio": "#f59e0b",
        "Medio": "#f59e0b",
        "Alto": "#dc2626",
    }


def _bar_chart(df: pd.DataFrame, x: str, y: str, color: str, title: str, orientation: str = "v"):
    return px.bar(
        df,
        x=x if orientation == "v" else y,
        y=y if orientation == "v" else x,
        color=color,
        title=title,
        orientation=orientation,
        text_auto=".2s",
    )


def create_credit_by_region_chart(df: pd.DataFrame):
    fig = _bar_chart(df, "regiao", "volume_total_credito", "regiao", "Volume de credito por regiao")
    fig.update_layout(showlegend=False, yaxis_title="Volume total de credito", xaxis_title="Regiao")
    return fig


def create_credit_by_uf_chart(df: pd.DataFrame):
    top_df = df.sort_values("volume_total_credito", ascending=False).head(10)
    fig = _bar_chart(top_df, "uf", "volume_total_credito", "uf", "Top 10 UFs por volume de credito", orientation="h")
    fig.update_layout(showlegend=False, xaxis_title="Volume total de credito", yaxis_title="UF")
    return fig


def create_credit_by_modality_chart(df: pd.DataFrame):
    fig = _bar_chart(df, "modalidade_credito", "volume_total_credito", "modalidade_credito", "Volume de credito por modalidade")
    fig.update_layout(showlegend=False, xaxis_title="Modalidade", yaxis_title="Volume total de credito")
    return fig


def create_inadimplencia_by_modality_chart(df: pd.DataFrame):
    ordered = df.sort_values("inadimplencia_media", ascending=False)
    fig = px.bar(
        ordered,
        x="modalidade_credito",
        y="inadimplencia_media",
        color="modalidade_credito",
        title="Inadimplencia media por modalidade",
        text_auto=".2f",
    )
    fig.update_layout(showlegend=False, xaxis_title="Modalidade", yaxis_title="Inadimplencia media")
    return fig


def create_credit_evolution_chart(df: pd.DataFrame):
    fig = px.line(
        df,
        x="periodo_rotulo",
        y="volume_total_credito",
        markers=True,
        title="Evolucao temporal do volume de credito",
    )
    fig.update_layout(xaxis_title="Periodo", yaxis_title="Volume total de credito")
    return fig


def create_inadimplencia_evolution_chart(df: pd.DataFrame):
    fig = px.line(
        df,
        x="periodo_rotulo",
        y="inadimplencia_media",
        markers=True,
        title="Evolucao temporal da inadimplencia media",
    )
    fig.update_layout(xaxis_title="Periodo", yaxis_title="Inadimplencia media")
    return fig


def create_taxa_juros_evolution_chart(df: pd.DataFrame):
    fig = px.line(
        df,
        x="periodo_rotulo",
        y="taxa_media_juros",
        markers=True,
        title="Evolucao temporal da taxa media de juros",
    )
    fig.update_layout(xaxis_title="Periodo", yaxis_title="Taxa media de juros")
    return fig


def create_temporal_heatmap(df: pd.DataFrame):
    heatmap_df = (
        df.copy()
        .assign(
            ano=df["periodo_rotulo"].str[-4:].astype(int),
            mes_rotulo=df["periodo_rotulo"].str[:3],
        )
        .pivot_table(index="ano", columns="mes_rotulo", values="volume_total_credito", aggfunc="sum")
        .fillna(0)
    )
    return px.imshow(
        heatmap_df,
        text_auto=".2s",
        aspect="auto",
        color_continuous_scale="Blues",
        title="Heatmap temporal do volume de credito",
    )


def create_juro_vs_inadimplencia_scatter(df: pd.DataFrame):
    fig = px.scatter(
        df,
        x="taxa_juros",
        y="inadimplencia_percentual",
        color="risco_credito",
        hover_data=["regiao", "uf", "modalidade_credito", "setor_economico"],
        title="Relacao entre juros e inadimplencia",
        opacity=0.6,
    )
    fig.update_layout(xaxis_title="Taxa de juros", yaxis_title="Inadimplencia percentual")
    return fig


def create_risk_distribution_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="risco_credito",
        y="quantidade_registros",
        color="risco_credito",
        title="Distribuicao por risco de credito",
        text_auto=True,
    )
    fig.update_layout(showlegend=False, xaxis_title="Risco de credito", yaxis_title="Quantidade de registros")
    return fig
