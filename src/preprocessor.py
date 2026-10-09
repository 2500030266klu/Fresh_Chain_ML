"""
src/preprocessor.py
--------------------
Feature preprocessing and target encoding transformations.
"""

from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from src.config import NUMERIC_FEATURES, CATEGORICAL_FEATURES, TARGET


def build_preprocessor() -> ColumnTransformer:
    """
    Constructs a ColumnTransformer that scales numeric features
    and one-hot encodes categorical fruit types.
    """
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ]
    )


def prepare_features_and_target(
    df: pd.DataFrame
) -> Tuple[pd.DataFrame, np.ndarray, LabelEncoder]:
    """
    Separates predictors and encoded target vector.
    Target convention: Bad=0, Good=1.
    """
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    y = df[TARGET].copy()

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    return X, y_encoded, label_encoder
