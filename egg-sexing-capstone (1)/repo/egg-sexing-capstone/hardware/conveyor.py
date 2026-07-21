"""
Kontrol Mini Conveyor via Motor Driver L298N.
Referensi: Buku Capstone Design, Bab 4.2.1 (Software Raspberry Pi - Kontrol Conveyor).
"""

import time
import RPi.GPIO as GPIO
from config import ENA, IN1, IN2, SPEED_CONVEYOR, JEDA_STOP

GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

pwm_motor = GPIO.PWM(ENA, 1000)  # 1kHz PWM
pwm_motor.start(0)


def conveyor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm_motor.ChangeDutyCycle(0)
    time.sleep(JEDA_STOP)


def conveyor_maju(durasi: float):
    pwm_motor.ChangeDutyCycle(SPEED_CONVEYOR)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(durasi)
    conveyor_stop()


# TODO: fungsi conveyor_mundur() belum ada di buku TA — tambahkan kalau
# alatmu butuh gerak mundur (misal untuk reset posisi tatakan telur).
