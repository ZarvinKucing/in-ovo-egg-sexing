import RPi.GPIO as GPIO
import time

LED = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED, GPIO.OUT)

try:
    while True:
        GPIO.output(LED, GPIO.HIGH)
        print("ON")
        time.sleep(2)

        GPIO.output(LED, GPIO.LOW)
        print("OFF")
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.output(LED, GPIO.LOW)
    GPIO.cleanup()
