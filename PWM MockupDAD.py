import _thread
import utime
from machine import Pin, PWM


class SetupPWM: # oder einfach Controller, dann weiß man um was es geht
    """
        Controller Class for PID Control
    """

    def __init__(self, outputPin: int) -> None:
        # Set PID Parameters
        self.__Kp = 0.0
        self.__Ki = 0.0
        self.__Kd = 0.0
        self.__target = 0
        self.__actual = 0
        self.__error = 0
        self.__lasterror = 0
        self.__sumerror = 0
        self.__last_calculation_time = utime.time() #einheitliche variablen benennung -> __lastCalculationTime oder den rest ändern. Würde es auf 0 setzen und dann in der start funktion auf den wert ziehen
        self.__output = 0

        # Threading
        self.__thread = None
        self.__isrunning = False

        # was ist dt? 
        # Hardware
        self.__outputPin = outputPin
        self.__freq = XY  # anpassen # hier fehlt noch was

        # Ranges --> anpassen
        self.__inputRange = [XY, XY] # hier auch
        self.__outputRange = [XY, XY]


    def __repr__(self) -> str:
        return f"Regler Status: {self.__isrunning}"

#  Public Functions
    def start(self) -> None:
        """
            Starts the controller and initializes PWM. Creates a new thread for the controller logic.
        """
        if not self.__isrunning:
            self.__initPWM()
            self.__isrunning = True
            self.__thread = _thread.start_new_thread(self.__controller, ())

    def stop(self) -> None:
        """
            Stops the controller and resets PWM. Closes the thread for the controller logic.
        """
        if self.__isrunning:
            self.__isrunning = False
            self.__deinitPWM()
            self.__thread = None

    def setTarget(self, target: float) -> bool:
        """
            Sets the target value and returns out of range state 
        """
        # die funktion der klasse von Display und Taster ruft diese an wenn die bedienfläche benutzt wird
        # self.__target = readdisplay(display.address) 

        # huch, wozu brauchst du einen PID Regler für das Display??
        # Diese Klasse soll nur den PID Regler abbilden, in unserem Fall für die Heizung
        # Du rufst von außen die Funktion setTarget auf und übergibst den gewünschten Temperaturwert
        # Der Regler macht dann den Rest.
        # Hier in der Funktion überprüfst du nur ob der Wert im gültigen Bereich liegt und setzt ihn dann
        # Der Rückgabewert gibt an ob der Wertebereich gepasst hat (input_range)
        # Wenn nicht kannst du dir überlegen ob du nur False zurückgibst oder ob du den max/min Wert dann auch setzt
    
    

        # ?? 
        # ahh jetzt check ichs glaub. willst du den wert vom display lesen ? 
        # du hast im hauptprogramm den richtigen wert ja schon, übergib einfach den und check  hier nich die limits und entscheide was passieren soll wenn die überschritten werden
        if self.__actual == self.__target:
            # turn LED on calling the setup function of making LED on --> aus nem beispiel?
            return True
        else:
            return False
        
    def getTarget():
    
    def setParameters(self, ) -> None:
        """
            Sets the PID Parameters
        """
        # hier Ki Kp und Kd setzen, entweder alle auf einmal oder einzeln, dann überlegen ob das direkt aktualiseren wird oder der Regler neu gestartet werden muss

        pass

