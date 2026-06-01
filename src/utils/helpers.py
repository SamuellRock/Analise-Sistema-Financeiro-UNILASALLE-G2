"""Reusable helper functions for normalization, formatting and percentages."""

from __future__ import annotations

import math
import unicodedata

import pandas as pd


def normalizar_nome_coluna(nome: str) -> str:
    """Normalize a column name to snake_case without accents."""
    texto = unicodedata.normalize("NFKD", str(nome).strip().lower())
    texto = texto.encode("ascii", "ignore").decode("ascii")
    partes = texto.replace("-", " ").replace("/", " ").split()
    return "_".join(partes)


def normalizar_texto(valor):
    """Strip text values and collapse internal spaces while preserving content."""
    if pd.isna(valor):
        return pd.NA
    texto = " ".join(str(valor).strip().split())
    return texto if texto else pd.NA


def formatar_moeda_brl(valor) -> str:
    """Format a numeric value as BRL currency text."""
    if valor is None or (isinstance(valor, float) and math.isnan(valor)):
        return "R$ 0,00"
    texto = f"{float(valor):,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def formatar_percentual(valor) -> str:
    """Format a numeric value as percentage text."""
    if valor is None or (isinstance(valor, float) and math.isnan(valor)):
        return "0,00%"
    texto = f"{float(valor):.2f}".replace(".", ",")
    return f"{texto}%"


def formatar_numero(valor) -> str:
    """Format a numeric value using Brazilian separators."""
    if valor is None or (isinstance(valor, float) and math.isnan(valor)):
        return "0"
    if float(valor).is_integer():
        texto = f"{int(valor):,}"
    else:
        texto = f"{float(valor):,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_percentual_sim(serie: pd.Series) -> float:
    """Calculate the percentage of values equal to 'Sim' in a series."""
    if serie.empty:
        return 0.0
    serie_texto = serie.astype(str).str.strip().str.lower()
    return float((serie_texto == "sim").mean() * 100.0)
