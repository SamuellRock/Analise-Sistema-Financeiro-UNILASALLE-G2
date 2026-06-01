"""Feature engineering functions that reproduce the notebook transformation stage."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.utils.helpers import normalizar_nome_coluna


RISK_SCORE_MAP = {
    "baixo": 1,
    "medio": 2,
    "alto": 3,
}


def _normalize_risk_text(value) -> str:
    return normalizar_nome_coluna(value).replace("_", "")


def _safe_quantile_binning(
    series: pd.Series,
    labels: list[str],
    fallback_prefix: str,
) -> pd.Series:
    clean_series = series.astype(float)
    quantiles = min(len(labels), clean_series.nunique(dropna=True))
    if quantiles <= 1:
        return pd.Series([labels[0]] * len(clean_series), index=clean_series.index, dtype="object")
    try:
        return pd.qcut(
            clean_series,
            q=quantiles,
            labels=labels[:quantiles],
            duplicates="drop",
        )
    except ValueError:
        return pd.cut(
            clean_series,
            bins=quantiles,
            labels=labels[:quantiles] if quantiles <= len(labels) else [f"{fallback_prefix} {i + 1}" for i in range(quantiles)],
            include_lowest=True,
        )


def transform_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the project feature engineering logic to the cleaned dataset."""
    df_transformed = df.copy()

    df_transformed["credito_medio_por_cliente"] = np.where(
        df_transformed["quantidade_clientes"] > 0,
        df_transformed["valor_credito"] / df_transformed["quantidade_clientes"],
        np.nan,
    )
    df_transformed["credito_medio_por_cliente"] = df_transformed["credito_medio_por_cliente"].replace(
        [np.inf, -np.inf],
        np.nan,
    )

    df_transformed["risco_credito_normalizado"] = df_transformed["risco_credito"].apply(_normalize_risk_text)
    df_transformed["risco_score"] = (
        df_transformed["risco_credito_normalizado"].map(RISK_SCORE_MAP).astype("Int64")
    )

    df_transformed["faixa_inadimplencia"] = pd.cut(
        df_transformed["inadimplencia_percentual"],
        bins=[-np.inf, 3, 6, 10, np.inf],
        labels=["Baixa", "Media", "Alta", "Critica"],
        include_lowest=True,
    )
    df_transformed["faixa_juros"] = _safe_quantile_binning(
        df_transformed["taxa_juros"],
        labels=["Juros baixos", "Juros medios", "Juros altos"],
        fallback_prefix="Faixa",
    )
    df_transformed["faixa_renda"] = _safe_quantile_binning(
        df_transformed["renda_media"],
        labels=["Renda baixa", "Renda media", "Renda alta"],
        fallback_prefix="Faixa",
    )
    df_transformed["faixa_prazo_pagamento"] = _safe_quantile_binning(
        df_transformed["prazo_medio_pagamento"],
        labels=["Curto prazo", "Medio prazo", "Longo prazo"],
        fallback_prefix="Faixa",
    )

    # operacao_critica remains an exploratory signal, not a definitive risk model.
    df_transformed["operacao_critica"] = np.where(
        (df_transformed["risco_score"] == 3)
        | (df_transformed["faixa_inadimplencia"].astype(str).isin(["Alta", "Critica"]))
        | (df_transformed["faixa_juros"].astype(str) == "Juros altos"),
        "Sim",
        "Nao",
    )

    total_credito = float(df_transformed["valor_credito"].sum())
    if total_credito > 0:
        df_transformed["participacao_credito_percentual"] = (
            df_transformed["valor_credito"] / total_credito * 100.0
        )
    else:
        df_transformed["participacao_credito_percentual"] = 0.0

    df_transformed["ordem_periodo"] = (df_transformed["ano"] * 100) + df_transformed["mes"]
    if "data" in df_transformed.columns:
        df_transformed["periodo_rotulo"] = df_transformed["data"].dt.strftime("%b/%Y")
    else:
        df_transformed["periodo_rotulo"] = (
            df_transformed["mes"].astype(str).str.zfill(2) + "/" + df_transformed["ano"].astype(str)
        )

    return df_transformed.reset_index(drop=True)
