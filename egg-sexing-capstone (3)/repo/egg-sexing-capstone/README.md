# 🥚 In-Ovo Sex Detection of Laying Hen Eggs

**Deteksi Jenis Kelamin Telur pada Ras Ayam Petelur berbasis Raspberry Pi, Computer Vision, dan Machine Learning (SVM)**

Capstone Design — S1 Teknik Komputer, Fakultas Teknik Elektro, Universitas Telkom (2026)

[🇬🇧 Read in English](README.en.md)

> Sistem non-destructive & non-invasive untuk memprediksi jenis kelamin embrio ayam ras ISA Brown pada hari ke-0 inkubasi, menggunakan teknik *candling*, ekstraksi 13 fitur morfologi/fisik/tekstur, dan klasifikasi SVM (kernel RBF) — mencapai **akurasi 88%**, **F1-score 89,65%**, dan **ROC-AUC 94,74%**.

## 🤝 Riset Kolaborasi

Proyek ini dilaksanakan sebagai kerja sama riset antara **Universitas Telkom**, **Badan Riset dan Inovasi Nasional (BRIN)**, dan **Hatchery PT Super Unggas Jaya (PT SUJA), Cirebon**. Spesifikasi & kebutuhan sistem disusun berdasarkan wawancara langsung dengan tim peneliti/teknisi BRIN dan pihak hatchery PT SUJA. Pengambilan dataset (250 sampel telur), pengujian lapangan, serta proses validasi ground truth (penetasan → sexing DOC) seluruhnya dilakukan di fasilitas Hatchery PT SUJA, Cirebon (5–30 April 2026).

## 📌 Latar Belakang

Industri ayam petelur menghadapi masalah pemusnahan anak ayam jantan (DOC jantan) yang tidak produktif secara ekonomi, sehingga menimbulkan kerugian ekonomi sekaligus isu kesejahteraan hewan. Sistem ini dikembangkan sebagai solusi *in-ovo sexing* yang dapat mendeteksi jenis kelamin telur **sebelum menetas**, tanpa merusak cangkang telur.

## 🧠 Alur Sistem

1. Telur diletakkan di atas **load cell (HX711)** → berat terukur
2. Operator menekan **push button** → telur berpindah lewat **mini conveyor (L298N)**
3. **LED candling (MOSFET MTR-0037)** menyala → **kamera Raspberry Pi** mengambil citra
4. Citra diproses: segmentasi HSV → *ellipse fitting* → ekstraksi 10 fitur dasar (height, width, shape index, ovality, eccentricity, surface area, volume, density, weight, GLCM contrast) + 3 fitur turunan
5. Fitur diklasifikasi model **SVM (RBF kernel)** → hasil prediksi (Jantan/Betina) + confidence score
6. Hasil dikirim ke **Firebase Realtime Database** (+ backup CSV lokal)
7. **Dashboard web (React)** menampilkan hasil secara real-time

### Diagram Blok Hardware

![Hardware Block Diagram](docs/images/hardware_block_diagram.png)

### Wiring Diagram

![Wiring Diagram](docs/images/wiring_diagram_0.png)

### Flowchart Sistem & Model ML

<table>
<tr>
<td><img src="docs/images/flowchart_sistem_0.png" width="380"/></td>
<td><img src="docs/images/flowchart_ml_0.png" width="380"/></td>
</tr>
</table>

## 📷 Foto Hardware & Prototipe

<table>
<tr>
<td><img src="docs/images/hardware_raspberry_pi4.png" width="220"/><br/><sub>Raspberry Pi 4B</sub></td>
<td><img src="docs/images/hardware_camera_or_loadcell_1.png" width="220"/><br/><sub>Kamera / Load Cell</sub></td>
<td><img src="docs/images/hardware_conveyor_or_lcd.png" width="220"/><br/><sub>Conveyor / LCD</sub></td>
<td><img src="docs/images/prototipe_alat_0.png" width="165"/><br/><sub>Prototipe Lengkap</sub></td>
</tr>
</table>

Galeri lengkap (semua komponen + proses validasi dataset): [`docs/gallery.md`](docs/gallery.md)

## 🖥️ Dashboard Web

<table>
<tr>
<td colspan="2"><img src="docs/images/dashboard_tabel_data_telur.png" width="600"/><br/><sub>Tabel Data Telur (real-time)</sub></td>
</tr>
<tr>
<td><img src="docs/images/dashboard_stats_cards.png" width="290"/><br/><sub>Statistik</sub></td>
<td><img src="docs/images/dashboard_pie_chart_gender.png" width="290"/><br/><sub>Distribusi Gender</sub></td>
</tr>
</table>

Dibangun dengan **React + Vite**, terhubung real-time ke **Firebase Realtime Database** (autentikasi anonymous, akses tulis hanya dari Raspberry Pi via Admin SDK).

## 🏗️ Struktur Repo

