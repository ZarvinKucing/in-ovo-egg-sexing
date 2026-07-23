#!/usr/bin/env python3
# ======================================================
# Raspberry Pi 4 – Egg Feature Extraction
# UPDATED FLOW:
# 1) Load cell dulu
# 2) Button untuk lanjut tahap
# 3) Conveyor maju
# 4) Senter/candling ON
# 5) Preview kamera sampai tombol ditekan
# 6) Capture + ekstraksi fitur
# 7) Conveyor mundur
# ======================================================

import time
import os
import csv
import cv2
import numpy as np
import subprocess
import RPi.GPIO as GPIO
from datetime import datetime, timezone, timedelta

import joblib

import firebase_admin
from firebase_admin import credentials, db
from skimage.feature import graycomatrix, graycoprops
from hx711 import HX711
from scipy.ndimage import convolve


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ===========================
# CONFIG
# ===========================
CM_PER_PIXEL_MAJOR = 0.00541
CM_PER_PIXEL_MINOR = 0.00540 

# --- GPIO PIN ---
BUTTON_PIN = 19          # P19 = OUT button
SENTER_PIN = 18          # P18 = TRIG/PWM MOSFET MTR-0037

# HX711
DOUT = 5                 # P05 = DT HX711
SCK = 6                  # P06 = SCK HX711

# L298N Conveyor
ENA = 13                 # P13 = PWM speed
IN1 = 20                 # P20 = IN1
IN2 = 16                 # P16 = IN2

# --- FLOW SETTING ---
DEFAULT_BATCH_LABEL = "batch_auto"
DEFAULT_INCUBATION_DAY = 0

SPEED_CONVEYOR = 45      # 0 - 100
DURASI_MAJU = 0.75        # detik, kalibrasi sesuai posisi kamera
DURASI_MUNDUR = 0.8      # detik, kalibrasi sesuai balik awal
JEDA_STOP = 0.7
JEDA_SENTER_STABIL = 1.0


USE_TARE_OFFSET = False

PREVIEW_X = 50
PREVIEW_Y = 50
PREVIEW_W = 480
PREVIEW_H = 360

RESULT_WINDOW = "EXTRACTION RESULT"

FIREBASE_CRED = os.path.join(BASE_DIR, "in-ovo-sexing-firebase-adminsdk-fbsvc-40e9f3160c.json")

FIREBASE_DB_URL = (
    "https://in-ovo-sexing-default-rtdb.asia-southeast1.firebasedatabase.app/"
)

MODEL_PATH = os.path.join(BASE_DIR, "egg_gender_model.pkl")

IMG_DIR = os.path.join(BASE_DIR, "captures")
RAW_DIR = os.path.join(IMG_DIR, "raw")
BOXED_DIR = os.path.join(IMG_DIR, "boxed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(BOXED_DIR, exist_ok=True)

CSV_PATH = os.path.join(BASE_DIR, "egg_features_batch2.csv")

GLCM_LEVELS = 32
GLCM_DIST = [1]
GLCM_ANGLES = [0, np.pi/2]

wib = timezone(timedelta(hours=7))

# ===========================
# LOAD SCALE FACTOR
# ===========================
def load_scale_factor():
    path = os.path.join(BASE_DIR, "scale_factor.txt")

    with open(path, "r") as f:
        return float(f.read().strip())

# ===========================
# INIT GPIO
# ===========================
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Button module:
# VCC putih  -> pin 17 / 3.3V
# OUT coklat -> GPIO19 / P19
# GND hitam  -> GND
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Senter/MOSFET
GPIO.setup(SENTER_PIN, GPIO.OUT)
GPIO.output(SENTER_PIN, GPIO.LOW)

# Conveyor
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
pwm_motor = GPIO.PWM(ENA, 1000)
pwm_motor.start(0)

# HX711
scale_factor = load_scale_factor()
hx = HX711(DOUT, SCK)
hx.reset()
print("[HX711] Ready")
print("[HX711] Scale factor:", scale_factor)

# ===========================
# LOAD MODEL
# ===========================
model_package = None

if os.path.exists(MODEL_PATH):
    model_package = joblib.load(MODEL_PATH)
    print("[MODEL] Loaded:", MODEL_PATH)
    print("[MODEL] Features:", model_package["features"])
else:
    print(f"[MODEL] WARNING: Model tidak ditemukan di {MODEL_PATH}. Prediksi gender tidak akan aktif.")

# ===========================
# INIT FIREBASE
# ===========================
firebase_ready = False

if os.path.exists(FIREBASE_CRED) and not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED)
    firebase_admin.initialize_app(cred, {
        "databaseURL": FIREBASE_DB_URL
    })
    firebase_ready = True
    print("[Firebase] Initialized")
