import pathlib as pl
from time import sleep

from ultralytics import YOLO

import cv2

WND_NAME = "Camera View"
MODEL_PATH = pl.Path(r"model/torch.pt")

model = YOLO(MODEL_PATH, task="detect")
    
cv2.namedWindow(WND_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WND_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

results = model.predict(0, True)

for result in results:
    
    image = result.orig_img
    
    result
        
    cv2.imshow(WND_NAME, image)
    k = cv2.waitKey(1)
    if k != -1:
        break
    else:
        sleep(0.5)
