import gpiozero as gpio

from time import sleep

factory = gpio.pins.pigpio.PiGPIOFactory()
    
SENSOR = gpio.Button(21, pin_factory=factory)

while True:
    print(f"IR: {SENSOR.value}")
    sleep(0.125)


