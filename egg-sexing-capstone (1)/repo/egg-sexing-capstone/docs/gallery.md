# Galeri Dokumentasi Visual

Seluruh gambar diambil langsung dari Buku Capstone Design (diekstrak otomatis dari PDF).
Kalau ada gambar yang tertukar/kurang pas dengan captionnya (wajar, ekstraksi dilakukan otomatis
per-halaman), tinggal ganti file-nya dengan foto/screenshot aslimu — nama file & struktur foldernya
sudah dibuat mengikuti pengelompokan berikut.

## 1. Hardware & Prototipe

| | |
|---|---|
| ![Raspberry Pi 4B](images/hardware_raspberry_pi4.png) Raspberry Pi 4 Model B | ![Komponen](images/hardware_camera_or_loadcell_1.png) Kamera / Load Cell |
| ![Komponen](images/hardware_camera_or_loadcell_2.png) PCB LED / MOSFET Candling | ![Conveyor/LCD](images/hardware_conveyor_or_lcd.png) Mini Conveyor / LCD 4.3" |

**Prototipe alat lengkap:**

![Prototipe Alat](images/prototipe_alat_0.png)

## 2. Diagram Sistem

| Hardware Block Diagram | Wiring Diagram |
|---|---|
| ![Hardware Block Diagram](images/hardware_block_diagram.png) | ![Wiring Diagram](images/wiring_diagram_0.png) |

| Flowchart Sistem | Flowchart Model ML |
|---|---|
| ![Flowchart Sistem](images/flowchart_sistem_0.png) | ![Flowchart ML](images/flowchart_ml_0.png) |

## 3. Dashboard Web

Desain awal (mockup) halaman Data Telur:

![Mockup Data Telur](images/dashboard_mockup_data_telur.png)

Hasil implementasi:

| Tabel Data Telur | Card Data Terbaru |
|---|---|
| ![Tabel](images/dashboard_tabel_data_telur.png) | ![Egg Card](images/dashboard_egg_card_terbaru.png) |

| Statistik | Pie Chart Gender |
|---|---|
| ![Stats Card](images/dashboard_stats_cards.png) | ![Pie Chart](images/dashboard_pie_chart_gender.png) |

**Grouped bar chart — distribusi fitur top berdasarkan gender:**

![Grouped Bar Chart](images/dashboard_grouped_bar_top_feature.png)

## 4. Proses Validasi Dataset (Ground Truth)

Alur pelacakan telur individual dari akuisisi data → penetasan → sexing DOC, untuk memastikan label
jenis kelamin pada dataset sesuai kondisi nyata:

| Labeling Telur | Akuisisi Data (Candling) |
|---|---|
| ![Labeling](images/validasi_proses_labeling.jpeg) | ![Akuisisi](images/validasi_proses_akuisisi.jpeg) |

| Candling Hari ke-19 | Basket Penetasan + Sekat |
|---|---|
| ![Candling H-19](images/validasi_candling_hari19.jpeg) | ![Basket Sekat](images/validasi_basket_sekat.jpeg) |

**Proses Sexing DOC (pencocokan hasil dengan kode identifikasi telur):**

![Sexing DOC](images/validasi_sexing_doc.jpeg)

## 5. Evaluasi Model Machine Learning

**Confusion Matrix (SVM-RBF + GLCM Contrast, 50 data uji):**

![Confusion Matrix](images/confusion_matrix_svm.png)

- Betina: 21 aktual → 18 benar, 3 salah diprediksi jantan
- Jantan: 29 aktual → 26 benar, 3 salah diprediksi betina
- Akurasi keseluruhan: **88%**

**Feature Contribution (Permutation Importance):**

![Feature Contribution](images/feature_contribution_svm.png)

GLCM Contrast mendominasi kontribusi (44%) — lihat rincian di [`model_results.md`](model_results.md).
