import pathlib as pl
from time import sleep, time_ns

import cv2
import numpy as np

from ultralytics import YOLO

import gpiozero as gpio

from there_goes_mangoes.util.draw_crosshair import crosshair_norm

WND_NAME = "Camera View"
PARAM_MODEL = pl.Path(__file__).parents[1].joinpath("model/torch.pt")
# PARAM_MODEL = pl.Path(r"model/_train/small-256/weights/best.pt")

MOTOR = gpio.OutputDevice(20, active_high=False)
VALVE = gpio.OutputDevice(21, active_high=False)

MOTOR.off()
VALVE.off()

cv2.namedWindow(WND_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WND_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

model = YOLO(PARAM_MODEL)

factory = gpio.pins.pigpio.PiGPIOFactory()

SENSOR = gpio.Button(7, pull_up=True, pin_factory=factory)

cam = cv2.VideoCapture(0)

LOCK = False
while True:

    mintime = 0
    maxtime = 0

    if not LOCK:
        if not cam.isOpened():
            cam = cv2.VideoCapture(0)
            sleep(0.01)
        else:
            LOCK = True

    while True:
        otime = time_ns()

        _, image = cam.read()
        cap = time_ns()
        
        results = model.predict(
            cv2.resize(image, dsize=(256, 192), interpolation=cv2.INTER_AREA),
            stream=False,
            conf=0.6,
            imgsz=(256, 192)
        )
        
        delay = time_ns() - cap
        
        dist = SENSOR.is_pressed
            
        image = cv2.putText(image, f"{dist}", (5, 270), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), thickness=2)
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
                    
                    TARGET = dist
                    
                image = cv2.rectangle(image, (fbx, fby), (fex, fey), color=color, thickness=5)
                
        if TARGET:
            image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
        else:
            image = crosshair_norm(image, 0.1, 0.1, 0.05)
        
        imintime = time_ns()
        mintime = (imintime - otime) / 1000000000
        image = cv2.putText(image, f"min: {mintime:.6f}s | max: {maxtime:.6f}s", (5, 235), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), thickness=2)
        
        cv2.imshow(WND_NAME, image)
        
        if TARGET:
            
            VALVE.on()
            
            _, image = cam.read()
            
            image = cv2.putText(image, f"PROCESSING", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
            image = cv2.rectangle(image, (fbx, fby), (fex, fey), color=color, thickness=5)
            image = cv2.putText(image, f"min: {mintime:.6f}s | max: {maxtime:.6f}s", (5, 235), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), thickness=2)
            image = cv2.putText(image, f"{dist}", (5, 270), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), thickness=2)
            image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
            MOTOR.on()
            
            cv2.imshow(WND_NAME, image)
            sleep(1)
        
            #for ii in range(int(tspray * 10)):
            #    _, image = cam.read()
            #    image = cv2.putText(image, f"SPRAYING", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
            #    image = cv2.rectangle(image, (fbx, fby), (fex, fey), color=color, thickness=5)
            #    image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
            #    
            #    cv2.imshow(WND_NAME, image)
            #    sleep(0.01)
            sleep(0.5)

            MOTOR.off()
            VALVE.off()

            imaxtime = time_ns()
            maxtime = (imaxtime - otime) / 1000000000


            for ii in range(25):
                _, image = cam.read()
                
                image = crosshair_norm(image, 0.1, 0.1, 0.05, color=(0, 255, 0))
                image = cv2.putText(image, f"DOWNTIME: {(25 - ii) / 10}s", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
                image = cv2.putText(image, f"min: {mintime:.6f}s | max: {maxtime:.6f}s", (5, 235), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), thickness=2)
                image = cv2.putText(image, f"{dist}", (5, 270), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), thickness=2)
                cv2.imshow(WND_NAME, image)
                
                k = cv2.waitKey(1)
                if k != -1:
                    break
                else:
                    sleep(0.03) # sleep for 1 frame time

        mintime = 0
        maxtime = 0
        
        dist = False
        
        k = cv2.waitKey(1)
        if k != -1:
            break
        else:
            sleep(0.05)
        
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(0.05)

