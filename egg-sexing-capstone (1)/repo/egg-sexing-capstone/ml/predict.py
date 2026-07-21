"""
Inferensi Model SVM untuk Prediksi Jenis Kelamin Telur.
Dipanggil dari hardware/main.py setelah fitur diekstraksi.
"""

import joblib
from preprocessing import FEATURES

MODEL_PATH = "models/svm_model.pkl"  # TODO: sesuaikan path relatif saat dipanggil dari hardware/main.py

_model = None


def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_gender(features: dict) -> str:
    """
    features: dict dengan key height_cm, width_cm, shape_index, volume,
              weight_grams, glcm_contrast
    return: "jantan" atau "betina"
    """
    model = _load_model()
    x = [[features[f] for f in FEATURES]]
    pred = model.predict(x)[0]
    return "jantan" if pred == 1 else "betina"