```
egg-sexing-capstone/
├── hardware/            # 🟢 Kode ASLI dari Raspberry Pi
│   ├── main.py          #    Program utama (load cell → candling → ML → Firebase)
│   ├── hx711.py         #    Driver load cell
│   ├── calibrate.py     #    Kalibrasi load cell
│   └── tests/           #    Script tes komponen (motor, senter, button)
├── ml/                  # Ekstraksi fitur, preprocessing, training & evaluasi SVM
├── dashboard/           # Web dashboard React + Firebase (rekonstruksi dari buku TA)
├── firebase/            # Security rules & contoh kredensial
├── docs/                # Diagram, wiring, rumus, hasil pengujian, galeri foto
└── data/                # Dataset (tidak disertakan / lihat data/README.md)
```

> 🟢 = kode asli yang terbukti berjalan di alat. Lihat status detail tiap bagian di
> [`docs/CONTRIBUTING_NOTES.md`](docs/CONTRIBUTING_NOTES.md).

## ⚙️ Hardware

| Komponen | Fungsi | GPIO |
|---|---|---|
| Raspberry Pi 4 Model B | Edge computing / kontrol utama | — |
| Kamera Raspberry Pi 5MP | Akuisisi citra candling | CSI |
| Load Cell + HX711 | Pengukuran berat telur | GPIO 5, 6 |
| LED Candling 800 lumen + MOSFET MTR-0037 | Sumber cahaya candling | GPIO 18 |
| Mini Conveyor + Driver Motor L298N | Pemindahan telur otomatis | GPIO 13, 20, 16 |
| Push Button | Trigger proses akuisisi | GPIO 19 |
| LCD 4.3 inch | Tampilan status alat | DSI |

Detail wiring & pin GPIO lengkap: [`docs/hardware_wiring.md`](docs/hardware_wiring.md) · Setup & cara jalankan: [`hardware/README.md`](hardware/README.md)

## 🤖 Machine Learning

- **13 Fitur:** `height_cm`, `width_cm`, `shape_index`, `ovality`, `eccentricity`, `surface_area`, `volume`, `density`, `weight_grams`, `glcm_contrast` + 3 fitur turunan (`height_width_ratio`, `volume_surface_ratio`, `density_ratio`)
- **Model:** SVM kernel RBF (`C=100`, `gamma=0.01`), dioptimasi via Grid Search CV (5-fold, scoring F1)
- **Dataset:** 250 sampel telur (Hatchery PT SUJA), divalidasi lewat proses penetasan & sexing DOC
- **Perbandingan model:** SVM mengungguli KNN dan LightGBM pada seluruh metrik

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| KNN | 80.00% | 85.18% | 79.31% | 82.14% | 88.50% |
| LightGBM | 80.00% | 82.75% | 82.75% | 82.75% | 90.14% |
| **SVM (final)** | **88.00%** | **89.65%** | **89.65%** | **89.65%** | **94.74%** |

### Confusion Matrix

<img src="docs/images/confusion_matrix_svm.png" width="380"/>

| | Prediksi Betina | Prediksi Jantan |
|---|---|---|
| **Aktual Betina** (21) | 18 ✅ | 3 ❌ |
| **Aktual Jantan** (29) | 3 ❌ | 26 ✅ |

### Feature Contribution (Permutation Importance)

<img src="docs/images/feature_contribution_svm.png" width="500"/>

GLCM Contrast (fitur tekstur) mendominasi dengan kontribusi **44%** — jauh di atas fitur morfologi/fisik lainnya. Menambahkan GLCM Contrast ke model meningkatkan akurasi dari 56% → 88% (+32 poin persentase).

📊 Metrik lengkap (dampak GLCM Contrast, response time, konsumsi daya, uptime): [`docs/model_results.md`](docs/model_results.md)
🧮 Rumus fitur (shape index, ovality, eccentricity, volume, GLCM contrast): [`docs/formulas.md`](docs/formulas.md)
📷 Galeri foto hardware, dashboard, & proses validasi: [`docs/gallery.md`](docs/gallery.md)

## 🚀 Cara Menjalankan

### Hardware (Raspberry Pi)
```bash
cd hardware
pip install -r requirements.txt --break-system-packages
python calibrate.py    # kalibrasi load cell sekali di awal
python main.py         # jalankan sistem utama
```
Detail lengkap (file kredensial yang dibutuhkan, urutan tombol, dst.): [`hardware/README.md`](hardware/README.md)

### Training Model ML
```bash
cd ml
pip install -r requirements.txt
python train.py --csv ../data/dataset_telur.csv --out models/egg_gender_model.pkl
```
Lalu salin `models/egg_gender_model.pkl` ke `hardware/egg_gender_model.pkl` di Raspberry Pi.

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
**Mitra Riset:** Badan Riset dan Inovasi Nasional (BRIN) · Hatchery PT Super Unggas Jaya, Cirebon

## 📄 Status

Kode hardware (`hardware/`) sudah **kode asli**, terbukti jalan di alat. Bagian dashboard masih
rekonstruksi dari buku TA, dan dataset/model terlatih belum disertakan (data milik mitra riset).
Detail lengkap: [`docs/CONTRIBUTING_NOTES.md`](docs/CONTRIBUTING_NOTES.md).

## 📜 Lisensi

Lihat [`LICENSE`](LICENSE).
