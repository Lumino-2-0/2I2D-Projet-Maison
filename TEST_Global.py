from machine import Pin, ADC
from time import sleep
import math

# =========================================
#               CONFIGURATION
# =========================================

# --- PIR (mouvement) ---
pir = Pin(20, Pin.IN, Pin.PULL_DOWN)
led_mvt = Pin(18, Pin.OUT)

# --- LDR (luminosité) ---
ldr = ADC(26)  # ADC0
R_FIXED_LDR = 10000  # 10kΩ (à adapter si besoin)

# --- Thermistor (temperature) ---
adc_temp = ADC(27)  # ADC1
VCC = 3.3
B = 4275.0
R_NOMINAL = 100000.0
R_SERIES = 100000.0  # résistance du module
DISCONNECT_THRESHOLD = 15000

# =========================================#
#                 MÉTHODES                 #
# =========================================#

# --- LECTURE DU PIR ---
def detecter_mouvement():
    val = pir.value()
    if val == 1:
        led_mvt.value(1)
        print("[PIR] Mouvement detecte")
    else:
        led_mvt.value(0)
        print("[PIR] Aucun mouvement")
    return val


# --- LECTURE LUMINOSITÉ ---
def lire_luminosite():
    raw = ldr.read_u16()
    v = raw * 3.3 / 65535

    # Conversion tension vers résistance LDR
    # Formule pont diviseur : Rldr = Rfixed * (3.3/V - 1)
    if v <= 0.01:
        return raw, v, None, 0  # évite division par zéro

    R_ldr = R_FIXED_LDR * (3.3 / v - 1)

    # Conversion résist vers lux (approximation)
    # Formule empirique typique : lux = A * R^(-alpha)
    # Paramètres moyens pour LDR CdS
    A = 50000
    alpha = 1.4
    lux = A * (R_ldr ** (-alpha))
    
    # Seuil (à ajuster selon mesures)
    # Ici on prend un seuil ~1.5 V, à adapter
    SEUIL_V = 2.5   # tension en volts

    raw = ldr.read_u16()
    voltage = raw * 3.3 / 65535
    
    print("Raw :", raw, "| Tension :", voltage, "V")
    
    if voltage > SEUIL_V:
        # sombre -> allumer la LED
        led_mvt.value(1)
    else:
        # clair -> éteindre la LED
        led_mvt.value(0)
    
    print(f"[LUMINOSITE] raw={raw}  | tension={v:.3f} V  | R_LDR={R_ldr:.0f} Ω  | ~{lux:.1f} lux")

    return raw, v, R_ldr, lux


# --- LECTURE TEMPÉRATURE ---
def lire_temperature():
    raw = adc_temp.read_u16()
    if raw < DISCONNECT_THRESHOLD:
        print("[TEMP] Capteur debranche ? ADC =", raw)
        return None

    # calcul tension
    v_out = raw / 65535 * VCC
    if v_out <= 0:
        return None

    # résistance NTC
    R_th = R_SERIES * (VCC / v_out - 1)

    try:
        tempK = 1.0 / (math.log(R_th / R_NOMINAL) / B + 1.0 / (25 + 273.15))
        tempC = tempK - 273.15
    except:
        return None

    print(f"[TEMP] raw={raw} | {tempC:.2f} deg_C | Rth={R_th:.0f} Ω")
    return tempC


# --- GESTION CHAUFFAGE OU CLIM ---
def chauffage_clim(temp):
    if temp < 19:
        print("[ACTION] Chauffage ON (temp basse)")
    elif temp > 28:
        print("[ACTION] Climatisation ON (temp haute)")
    else:
        print("[ACTION] Confort OK (aucune action)")


# =========================================#
#              BOUCLE PRINCIPALE           #
# =========================================#

print("=== SYS multi capteur started ! ===")

while True:
    print("\n-------------------------------------")

    # PIR
    detecter_mouvement()

    # Luminosité
    lire_luminosite()

    # Température
    temp = lire_temperature()
    if temp is not None:
        chauffage_clim(temp)
    else:
        print("Température indisponible")

    sleep(1)

