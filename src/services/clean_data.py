"""Data cleaning functions that reproduce the notebook cleaning stage."""

from __future__ import annotations

from typing import Iterable

import pandas as pd

from src.utils.helpers import normalizar_nome_coluna, normalizar_texto


EXPECTED_YEAR_MIN = 2015
EXPECTED_YEAR_MAX = 2024
MAIN_CATEGORICAL_COLUMNS = [
    "regiao",
    "uf",
    "modalidade_credito",
    "risco_credito",
    "setor_economico",
]
NON_NEGATIVE_COLUMNS = [
    "valor_credito",
    "taxa_juros",
    "inadimplencia_percentual",
    "quantidade_clientes",
    "renda_media",
    "prazo_medio_pagamento",
]


def _replace_empty_strings(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(normalizar_texto)
    return df


def _fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            if df[column].isna().any():
                df[column] = df[column].fillna(df[column].median())
        else:
            if df[column].isna().any():
                df[column] = df[column].fillna("Nao informado")
    return df


def _filter_impossible_values(df: pd.DataFrame) -> pd.DataFrame:
    if not NON_NEGATIVE_COLUMNS:
        return df
    valid_mask = pd.Series(True, index=df.index)
    for column in NON_NEGATIVE_COLUMNS:
        if column in df.columns:
            valid_mask &= df[column] >= 0
    return df.loc[valid_mask].copy()


def clean_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the financial dataset and return a prepared DataFrame."""
    df_clean = df.copy()
    df_clean.columns = [normalizar_nome_coluna(column) for column in df_clean.columns]

    df_clean = _replace_empty_strings(df_clean, MAIN_CATEGORICAL_COLUMNS)

    if "data" in df_clean.columns:
        df_clean["data"] = pd.to_datetime(df_clean["data"], errors="coerce")
        df_clean = df_clean.loc[df_clean["data"].notna()].copy()
        df_clean["ano"] = df_clean["data"].dt.year
        df_clean["mes"] = df_clean["data"].dt.month

    df_clean = df_clean.drop_duplicates().copy()

    for column in MAIN_CATEGORICAL_COLUMNS:
        if column not in df_clean.columns:
            continue
        df_clean[column] = df_clean[column].apply(normalizar_texto)

    if "uf" in df_clean.columns:
        df_clean["uf"] = df_clean["uf"].astype("string").str.upper()

    df_clean = _fill_missing_values(df_clean)

    if "ano" in df_clean.columns:
        df_clean = df_clean.loc[
            df_clean["ano"].between(EXPECTED_YEAR_MIN, EXPECTED_YEAR_MAX)
        ].copy()
    if "mes" in df_clean.columns:
        df_clean = df_clean.loc[df_clean["mes"].between(1, 12)].copy()

    df_clean = _filter_impossible_values(df_clean)

    if "data" in df_clean.columns:
        df_clean["periodo"] = df_clean["data"].dt.to_period("M").astype(str)
        df_clean["ano_mes"] = df_clean["data"].dt.strftime("%Y-%m")
        df_clean["nome_mes"] = df_clean["data"].dt.strftime("%b")
        df_clean["trimestre"] = "T" + df_clean["data"].dt.quarter.astype(str)

    return df_clean.reset_index(drop=True)
