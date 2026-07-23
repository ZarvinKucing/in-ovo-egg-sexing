"""
Ekstraksi Fitur Morfologi, Fisik, dan Tekstur Telur.

Ini adalah versi standalone dari fungsi `compute_features()` yang dipakai
langsung di `hardware/main.py`. Kegunaannya di sini: mengekstraksi ulang
fitur secara batch dari kumpulan citra mentah (mis. folder `captures/raw/`)
untuk membangun/reproduce dataset CSV training tanpa harus menjalankan
Raspberry Pi.

Fitur yang dihasilkan (10 fitur dasar + 3 fitur turunan, total 13):
height_cm, width_cm, shape_index, ovality, eccentricity, surface_area,
volume, density, weight_grams, glcm_contrast,
height_width_ratio, volume_surface_ratio, density_ratio
"""

import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops

# Faktor skala hasil kalibrasi kamera (cm/pixel) -- lihat hardware/main.py CONFIG
CM_PER_PIXEL_MAJOR = 0.00541
CM_PER_PIXEL_MINOR = 0.00540

# Rentang HSV hasil tuning untuk segmentasi objek telur saat candling
HSV_LOWER = np.array([8, 45, 60])
HSV_UPPER = np.array([40, 255, 255])

GLCM_LEVELS = 32
GLCM_DIST = [1]
GLCM_ANGLES = [0, np.pi / 2]


def segment_egg(img):
    """Segmentasi objek telur dari background chamber (HSV threshold + morphology + largest contour)."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, HSV_LOWER, HSV_UPPER)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    kernel_close = np.ones((7, 7), np.uint8)
    kernel_open = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open, iterations=1)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return None, None

    contour = max(cnts, key=cv2.contourArea)
    mask = np.zeros_like(mask)
    cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = [c for c in cnts if cv2.contourArea(c) > 5000]
    if not cnts:
        return None, None

    contour = max(cnts, key=cv2.contourArea)
    return contour, mask


def extract_glcm_contrast(gray, mask):
    """Fitur tekstur GLCM Contrast, dihitung hanya di dalam mask objek telur."""
    roi = gray.copy()
    roi[mask == 0] = 0
    roi_q = np.floor(roi / (256 / GLCM_LEVELS)).astype(np.uint8)

    glcm = graycomatrix(
        roi_q,
        distances=GLCM_DIST,
        angles=GLCM_ANGLES,
        levels=GLCM_LEVELS,
        symmetric=True,
        normed=True,
    )
    return graycoprops(glcm, "contrast").mean()


def compute_features(img, contour, weight_grams, egg_mask):
    """Pipeline ekstraksi 10 fitur dasar dari satu citra + berat telur (gram)."""
    ellipse = cv2.fitEllipse(contour)
    (xc, yc), (w_px, h_px), angle = ellipse

    long_px = max(w_px, h_px)
    short_px = min(w_px, h_px)

    height_cm = long_px * CM_PER_PIXEL_MAJOR
    width_cm = short_px * CM_PER_PIXEL_MINOR
    shape_index = width_cm / height_cm if height_cm else 0

    # Ovality: seberapa jauh kontur asli menyimpang dari elips ideal
    theta = np.radians(angle)
    dx, dy = np.cos(theta), np.sin(theta)
    proj = [(pt[0] - xc) * dx + (pt[1] - yc) * dy for pt in contour[:, 0]]
    ae_px = max(np.abs(proj)) if len(proj) else 0
    ae_cm = ae_px * CM_PER_PIXEL_MAJOR
    ovality = (height_cm - ae_cm) / height_cm if height_cm else 0

    # Eccentricity elips (a = sumbu panjang/2, b = sumbu pendek/2)
    a = long_px / 2
    b = short_px / 2
    eccentricity = np.sqrt(1 - (b * b) / (a * a)) if a else 0

    # Pendekatan empiris luas permukaan & volume dari massa
    # (rumus dari Buku Capstone Design, sudah dikonfirmasi via kode asli di Raspberry Pi)
    surface_area = 4.835 * (weight_grams ** 0.662)
    volume = (surface_area / 4.951) ** (1 / 0.666)
    density = weight_grams / volume if volume else 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    glcm_contrast = extract_glcm_contrast(gray, egg_mask)

    return {
        "weight_grams": round(weight_grams, 2),
        "height_cm": round(height_cm, 4),
        "width_cm": round(width_cm, 4),
        "shape_index": round(shape_index, 4),
        "ovality": round(ovality, 4),
        "eccentricity": round(eccentricity, 4),
        "surface_area": round(surface_area, 4),
        "volume": round(volume, 4),
        "density": round(density, 6),
        "glcm_contrast": round(glcm_contrast, 6),
    }


def extract_all_features(image_path: str, weight_grams: float) -> dict:
    """Ekstraksi lengkap dari path citra + berat -> dict 10 fitur dasar."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Gagal membaca citra: {image_path}")

    contour, mask = segment_egg(img)
    if contour is None:
        raise ValueError("Tidak ada objek telur terdeteksi pada citra.")

    return compute_features(img, contour, weight_grams, mask)
