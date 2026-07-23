"""
Training & Hyperparameter Tuning Model SVM.

Hasil terbaik dari penelitian: kernel=rbf, C=100, gamma=0.01, CV F1=0.8354
Performa akhir (skenario dengan GLCM Contrast): Accuracy 88.00%, F1 89.65%,
ROC-AUC 94.74% (stratified split 80:20)

PENTING: model disimpan sebagai dict {"model": pipeline, "features": [...]}
supaya bisa langsung dipakai oleh `hardware/main.py::predict_gender()` tanpa
perubahan apa pun -- tinggal salin hasil `models/egg_gender_model.pkl` ke
folder `hardware/` di Raspberry Pi.

# TODO: ganti path CSV dataset sesuai lokasi dataset kamu.
# Dataset asli (250 sampel telur, PT Super Unggas Jaya) tidak disertakan di
# repo ini -- lihat data/README.md
"""

import argparse
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from preprocessing import load_and_prepare, FEATURES

PARAM_GRID = {
    "svm__C": [1, 10, 50, 100],
    "svm__gamma": [0.001, 0.01, 0.1, 1],
    "svm__kernel": ["rbf"],
}


def build_pipeline():
    return Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(probability=True, random_state=42)),
    ])


def main(csv_path: str, output_model_path: str, test_size: float = 0.2):
    X, y = load_and_prepare(csv_path)
    pipeline = build_pipeline()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=42
    )

    grid_search = GridSearchCV(
        pipeline, param_grid=PARAM_GRID, cv=5, scoring="f1", n_jobs=-1
    )
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    y_proba = best_model.predict_proba(X_test)[:, 1]

    print("Best params :", grid_search.best_params_)
    print("Best CV F1  :", round(grid_search.best_score_, 4))
    print("Accuracy    :", round(accuracy_score(y_test, y_pred), 4))
    print("F1-Score    :", round(f1_score(y_test, y_pred), 4))
    print("ROC-AUC     :", round(roc_auc_score(y_test, y_proba), 4))

    model_package = {
        "model": best_model,
        "features": FEATURES,  # urutan HARUS sama dengan yang dipakai main.py::predict_gender()
    }
    joblib.dump(model_package, output_model_path)
    print(f"\nModel package disimpan di: {output_model_path}")
    print("Salin file ini ke `hardware/egg_gender_model.pkl` di Raspberry Pi.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="../data/dataset_telur.csv",
                         help="Path ke dataset CSV")
    parser.add_argument("--out", default="models/egg_gender_model.pkl",
                         help="Path output model .pkl")
    parser.add_argument("--test-size", type=float, default=0.2)
    args = parser.parse_args()
    main(args.csv, args.out, args.test_size)
