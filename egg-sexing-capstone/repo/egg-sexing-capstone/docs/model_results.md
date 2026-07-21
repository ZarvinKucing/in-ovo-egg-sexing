# Hasil Pengujian Model

## Hyperparameter Tuning (Grid Search CV, 5-fold, scoring=F1)

```python
param_grid = {
    "svm__C": [1, 10, 50, 100],
    "svm__gamma": [0.001, 0.01, 0.1, 1],
    "svm__kernel": ["rbf"],
}
```

20 kombinasi × 5 fold = 100 proses pelatihan & validasi.

**Hasil terbaik:**

| Parameter | Nilai |
|---|---|
| Kernel | RBF |
| C | 100 |
| Gamma | 0.01 |
| Best CV F1-Score | 0.8354 |

## Perbandingan Rasio Train-Test Split

| Split | Train Size | Test Size | Accuracy | F1-Score | CV F1 |
|---|---|---|---|---|---|
| 80:20 | 200 | 50 | 88.00% | 89.66% | 0.8354 |
| 70:30 | 175 | 75 | 88.00% | 89.16% | 0.7985 |
| 60:40 | 150 | 100 | 88.00% | 89.66% | 0.8229 |
| 50:50 | 125 | 125 | 84.00% | 85.71% | 0.7831 |

→ **80:20 dipilih** sebagai konfigurasi final (CV F1 tertinggi, akurasi & F1 tetap optimal).

## Perbandingan Antar Model (split 80:20, fitur sama)

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| KNN | 80.00% | 85.18% | 79.31% | 82.14% | 88.50% |
| LightGBM | 80.00% | 82.75% | 82.75% | 82.75% | 90.14% |
| **SVM (RBF)** | **88.00%** | **89.65%** | **89.65%** | **89.65%** | **94.74%** |

## Kalibrasi Load Cell

| No | Raw HX711 | Berat Aktual (g) | Scale Factor |
|---|---|---|---|
| 1 | 397225 | 55.5 | 7157.21 |
| 2 | 391204 | 49.4 | 7919.11 |
| 3 | 387044 | 45.0 | 8600.98 |
| 4 | 397121 | 55.3 | 7181.21 |
| 5 | 393400 | 51.6 | 7624.03 |
| **Rata-rata** | | | **7696.51** |

## Validasi Lapangan (field testing)

Pengujian akhir terhadap **50 sampel telur** yang berhasil ditetaskan dan divalidasi lewat proses sexing DOC menunjukkan akurasi model **88%**.
