# Representasi Matematis Fitur

Sistem mengekstraksi 6 fitur dari citra candling + sensor berat, dikombinasikan menjadi satu *feature vector* per sampel telur.

## 1. Shape Index (SI)

```
SI = Short Axis / Long Axis = width / height
```

Semakin mendekati 1 → telur semakin bulat. Semakin kecil → telur semakin lonjong.

## 2. Surface Area & Volume (pendekatan empiris berbasis massa)

```
SA = 4.835 * (mass ** 0.662)          # luas permukaan telur (cm²)
V  = (SA / 4.951) ** (1 / 0.666)      # volume telur (cm³)
Density = mass / V                    # densitas (g/cm³)
```

> ✅ Dikonfirmasi dari kode asli (`hardware/main.py::compute_features()`): eksponen pembagi volume
> yang dipakai adalah **1/0.666** (bukan 1/0.662 seperti sempat disangka dari rumus teori di buku).

## 3. Ovality & Eccentricity

```
Ovality = (height_cm - AE_cm) / height_cm
```
`AE_cm` adalah jarak proyeksi titik terjauh kontur asli telur terhadap sumbu panjang elips hasil
`cv2.fitEllipse()` — mengukur seberapa jauh bentuk telur menyimpang dari elips sempurna.

```
Eccentricity = sqrt(1 - (b² / a²))
```
di mana `a` = setengah sumbu panjang, `b` = setengah sumbu pendek elips.

## 4. GLCM Contrast (tekstur)

```
Contrast = Σ (i - j)² * P(i, j)     untuk i, j = 0 ... N-1
```

di mana `P(i,j)` adalah probabilitas kemunculan pasangan piksel bertetangga dengan intensitas `i` dan `j`, dan `N` adalah jumlah gray level.

Implementasi menggunakan `skimage.feature.graycomatrix` + `graycoprops` dengan `distances=[1]`, `angles=[0, π/2]`, `levels=32` (dikonfirmasi dari `hardware/main.py`).

## 5. Feature Vector (Model Final — 13 Fitur)

10 fitur dasar hasil ekstraksi + 3 fitur turunan (engineered), urutan sesuai `ml/preprocessing.py`:

```
x_i = [height_cm, width_cm, shape_index, ovality, eccentricity,
       surface_area, volume, density, weight_grams, glcm_contrast,
       height_width_ratio, volume_surface_ratio, density_ratio]
```

Fitur turunan:
```
height_width_ratio   = height_cm / (width_cm + 1e-6)
volume_surface_ratio = volume / (surface_area + 1e-6)
density_ratio         = density / (weight_grams + 1e-6)
```

> ℹ️ Buku TA (Tabel 5.17) hanya menyebutkan 6 fitur dalam narasi kontribusi fitur teratas
> (GLCM Contrast, width_cm, shape_index, volume, weight_grams + height_cm dengan kontribusi kecil),
> tapi kode asli di alat ternyata memakai 13 fitur total. Dokumentasi ini sudah disesuaikan dengan
> kode asli — kalau kamu update jurnal/tugas akhir, pertimbangkan menyebutkan seluruh 13 fitur ini.

## 6. Kalibrasi Skala Piksel → CM

```
scale_factor (load cell) = raw_hx711 / berat_aktual_gram
SCALE_MAJOR / SCALE_MINOR (kamera) = ukuran_aktual_cm / ukuran_piksel
```

Hasil kalibrasi (dari kode asli `hardware/main.py`):
- `CM_PER_PIXEL_MAJOR = 0.00541`
- `CM_PER_PIXEL_MINOR = 0.00540`
- Rata-rata scale factor load cell (contoh pengujian buku TA): **7696.51**
