"""
Kontrol LED Candling via MOSFET PWM Trigger Switch MTR-0037.
Referensi: Buku Capstone Design, Bab 4.2.1 (Software Raspberry Pi - Kontrol LED Candling).
"""

import RPi.GPIO as GPIO
from config import SENTER

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENTER, GPIO.OUT)
GPIO.output(SENTER, GPIO.LOW)


def senter_on():
    GPIO.output(SENTER, GPIO.HIGH)
    print("[SENTER] ON")


def senter_off():
    GPIO.output(SENTER, GPIO.LOW)
    print("[SENTER] OFF")