else:
    print("[Firebase] Credential tidak ditemukan / Firebase tidak aktif. Data tetap disimpan ke CSV lokal.")

# ===========================
# BUTTON HELPER
# ===========================
def wait_button(message="Tekan tombol untuk lanjut..."):
    print("\n" + message)

    # tunggu tombol dilepas dulu supaya tidak double-trigger
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        cv2.waitKey(30)
        time.sleep(0.03)

    # tunggu tombol ditekan
    while GPIO.input(BUTTON_PIN) == GPIO.LOW:
        cv2.waitKey(30)
        time.sleep(0.03)

    time.sleep(0.25)  # debounce

    # tunggu dilepas lagi
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        cv2.waitKey(30)
        time.sleep(0.03)

    time.sleep(0.15)

# ===========================
# CSV SAVE
# ===========================
def append_csv(row):
    exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(row)

# ===========================
# HX711 READ
# ===========================
def read_raw_average(samples=10):
    values = []
    for _ in range(samples):
        raw = hx.read_long()
        values.append(raw)
        time.sleep(0.08)

    return sum(values) / len(values)

def tare_loadcell():
    if not USE_TARE_OFFSET:
        hx.reset()
        return 0.0

    print("[HX711] Tare: kosongkan load cell...")
    tare_raw = read_raw_average(samples=15)
    print("[HX711] Tare raw =", round(tare_raw, 2))
    return tare_raw

def read_weight_grams(tare_raw=0.0):
    raw = read_raw_average(samples=15)

    if USE_TARE_OFFSET:
        weight = (raw - tare_raw) / scale_factor
    else:
        weight = raw / scale_factor

    return weight, raw

# ===========================
# CONVEYOR CONTROL
# ===========================
def conveyor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm_motor.ChangeDutyCycle(0)
    print("[CONVEYOR] Stop")
    time.sleep(JEDA_STOP)

def conveyor_maju():
    print("[CONVEYOR] Maju")
    pwm_motor.ChangeDutyCycle(SPEED_CONVEYOR)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(DURASI_MAJU)
    conveyor_stop()

def conveyor_mundur():
    print("[CONVEYOR] Mundur")
    pwm_motor.ChangeDutyCycle(SPEED_CONVEYOR)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(DURASI_MUNDUR)
    conveyor_stop()

# ===========================
# SENTER CONTROL
# ===========================
def senter_on():
    GPIO.output(SENTER_PIN, GPIO.HIGH)
    print("[SENTER] ON")

def senter_off():
    GPIO.output(SENTER_PIN, GPIO.LOW)
    print("[SENTER] OFF")

# ===========================
# LIVE PREVIEW
# ===========================
def live_preview_until_button():
    p = subprocess.Popen([
        "rpicam-hello",
        "-t", "0"
    ])

    print("[CAMERA] Preview aktif.")
    print("[CAMERA] Tekan tombol jika posisi telur sudah siap untuk capture.")

    # tunggu tombol dilepas dulu
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        time.sleep(0.05)

    # tunggu tombol capture
    while GPIO.input(BUTTON_PIN) == GPIO.LOW:
        time.sleep(0.05)

    time.sleep(0.25)

    # tutup preview
    p.terminate()

    try:
        p.wait(timeout=3)
    except subprocess.TimeoutExpired:
        p.kill()

    # pastikan semua proses rpicam mati
    subprocess.run(
        ["pkill", "-f", "rpicam"],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    )

    # beri waktu libcamera release resource
    time.sleep(2)

# ===========================
# GLCM FEATURE
# ===========================
def extract_glcm_features(gray, mask):
    roi = gray.copy()
    roi[mask == 0] = 0
    roi_q = np.floor(roi / (256 / GLCM_LEVELS)).astype(np.uint8)

    glcm = graycomatrix(
        roi_q,
        distances=GLCM_DIST,
        angles=GLCM_ANGLES,
        levels=GLCM_LEVELS,
        symmetric=True,
        normed=True
    )

    return (
        graycoprops(glcm, 'contrast').mean()
    )

