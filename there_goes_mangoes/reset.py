import gpiozero as gpio
import os
from time import sleep

MOTOR = gpio.OutputDevice(20, active_high=False)
VALVE = gpio.OutputDevice(21, active_high=False)

button = gpio.Button(6, pull_up=False)
button.hold_time = 1

button.when_released = lambda: MOTOR.on(); VALVE.on()

while True:
    MOTOR.off()
    VALVE.on()
    sleep(0.01)