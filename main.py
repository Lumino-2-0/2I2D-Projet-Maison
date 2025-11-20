from machine import ADC, Pin
from time import sleep
import math

# --------------------------------------------------------
# CONFIG CAPTEUR LDR (luminosite)
# --------------------------------------------------------
ldr = ADC(26)  # Entrée analogique GP26

# --------------------------------------------------------
# CONFIG CAPTEUR PIR
# --------------------------------------------------------
pir = Pin(16, Pin.IN, Pin.PULL_DOWN)

# --------------------------------------------------------
# LED témoin
# --------------------------------------------------------
led = Pin(18, Pin.OUT)

# --------------------------------------------------------
# CONFIG CAPTEUR TEMPERATURE (Grove thermistor)
# --------------------------------------------------------
adc_temp = ADC(28)  # ATTENTION: changer la pin si ton capteur n'est pas sur GP27

VCC = 3.3
B = 4275.0
R_NOMINAL = 100000.0
R_SERIES = 100000.0
DISCONNECT_THRESHOLD = 15000

# --------------------------------------------------------
# PARAMETRES SYSTEME
# --------------------------------------------------------
DELAI_BOUCLE_S = 0.2
SEUIL_LUMIERE_V = 2.4

# --------------------------------------------------------
# FONCTION : lecture temperature
# --------------------------------------------------------
def lire_temperature():
    raw = adc_temp.read_u16()

    if raw < DISCONNECT_THRESHOLD:
        return None, raw, None

    v_out = (raw / 65535.0) * VCC
    if v_out <= 0:
        return None, raw, None

    R_th = R_SERIES * (VCC / v_out - 1.0)

    try:
        tempK = 1.0 / (math.log(R_th / R_NOMINAL) / B + 1.0 / (25.0 + 273.15))
        tempC = tempK - 273.15
    except ValueError:
        return None, raw, R_th

    return tempC, raw, R_th

# --------------------------------------------------------
# CHAUFFAGE
# --------------------------------------------------------
def allumer_chauffage():
    print("Chauffage ON")

def eteindre_chauffage():
    print("Chauffage OFF")

# --------------------------------------------------------
# CLIM
# --------------------------------------------------------
def allumer_clim():
    print("Clim ON")

def eteindre_clim():
    print("Clim OFF")

# --------------------------------------------------------
# BOUCLE PRINCIPALE
# --------------------------------------------------------
print("Demarrage du systeme unifie...")

while True:

    # ----------------------------------------------------
    # LECTURE LUMINOSITE
    # ----------------------------------------------------
    raw_lumiere = ldr.read_u16()
    voltage_lumiere = raw_lumiere * 3.3 / 65535

    print("LDR raw =", raw_lumiere, "| tension =", voltage_lumiere, "V")

    # ----------------------------------------------------
    # LECTURE PIR
    # ----------------------------------------------------
    mouvement = pir.value()
    print("PIR =", mouvement)

    # ----------------------------------------------------
    # DECISION LED
    # ----------------------------------------------------
    if mouvement == 1 and voltage_lumiere > SEUIL_LUMIERE_V:
        led.value(1)
        print("LED ON (mouvement + obscurite)")
    else:
        led.value(0)
        print("LED OFF")

    # ----------------------------------------------------
    # LECTURE TEMPERATURE
    # ----------------------------------------------------
    temp, rawT, Rth = lire_temperature()

    if temp is None:
        print("Temp invalide / capteur possiblement debranche. ADC =", rawT, " Rth =", Rth)
    else:
        print("Temperature =", temp, "degC")

        # ------------------------------------------------
        # LOGIQUE CHAUFFAGE / CLIM
        # ------------------------------------------------
        if temp < 19:
            allumer_chauffage()
            eteindre_clim()
        elif temp > 28:
            allumer_clim()
            eteindre_chauffage()
        else:
            # Zone confortable
            eteindre_chauffage()
            eteindre_clim()

    sleep(DELAI_BOUCLE_S)
