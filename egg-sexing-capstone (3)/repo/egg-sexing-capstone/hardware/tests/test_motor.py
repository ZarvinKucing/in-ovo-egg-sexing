import RPi.GPIO as GPIO
import time

ENA = 13   # PWM speed
IN1 = 20
IN2 = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

pwm = GPIO.PWM(ENA, 500)
pwm.start(50)  # speed 50%

try:
    # MAJU
    print("Motor MAJU...")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(0.65)

    # STOP
    print("Motor STOP...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(3)

    # MUNDUR
    print("Motor MUNDUR...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(0.6)

    # STOP
    print("Motor STOP...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

finally:
    pwm.stop()
    GPIO.cleanup()
