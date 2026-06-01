"""Simple pipeline to prepare the processed dataset for the future dashboard."""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

from src.services.clean_data import clean_financial_data
from src.services.load_data import DEFAULT_DATA_PATH, load_original_data
from src.services.transform_data import transform_financial_data


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ORIGIN_OUTPUT = PROJECT_ROOT / "database" / "origin" / "dados_originais.csv"
DEFAULT_PROCESSED_OUTPUT = PROJECT_ROOT / "database" / "processed" / "dados_tratados.csv"


def prepare_processed_dataset(input_path=None, output_path=None) -> pd.DataFrame:
    """Load, clean, transform and persist the processed dataset."""
    source_path = Path(input_path) if input_path is not None else DEFAULT_DATA_PATH
    processed_path = Path(output_path) if output_path is not None else DEFAULT_PROCESSED_OUTPUT
    origin_path = DEFAULT_ORIGIN_OUTPUT

    origin_path.parent.mkdir(parents=True, exist_ok=True)
    processed_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(source_path, origin_path)

    df_original = load_original_data(source_path)
    df_clean = clean_financial_data(df_original)
    df_transformed = transform_financial_data(df_clean)
    df_transformed.to_csv(processed_path, index=False)
    return df_transformed
