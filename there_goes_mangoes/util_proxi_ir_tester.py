import gpiozero as gpio

from time import sleep

factory = gpio.pins.pigpio.PiGPIOFactory()
    
SENSOR = gpio.Button(21, pull_up=True, pin_factory=factory)

while True:
    print(f"IR: {SENSOR.is_pressed}")
    sleep(0.125)
