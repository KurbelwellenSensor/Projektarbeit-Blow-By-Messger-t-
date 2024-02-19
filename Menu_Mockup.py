from machine import pin, I2C
import utime
from collections import OrderedDict
#   import I2C Display Class 

class Menu:
    """
    Bedienkonzept für das Menu des Messgerätes. Erstellt meherere Objekte für die Bedienung des Displays am Gerät

    Ablauf:
    1. Menu Knopf Interrupt Pin aktiviert einen Signal am Board (if Kondition oder Breakout Pin) [Wird im Main aufgerufen]
    2. Timeout Kondition wird initiert und während die Zeit nicht abgelaufen ist läuft die Schleife für +, - und Menu [Funktion gerufen]
    3. Jedes Knopfdruck setzt den Timeout Count zurück
    4. In der Schleife, werden if statements aufgerufen für jeden Knopf
        4.1. Einen Menu-Knopf Druck tauscht die angezeigte und bearbeitbare Variable
        4.2. + und - werden für die Einstellung benutzt
    5. Nach einer gegebene Zeit von 5 Sekunden ist der Timeout An und Main läuft weiter
    """
    def __init__(MenuKnopfPin: int, PlusKnopfPin: int, MinusKnopfPin: int) -> None:
        self.__MenuKnopfPin = MenuKnopfPin
        self.__PlusKnopfPin = PlusKnopfPin
        self.__MinusKnopfPin = MinusKnopfPin
        self.__timeoutCounter = 0 
        self.__variableIndex = 0
        self.__MenuKi = 0.1
        self.__MenuKp = 0.1
        self.__MenuKd = 0.1
        self.__MenusollTemperatur = 45
        self.__variables = OrderedDict([
                                    ('Ki', self.__MenuKi),
                                    ('Kp', self.__MenuKp),
                                    ('Kd', self.__MenuKd),
                                    ('Soll Temperatur', self.__MenusollTemperatur)
                                    ])                                              
        #   Hier möchte ich über einen n-Zähler im Kreislauf durch alle Variablen Tauschen
        #   Das Problem ist jetzt wie ich dann das entsprechende Wert einzeln an der PWM Klasse übergebe
        #   Kann man die alle auf einmal übergeben? 
        

    def Menu_Bedienung(self):
        """
        Controller Klasse für das Menu sobald die Menu Taste gedrückt wird
        """

        while self.__timeout < 5:               
            self.__timeoutCounter = utime.time() #    insert time marker
            self.__variableIndex = 0

            #   Display Element n in Dictionary

            #   if Menu_Breakout pressed                
                #   zeit_anfang = utime.time()
                #   Display Print n + 1
            #   if + pressed
                #   zeit_anfang = utime.time()
                #   Entry n in Dictionary =+ 0.1
            #   if - pressed
                #   Entry n in Dictionary =- 0.1
            self.__timeoutCounter = utime.time() - zeit_anfang
        
        pass

    def Running(self):
        """
        Standar ablauf für das Feedback vom Gerät
        """

        #   Display Blow-By Wert aus Rechner Klasse