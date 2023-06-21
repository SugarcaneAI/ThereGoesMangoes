
import pathlib as pl
from time import sleep

import cv2
import VL53L0X

from ultralytics import YOLO

from there_goes_mangoes.util.draw_crosshair import crosshair_norm

PARAM_MODEL = pl.Path(r"E:\Git\ThereGoesMangoes\model\nano-640\weights\best.pt")

cam = cv2.VideoCapture(0)

while not cam.isOpened():
    cam = cv2.VideoCapture(0)
    sleep(0.01)

tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
tof.open()
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000

cv2.namedWindow("Camera View: Ultrasonic", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera View: Ultrasonic", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

results = YOLO()

while True:
    ret, image = cam.read()
    
    dist = tof.get_distance() / 10
    dist -= 4
    
    image = crosshair_norm(image, 0.1, 0.1, 0.05)
    image = cv2.putText(image, f"{dist:.2f}cm", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
    
    cv2.imshow("Camera View: Ultrasonic", image)
    
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(timing / 1000000)
    
cam.release()
cv2.destroyAllWindows()
