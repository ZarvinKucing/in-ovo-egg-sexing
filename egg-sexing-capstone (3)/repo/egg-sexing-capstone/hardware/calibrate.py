from hx711 import HX711
import time

DOUT = 5
SCK = 6

hx = HX711(DOUT, SCK)

try:
    print("Kosongkan timbangan...")
    time.sleep(1)
    hx.reset()  # ganti hx.zero() atau hx.tare()
    
    input("\n>>> Letakkan beban kalibrasi lalu tekan ENTER")

    raw_with_weight = hx.read_long()  # ganti hx.get_value()
    print("Raw dengan beban:", raw_with_weight)

    real_weight = float(input("Masukkan berat beban (gram): "))

    scale = raw_with_weight / real_weight
    print("Scale Factor =", scale)

    with open("scale_factor.txt", "w") as f:
        f.write(str(scale))

    print("Scale factor disimpan!")

except KeyboardInterrupt:
    print("Keluar dari program.")
