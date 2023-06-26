
import pathlib as pl
from time import sleep

import cv2
import VL53L0X

from ultralytics import YOLO

import gpiozero as gpio

from there_goes_mangoes.util.draw_crosshair import crosshair_norm

WND_NAME = "Camera View"
PARAM_MODEL = pl.Path(__file__).parents[1].joinpath("model/torch.pt")

XSHUT = gpio.OutputDevice(4)
MOTOR = gpio.OutputDevice(20)
VALVE = gpio.OutputDevice(21)
XSHUT.on()
MOTOR.on()
VALVE.on()

cv2.namedWindow(WND_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WND_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

model = YOLO(PARAM_MODEL)

tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
tof.open()
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000

results = model.predict(0, stream=True)

XSHUT.off()

for result in results:
    image = result.orig_img
    
    dist = tof.get_distance() / 10
    dist -= 4
    
    image = crosshair_norm(image, 0.1, 0.1, 0.05)
    image = cv2.putText(image, f"{dist:.2f}cm", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
    
    cv2.imshow(WND_NAME, image)
    
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(timing / 1000000)
    
cv2.destroyAllWindows()
