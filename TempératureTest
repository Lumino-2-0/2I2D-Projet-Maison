from machine import ADC
from time import sleep
import math
 
# --- Configuration ADC ---
adc = ADC(26)  # A0 -> GP26 (vérifie que ton capteur est bien sur A0)
 
# --- Constantes (typique pour Grove Temp Sensor v1.2) ---
VCC = 3.3
B = 4275.0            # B-constant (typique)
R_NOMINAL = 100000.0  # R0 = 100k (thermistor nominal)
R_SERIES = 100000.0   # résistance fixe du module (100 kΩ sur la plupart des versions)
DISCONNECT_THRESHOLD = 15000  # si ADC < ce seuil, on considère la broche "débranchée" (à ajuster)
 
def lire_temperature():
    raw = adc.read_u16()  # 0..65535
    # debug / sécurité : si la lecture est très basse -> broche flottante / débranchée
    if raw < DISCONNECT_THRESHOLD:
        return None, raw, None
 
    # calculer la tension mesurée
    v_out = (raw / 65535.0) * VCC
    # éviter division par zéro
    if v_out <= 0:
        return None, raw, None
 
    # calculer R_th selon le montage diviseur : thermistor entre VCC et point milieu,
    # R_series entre point milieu et GND -> R_th = R_series * (VCC / Vout - 1)
    R_th = R_SERIES * (VCC / v_out - 1.0)
 
    # conversion avec paramètre B : 1/T = 1/T0 + (1/B) * ln(R/R0)
    try:
        tempK = 1.0 / (math.log(R_th / R_NOMINAL) / B + 1.0 / (25.0 + 273.15))
        tempC = tempK - 273.15
    except ValueError:
        return None, raw, R_th
 
    return tempC, raw, R_th
 
 
def allumer_Chauffage(temp) :
    print("Simulation du chauffage qui s'allume...")
    while(temp>19):
        print("température à ", temp)
    print("Extinction clim !")
 
def refroidir_Piece(temp):
    print("Simulation du clim qui s'allume...")
    while(temp<23):
        print("température à ", temp)
    print("Extinction clim !")
 
# --- Boucle principale ---
try:
    while True:
        temp, raw, Rth = lire_temperature()
        if temp is None:
            print("Lecture invalide / capteur debranche ? ADC:", raw, " Rth:", Rth)
        else:
            if temp < 19 :
                allumer_Chauffage(temp)
            elif temp > 28:
                refroidir_Piece(temp)
 
            print("Temperature: ", temp, "Degre Celsius")
        sleep(2)
 
except KeyboardInterrupt:
    print("Arret du programme")
 
