import RPi.GPIO as GPIO
import time

BUTTON_PIN = 19  # pakai GPIO 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# PUD_UP = tombol aktif saat ditekan (LOW)

print("Tes tombol dimulai...")
print("Tekan tombol untuk melihat output.\n")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Tombol DITEKAN!")
            time.sleep(0.2)  # debounce/simple delay
        else:
            print("Tombol dilepas")
            time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nProgram dihentikan.")
