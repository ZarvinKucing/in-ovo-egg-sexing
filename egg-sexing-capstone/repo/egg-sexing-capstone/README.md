# 🥚 In-Ovo Sex Detection of Laying Hen Eggs

**Deteksi Jenis Kelamin Telur pada Ras Ayam Petelur berbasis Raspberry Pi, Computer Vision, dan Machine Learning (SVM)**

Capstone Design — S1 Teknik Komputer, Fakultas Teknik Elektro, Universitas Telkom (2026)
Kolaborasi dengan **BRIN** dan **PT Super Unggas Jaya, Cirebon**.

> Sistem non-destructive & non-invasive untuk memprediksi jenis kelamin embrio ayam ras ISA Brown pada hari ke-0 inkubasi, menggunakan teknik *candling*, ekstraksi fitur morfologi/fisik/tekstur, dan klasifikasi SVM (kernel RBF) — mencapai **akurasi 88%**, **F1-score 89,65%**, dan **ROC-AUC 94,74%**.

---

## 📌 Latar Belakang

Industri ayam petelur menghadapi masalah pemusnahan anak ayam jantan (DOC jantan) yang tidak produktif secara ekonomi, sehingga menimbulkan kerugian ekonomi sekaligus isu kesejahteraan hewan. Sistem ini dikembangkan sebagai solusi *in-ovo sexing* yang dapat mendeteksi jenis kelamin telur **sebelum menetas**, tanpa merusak cangkang telur.

## 🧠 Alur Sistem

1. Telur diletakkan di atas **load cell (HX711)** → berat terukur
2. Operator menekan **push button** → telur berpindah lewat **mini conveyor (L298N)**
3. **LED candling (MOSFET MTR-0037)** menyala → **kamera Raspberry Pi** mengambil citra
4. Citra diproses: segmentasi HSV → *ellipse fitting* → ekstraksi fitur (`height`, `width`, `shape_index`, `volume`, `weight`, `GLCM contrast`)
5. Fitur diklasifikasi model **SVM (RBF kernel)** → hasil prediksi (Jantan/Betina)
6. Hasil dikirim ke **Firebase Realtime Database**
7. **Dashboard web (React)** menampilkan hasil secara real-time

![Hardware Block Diagram](docs/images/hardware_block_diagram_0.png)

## 🏗️ Struktur Repo

```
egg-sexing-capstone/
├── hardware/         # Script Raspberry Pi (akuisisi data, kontrol aktuator, upload Firebase)
├── ml/               # Ekstraksi fitur, preprocessing, training & evaluasi model SVM
├── dashboard/        # Web dashboard React + Firebase Realtime Database
├── firebase/         # Security rules & contoh kredensial
├── docs/             # Diagram, wiring table, rumus matematis, hasil pengujian
└── data/             # Dataset (tidak disertakan / lihat data/README.md)
```

## ⚙️ Hardware

| Komponen | Fungsi |
|---|---|
| Raspberry Pi 4 Model B | Edge computing / kontrol utama |
| Kamera Raspberry Pi 5MP | Akuisisi citra candling |
| Load Cell + HX711 | Pengukuran berat telur |
| LED Candling 800 lumen + MOSFET MTR-0037 | Sumber cahaya candling |
| Mini Conveyor + Driver Motor L298N | Pemindahan telur otomatis |
| Push Button | Trigger proses akuisisi |
| LCD 4.3 inch | Tampilan status alat |

Detail wiring & pin GPIO lengkap: [`docs/hardware_wiring.md`](docs/hardware_wiring.md)

## 🤖 Machine Learning

- **Fitur:** `height_cm`, `width_cm`, `shape_index`, `volume`, `weight_grams`, `glcm_contrast`
- **Model:** SVM kernel RBF (`C=100`, `gamma=0.01`), dioptimasi via Grid Search CV (5-fold, scoring F1)
- **Dataset:** 250 sampel telur (PT Super Unggas Jaya), divalidasi lewat proses penetasan & sexing DOC
- **Perbandingan model:** SVM mengungguli KNN dan LightGBM pada seluruh metrik (lihat [`docs/model_results.md`](docs/model_results.md))

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| KNN | 80.00% | 85.18% | 79.31% | 82.14% | 88.50% |
| LightGBM | 80.00% | 82.75% | 82.75% | 82.75% | 90.14% |
| **SVM (final)** | **88.00%** | **89.65%** | **89.65%** | **89.65%** | **94.74%** |

Rumus fitur (shape index, volume, GLCM contrast) ada di [`docs/formulas.md`](docs/formulas.md)

## 🖥️ Dashboard

Dibangun dengan **React + Vite**, terhubung real-time ke **Firebase Realtime Database** (autentikasi anonymous, akses tulis hanya dari Raspberry Pi via Admin SDK). Menampilkan:
- Data telur terbaru + confidence score
- Statistik total, jumlah betina/jantan, model accuracy
- Grafik distribusi gender (pie chart, Recharts)
- Pencarian & filter data

## 🚀 Cara Menjalankan

### Hardware (Raspberry Pi)
```bash
cd hardware
pip install -r requirements.txt
python calibration.py      # kalibrasi load cell sekali di awal
python main.py              # jalankan sistem utama
```

### Training Model ML
```bash
cd ml
pip install -r requirements.txt
python train.py
```

### Dashboard
```bash
cd dashboard
npm install
npm run dev
```

## 👥 Tim

| Nama | NIM |
|---|---|
| Muhammad Naufal Firdaus | 1103220083 |
| Zarvin Heruwin | 1103223120 |
| Alfikri | 1103223015 |

**Dosen Pembimbing:** Dr. Meta Kallista, S.Si., M.Si. · Dr. Ig. Prasetya Dwi Wibawa, S.T., M.T.

## 📄 Status

> ⚠️ Beberapa file kode (script Raspberry Pi lengkap & training ML final) masih dalam proses dipindahkan dari perangkat asli / belum final. Bagian yang belum lengkap ditandai `# TODO` di masing-masing file. Lihat [`docs/CONTRIBUTING_NOTES.md`](docs/CONTRIBUTING_NOTES.md).

## 📜 Lisensi

Lihat [`LICENSE`](LICENSE).
