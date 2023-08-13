import pathlib as pl
from time import sleep, time_ns

import cv2
import numpy as np
import VL53L0X

from ultralytics import YOLO

import gpiozero as gpio

from there_goes_mangoes.util.draw_crosshair import crosshair_norm

WND_NAME = "Camera View"
PARAM_MODEL = pl.Path(__file__).parents[1].joinpath("model/torch.pt")
# PARAM_MODEL = pl.Path(r"model/_train/small-256/weights/best.pt")

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
    
LOCK = False
      
    if not LOCK: 
        if not cam.isOpened():
            cam = cv2.VideoCapture(0)
            sleep(0.01)
        else:
            LOCK = True
        
    while True:
        _, image = cam.read()
        cap = time_ns()
        
        results = model.predict(
            cv2.resize(image, dsize=(256, 192), interpolation=cv2.INTER_AREA), 
            stream=False, 
            conf=0.6, 
            imgsz=(256, 192)
        )
        
        delay = time_ns() - cap
        
        dist = (tof.get_distance() / 10) - 2
            
        image = cv2.putText(image, f"{dist:.2f}cm", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
        image = cv2.putText(image, f"{(delay / 1000000000):.2f}s @ {(1 / (delay / 1000000000)):.2f} FPS", (5, image.shape[0] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2)
            
        nh, nw, _ = image.shape
        
        TARGET = False
        
        for result in results:
    
            color = (255, 0, 0)
            
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
                    
                    area = (ex - bx) * (ey - by)
                    if area >= (nh * nw * 0.90):
                        continue
                    
                    image = cv2.rectangle(image, (bx, by), (ex, ey), (0, 0, 127), thickness=2)
                    
                    ax, ay = np.power((np.array((0.5, 0.5)) - np.array((cx, cy))), 2)
                    rdist = np.abs(np.sqrt([ax + ay]))[0]
                    
                    if rdist < brdist:
                        brdist = rdist
                        fbx = bx
                        fby = by
                        fex = ex
                        fey = ey
                        
                if brdist <= 0.15:
                    color = (0, 255, 0)
                    
                    if 30 <= dist <= 35:
                        TARGET = True                
                    
                image = cv2.rectangle(image, (fbx, fby), (fex, fey), color=color, thickness=5)
                
        if TARGET:
            image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
        else:
            image = crosshair_norm(image, 0.1, 0.1, 0.05)
            
        cv2.imshow(WND_NAME, image)
        
        if TARGET:
            tof.stop_ranging()
            XSHUT.off()
            
            tspray = ((dist - 30) / 5)
            VALVE.on()
            sleep(1)
            
            _, image = cam.read()
            
            image = cv2.putText(image, f"PROCESSING", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
            image = cv2.rectangle(image, (fbx, fby), (fex, fey), color=color, thickness=5)
            image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
            MOTOR.on()
            
            cv2.imshow(WND_NAME, image)
            sleep(1.25)
        
            #for ii in range(int(tspray * 10)):
            #    _, image = cam.read()
            #    image = cv2.putText(image, f"SPRAYING", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
            #    image = cv2.rectangle(image, (fbx, fby), (fex, fey), color=color, thickness=5)
            #    image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
            #    
            #    cv2.imshow(WND_NAME, image)
            #    sleep(0.01)
            sleep(1 * tspray)

            MOTOR.off()
            VALVE.off()
            for ii in range(25):
                _, image = cam.read()
                
                image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
                image = cv2.putText(image, f"DOWNTIME: {(25 - ii) / 10}s", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
                
                cv2.imshow(WND_NAME, image)
                
                k = cv2.waitKey(1)
                if k != -1:
                    break
                else:
                    sleep(0.03) # sleep for 1 frame time
            
            tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)

            XSHUT.on()

            tof.open()

            tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
            
        k = cv2.waitKey(1)
        if k != -1:
            break
        else:
            sleep(timing / 1000000)
        
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(timing / 1000000)

