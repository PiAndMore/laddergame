#!/usr/bin/python
# -*- coding: utf-8 -*-

# Ladder Game für den Raspberry Pi
#
# Erweiterungsvorschläge:
# - Mehr Zufall bei der Bestimmung der An-/Aus-Zeiten
# - Andere Funktion für die An-Aus-Zeiten verwenden 
# - Zwei-Spieler-Variante (mit zwei Eingabeknöpfen)

import smbus
import math
from time import sleep

# Der erste I2C-Bus am Raspberry Pi.
bus = smbus.SMBus(0)

# Setze die Pins 0.0 bis 0.7 auf Eingang 
bus.write_byte_data(0x20, 0x06, 0xff) # 0xff -> Bitmuster 0x11111111
# Setze die Pins 1.0 bis 1.7 auf Ausgang
bus.write_byte_data(0x20, 0x07, 0x00) # 0x00 -> Bitmuster 0x00000000
# Schalte alle Pins 1.* auf "Ein"
bus.write_byte_data(0x20, 0x01, 0xff)

def set_leds(value):
    # Eingabe ist ein Byte, welches das Bitmuster beschreibt
    bus.write_byte_data(0x20, 0x01, value)
    
def get_input(value):
    # Eingabe ist Nummer des Pins, z.B. 7 für Pin 0.7 
    return ((bus.read_byte_data(0x20, 0x08) & int(math.pow(2,value))) > 0)

sleep(0.5)
i = 0
while i < 8: # Das Spiel läuft bis 8 LEDs

    # n wird hochgezählt von 0 bis n_max
    # Die aktuelle LED (das ist die i.) leuchtet nur während n zwischen n_ein und n_aus ist
    n_max = 200
    n_ein = 100  # Vorschlag: n_ein = 100 + i*5  damit das Spiel zunehmend schneller wird
    n_aus = 200  # Vorschlag: n_aus = 200 - i*5  damit das Spiel zunehmend schneller wird
    n = 0
    sleep(0.1)
    while True:
        n += 1 
        # Soll die aktuelle LED eingeschaltet werden?
        aktiv = (n > n_ein and n < n_aus)
        
        # Schalte alle LEDs bis zur i. ein
        # Dazu berechne das Bitmuster mit (2^i)-1
        # Beispiel: 
        #  i = 1 (d.h., eine LED soll an sein)
        #  dann ist 2^1 = 2   -> Bitmuster 00000010
        #  und     2^1-1 = 1  -> Bitmuster 00000001
        #  
        #  i = 4 (d.h., 4 LEDs sollen an sein)
        #  dann ist 2^4 = 16  -> Bitmuster 00010000
        #  und     2^4-1 = 15 -> Bitmuster 00001111
        led_muster = int(math.pow(2, i)) - 1 
        
        # Außerdem noch eine weitere LED einschalten, wenn gewünscht.
        if aktiv:
            led_muster += int(math.pow(2,i))
            
        # Jetzt LEDs schalten
        set_leds(led_muster)
            
        # Schalter auslesen
        s = get_input(7)

        # Benutzer hat richtig gedrückt.        
        if s and aktiv:
            # Es geht mit der nächsten LED weiter
            i += 1
            # Dem Benutzer Zeit geben, den Finger wieder vom Schalter zu nehmen
            sleep(0.5)
            break

        # Benutzer hat nicht richtig gedrückt.
        if s and not aktiv:
            i = 0
            break
        
        if n > n_max:
            # n wird zurückgesetzt
            n = 0
        sleep(0.01)
        
# Benutzer hat gewonnen!
while True:
    for i in range(0, 7):
        set_leds(int(math.pow(2, i)))
        sleep(0.1)
    for i in range(7, 0, -1):
        set_leds(int(math.pow(2, i)))
        sleep(0.1)
