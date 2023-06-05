from time import sleep

import cv2
import gpiozero as gpio

from there_goes_mangoes.util.draw_crosshair import crosshair_norm

cam = cv2.VideoCapture(0)

while not cam.isOpened():
    cam = cv2.VideoCapture(0)
    sleep(0.01)
    
SENSOR = gpio.Button(21)

while True:
    
    color = (0, 0, 255)
    
    _, image = cam.read()
    
    if SENSOR.is_pressed():
        color = (0, 255, 0)
    
    cv2.namedWindow("Camera View: Ultrasonic", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Camera View: Ultrasonic", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

    image = crosshair_norm(image, 0.1, 0.1, 0.05, color=color)
    
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(0.5)
        
cv2.destroyAllWindows()
    