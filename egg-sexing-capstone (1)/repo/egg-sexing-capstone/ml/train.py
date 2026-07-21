"""
Training & Hyperparameter Tuning Model SVM.
Referensi: Buku Capstone Design, Bab 4.2.2 (Pelatihan Model & Optimasi Hyperparameter),
dan Bab 4.2.2.G (Perbandingan Model Machine Learning).

Hasil terbaik dari penelitian: kernel=rbf, C=100, gamma=0.01, CV F1=0.8354
Performa akhir: Accuracy 88.00%, F1 89.65%, ROC-AUC 94.74% (split 80:20)

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
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report

from preprocessing import load_and_prepare

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


def run_split_scenario(X, y, test_size, pipeline):
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

    metrics = {
        "test_size": test_size,
        "train_size": len(X_train),
        "test_n": len(X_test),
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "cv_f1": grid_search.best_score_,
        "best_params": grid_search.best_params_,
    }
    return best_model, metrics


def main(csv_path: str, output_model_path: str):
    X, y = load_and_prepare(csv_path)
    pipeline = build_pipeline()

    print("=== Perbandingan Skenario Train-Test Split ===")
    best_overall = None
    for test_size in [0.2, 0.3, 0.4, 0.5]:
        model, metrics = run_split_scenario(X, y, test_size, pipeline)
        print(f"Split {int((1-test_size)*100)}:{int(test_size*100)} -> "
              f"Acc={metrics['accuracy']:.4f}  F1={metrics['f1']:.4f}  "
              f"ROC-AUC={metrics['roc_auc']:.4f}  CV-F1={metrics['cv_f1']:.4f}")

        # Simpan model dari skenario 80:20 sebagai model final (sesuai hasil penelitian)
        if test_size == 0.2:
            best_overall = model

    if best_overall is not None:
        joblib.dump(best_overall, output_model_path)
        print(f"\nModel final (split 80:20) disimpan di: {output_model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="../data/dataset_telur.csv",
                         help="Path ke dataset CSV")
    parser.add_argument("--out", default="models/svm_model.pkl",
                         help="Path output model .pkl")
    args = parser.parse_args()
    main(args.csv, args.out)
