# Catatan Pengisian Repo

Repo ini disusun berdasarkan potongan kode (*snippet*) yang tercantum di Buku Capstone
Design, karena kode program penuh belum tersedia sebagai file terpisah saat repo ini dibuat.
Bagian berikut perlu kamu lengkapi/verifikasi dengan kode asli dari perangkatmu:

## Hardware (`hardware/`)
- [ ] `main.py` — kerangka integrasi saja, belum pernah dijalankan utuh di Raspberry Pi asli
- [ ] `config.py` — konfirmasi ulang pin GPIO LED candling (17 vs 18, ada inkonsistensi di buku)
- [ ] Timing conveyor (`durasi` pada `conveyor_maju()`) — sesuaikan dengan jarak fisik alatmu
- [ ] `firebase_uploader.py` — isi `FIREBASE_DB_URL`, taruh `serviceAccountKey.json` asli

## Machine Learning (`ml/`)
- [ ] Dataset asli (`data/dataset_telur.csv`) belum disertakan (250 sampel, PT Super Unggas Jaya)
- [ ] `feature_extraction.py` — cek konsistensi rumus volume (`1/0.662` vs `1/0.666`)
- [ ] `feature_extraction.py` — ROI cropping sebelum hitung GLCM contrast (di buku hanya
      disebutkan konsepnya, kode ROI cropping-nya tidak dikutip utuh)
- [ ] Model final `.pkl` belum ada — jalankan `train.py` setelah dataset tersedia
- [ ] Kode training KNN & LightGBM (perbandingan model) belum dikutip di buku — tambahkan
      sendiri kalau ingin reproduce Tabel 4.7

## Dashboard (`dashboard/`)
- [ ] Fitur search, filter kategori gender, dan pagination disebutkan sudah ada di dashboard
      asli, tapi kodenya tidak dikutip di buku — perlu ditambahkan sendiri
- [ ] Kredensial Firebase (`.env`) — isi dari Firebase Console proyekmu

## Umum
- Semua bagian yang direkonstruksi dari buku ditandai komentar `# TODO` atau `// TODO`
  di kode masing-masing, supaya gampang dicari dengan `grep -rn "TODO" .`
