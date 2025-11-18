from machine import Pin, ADC
from time import sleep

# DEL sur GP16
led = Pin(16, Pin.OUT)

# LDR sur GP26 (ADC0)
ldr = ADC(26)

# Seuil (à ajuster selon mesures)
# Ici on prend un seuil ~1.5 V, à adapter
SEUIL_V = 2.4   # tension en volts

while True:
    raw = ldr.read_u16()
    voltage = raw * 3.3 / 65535
    
    print("Raw :", raw, "| Tension :", voltage, "V")
    
    if voltage > SEUIL_V:
        # sombre -> allumer la LED
        led.value(1)
    else:
        # clair -> éteindre la LED
        led.value(0)
    
    sleep(0.1)
