import cv2
import numpy as np
import typing

def crosshair_norm(
    image: np.ndarray, 
    pct_length: float, 
    pct_height: float,
    pct_radius: float,
    *, 
    color: typing.Tuple[int, int, int] = (255, 0, 0),
):
    yy, xx, _ = image.shape
    
    bx = int((xx // 2) - (xx * pct_length))
    ex = int((xx // 2) + (xx * pct_length))
    
    by = int((yy // 2) - (yy * pct_height))
    ey = int((yy // 2) + (yy * pct_height))
    
    rad = int(np.max([yy, xx]) * pct_radius)
    
    image = cv2.line(image, (bx, yy // 2), (ex, yy // 2), color)
    image = cv2.line(image, (xx // 2, by), (xx // 2, ey), color)
    image = cv2.circle(image, (xx // 2, yy // 2), rad, color)
    
    return image
