from machine import ADC, Pin
from time import sleep
 
# --- CONFIGURATION CAPTEURS ---
ldr = ADC(27)             # Photorésistance sur GP27
pir = Pin(16, Pin.IN)     # Capteur PIR sur GP16
led = Pin(15, Pin.OUT)    # LED témoin sur GP15
 
# --- PARAMÈTRES ---
SEUIL_LUMIERE = 20000      # seuil pour considérer qu'il fait sombre (0 = sombre, 65535 = très clair)
DELAI_BOUCLE_S = 0.2       # délai entre lectures
 
ancienne_lumiere = ldr.read_u16()  # valeur initiale pour suivi des variations
 
while True:
    # --- LECTURE LUMINOSITÉ ---
    valeur_lumiere = ldr.read_u16()
   
    # Détecter variations
    if valeur_lumiere > ancienne_lumiere + 1000:
        print("[+] Lumière augmente :", valeur_lumiere)
    elif valeur_lumiere < ancienne_lumiere - 1000:
        print("[-] Lumière diminue :", valeur_lumiere)
   
    ancienne_lumiere = valeur_lumiere
 
    # --- LECTURE MOUVEMENT PIR ---
    mouvement = pir.value() == 1
 
    # --- DÉCISION : allumer LED si mouvement + sombre ---
    if mouvement and valeur_lumiere < SEUIL_LUMIERE:
        led.value(1)
        print("[~] Mouvement détecté et il fait sombre -> LED ON")
    else:
        led.value(0)
 
    sleep(DELAI_BOUCLE_S)