# Private Functions
    def __getactual(self) -> float:
        """
            Get current Temperature from defined source, calling global temperature from sensor in i2c class
        """
        # self.__actual = Sensor1.readTemperature(address) # read from i2c address of sensor

        # und wo ist Sensor1 definiert??
        # je nachdem wie du es aufbaust musst du hier auch noch checken ob der Wert plausibel ist
    
    def __controller(self) -> None:
        """
            Controller Logic, initializes/resets PID values and calculates the output. Function calls __setPWM()
        """
        # hier einmalig beim Funktionsauruf alles resetten/vorbelgen

        while self.__isrunning:
            self.__actual = self.__getactual()
            self.__error = self.__target - self.__actual
            self.__sumerror += self.__error

            # idee gut aber die Zeitdifferenz ist jetzt negativ da utime.time() >= self.__last_calculation_time -> läuft das irgendwann über? überprüf das noch
            self.__derivative = (self.__error - self.__lasterror)/(self.__last_calculation_time - utime.time())     #hier derivative mit utime definiert
            
            # du verwendest hier lokale variablen Kp, Ki und Kd, die du nicht definiert hast, das geht so nicht gut
            # und es fehlt ein punkt zwischen self und __output
            # __derivative ist nicht in der init
            self.__output = Kp * self.__error + Ki * self.__sumerror + Kd * self.__derivative
            
            # anti windup fehlt noch

            self.__last_calculation_time = utime.time()


            self.__lasterror = self.__error
            self.__setPWM() # ich würde mit übergabe wert arbeiten, set und get trennen

            # pausiere hier das Skript damit du eine definierte Freuqenz für den Regler hast, sleep function suchen
            pass

    def __initPWM(self) -> None:
        """
            Initializes the PWM with the given Pin, frequency and sets the output to 0 
        """
        self.__PWM = PWM(Pin(self.__outputPin))
        self.__PWM.freq(self.__freq)  
        self.__PWM.duty_u16(0) # passt, aber stichwort failsafe: je nachdem wie ihr die heizung (transitor) ansteuert bedeutet 0 vollgas
        pass

    def __deinitPWM(self) -> None:
        """
            Disables the PWM and sets the output to 0
        """
        self.__PWM.deinit()
        self.__PWM.duty_u16(0)
        pass

    def __setPWM(self) -> bool:
        """
            Handles the PWM output and limits the value to the given range, converts type, returns out of range state
        """
        # Check Output in Range

        # value ist nicht definiert. Willst du __setPWM(self, value) oder __setPWM(self) verwenden?
        # du kannst es einfacher machen: if value not in self.__outputRange: return False
        # ah und was soll value sein? der output?
        # bedenke dass du beim übersteuern dann immer den aktuellen wert beibehäst, failsafae mäßig doof wenn du eigentlich abschalten willst

        if self.__value not in range(self.__outputRange[0], self.__outputRange[1] + 1):
            return False
        
        # Grenzwerte von Output bekommen, von 0 bis 1 skalieren und das duty cycle eingeben^

        #die nächste Zeile weglassen und NIE in methoden neue variablen auf der klasse definieren. du hast es außerdem schon in der range
        self.__min_output, self.__max_output = self.__outputRange

        # ja kann man auch so machen. hab jetzt nicht geschaut ob es mit dem rest überienstimmt aber sehen wir ja dann
        self.__duty_cycle =  (self.__output - min_output) / (max_output - min_output)
        self.__PWM.duty_u16(int(65535 * self.__duty_cycle))


        return self.__duty_cycle

"""
    Zukünftige Implementationen:
        Ist-Größe bekommen von i2c sensor 
        i2c bedienfläche in Klasse implementieren #ok? aber nicht hier!?
        Setter für die Temperatur (über Knopf?)  # hier schreibst du nur die methode die dein Knopf nacher aufruft. "Verkabeln" tust du es woanders
        Setter für PID Parameter (über Knopf?)
        # Überwachung fehlt auch noch
"""

# Zu deinen Fragen


# 1.	Bei der getactual Funktion muss ich die andere read Funktion von der I2C Klasse aufrufen, da machebin ich unsicher ob es man im Rahmen von OOP gut gesehen ist. Meine Idee ist die Addresse vom individuellen Sensor in der Funktion einfach angeben und ablesen
# 2.	 Setterfunktion möchte ich noch ausbauen, die neue Idee um es praktischer zu machen ist mit einem + und - Knopf zu arbeiten und einen "Auswahl" Taster tauscht zwischen alle Stellvariablen
# 3.	In der I2C Klasse habe ich effektiv keinen Threat angewiesen da die read Funktion schon in einem anderem Threat aufgerufen 



# 1. 
# du köntest dem Konstruktor noch actualValueFunction übergeben. dafür übergibst du dann von deinem Hauptprogramm die Funktion die dort die Temperatur ermittelt.
# in der Regler klasse weist du self.__ActualValueFunction = actualValueFunction zu und in der getActual Methode rufst du dann self.__ActualValueFunction() auf, überprüfst den Wert und gibst ihn zurück
# wie immer aber nur ein Vorschlag, so hätte ichs probiert

# 2. 
# ja ist ein konzept, bedenke dass die Methoden hier aber nur werte übergeben bekommen.
# Die Taster/ Bedien Logik kommt nachher in ne eigene Klasse. Da ihr euch jetzt dafür entschieden habt könnt ihr euch direkt mal in das Thema Bounce/ Debounce bzw. Entprellen einlesen. 
# schaut mal ob ihr bis zum termin paar infos dazu findet, dann können wir das mal besprechen.

# ok da es bereits morgen ist erspare ich euch die Suche: https://www.mikrocontroller.net/articles/Entprellung einfach mal ins thema einlesen


# 3. 
# so wie es jetzt geschrieben ist instanziierst du den Sensor ja nicht in dieser Klasse. Dann kommt es auf euer Konzept und den zeitlichen ablauf an. Wie oft braucht ihr neue Werte und wie stellt ihr sicher dass die abgefragt werden?
# Bedenkt auch: Der Regler hat ne andere Frequenz als die Berechnung. aber reden wir morgen drüber

