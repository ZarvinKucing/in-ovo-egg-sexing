# Catatan Status Repo

## ✅ Sudah Lengkap (kode asli, bukan rekonstruksi)

- `hardware/main.py` — program utama asli dari Raspberry Pi (load cell → button → conveyor →
  candling → capture → ekstraksi fitur → prediksi SVM → Firebase + CSV)
- `hardware/hx711.py` — library driver load cell asli
- `hardware/calibrate.py` — script kalibrasi load cell asli
- `hardware/tests/*.py` — script tes standalone (motor, senter, button) asli
- Semua rumus fitur (`docs/formulas.md`) sudah dikonfirmasi langsung dari kode asli
- Wiring/pin GPIO (`docs/hardware_wiring.md`) sudah dikonfirmasi 1:1 dengan kode asli
- `ml/feature_extraction.py`, `ml/preprocessing.py`, `ml/train.py` sudah disesuaikan supaya
  konsisten dengan 13 fitur yang benar-benar dipakai model (bukan 6 fitur seperti versi awal repo)

## 🟡 Masih Perlu Dilengkapi

- [ ] **Dataset asli** (`data/dataset_telur.csv`, 250 sampel berlabel ground truth) — belum ada,
      lihat `data/README.md` untuk format yang dibutuhkan
- [ ] **Model terlatih** (`hardware/egg_gender_model.pkl`) — belum ada, hasilkan dengan
      `python ml/train.py` setelah dataset tersedia
- [ ] **Firebase service account key** (`hardware/*-firebase-adminsdk-*.json`) — isi dari Firebase
      Console proyekmu sendiri, jangan commit ke git
- [ ] **Dashboard React** (`dashboard/`) — bagian ini **masih rekonstruksi** dari potongan kode di
      Buku Capstone Design (belum ada file dashboard asli). Fitur search, filter, dan pagination
      disebutkan di buku tapi kodenya belum dikutip utuh — perlu kamu lengkapi sendiri kalau
      sudah menemukan source code dashboard aslinya
- [ ] Kode training KNN & LightGBM (perbandingan model di Tabel 4.7/5.x buku) belum ada file
      aslinya — kalau mau reproduce tabel perbandingan model, perlu ditambahkan sendiri

## 📷 Gambar/Foto (`docs/images/`)

Semua gambar diekstrak **otomatis** dari file PDF Buku Capstone Design berdasarkan halaman &
caption terdekat. Sudah dicek ulang sebagian (mis. `hardware_block_diagram.png` sempat ketuker
sama mockup dashboard dan sudah diperbaiki), tapi ada kemungkinan kecil gambar dengan nama generik
(`hardware_camera_or_loadcell_1.png`, `hardware_conveyor_or_lcd.png`) masih belum 100% pas dengan
caption-nya. Cek sekilas di `docs/gallery.md`, ganti dengan foto asli/screenshot-mu kalau ada yang
meleset.

## Umum

Bagian yang masih rekonstruksi (belum ada file asli) ditandai komentar `# TODO` di kode
masing-masing — cari dengan `grep -rn "TODO" .`
