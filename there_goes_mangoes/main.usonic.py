from time import sleep

import cv2
import gpiozero as gpio

from there_goes_mangoes.util.draw_crosshair import crosshair_norm

cam = cv2.VideoCapture(0)

while not cam.isOpened():
    cam = cv2.VideoCapture(0)
    sleep(0.01)

factory = gpio.pins.pigpio.PiGPIOFactory()

while True:
    try:
        SENSOR = gpio.DistanceSensor(echo=21, trigger=20, pin_factory=factory, partial=True)
        break
    except:
        sleep(0.01)

cv2.namedWindow("Camera View: Ultrasonic", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera View: Ultrasonic", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

while True:
    ret, image = cam.read()
    
    try:
        dist = SENSOR.distance * 100
    except:
        sleep(0.25)
        continue
    
    image = crosshair_norm(image, 0.1, 0.1, 0.05)
    image = cv2.putText(image, f"{dist:.2f}cm", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
    
    cv2.imshow("Camera View: Ultrasonic", image)
    
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(0.05)
    
cam.release()
cv2.destroyAllWindows()
