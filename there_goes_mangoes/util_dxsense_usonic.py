import gpiozero as gpio
from time import sleep, time_ns
import itertools

factory = gpio.pins.pigpio.PiGPIOFactory()

while True:
    try:
        SENSOR = gpio.DistanceSensor(echo=21, trigger=20, pin_factory=factory, partial=True)
        break
    except:
        sleep(0.5)
    
begin = time_ns()
cur = time_ns()
for count in itertools.count():
    try:
        dist = SENSOR.distance * 100
    except:
        sleep(0.25)
        continue
    print(f"{count}: {dist:.2f}cm  @ {(time_ns() - cur) / 100000000:.2f}s ({(time_ns() - begin()) / 1000000000:.2f}s)")
    cur = time_ns()
    
