# Hardware — Raspberry Pi

Ini adalah kode **asli** yang berjalan di Raspberry Pi 4B alat capstone (bukan rekonstruksi).

## Isi Folder

| File | Fungsi |
|---|---|
| `main.py` | Program utama sistem lengkap: load cell → button → conveyor → candling → capture → ekstraksi fitur → prediksi SVM → upload Firebase + simpan CSV lokal |
| `hx711.py` | Library driver HX711 (load cell amplifier), dipakai `calibrate.py` & `main.py` |
| `calibrate.py` | Script kalibrasi load cell — hasilkan `scale_factor.txt` |
| `tests/test_motor.py` | Tes standalone motor conveyor (L298N) |
| `tests/test_senter.py` | Tes standalone LED candling (MOSFET) |
| `tests/test_button.py` | Tes standalone push button trigger |
| `requirements.txt` | Dependency Python |

## Setup di Raspberry Pi

```bash
pip install -r requirements.txt --break-system-packages
```

### 1. Tes komponen satu-satu (opsional tapi disarankan)

```bash
python tests/test_button.py
python tests/test_senter.py
python tests/test_motor.py
```

### 2. Kalibrasi load cell

```bash
python calibrate.py
```
Ikuti instruksi di terminal (kosongkan timbangan → taruh beban referensi → masukkan berat aktual).
Hasilnya tersimpan di `scale_factor.txt` (dibaca otomatis oleh `main.py`).

### 3. Siapkan file pendukung

Taruh 2 file berikut di folder `hardware/` (JANGAN commit ke git — sudah di-`.gitignore`):

- **Firebase service account key**: file `*-firebase-adminsdk-*.json` dari Firebase Console
  → sesuaikan nama file di `FIREBASE_CRED` pada `main.py` kalau beda
- **Model SVM terlatih**: `egg_gender_model.pkl` (hasil `ml/train.py`, format
  `{"model": ..., "features": [...]}`)

> Kalau kedua file ini belum ada, `main.py` tetap bisa jalan (fitur tetap diekstrak & disimpan ke
> CSV lokal), hanya saja hasil prediksi gender akan `"unknown"` dan/atau data tidak terupload ke Firebase.

### 4. Jalankan sistem

```bash
python main.py
```

## Alur Kerja (`main.py`)

1. **Tare load cell** — tekan tombol setelah load cell dikosongkan
2. **Timbang telur** — taruh telur di load cell, tekan tombol
3. **Pindah manual ke conveyor** — operator angkat telur dari load cell ke tatakan conveyor
4. **Conveyor maju** ke posisi kamera
5. **LED candling ON** + **live preview kamera** sampai tombol ditekan (posisi telur pas)
6. **Capture** citra + segmentasi HSV + ekstraksi fitur (ellipse fitting, ovality, eccentricity, GLCM contrast, dst.)
7. **Prediksi gender** via model SVM (kalau model tersedia)
8. **Upload ke Firebase** (kalau kredensial tersedia) **+ simpan ke CSV lokal** (selalu, sebagai backup offline)
9. **Conveyor mundur** ke posisi semula, siap untuk telur berikutnya

## Konfigurasi Penting (di dalam `main.py`)

```python
CM_PER_PIXEL_MAJOR = 0.00541   # kalibrasi kamera - sumbu panjang
CM_PER_PIXEL_MINOR = 0.00540   # kalibrasi kamera - sumbu lebar

BUTTON_PIN = 19
SENTER_PIN = 18       # MOSFET LED candling
DOUT, SCK = 5, 6      # HX711
ENA, IN1, IN2 = 13, 20, 16   # L298N conveyor

SPEED_CONVEYOR = 45   # duty cycle PWM (0-100)
DURASI_MAJU = 0.75    # detik
DURASI_MUNDUR = 0.8   # detik
```

> ⚠️ `DURASI_MAJU`/`DURASI_MUNDUR` dan `SPEED_CONVEYOR` sangat bergantung pada jarak fisik &
> gesekan mekanik alatmu — kalibrasi ulang kalau posisi berhenti conveyor meleset dari kamera.
