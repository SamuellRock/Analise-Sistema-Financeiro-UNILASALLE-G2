"""Chart factory functions for the Streamlit dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.express as px


CHART_COLORS = ["#2563EB", "#3B82F6", "#60A5FA", "#93C5FD", "#1E3A8A", "#BFDBFE"]
RISK_COLOR_MAP = {"Baixo": "#93C5FD", "Medio": "#3B82F6", "Médio": "#3B82F6", "Alto": "#1E3A8A"}


def create_default_color_map() -> dict[str, str]:
    """Preserve the original chart color map API for package imports."""
    return {
        "Norte": "#2563EB",
        "Nordeste": "#3B82F6",
        "Centro-Oeste": "#60A5FA",
        "Sudeste": "#1E3A8A",
        "Sul": "#93C5FD",
        "Cartao": "#2563EB",
        "Credito pessoal": "#3B82F6",
        "Crédito pessoal": "#3B82F6",
        "Empresarial": "#60A5FA",
        "Imobiliário": "#1E3A8A",
        "Imobiliario": "#1E3A8A",
        "Veículos": "#93C5FD",
        "Veiculos": "#93C5FD",
        **RISK_COLOR_MAP,
    }


def apply_chart_layout(fig, title: str | None = None, height: int = 420):
    """Apply the common Plotly layout used across the dashboard."""
    fig.update_layout(
        title=title,
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        colorway=CHART_COLORS,
        font=dict(color="#0F172A", family="Trebuchet MS, Segoe UI, sans-serif", size=13),
        margin=dict(l=20, r=20, t=60, b=30),
        height=height,
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#DBEAFE", font=dict(color="#0F172A")),
        legend=dict(
            bgcolor="rgba(255,255,255,0.86)",
            bordercolor="#E2E8F0",
            borderwidth=1,
            font=dict(size=11),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#E2E8F0",
        tickfont=dict(color="#64748B"),
        title_font=dict(color="#0F172A"),
        zeroline=False,
    )
    fig.update_yaxes(
        gridcolor="#E2E8F0",
        griddash="dot",
        linecolor="#E2E8F0",
        tickfont=dict(color="#64748B"),
        title_font=dict(color="#0F172A"),
        zeroline=False,
    )
    return fig


def _bar_chart(df: pd.DataFrame, x: str, y: str, color: str, title: str, orientation: str = "v"):
    fig = px.bar(
        df,
        x=x if orientation == "v" else y,
        y=y if orientation == "v" else x,
        color=color,
        title=title,
        orientation=orientation,
        text_auto=".2s",
        color_discrete_sequence=CHART_COLORS,
    )
    fig.update_traces(
        marker_line_color="#FFFFFF",
        marker_line_width=0.8,
        textfont=dict(color="#0F172A", size=11),
        hovertemplate="%{y}: %{x}<extra></extra>" if orientation == "h" else "%{x}: %{y}<extra></extra>",
    )
    return apply_chart_layout(fig, title=title)


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
        color_discrete_sequence=CHART_COLORS,
    )
    fig.update_traces(marker_line_color="#FFFFFF", marker_line_width=0.8, textfont=dict(color="#0F172A", size=11))
    fig.update_layout(showlegend=False, xaxis_title="Modalidade", yaxis_title="Inadimplencia media")
    return apply_chart_layout(fig, title="Inadimplencia media por modalidade")


def create_credit_evolution_chart(df: pd.DataFrame):
    fig = px.line(
        df,
        x="periodo_rotulo",
        y="volume_total_credito",
        markers=True,
        title="Evolucao temporal do volume de credito",
        color_discrete_sequence=[CHART_COLORS[0]],
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=7, line=dict(width=1, color="#FFFFFF")))
    fig.update_layout(xaxis_title="Periodo", yaxis_title="Volume total de credito")
    return apply_chart_layout(fig, title="Evolucao temporal do volume de credito")


def create_inadimplencia_evolution_chart(df: pd.DataFrame):
    fig = px.line(
        df,
        x="periodo_rotulo",
        y="inadimplencia_media",
        markers=True,
        title="Evolucao temporal da inadimplencia media",
        color_discrete_sequence=[CHART_COLORS[1]],
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=7, line=dict(width=1, color="#FFFFFF")))
    fig.update_layout(xaxis_title="Periodo", yaxis_title="Inadimplencia media")
    return apply_chart_layout(fig, title="Evolucao temporal da inadimplencia media")


def create_taxa_juros_evolution_chart(df: pd.DataFrame):
    fig = px.line(
        df,
        x="periodo_rotulo",
        y="taxa_media_juros",
        markers=True,
        title="Evolucao temporal da taxa media de juros",
        color_discrete_sequence=[CHART_COLORS[4]],
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=7, line=dict(width=1, color="#FFFFFF")))
    fig.update_layout(xaxis_title="Periodo", yaxis_title="Taxa media de juros")
    return apply_chart_layout(fig, title="Evolucao temporal da taxa media de juros")


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
    fig = px.imshow(
        heatmap_df,
        text_auto=".2s",
        aspect="auto",
        color_continuous_scale=["#EFF6FF", "#BFDBFE", "#60A5FA", "#2563EB", "#1E3A8A"],
        title="Heatmap temporal do volume de credito",
    )
    fig.update_layout(coloraxis_colorbar=dict(title="Volume", thickness=12))
    return apply_chart_layout(fig, title="Heatmap temporal do volume de credito")


def create_juro_vs_inadimplencia_scatter(df: pd.DataFrame):
    fig = px.scatter(
        df,
        x="taxa_juros",
        y="inadimplencia_percentual",
        color="risco_credito",
        color_discrete_map=RISK_COLOR_MAP,
        hover_data=["regiao", "uf", "modalidade_credito", "setor_economico"],
        title="Relacao entre juros e inadimplencia",
        opacity=0.62,
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=0.6, color="#FFFFFF")))
    fig.update_layout(xaxis_title="Taxa de juros", yaxis_title="Inadimplencia percentual")
    return apply_chart_layout(fig, title="Relacao entre juros e inadimplencia")


def create_risk_distribution_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="risco_credito",
        y="quantidade_registros",
        color="risco_credito",
        color_discrete_map=RISK_COLOR_MAP,
        title="Distribuicao por risco de credito",
        text_auto=True,
    )
    fig.update_traces(marker_line_color="#FFFFFF", marker_line_width=0.8, textfont=dict(color="#0F172A", size=11))
    fig.update_layout(showlegend=False, xaxis_title="Risco de credito", yaxis_title="Quantidade de registros")
    return apply_chart_layout(fig, title="Distribuicao por risco de credito")
