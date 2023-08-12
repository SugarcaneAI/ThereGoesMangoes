import gpiozero as gpio
import os
from time import sleep

factory = gpio.pins.pigpio.PiGPIOFactory()

MOTOR = gpio.OutputDevice(20, active_high=False, pin_factory=factory)
VALVE = gpio.OutputDevice (21, active_high=False, pin_factory=factory)

button = gpio.Button(6, pull_up=False)
button.hold_time = 1

button.when_pressed = lambda: MOTOR.on(); VALVE.on()
button.when_released = lambda: MOTOR.off(); VALVE.off()

while True:
    try:
        if button.is_pressed:
            MOTOR.on()
            VALVE.on()
        elif button.is_released:
            MOTOR.off()
            VALVE.off()
    except:
        os.system("sudo killall pigpiod")
        os.system("sudo pigpiod")
    sleep(0.01)