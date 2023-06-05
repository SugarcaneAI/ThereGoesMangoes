from time import sleep

import cv2
import gpiozero as gpio

from there_goes_mangoes.util.draw_crosshair import crosshair_norm

factory = gpio.pins.pigpio.PiGPIOFactory()

while True:
    try:
        SENSOR = gpio.DistanceSensor(echo=21, trigger=20, pin_factory=factory, partial=True)
        break
    except:
        sleep(0.5)
    

while True:
    try:
        dist = SENSOR.distance * 100
    except:
        sleep(0.25)
        continue
    
    sleep(0.25)
