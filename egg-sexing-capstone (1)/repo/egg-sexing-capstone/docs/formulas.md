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
V  = (SA / 4.951) ** (1 / 0.662)      # volume telur (cm³)
```

> Catatan implementasi: pada kode di buku TA eksponen pembagi volume tertulis `1/0.666`, sedangkan rumus (3) di bagian teori memakai `0.662`. Cek ulang mana yang dipakai final — kemungkinan salah satunya typo pengetikan di buku.

## 3. GLCM Contrast (tekstur)

```
Contrast = Σ (i - j)² * P(i, j)     untuk i, j = 0 ... N-1
```

di mana `P(i,j)` adalah probabilitas kemunculan pasangan piksel bertetangga dengan intensitas `i` dan `j`, dan `N` adalah jumlah gray level.

Implementasi menggunakan `skimage.feature.graycomatrix` + `graycoprops` dengan `distances=[1,2]`, `angles=[0, π/4, π/2]`, `levels=32`.

## 4. Feature Vector

```
x_i = [height_cm, width_cm, shape_index, volume, weight_grams, glcm_contrast]
```

## 5. Kalibrasi Skala Piksel → CM

```
scale_factor (load cell) = raw_hx711 / berat_aktual_gram
SCALE_MAJOR / SCALE_MINOR (kamera) = ukuran_aktual_cm / ukuran_piksel
```

Hasil kalibrasi (contoh dari pengujian):
- Rata-rata scale factor load cell: **7696.51**
- Scale factor kamera: **0.005666 cm/px** (panjang), **0.005719 cm/px** (lebar)
- MAPE pengukuran: **0.744%** (panjang), **1.537%** (lebar)
