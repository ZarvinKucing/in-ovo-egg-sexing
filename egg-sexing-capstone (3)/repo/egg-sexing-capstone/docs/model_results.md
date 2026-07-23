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

## Confusion Matrix (Model Final)

![Confusion Matrix](images/confusion_matrix_svm.png)

| | Prediksi Betina | Prediksi Jantan |
|---|---|---|
| **Aktual Betina** (21) | 18 (benar) | 3 (salah) |
| **Aktual Jantan** (29) | 3 (salah) | 26 (benar) |

Dari 50 sampel uji: 44 prediksi benar, 6 salah → akurasi 88%.

## Dampak Fitur GLCM Contrast

Perbandingan model **dengan** vs **tanpa** fitur GLCM Contrast (fitur lain tetap sama):

| Metrik | Dengan GLCM Contrast | Tanpa GLCM Contrast | Selisih |
|---|---|---|---|
| Accuracy | 88.00% | 56.00% | +32.00 pp |
| Precision | 89.65% | 58.97% | +30.68 pp |
| Recall | 89.65% | 79.31% | +10.34 pp |
| F1-Score | 89.65% | 67.64% | +22.01 pp |
| ROC-AUC | 94.74% | 65.68% | +29.06 pp |
| Best CV F1 (5-fold) | 83.54% | 73.25% | +10.29 pp |
| Correct Prediction (dari 50) | 44 | 28 | +16 |
| Wrong Prediction (dari 50) | 6 | 22 | -16 |

→ Menambahkan GLCM Contrast menurunkan kesalahan klasifikasi sebesar **70%**.

## Feature Contribution (Permutation Importance)

![Feature Contribution](images/feature_contribution_svm.png)

| Peringkat | Fitur | Kontribusi |
|---|---|---|
| 1 | GLCM Contrast | 44.0% |
| 2 | width_cm | 15.6% |
| 3 | shape_index | 15.0% |
| 4 | volume | 11.9% |
| 5 | weight_grams | 11.9% |

GLCM Contrast (fitur tekstur) mendominasi kontribusi klasifikasi — jauh di atas fitur morfologi (width, shape index) maupun fisik (volume, weight).

## Distribusi Dataset

| Kategori | Jumlah |
|---|---|
| Total Data Telur | 250 |
| DOC Jantan | 144 |
| DOC Betina | 106 |
| Data Training (80%) | 200 |
| Data Testing (20%) | 50 |

## Performa Sistem (Response Time)

Rata-rata waktu tiap tahap proses (dari trigger sampai data terkirim ke Firebase):

| Tahap | Rata-rata | Std. Deviasi |
|---|---|---|
| Boot Raspberry Pi hingga siap pakai | 44 detik 894 ms | 1 detik 16 ms |
| Pembacaan berat (load cell) | 2.85 ms | 0.018 ms |
| Conveyor menuju posisi capture | 1001 ms | 2.24 ms |
| Pengambilan citra (capture) | 6 detik 31 ms | 3.24 ms |
| Deteksi objek + ekstraksi fitur | 586.16 ms | 1.25 ms |
| Conveyor kembali ke posisi semula | 900.60 ms | 2.07 ms |
| Pengiriman data ke Firebase | 370.49 ms | 1.06 ms |

**Sinkronisasi dashboard:** data baru tampil di dashboard rata-rata **1 ms** setelah masuk Firebase; pie chart & grafik ter-update dalam **10–21 ms**.

## Konsumsi Daya

| Kondisi | Total Daya |
|---|---|
| Idle | 33.9 W |
| Aktif (conveyor bergerak) | 41.1 W |

→ Energi per jam operasi: **0.0303 – 0.0411 kWh**.

## Reliability (Uptime)

| Parameter | Nilai |
|---|---|
| Jumlah pengujian | 300 pengiriman data |
| Gagal terkirim | 3 data |
| Uptime | **99.00%** |
| Target NFR | ≥99% — **Terpenuhi** |
