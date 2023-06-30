import pathlib as pl
from time import sleep

import cv2
import numpy as np
import VL53L0X

from ultralytics import YOLO

import gpiozero as gpio

from there_goes_mangoes.util.draw_crosshair import crosshair_norm

WND_NAME = "Camera View"
PARAM_MODEL = pl.Path(__file__).parents[1].joinpath("model/torch.pt")

XSHUT = gpio.OutputDevice(4)
MOTOR = gpio.OutputDevice(20, active_high=False)
VALVE = gpio.OutputDevice(21, active_high=False)
XSHUT.off()
MOTOR.off()
VALVE.off()

cv2.namedWindow(WND_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WND_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

model = YOLO(PARAM_MODEL)

tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)

XSHUT.on()

tof.open()

tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
    
cam = cv2.VideoCapture(0)
    
while True:
    if not cam.isOpened():
        cam = cv2.VideoCapture(0)
        sleep(0.01)
    
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(timing / 1000000)

