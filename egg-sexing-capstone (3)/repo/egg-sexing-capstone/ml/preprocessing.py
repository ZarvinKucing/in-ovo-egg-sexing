"""
Preprocessing Dataset sebelum Training.

Model final memakai 13 fitur: 10 fitur dasar hasil ekstraksi citra
(lihat feature_extraction.py) + 3 fitur turunan (engineered) yang dihitung
dengan cara PERSIS SAMA seperti di `hardware/main.py::predict_gender()`,
supaya urutan & definisi fitur konsisten antara training dan inferensi di alat.
"""

import numpy as np
import pandas as pd

BASE_FEATURES = [
    "height_cm",
    "width_cm",
    "shape_index",
    "ovality",
    "eccentricity",
    "surface_area",
    "volume",
    "density",
    "weight_grams",
    "glcm_contrast",
]

ENGINEERED_FEATURES = [
    "height_width_ratio",
    "volume_surface_ratio",
    "density_ratio",
]

FEATURES = BASE_FEATURES + ENGINEERED_FEATURES


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Tambahkan 3 fitur turunan -- HARUS identik dengan rekonstruksi di hardware/main.py."""
    df = df.copy()
    df["height_width_ratio"] = df["height_cm"] / (df["width_cm"] + 1e-6)
    df["volume_surface_ratio"] = df["volume"] / (df["surface_area"] + 1e-6)
    df["density_ratio"] = df["density"] / (df["weight_grams"] + 1e-6)
    return df


def clean_and_encode(df: pd.DataFrame) -> pd.DataFrame:
    """Ambil hanya baris jantan/betina, hapus missing value, encode label ke 0/1."""
    df = df[df["gender"].isin(["jantan", "betina"])].copy()
    df = df.dropna(subset=BASE_FEATURES + ["gender"])
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
    """Pisahkan feature matrix X (13 fitur) dan label y."""
    X = df[FEATURES]
    y = df["gender"]
    return X, y


def load_and_prepare(csv_path: str):
    """Pipeline lengkap: load CSV -> clean -> feature engineering -> select -> clip outliers."""
    df = pd.read_csv(csv_path)
    df = clean_and_encode(df)
    df = add_engineered_features(df)
    X, y = select_features(df)
    X = clip_outliers(X)
    return X, y