# ===========================
# FEATURE EXTRACTION
# ===========================
def compute_features(img, contour, weight, egg_mask, out_img):
    ellipse = cv2.fitEllipse(contour)
    (xc,yc),(w_px,h_px),angle = ellipse

    long_px = max(w_px,h_px)
    short_px = min(w_px,h_px)

    height_px = round(long_px, 2)
    width_px  = round(short_px, 2)

    height_cm = long_px * CM_PER_PIXEL_MAJOR
    width_cm  = short_px * CM_PER_PIXEL_MINOR
    shape_index = width_cm / height_cm if height_cm else 0

    theta = np.radians(angle)
    dx,dy = np.cos(theta), np.sin(theta)
    proj = [(pt[0]-xc)*dx + (pt[1]-yc)*dy for pt in contour[:,0]]
    AE_px = max(np.abs(proj)) if proj else 0
    AE_cm = AE_px * CM_PER_PIXEL_MAJOR
    ovality = (height_cm - AE_cm) / height_cm if height_cm else 0

    a = long_px / 2
    b = short_px / 2
    eccentricity = np.sqrt(1 - (b*b)/(a*a)) if a else 0

    surface_area = 4.835 * (weight ** 0.662)
    volume = (surface_area / 4.951) ** (1 / 0.666)
    density = weight / volume if volume else 0


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    glcm_contrast = extract_glcm_features(gray, egg_mask)

    vis = img.copy()
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(vis,(x,y),(x+w,y+h),(0,255,255),2)
    cv2.ellipse(vis,ellipse,(0,255,0),2)

    vis_small = cv2.resize(vis, (PREVIEW_W, PREVIEW_H))
    cv2.imwrite(out_img, vis_small)

    cv2.imshow(RESULT_WINDOW, vis_small)
    cv2.waitKey(1)

    return {
        "weight_grams": round(weight,2),
        "width_px": width_px,
        "height_px": height_px,
        "width_cm": round(width_cm,4),
        "height_cm": round(height_cm,4),
        "shape_index": round(shape_index,4),
        "ovality": round(ovality,4),
        "eccentricity": round(eccentricity,4),
        "surface_area": round(surface_area,4),
        "volume": round(volume,4),
        "density": round(density,6),
        "glcm_contrast": round(glcm_contrast,6),
    }

# ===========================
# GENDER PREDICTION
# ===========================
def predict_gender(features: dict) -> dict:
    """
    Jalankan inferensi model SVM dari feature dict hasil compute_features().
    Return dict berisi: gender_label, gender_code, confidence_pct
    """
    if model_package is None:
        return {
            "gender_label": "unknown",
            "gender_code": -1,
            "confidence_pct": 0.0
        }

    clf   = model_package["model"]
    feat_names = model_package["features"]   # 13 fitur (10 raw + 3 engineered)

    # --- Ambil 10 fitur dasar dari hasil ekstraksi ---
    base = {
        "height_cm"    : features["height_cm"],
        "width_cm"     : features["width_cm"],
        "shape_index"  : features["shape_index"],
        "ovality"      : features["ovality"],
        "eccentricity" : features["eccentricity"],
        "surface_area" : features["surface_area"],
        "volume"       : features["volume"],
        "density"      : features["density"],
        "weight_grams" : features["weight_grams"],
        "glcm_contrast": features["glcm_contrast"],
    }

    # --- Rekonstruksi 3 fitur engineered (sama persis seperti saat training) ---
    base["height_width_ratio"]   = base["height_cm"]   / (base["width_cm"]    + 1e-6)
    base["volume_surface_ratio"] = base["volume"]       / (base["surface_area"] + 1e-6)
    base["density_ratio"]        = base["density"]      / (base["weight_grams"] + 1e-6)

    # --- Susun array sesuai urutan kolom yang diharapkan model ---
    X = np.array([[base[f] for f in feat_names]])

    pred       = clf.predict(X)[0]
    proba      = clf.predict_proba(X)[0]
    confidence = float(proba[int(pred)]) * 100.0

    label_map = {0: "betina", 1: "jantan"}
    return {
        "gender_label"    : label_map[int(pred)],
        "gender_code"     : int(pred),
        "confidence_pct"  : round(confidence, 2)
    }

def generate_egg_code():
    date_str = datetime.now(wib).strftime("%Y%m%d")

    if firebase_ready:
        ref = db.reference("COUNTER")

        counter = ref.get()

        if counter is None:
            counter = 1
        else:
            counter += 1

        ref.set(counter)

    else:
        if not hasattr(generate_egg_code, "counter"):
            generate_egg_code.counter = 1
        else:
            generate_egg_code.counter += 1

        counter = generate_egg_code.counter

    return f"EGG-{counter:04d}"

