
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
MOTOR = gpio.OutputDevice(16)
VALVE = gpio.OutputDevice(21)
XSHUT.on()
MOTOR.off()
VALVE.off()

cv2.namedWindow(WND_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WND_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

model = YOLO(PARAM_MODEL)

tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
tof.open()
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000

#results = model.predict(r"/home/theregoesmangoes/system/ThereGoesMangoes/data/sets/xen/mango_7_carabao_C1.png", stream=True, conf=0.6)
results = model.predict(0, stream=True, conf=0.6, vid_stride=5)

for result in results:
    image = result.orig_img
    
    image = crosshair_norm(image, 0.1, 0.1, 0.05)
    
    nh, nw, _ = image.shape
    
    if len(result.boxes) > 0:
        brdist = 1
        color = (255, 0, 0)
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
            
            ax, ay = np.power((np.array((0.5, 0.5)) - np.array((cx, cy))), 2)
            rdist = np.sqrt([ax + ay])[0]
            
            if rdist < brdist:
                brdist = rdist
                fbx = bx
                fby = by
                fex = ex
                fey = ey
               
        dist = tof.get_distance() / 10
            
        image = cv2.putText(image, f"{dist:.2f}cm", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
                
        if rdist >= 0.15:
            color = (0, 255, 0)
            
        image = cv2.rectangle(image, (fbx, fby), (fex, fey), color=color, thickness=5)
        
    
    cv2.imshow(WND_NAME, image)
    
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(timing / 1000000)
    
cv2.destroyAllWindows()
XSHUT.off()
