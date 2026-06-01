"""Functions for loading the original dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = PROJECT_ROOT / "dados" / "simulacao_sistema_financeiro_brasil.csv"


def load_csv_data(path) -> pd.DataFrame:
    """Load a CSV file and return the DataFrame without applying transformations."""
    csv_path = Path(path)
    return pd.read_csv(csv_path)


def load_original_data(path=None) -> pd.DataFrame:
    """Load the original project dataset or a custom CSV path."""
    target_path = Path(path) if path is not None else DEFAULT_DATA_PATH
    return load_csv_data(target_path)
