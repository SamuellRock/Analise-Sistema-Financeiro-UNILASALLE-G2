"""KPI and summary calculations reused by the future dashboard."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.utils.helpers import calcular_percentual_sim


def _add_common_group_metrics(grouped: pd.DataFrame) -> pd.DataFrame:
    grouped["credito_medio_por_cliente"] = np.where(
        grouped["total_clientes"] > 0,
        grouped["volume_total_credito"] / grouped["total_clientes"],
        np.nan,
    )
    return grouped


def calculate_general_kpis(df: pd.DataFrame) -> dict:
    """Calculate the main general KPIs from the transformed dataset."""
    total_credito = float(df["valor_credito"].sum())
    total_clientes = float(df["quantidade_clientes"].sum())
    credito_medio = total_credito / total_clientes if total_clientes > 0 else 0.0
    return {
        "volume_total_credito": total_credito,
        "taxa_media_juros": float(df["taxa_juros"].mean()),
        "inadimplencia_media": float(df["inadimplencia_percentual"].mean()),
        "total_clientes": int(df["quantidade_clientes"].sum()),
        "renda_media_geral": float(df["renda_media"].mean()),
        "prazo_medio_pagamento": float(df["prazo_medio_pagamento"].mean()),
        "credito_medio_por_cliente": float(credito_medio),
        "percentual_operacoes_criticas": float(calcular_percentual_sim(df["operacao_critica"])),
    }


def create_kpis_dataframe(kpis: dict) -> pd.DataFrame:
    """Create a tabular representation of the KPI dictionary."""
    return pd.DataFrame(
        [{"indicador": indicador, "valor": valor} for indicador, valor in kpis.items()]
    )


def _calculate_group_summary(df: pd.DataFrame, group_column: str) -> pd.DataFrame:
    grouped = (
        df.groupby(group_column, dropna=False)
        .agg(
            quantidade_registros=(group_column, "size"),
            volume_total_credito=("valor_credito", "sum"),
            inadimplencia_media=("inadimplencia_percentual", "mean"),
            taxa_media_juros=("taxa_juros", "mean"),
            total_clientes=("quantidade_clientes", "sum"),
            renda_media=("renda_media", "mean"),
            prazo_medio_pagamento=("prazo_medio_pagamento", "mean"),
            risco_medio=("risco_score", "mean"),
        )
        .reset_index()
    )
    grouped = _add_common_group_metrics(grouped)
    criticas = (
        df.groupby(group_column, dropna=False)["operacao_critica"]
        .apply(calcular_percentual_sim)
        .reset_index(name="percentual_operacoes_criticas")
    )
    grouped = grouped.merge(criticas, on=group_column, how="left")
    return grouped.sort_values("volume_total_credito", ascending=False).reset_index(drop=True)


def calculate_ranking_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return _calculate_group_summary(df, "regiao")


def calculate_ranking_by_uf(df: pd.DataFrame) -> pd.DataFrame:
    return _calculate_group_summary(df, "uf")


def calculate_ranking_by_modality(df: pd.DataFrame) -> pd.DataFrame:
    return _calculate_group_summary(df, "modalidade_credito")


def calculate_ranking_by_sector(df: pd.DataFrame) -> pd.DataFrame:
    return _calculate_group_summary(df, "setor_economico")


def calculate_risk_summary(df: pd.DataFrame) -> pd.DataFrame:
    return _calculate_group_summary(df, "risco_credito")


def calculate_annual_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("ano", dropna=False)
        .agg(
            volume_total_credito=("valor_credito", "sum"),
            inadimplencia_media=("inadimplencia_percentual", "mean"),
            taxa_media_juros=("taxa_juros", "mean"),
            total_clientes=("quantidade_clientes", "sum"),
            renda_media=("renda_media", "mean"),
            prazo_medio_pagamento=("prazo_medio_pagamento", "mean"),
            risco_medio=("risco_score", "mean"),
        )
        .reset_index()
        .sort_values("ano")
        .reset_index(drop=True)
    )
    summary = _add_common_group_metrics(summary)
    criticas = (
        df.groupby("ano", dropna=False)["operacao_critica"]
        .apply(calcular_percentual_sim)
        .reset_index(name="percentual_operacoes_criticas")
    )
    return summary.merge(criticas, on="ano", how="left")


def calculate_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["ordem_periodo", "periodo_rotulo"], dropna=False)
        .agg(
            volume_total_credito=("valor_credito", "sum"),
            inadimplencia_media=("inadimplencia_percentual", "mean"),
            taxa_media_juros=("taxa_juros", "mean"),
            total_clientes=("quantidade_clientes", "sum"),
            renda_media=("renda_media", "mean"),
            prazo_medio_pagamento=("prazo_medio_pagamento", "mean"),
            risco_medio=("risco_score", "mean"),
        )
        .reset_index()
        .sort_values("ordem_periodo")
        .reset_index(drop=True)
    )
    summary = _add_common_group_metrics(summary)
    criticas = (
        df.groupby(["ordem_periodo", "periodo_rotulo"], dropna=False)["operacao_critica"]
        .apply(calcular_percentual_sim)
        .reset_index(name="percentual_operacoes_criticas")
    )
    return summary.merge(criticas, on=["ordem_periodo", "periodo_rotulo"], how="left")
