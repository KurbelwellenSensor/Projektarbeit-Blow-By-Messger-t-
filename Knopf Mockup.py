from machine import Pin
import utime


class Knopf:
    """
    Controller Class for the Buttons an their functions in the Sensor
    """
    def __init__(self, Pin: int, name: str) -> None:
        self.__value = 0
        self.__pin = Pin(Pin, Pin.IN)
        self.__name = name    
        self.__letztenZeitmarker = 0
        self.__neuenZeitmarker = 0

        pass

# Private Functions    
    def __entprellung():
        """
        Software-Entprellungs Mechanismus. 
        Wenn Knopf betätigt wird, warten für 20ms und erst Knopfdruck ablesen.
        Basiert auf:    https://docs.micropython.org/en/latest/library/machine.Pin.html#machine.Pin
                        unter "pin.irq" Funktion
                        https://www.coderdojotc.org/micropython/advanced-labs/02-interrupt-handlers/#debounced-version-of-a-button-press-detection
        """
        self.__neuenZeitmarker = utime.ticks_ms()
            if (self.__neuenZeitmarker - self.__letztenZeitmarker) > 200: 
                self.__value +=0.1
                self.__letztenZeitmarker = self.__neuenZeitmarker
