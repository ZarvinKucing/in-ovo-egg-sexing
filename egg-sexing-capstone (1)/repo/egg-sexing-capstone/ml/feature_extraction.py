"""
Ekstraksi Fitur Morfologi, Fisik, dan Tekstur Telur.
Referensi: Buku Capstone Design, Bab 4.2.2 (Implementasi Machine Learning - Ekstraksi Data).

Fitur yang dihasilkan: height_cm, width_cm, shape_index, volume, weight_grams, glcm_contrast
"""

import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops

# Faktor skala hasil kalibrasi kamera (cm/pixel)
# TODO: ganti dengan hasil kalibrasi kamera terbaru di alatmu
SCALE_MAJOR = 0.005666
SCALE_MINOR = 0.005719

# Rentang HSV untuk thresholding objek telur saat candling
# TODO: nilai ini sangat bergantung pada kondisi chamber & LED — kalibrasi ulang
# kalau hasil segmentasi meleset (mask kosong / noise besar)
HSV_LOWER = np.array([8, 45, 60])
HSV_UPPER = np.array([40, 255, 255])


def segment_egg(img):
    """Segmentasi objek telur dari background chamber menggunakan HSV thresholding."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, HSV_LOWER, HSV_UPPER)
    return mask


def detect_ellipse(mask):
    """Deteksi kontur terbesar & fitting elips untuk mendapat sumbu mayor/minor."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    largest_contour = max(contours, key=cv2.contourArea)
    if len(largest_contour) >= 5:
        ellipse = cv2.fitEllipse(largest_contour)
        (x, y), (axes_width, axes_height), angle = ellipse
        major = max(axes_width, axes_height)
        minor = min(axes_width, axes_height)
        return {"ellipse": ellipse, "major_px": major, "minor_px": minor,
                "center": (x, y), "angle": angle}
    return None


def compute_glcm_contrast(roi_gray):
    """Hitung fitur tekstur GLCM Contrast dari ROI grayscale citra telur."""
    glcm = graycomatrix(
        roi_gray,
        distances=[1, 2],
        angles=[0, np.pi / 4, np.pi / 2],
        levels=32,
        symmetric=True,
        normed=True,
    )
    glcm_contrast = graycoprops(glcm, "contrast").mean()
    return glcm_contrast


def compute_volume(weight_grams: float) -> float:
    """Estimasi volume telur (cm^3) dari massa, via pendekatan empiris luas permukaan."""
    surface_area = 4.835 * (weight_grams ** 0.662)
    # TODO: cek konsistensi eksponen -- buku TA menulis 1/0.666 di kode,
    # tapi 0.662 di rumus teoritis. Pilih salah satu & samakan di semua tempat.
    volume = (surface_area / 4.951) ** (1 / 0.662)
    return volume


def extract_all_features(image_path: str, weight_grams: float) -> dict:
    """Pipeline ekstraksi fitur lengkap dari satu citra + berat telur."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Gagal membaca citra: {image_path}")

    mask = segment_egg(img)
    ellipse_data = detect_ellipse(mask)
    if ellipse_data is None:
        raise ValueError("Tidak ada objek telur terdeteksi pada citra.")

    height_cm = ellipse_data["major_px"] * SCALE_MAJOR
    width_cm = ellipse_data["minor_px"] * SCALE_MINOR
    shape_index = width_cm / height_cm

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # TODO: crop ROI di sekitar area telur saja sebelum hitung GLCM
    # supaya tidak ikut menghitung tekstur background chamber
    roi_gray = gray
    glcm_contrast = compute_glcm_contrast(roi_gray)

    volume = compute_volume(weight_grams)

    return {
        "height_cm": height_cm,
        "width_cm": width_cm,
        "shape_index": shape_index,
        "volume": volume,
        "weight_grams": weight_grams,
        "glcm_contrast": glcm_contrast,
    }
