"""
Kalibrasi Load Cell + HX711.

Jalankan sekali sebelum main.py untuk menghasilkan scale_factor.txt.
Referensi: Buku Capstone Design, Bab 4.2.1 (Hasil Kalibrasi Load Cell dan HX711).

scale_factor = raw_hx711 / berat_aktual_gram

# TODO: proses ini sebaiknya diulang tiap kali load cell dipasang ulang
# atau posisi mounting berubah, karena scale factor bisa bergeser.
"""

import statistics
from hx711 import HX711
from config import DOUT, SCK, SCALE_FACTOR_FILE


def kalibrasi(n_sample: int = 5):
    hx = HX711(DOUT, SCK)
    hx.tare()

    scale_factors = []
    for i in range(n_sample):
        input(f"Letakkan sampel telur ke-{i + 1}, lalu tekan Enter...")
        raw = hx.get_raw_data(times=10)
        raw_value = sum(raw) / len(raw)

        berat_aktual = float(input("Masukkan berat aktual (gram, dari timbangan digital): "))
        scale_factor = raw_value / berat_aktual
        scale_factors.append(scale_factor)
        print(f"  Raw: {raw_value:.2f}  Berat: {berat_aktual}g  Scale Factor: {scale_factor:.2f}")

    rata_rata = statistics.mean(scale_factors)
    with open(SCALE_FACTOR_FILE, "w") as f:
        f.write(str(rata_rata))

    print(f"\nKalibrasi selesai. Rata-rata scale factor: {rata_rata:.2f}")
    print(f"Tersimpan di {SCALE_FACTOR_FILE}")


if __name__ == "__main__":
    kalibrasi()
