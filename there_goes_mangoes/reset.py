import gpiozero as gpio
import os
from time import sleep

MOTOR = gpio.OutputDevice(20, active_high=False)
VALVE = gpio.OutputDevice(16, active_high=False)

button = gpio.Button(6, pull_up=False)
button.hold_time = 1

button.when_pressed = lambda: MOTOR.on(); VALVE.on()
button.when_released = lambda: MOTOR.off(); VALVE.off()

while True:
    sleep(0.01)