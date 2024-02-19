"""
Main Ablauf für das Blow-by Messgerät

"""

import utime
from Machine import Pin, PWM, I2C
from PWM_MockupDAD import SetupPWM
from Menu_Mockup import Menu

#   Energie an, Mikrokontroller auch an

#   create Heizungselement
heizungOutputPin = 12   #   Beispiel Pin
heizung = SetupPWM(heizungOutputPin)
heizung.start()

#   create i2c sensor objects
#   create i2c display object
#   create Analog output for Volumenstrom  object

while True:     #   soll hier eine Anfangskondition geprüft werden? Vielleicht das SollTemperatur erreicht ist
    
    #   Heizungregler läuft
    heizung.run()

    #   Volumenstromberechnung
    
    #   Menu Knopf Druck 

    pass