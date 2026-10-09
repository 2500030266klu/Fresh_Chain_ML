"""
src/data_loader.py
-------------------
Data ingestion, validation, and exploratory aggregation utilities.
"""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from src.config import DATA_PATH, NUMERIC_FEATURES, CATEGORICAL_FEATURES, TARGET


def load_data(path: Optional[str] = None) -> pd.DataFrame:
    """
    Safely load and validate the Fruit & Vegetable Spoilage dataset.
    """
    filepath = path or DATA_PATH
    if not filepath.exists() if hasattr(filepath, "exists") else not Path(filepath).exists():
        raise FileNotFoundError(f"Dataset not found at {filepath}")

    df = pd.read_csv(filepath)

    expected_columns = CATEGORICAL_FEATURES + NUMERIC_FEATURES + [TARGET]
    missing_cols = [c for c in expected_columns if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    return df


def get_dataset_summary(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Generate structured statistical overview of the dataset.
    """
    if df is None:
        df = load_data()

    total_rows, total_cols = df.shape
    missing_vals = df.isnull().sum().to_dict()
    duplicates = int(df.duplicated().sum())

    # Class & Fruit distribution
    class_counts = df[TARGET].value_counts().to_dict()
    fruit_counts = df["Fruit"].value_counts().to_dict()

    # Fruit x Class Crosstab
    crosstab_df = pd.crosstab(df["Fruit"], df[TARGET])
    fruit_class_matrix = {
        fruit: {
            "Good": int(crosstab_df.loc[fruit, "Good"]) if "Good" in crosstab_df.columns else 0,
            "Bad": int(crosstab_df.loc[fruit, "Bad"]) if "Bad" in crosstab_df.columns else 0,
            "SpoilageRate": round(
                (crosstab_df.loc[fruit, "Bad"] / crosstab_df.loc[fruit].sum()) * 100, 2
            ) if crosstab_df.loc[fruit].sum() > 0 else 0.0
        }
        for fruit in crosstab_df.index
    }

    # Descriptive Stats
    desc_df = df[NUMERIC_FEATURES].describe().round(3)
    stats_dict = {}
    for col in NUMERIC_FEATURES:
        stats_dict[col] = {
            "mean": float(desc_df.loc["mean", col]),
            "std": float(desc_df.loc["std", col]),
            "min": float(desc_df.loc["min", col]),
            "25%": float(desc_df.loc["25%", col]),
            "50%": float(desc_df.loc["50%", col]),
            "75%": float(desc_df.loc["75%", col]),
            "max": float(desc_df.loc["max", col]),
        }

    # Correlation Matrix
    corr_matrix = df[NUMERIC_FEATURES].corr().round(3).to_dict()

    # Means by class
    means_by_class = df.groupby(TARGET)[NUMERIC_FEATURES].mean().round(2).to_dict()

    return {
        "total_rows": total_rows,
        "total_cols": total_cols,
        "columns": list(df.columns),
        "missing_values": missing_vals,
        "duplicate_rows": duplicates,
        "class_counts": class_counts,
        "fruit_counts": fruit_counts,
        "fruit_class_matrix": fruit_class_matrix,
        "numeric_stats": stats_dict,
        "correlation_matrix": corr_matrix,
        "means_by_class": means_by_class,
    }


def get_preview_rows(df: Optional[pd.DataFrame] = None, limit: int = 50) -> list:
    """
    Get sample rows formatted for web display.
    """
    if df is None:
        df = load_data()
    return df.head(limit).to_dict(orient="records")
