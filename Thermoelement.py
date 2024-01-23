from max31856 import MAX31856
from machine import Pin
import time

sck = Pin(2, Pin.OUT)
cs = Pin(3, Pin.OUT)
so = Pin(4, Pin.IN)

sensor = MAX31856(sck, cs , so)

while True:
    print("temperature=")
    print(sensor.read())
    time.sleep(1)