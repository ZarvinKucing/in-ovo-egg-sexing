"""
Program Utama Sistem Deteksi Jenis Kelamin Telur.
Referensi: Buku Capstone Design, Bab 4.2.1 - 4.2.3.

Alur:
1. Tunggu trigger push button
2. Baca berat telur (load cell)
3. Gerakkan conveyor ke posisi akuisisi citra
4. Nyalakan LED candling -> ambil citra -> matikan LED
5. Ekstraksi fitur dari citra (lihat ml/feature_extraction.py)
6. Prediksi jenis kelamin dengan model SVM (lihat ml/predict.py)
7. Upload hasil ke Firebase

# TODO: Ini kerangka integrasi berdasarkan potongan kode di buku TA.
# Belum ada versi utuh & teruji langsung dari Raspberry Pi asli — silakan
# lengkapi/sesuaikan begitu file aslinya sudah dipindahkan dari Pi.
"""

import time
import sys
import RPi.GPIO as GPIO

from config import BUTTON_PIN
import conveyor
import led_control
import weight_sensor
import camera
import firebase_uploader

# Modul ML (lihat folder ../ml)
sys.path.append("../ml")
import feature_extraction  # TODO: pastikan model .pkl sudah ada di ml/models/
import predict


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def tunggu_trigger():
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        time.sleep(0.1)


def main_loop():
    firebase_uploader.init_firebase()
    egg_counter = 0

    print("Sistem siap. Tekan tombol untuk memulai proses akuisisi...")
    while True:
        tunggu_trigger()
        egg_counter += 1
        print(f"\n=== Memproses telur ke-{egg_counter} ===")

        # 1. Baca berat
        weight = weight_sensor.baca_berat()

        # 2. Gerakkan conveyor ke posisi kamera
        conveyor.conveyor_maju(durasi=2.0)  # TODO: sesuaikan durasi dengan jarak alatmu

        # 3. Nyalakan LED, ambil citra, matikan LED
        led_control.senter_on()
        img_path = camera.ambil_citra()
        led_control.senter_off()

        # 4. Ekstraksi fitur
        features = feature_extraction.extract_all_features(img_path, weight)

        # 5. Prediksi
        prediction = predict.predict_gender(features)
        print(f"Hasil prediksi: {prediction}")

        # 6. Upload ke Firebase
        firebase_uploader.upload_hasil(
            egg_id_prefix=f"EGG-{egg_counter:04d}",
            batch_label="batch-1",       # TODO: buat dinamis sesuai kebutuhan lapangan
            incubation_day=0,
            weight=weight,
            features=features,
            prediction=prediction,
        )


if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")
    finally:
        GPIO.cleanup()
