from machine import Pin
from time import sleep
 
# Capteur PIR sur GP16
pir = Pin(16, Pin.IN, Pin.PULL_DOWN)
 
# LED sur GP18
led = Pin(18, Pin.OUT)
 
while True:
    print(pir.value)
    if pir.value() == 1:      # Mouvement détecté
        led.value(1)          # Allume LED
        print("Mouvement ! LED ON")
    else:
        led.value(0)          # Éteint LED
        print("Aucun mouvement")
 
    sleep(0.1)
 
