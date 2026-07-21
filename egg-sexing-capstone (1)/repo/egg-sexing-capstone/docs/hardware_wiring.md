# Wiring & Pin Configuration

## Ringkasan Wiring pada Raspberry Pi

| No | Komponen | Fungsi | Pin Fisik | GPIO |
|----|----------|--------|-----------|------|
| 1 | HX711 | DOUT (DT) | Pin 29 | GPIO 5 |
| 2 | HX711 | SCK | Pin 31 | GPIO 6 |
| 3 | Push Button | Trigger Input | Pin 35 | GPIO 19 |
| 4 | Driver L298N | ENA (PWM) | Pin 33 | GPIO 13 |
| 5 | Driver L298N | IN1 | Pin 38 | GPIO 20 |
| 6 | Driver L298N | IN2 | Pin 36 | GPIO 16 |
| 7 | MOSFET LED Candling | PWM Output | Pin 12 | GPIO 18 |
| 8 | Kamera Raspberry Pi | Data | CSI Port | CSI |

> ⚠️ Catatan: pada beberapa potongan kode implementasi di buku TA, pin LED candling (`SENTER`) ditulis menggunakan **GPIO 17 (pin fisik 11)**. Cek ulang wiring fisik alatmu dan samakan dengan `hardware/config.py` sebelum menjalankan sistem — kemungkinan ini beda revisi prototipe.

## Diagram

![Hardware Block Diagram](images/hardware_block_diagram_0.png)

![Wiring Diagram](images/wiring_diagram_0.png)

## Modul Fungsional

- **Modul Pemrosesan & Kontrol** — Raspberry Pi 4B sebagai pusat kendali seluruh sistem, menjalankan program utama termasuk inferensi model ML.
- **Modul Akuisisi Citra** — Kamera Raspberry Pi via CSI, posisi tetap menghadap ke bawah untuk konsistensi sudut & pencahayaan.
- **Modul Pencahayaan** — LED 12V candling dikendalikan MOSFET via sinyal PWM, ditempatkan di bawah telur.
- **Modul Sensor Berat** — Load cell + HX711 (ADC 24-bit), hasil dikalibrasi dengan scale factor.
- **Modul Input Pengguna** — Push button sebagai trigger manual tiap tahap proses.
- **Modul Conveyor** — Motor DC + driver L298N, memindahkan telur ke area akuisisi citra secara otomatis.

## Bill of Materials (perkiraan biaya prototipe)

| Item | Qty | Harga Satuan (Rp) | Total (Rp) |
|---|---|---|---|
| Raspberry Pi 4 (4GB) + MicroSD 32GB | 1 | 1.350.000 | 1.350.000 |
| Layar LCD Raspberry Pi 4.3" | 1 | 450.000 | 450.000 |
| Kamera Raspberry Pi 5MP | 1 | 150.000 | 150.000 |
| Breadboard Half Size | 1 | 10.000 | 10.000 |
| Modul Load Cell + HX711 | 1 | 50.000 | 50.000 |
| Kabel Jumper, Resistor (1 set) | 1 | 15.000 | 15.000 |
| Bahan chamber pencahayaan (akrilik, LED) | 1 | 175.000 | 175.000 |
| Mini Conveyor | 1 | 298.000 | 298.000 |
| MOSFET Trigger Switch | 1 | 30.000 | 30.000 |
| Power Supply 12V 5A | 1 | 120.000 | 120.000 |
| Step-down module XY-3606 | 1 | 30.000 | 30.000 |
| **Total** | | | **Rp 2.100.000** |
