import pathlib as pl
from time import sleep

from ultralytics import YOLO

import cv2

WND_NAME = "Camera View"
MODEL_PATH = pl.Path(r"model/torch.pt")

model = YOLO(MODEL_PATH, task="detect")

cam = cv2.VideoCapture(0)

while not cam.isOpened():
    cam = cv2.VideoCapture(0)
    sleep(0.01)
    
#cv2.namedWindow(WND_NAME, cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty(WND_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

while True:
    result = None
    
    _, image = cam.read()
    
    results = model.predict(image, True)
    
    if results.gi_running:
        for result in results:
            pass
        
    cv2.imshow(WND_NAME, image)
    sleep(0.5)
