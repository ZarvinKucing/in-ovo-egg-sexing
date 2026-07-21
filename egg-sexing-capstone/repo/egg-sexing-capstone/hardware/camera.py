"""
Akuisisi citra telur via Kamera Raspberry Pi (CSI).
Referensi: Buku Capstone Design, Bab 4.2.1 (Software Raspberry Pi - Pengambilan Citra).
"""

import subprocess
from config import RAW_IMAGE_PATH


def ambil_citra(output_path: str = RAW_IMAGE_PATH) -> str:
    subprocess.run(
        ["rpicam-still", "-o", output_path, "--nopreview"],
        check=True,
    )
    return output_path
