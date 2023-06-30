import gpiozero as gpio
import os
from time import sleep

button = gpio.Button(6, pull_up=False)
button.hold_time = 1

button.when_held = lambda: print("sudo poweroff")
button.when_released = lambda: print("sudo shutdown -r now")

while True:
    sleep(0.01)