# ===========================
# MAIN LOOP
# ===========================
def main():
    print("======================================")
    print("SYSTEM READY - FLOW BARU")
    print("1. Load cell dulu")
    print("2. Pindah ke conveyor")
    print("3. Preview + capture")
    print("======================================")

    batch_label = DEFAULT_BATCH_LABEL
    incubation_day = DEFAULT_INCUBATION_DAY

    try:
        while True:
            # 1. Tare / reset load cell
            wait_button("[STEP 1] Kosongkan load cell, lalu tekan tombol untuk mulai.")
            tare_raw = tare_loadcell()

            # 2. Baca berat telur
            wait_button("[STEP 2] Letakkan telur di load cell, lalu tekan tombol untuk baca berat.")
            weight, raw_weight = read_weight_grams(tare_raw)
            print("\n=== BERAT TELUR ===")
            print("Raw HX711 :", round(raw_weight, 2))
            print("Berat     :", round(weight, 2), "gram")
            print("===================\n")

            # 3. User pindahkan telur ke conveyor
            wait_button("[STEP 3] Ambil telur dari load cell, taruh di tatakan conveyor, lalu tekan tombol.")

            # 4. Conveyor maju ke area kamera
            conveyor_maju()

            # 5. Senter ON + preview
            senter_on()
            time.sleep(JEDA_SENTER_STABIL)
            
            live_preview_until_button()

            # ===== CREATE ID FIRST
            if firebase_ready:
                kode = generate_egg_code()
            else:
                kode = datetime.now(wib).strftime("%Y%m%d_%H%M%S")

            raw_img = os.path.join(
                RAW_DIR,
                f"raw_{batch_label}_{kode}.jpg"
            )

            # 6. Capture image
            print("[CAMERA] Capture image...")
            subprocess.run(
                ["rpicam-still", "-n","-o", raw_img],
                check=True
            )

            img = cv2.imread(raw_img)
            if img is None:
                print("[ERROR] Gambar gagal dibaca.")
                senter_off()
                conveyor_mundur()
                continue

            # ===========================
            # HSV SEGMENTATION
            # ===========================
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Range HSV hasil tuning
            lower = np.array([8, 45, 60])
            upper = np.array([40, 255, 255])

            mask = cv2.inRange(hsv, lower, upper)

            # Blur
            mask = cv2.GaussianBlur(mask, (5, 5), 0)

# Morphology
            kernel_close = np.ones((7, 7), np.uint8)
            kernel_open  = np.ones((3, 3), np.uint8)

            mask = cv2.morphologyEx(
                mask,
                cv2.MORPH_CLOSE,
                kernel_close,
                iterations=2
            )

            mask = cv2.morphologyEx(
                mask,
                cv2.MORPH_OPEN,
                kernel_open,
                iterations=1
            )

# Ambil contour terbesar lalu isi penuh
            cnts, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            if cnts:
                contour = max(cnts, key=cv2.contourArea)

                mask = np.zeros_like(mask)

                cv2.drawContours(
                    mask,
                    [contour],
                    -1,
                    255,
                    thickness=cv2.FILLED
                )

            cnts,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = [c for c in cnts if cv2.contourArea(c) > 5000]

            if not cnts:
                print("No egg detected")
                senter_off()
                conveyor_mundur()
                continue

            contour = max(cnts, key=cv2.contourArea)

            boxed_img = os.path.join(
                BOXED_DIR,
                f"result_{batch_label}_{kode}.jpg"
            )

            features = compute_features(img, contour, weight, mask, boxed_img)

            # ===== GENDER PREDICTION =====
            gender_result = predict_gender(features)
            gender_label  = gender_result["gender_label"]
            confidence    = gender_result["confidence_pct"]

            print("\n=== HASIL DETEKSI TELUR ===")
            print(f"Berat           : {features['weight_grams']} gram")
            print(f"Tinggi (px)     : {features['height_px']}")
            print(f"Lebar  (px)     : {features['width_px']}")
            print(f"Tinggi (cm)     : {features['height_cm']}")
            print(f"Lebar  (cm)     : {features['width_cm']}")
            print(f"GLCM Contrast   : {features['glcm_contrast']}")
            print(f"--- PREDIKSI ---")
            print(f"Gender          : {gender_label.upper()}  (confidence: {confidence}%)")
            print("============================\n")

            row = {
                "kode": kode,
                "batch_label": batch_label,
                "incubation_day": incubation_day,
                "image_file": os.path.basename(boxed_img),
                "source_image": os.path.basename(raw_img),
                "raw_hx711": round(raw_weight, 2),
                **features,
                "gender"      : gender_label,
                "gender_code"      : gender_result["gender_code"],
                "confidence"   : confidence,
                "detected": True,
                "timestamp": datetime.now(wib).isoformat()
            }

            if firebase_ready:
                ref = db.reference(kode)
                ref.set(row)
                print("[Firebase] Uploaded:", kode)

            append_csv(row)
            print("[CSV] Saved:", CSV_PATH)

            # 7. User lihat hasil, lalu tekan tombol untuk balik awal
            wait_button("[STEP 4] Hasil tampil. Tekan tombol untuk matikan senter dan conveyor balik.")
            cv2.destroyAllWindows()

            senter_off()
            conveyor_mundur()

            print("\n[SYSTEM] Siap untuk telur berikutnya.\n")

    except KeyboardInterrupt:
        print("Exit")

    finally:
        try:
            senter_off()
            conveyor_stop()
            pwm_motor.stop()
        except:
            pass
        GPIO.cleanup()
        cv2.destroyAllWindows()

# ===========================
# ENTRY
# ===========================
if __name__ == "__main__":
    main()
