# Dataset

Dataset asli (250 sampel telur, PT Super Unggas Jaya, Cirebon) **tidak disertakan** di repo ini
karena merupakan data milik mitra riset.

## Format yang diharapkan (`dataset_telur.csv`)

Kolom yang dibutuhkan oleh `ml/preprocessing.py` dan `ml/train.py`:

| Kolom | Tipe | Keterangan |
|---|---|---|
| `height_cm` | float | Panjang telur (sumbu mayor) |
| `width_cm` | float | Lebar telur (sumbu minor) |
| `shape_index` | float | width_cm / height_cm |
| `volume` | float | Estimasi volume (cm³) |
| `weight_grams` | float | Berat telur (gram) |
| `glcm_contrast` | float | Fitur tekstur GLCM |
| `gender` | string | `"jantan"` atau `"betina"` (label hasil sexing DOC) |

Taruh file dataset kamu sebagai `data/dataset_telur.csv`, atau arahkan `--csv` di `ml/train.py` ke lokasi lain.

> ⚠️ File CSV nyata **jangan di-commit** kalau berisi data mitra riset yang sensitif — sudah di-exclude lewat `.gitignore`.
