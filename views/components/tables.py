"""Tabular rendering helpers for the Streamlit dashboard."""

from __future__ import annotations

from io import BytesIO

import pandas as pd
import streamlit as st

from src.utils.helpers import formatar_moeda_brl, formatar_numero, formatar_percentual


DISPLAY_LABELS = {
    "ano": "Ano",
    "mes": "Mes",
    "data": "Data",
    "regiao": "Regiao",
    "uf": "UF",
    "modalidade_credito": "Modalidade de credito",
    "setor_economico": "Setor economico",
    "risco_credito": "Risco de credito",
    "faixa_inadimplencia": "Faixa de inadimplencia",
    "faixa_juros": "Faixa de juros",
    "valor_credito": "Valor de credito",
    "volume_total_credito": "Volume total de credito",
    "credito_medio_por_cliente": "Credito medio por cliente",
    "quantidade_clientes": "Quantidade de clientes",
    "total_clientes": "Total de clientes",
    "taxa_juros": "Taxa de juros",
    "taxa_media_juros": "Taxa media de juros",
    "inadimplencia_percentual": "Inadimplencia percentual",
    "inadimplencia_media": "Inadimplencia media",
    "renda_media": "Renda media",
    "renda_media_geral": "Renda media geral",
    "prazo_medio_pagamento": "Prazo medio de pagamento",
    "quantidade_registros": "Quantidade de registros",
    "percentual_operacoes_criticas": "Operacoes criticas (%)",
    "participacao_credito_percentual": "Participacao no credito (%)",
    "operacao_critica": "Operacao critica",
    "periodo": "Periodo bruto",
    "ano_mes": "Ano mes",
    "periodo_rotulo": "Periodo exibido",
    "trimestre": "Trimestre",
    "nome_mes": "Nome do mes",
    "risco_score": "Risco score",
    "risco_medio": "Risco medio",
    "risco_credito_normalizado": "Risco de credito normalizado",
    "faixa_renda": "Faixa de renda",
    "faixa_prazo_pagamento": "Faixa de prazo de pagamento",
    "ordem_periodo": "Ordem do periodo",
}

CURRENCY_COLUMNS = {
    "valor_credito",
    "volume_total_credito",
    "credito_medio_por_cliente",
    "renda_media",
    "renda_media_geral",
}
PERCENT_COLUMNS = {
    "taxa_juros",
    "taxa_media_juros",
    "inadimplencia_percentual",
    "inadimplencia_media",
    "percentual_operacoes_criticas",
    "participacao_credito_percentual",
}
INTEGER_COLUMNS = {"ano", "mes", "quantidade_clientes", "total_clientes", "quantidade_registros"}
DECIMAL_COLUMNS = {"prazo_medio_pagamento", "risco_score", "risco_medio"}


def _format_decimal(value) -> str:
    if pd.isna(value):
        return "-"
    return f"{float(value):.2f}".replace(".", ",")


def _format_table_for_display(df: pd.DataFrame) -> pd.DataFrame:
    display_df = df.copy()
    for column in display_df.columns:
        if column in CURRENCY_COLUMNS:
            display_df[column] = display_df[column].apply(formatar_moeda_brl)
        elif column in PERCENT_COLUMNS:
            display_df[column] = display_df[column].apply(formatar_percentual)
        elif column in INTEGER_COLUMNS:
            display_df[column] = display_df[column].apply(formatar_numero)
        elif column in DECIMAL_COLUMNS:
            display_df[column] = display_df[column].apply(_format_decimal)
        elif pd.api.types.is_datetime64_any_dtype(display_df[column]):
            display_df[column] = display_df[column].dt.strftime("%d/%m/%Y")

    renamed_columns = {column: DISPLAY_LABELS.get(column, column.replace("_", " ").title()) for column in display_df.columns}
    return display_df.rename(columns=renamed_columns)


def render_table(
    df: pd.DataFrame,
    title: str,
    description: str = "Tabela de apoio para aprofundar a leitura do recorte selecionado.",
    use_container_width: bool = True,
) -> None:
    """Render a table with title, context and formatted values."""
    st.markdown(f'<div class="table-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="table-description">{description}</div>', unsafe_allow_html=True)
    dataframe_width = "stretch" if use_container_width else "content"
    st.dataframe(_format_table_for_display(df), width=dataframe_width, hide_index=True)


def render_download_button(df: pd.DataFrame, label: str = "Baixar CSV filtrado") -> None:
    """Render a CSV download button for the filtered dataset."""
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=BytesIO(csv_bytes),
        file_name="dados_filtrados_dashboard.csv",
        mime="text/csv",
    )
