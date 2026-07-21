"""
Upload hasil ekstraksi fitur & prediksi ke Firebase Realtime Database.
Referensi: Buku Capstone Design, Bab 4.2.3 (Implementasi Firebase Realtime Database).

Setup:
1. Download serviceAccountKey.json dari Firebase Console (Project Settings > Service Accounts)
2. Taruh file tersebut di folder hardware/ (JANGAN commit ke git — sudah ada di .gitignore)
3. Isi FIREBASE_DB_URL sesuai project Firebase-mu
"""

import os
from datetime import datetime
import pytz

import firebase_admin
from firebase_admin import credentials, db

FIREBASE_CRED = "serviceAccountKey.json"
FIREBASE_DB_URL = ""  # TODO: isi URL Firebase Realtime Database-mu, mis. "https://<project-id>-default-rtdb.asia-southeast1.firebasedatabase.app"

wib = pytz.timezone("Asia/Jakarta")


def init_firebase():
    if os.path.exists(FIREBASE_CRED) and not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CRED)
        firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_DB_URL})
        print("[Firebase] Initialized")


def upload_hasil(egg_id_prefix: str, batch_label: str, incubation_day: int,
                  weight: float, features: dict, prediction: str):
    """
    features: dict berisi width_cm, height_cm, shape_index, glcm_contrast, dll.
    prediction: "jantan" atau "betina" (hasil model SVM)
    """
    row = {
        "egg_id": egg_id_prefix,
        "batch_label": batch_label,
        "incubation_day": incubation_day,
        "weight_grams": weight,
        "width_cm": features["width_cm"],
        "height_cm": features["height_cm"],
        "shape_index": features["shape_index"],
        "glcm_contrast": features["glcm_contrast"],
        "gender": prediction,
        "timestamp": datetime.now(wib).isoformat(),
    }

    egg_id = db.reference("egg_id").push().key
    db.reference(f"{egg_id}").set(row)
    print("[Firebase] Uploaded:", egg_id)
    return egg_id
