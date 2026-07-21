"""
Pembacaan berat telur via Load Cell + HX711.
Referensi: Buku Capstone Design, Bab 4.2.1 (Software Raspberry Pi - Pembacaan Berat).
"""

import os
from hx711 import HX711
from config import DOUT, SCK, SCALE_FACTOR_FILE


def load_scale_factor() -> float:
    if not os.path.exists(SCALE_FACTOR_FILE):
        raise FileNotFoundError(
            f"{SCALE_FACTOR_FILE} tidak ditemukan. Jalankan calibration.py dulu."
        )
    with open(SCALE_FACTOR_FILE, "r") as f:
        return float(f.read().strip())


def baca_berat() -> float:
    scale = load_scale_factor()
    hx = HX711(DOUT, SCK)
    hx.tare()
    weight = hx.get_weight(scale)
    print(f"Berat: {weight:.2f} gram")
    return weight
