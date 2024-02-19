import _thread
import utime
from machine import Pin, PWM


class SetupPWM:
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
        self.__last_calculation_time = 0
        self.__output = 0
        self.__derivative = 0

        # Threading
        self.__thread = None
        self.__isrunning = False

        # Hardware
        self.__outputPin = outputPin
        self.__PWM = PWM(Pin(self.__outputPin))
        self.__freq = XY  # wie finde ich die frequenz raus?

        # Ranges --> anpassen
        self.__inputRange = [XY, XY] # werden experimentell bestimmt?
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

    def setTarget(self, target: float) -> bool:                 #   macht es hier eigentlich Sinn die OutOfState Kondiition zu checken? Wenn sie nicht ist, ist output von der Heizung bloß gleich 0 
        """
            Sets the target value and returns out of range state 
        """
        
    def run(self) -> None:
        self.__getactual()
        self.__controller()
        self.__setPWM()
               

# Private Functions
    def __getactual(self) -> float:
        """
            Get current Temperature from defined source, calling global temperature from sensor in i2c class
        """
        #   self.__actual = getActualValue()
    
    def __controller(self) -> None:
        """
            Controller Logic, initializes/resets PID values and calculates the output. Function calls __setPWM()
        """

        #   Im Funktionsaufruf alles Resetten
        self.stop()
        self.start()

        while self.__isrunning:
            self.__getactual()
            self.__error = self.__target - self.__actual
            self.__sumerror += self.__error

            #   läuft das irgendwann über? überprüf das noch
            self.__derivative = (self.__error - self.__lasterror)/(utime.time() - self.__last_calculation_time)     #hier derivative mit utime definiert
            
            self.__output = self.__Kp * self.__error + self.__Ki * self.__sumerror + self.__Kd * self.__derivative
            
            # anti windup fehlt noch

            self.__last_calculation_time = utime.time()


            self.__lasterror = self.__error
            self.__setPWM() # ich würde mit übergabe wert arbeiten, set und get trennen

            # pausiere hier das Skript damit du eine definierte Freuqenz für den Regler hast, sleep function suchen
            pass

        if self.__actual == self.__target:
            #   turn LED on calling the setup function of making LED on --> aus nem beispiel?
            return True
        else:
            return False

    def __initPWM(self) -> None:
        """
            Initializes the PWM with the given Pin, frequency and sets the output to 0 
        """
        
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
        # Check Output in Range für Antiwindup?

        if self.__value not in range(self.__outputRange):
            return False
        
        self.__duty_cycle =  (self.__output - min_output) / (max_output - min_output)
        self.__PWM.duty_u16(int(65535 * self.__duty_cycle))

        return self.__duty_cycle