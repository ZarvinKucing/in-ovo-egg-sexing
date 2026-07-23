# Dataset

Dataset asli (250 sampel telur, PT Super Unggas Jaya, Cirebon) **tidak disertakan** di repo ini
karena merupakan data milik mitra riset.

## Dari mana datanya berasal?

Setiap kali `hardware/main.py` dijalankan di alat, hasil ekstraksi fitur otomatis di-log ke
CSV lokal (default: `egg_features_batch2.csv`, lihat `CSV_PATH` di `main.py`) **dan** diupload ke
Firebase. Kolom `gender` di CSV ini adalah **hasil prediksi model**, bukan ground truth.

Untuk membangun/retrain dataset training yang valid, kolom `gender` perlu **ditimpa manual**
dengan hasil sexing DOC yang sebenarnya (dicocokkan lewat kolom `kode`), sesuai proses validasi
di `docs/gallery.md` bagian "Proses Validasi Dataset".

## Format yang diharapkan (`dataset_telur.csv`) untuk `ml/train.py`

10 fitur dasar (hasil ekstraksi citra + berat) — kolom ini harus ada persis seperti nama & satuan
yang dihasilkan `hardware/main.py::compute_features()` / `ml/feature_extraction.py`:

| Kolom | Tipe | Keterangan |
|---|---|---|
| `height_cm` | float | Panjang telur (sumbu mayor elips) |
| `width_cm` | float | Lebar telur (sumbu minor elips) |
| `shape_index` | float | width_cm / height_cm |
| `ovality` | float | Deviasi kontur asli terhadap elips ideal |
| `eccentricity` | float | Eksentrisitas elips |
| `surface_area` | float | Estimasi luas permukaan (cm²), dari berat |
| `volume` | float | Estimasi volume (cm³), dari surface_area |
| `density` | float | weight_grams / volume |
| `weight_grams` | float | Berat telur (gram) |
| `glcm_contrast` | float | Fitur tekstur GLCM Contrast |
| `gender` | string | `"jantan"` atau `"betina"` (ground truth pasca-sexing DOC) |

3 fitur turunan (`height_width_ratio`, `volume_surface_ratio`, `density_ratio`) **dihitung otomatis**
oleh `ml/preprocessing.py::add_engineered_features()` — tidak perlu ada di CSV mentah.

Taruh file dataset kamu sebagai `data/dataset_telur.csv`, atau arahkan `--csv` di `ml/train.py` ke lokasi lain.

> ⚠️ File CSV nyata **jangan di-commit** kalau berisi data mitra riset yang sensitif — sudah di-exclude lewat `.gitignore`.
