"""
Preprocessing Dataset sebelum Training.
Referensi: Buku Capstone Design, Bab 4.2.2 (Data Preprocessing).
"""

import numpy as np
import pandas as pd

FEATURES = [
    "height_cm",
    "width_cm",
    "shape_index",
    "volume",
    "weight_grams",
    "glcm_contrast",
]


def clean_and_encode(df: pd.DataFrame) -> pd.DataFrame:
    """Ambil hanya baris jantan/betina, hapus missing value, encode label ke 0/1."""
    df = df[df["gender"].isin(["jantan", "betina"])].copy()
    df = df.dropna()
    df["gender"] = df["gender"].map({"betina": 0, "jantan": 1})
    return df


def clip_outliers(X: pd.DataFrame) -> pd.DataFrame:
    """Clipping outlier per kolom fitur pada persentil 1% - 99%."""
    X = X.copy()
    for col in X.columns:
        lower = X[col].quantile(0.01)
        upper = X[col].quantile(0.99)
        X[col] = np.clip(X[col], lower, upper)
    return X


def select_features(df: pd.DataFrame):
    """Pisahkan feature matrix X dan label y."""
    X = df[FEATURES]
    y = df["gender"]
    return X, y


def load_and_prepare(csv_path: str):
    """Pipeline lengkap: load CSV -> clean -> select features -> clip outliers."""
    df = pd.read_csv(csv_path)
    df = clean_and_encode(df)
    X, y = select_features(df)
    X = clip_outliers(X)
    return X, y
