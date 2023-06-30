
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
#XSHUT.off()

timing = tof.get_timing()
if timing < 20000:
    timing = 20000

#results = model.predict(r"/home/theregoesmangoes/system/ThereGoesMangoes/data/sets/xen/mango_7_carabao_C1.png", stream=True, conf=0.6)
results = model.predict(0, stream=True, conf=0.6, vid_stride=5)

color = (255, 0, 0)

for result in results:
    image = result.orig_img
    
    dist = (tof.get_distance() / 10) - 2
            
    image = cv2.putText(image, f"{dist:.2f}cm", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
    
    nh, nw, _ = image.shape
    
    if len(result.boxes) > 0:
        brdist = 1
        
        fbx = 0
        fby = 0
        fex = 0
        fey = 0
        for box in result.boxes:
            if int(box.cls) == 1:
                continue
            
            cx, cy, ww, hh = box.cpu().xywhn[0].numpy()
            
            bx = int((cx - (ww / 2)) * nw)
            by = int((cy - (hh / 2)) * nh)
            ex = int((cx + (ww / 2)) * nw)
            ey = int((cy + (hh / 2)) * nh)
            
            image = cv2.rectangle(image, (bx, by), (ex, ey), (0, 0, 127), thickness=2)
            
            ax, ay = np.power((np.array((0.5, 0.5)) - np.array((cx, cy))), 2)
            rdist = np.abs(np.sqrt([ax + ay]))[0]
            
            if rdist < brdist:
                brdist = rdist
                fbx = bx
                fby = by
                fex = ex
                fey = ey
                
        if rdist <= 0.15:
            color = (0, 255, 0)
            
        image = cv2.rectangle(image, (fbx, fby), (fex, fey), color=color, thickness=5)
    
    if color == (0, 255, 0):
        image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
    else:
        image = crosshair_norm(image, 0.1, 0.1, 0.05)
    
    cv2.imshow(WND_NAME, image)
    
    if color == (0, 255, 0):
        MOTOR.on()
        sleep(0.05)
        VALVE.on()
        sleep(0.05)
        MOTOR.off()
        sleep(0.05)
        VALVE.off()
        
        for ii in range(50):            
            image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
            image = cv2.putText(image, f"DOWNTIME: {(50 - ii) / 10}s", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
            
            cv2.imshow(WND_NAME, image)
            
            sleep(0.01)
    
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(timing / 1000000)
    
cv2.destroyAllWindows()
