import gpiozero as gpio

from time import sleep

factory = gpio.pins.pigpio.PiGPIOFactory()
    
SENSOR = gpio.Button(7, pull_up=True, pin_factory=factory)

while True:
    print(f"IR: {SENSOR.is_pressed}", end="\r")
    sleep(0.125)
 