"""
Konfigurasi pin GPIO Raspberry Pi.
Referensi: docs/hardware_wiring.md — Tabel 3.20 (Buku Capstone Design)

# TODO: cocokkan ulang nomor pin dengan wiring fisik di alatmu.
# Ada sedikit ambiguitas di buku TA: LED candling (SENTER) tertulis GPIO 18
# di tabel wiring, tapi GPIO 17 di potongan kode software. Pilih salah satu
# sesuai wiring aktual sebelum menjalankan main.py.
"""

# --- Load Cell (HX711) ---
DOUT = 5     # Pin fisik 29
SCK = 6      # Pin fisik 31

# --- Push Button ---
BUTTON_PIN = 19  # Pin fisik 35

# --- Motor Driver L298N (Conveyor) ---
ENA = 13     # Pin fisik 33 (PWM)
IN1 = 20     # Pin fisik 38
IN2 = 16     # Pin fisik 36

# --- LED Candling (MOSFET MTR-0037) ---
SENTER = 17  # Pin fisik 11 (GPIO17) -- lihat catatan TODO di atas

# --- Parameter Conveyor ---
SPEED_CONVEYOR = 60   # duty cycle PWM (%)
JEDA_STOP = 0.3       # detik, jeda setelah conveyor berhenti

# --- Kalibrasi Kamera (hasil kalibrasi contoh, ganti sesuai kalibrasi ulangmu) ---
SCALE_MAJOR = 0.005666  # cm/pixel (panjang)
SCALE_MINOR = 0.005719  # cm/pixel (lebar)

# --- File paths ---
SCALE_FACTOR_FILE = "scale_factor.txt"
RAW_IMAGE_PATH = "capture.jpg"
