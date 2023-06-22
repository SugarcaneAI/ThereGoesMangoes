from time import sleep

import cv2
import gpiozero as gpio

from there_goes_mangoes.util.draw_crosshair import crosshair_norm

cam = cv2.VideoCapture(0)

while not cam.isOpened():
    cam = cv2.VideoCapture(0)
    sleep(0.01)
    
factory = gpio.pins.pigpio.PiGPIOFactory()
    
SENSOR = gpio.Button(7, pin_factory=factory)

cv2.namedWindow("Camera View: Proximity-IR", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera View: Proximity-IR", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

while True:
    
    color = (0, 0, 255)
    
    ret, image = cam.read()
    
    if SENSOR.is_pressed:
        color = (0, 255, 0)

    image = crosshair_norm(image, 0.1, 0.1, 0.05, color=color)
    image = cv2.putText(image, f"{SENSOR.is_pressed}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
    
    cv2.imshow("Camera View: Proximity-IR", image)
    
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(0.5)
        
cv2.destroyAllWindows()
    