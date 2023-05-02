import argparse as ap
import pathlib as pl
import random

import cv2
import numpy as np

PARAM_SOURCE_FOLDER = r"D:\Git\ThereGoesMangoes\data\augmented"
PARAM_TARGET_FOLDER = r"D:\Git\ThereGoesMangoes\data\collage"

PARAM_SOURCE_FOLDER = pl.Path(PARAM_SOURCE_FOLDER)
PARAM_TARGET_FOLDER = pl.Path(PARAM_TARGET_FOLDER)

if not PARAM_TARGET_FOLDER.exists() and not PARAM_TARGET_FOLDER.is_dir():
    PARAM_TARGET_FOLDER.mkdir(exist_ok=True, parents=True)
    
ITEMS = [x for x in PARAM_SOURCE_FOLDER.iterdir()]

PARAM_OBJECTS_TO_GENERATE = 135

PARAM_COLLAGE_SIZE_LENGTH = 2000
PARAM_COLLAGE_SIZE_HEIGHT = 2000
PARAM_COLLAGE_ROWS = 2
PARAM_COLLAGE_COLS = 2

PARAM_COLLAGE_ROW_DEPTH = PARAM_COLLAGE_SIZE_HEIGHT // PARAM_COLLAGE_ROWS
PARAM_COLLAGE_COL_DEPTH = PARAM_COLLAGE_SIZE_LENGTH // PARAM_COLLAGE_COLS

for count in range(PARAM_OBJECTS_TO_GENERATE):
    
    generated = np.zeros((PARAM_COLLAGE_SIZE_HEIGHT, PARAM_COLLAGE_SIZE_LENGTH, 3))
    
    if len(ITEMS) == 0 or len(ITEMS) < (PARAM_COLLAGE_COLS * PARAM_COLLAGE_ROWS):
        break
    
    for col in range(PARAM_COLLAGE_COLS):
        for row in range(PARAM_COLLAGE_ROWS):
            
            loc_begin_x = PARAM_COLLAGE_COL_DEPTH * col
            loc_begin_y = PARAM_COLLAGE_ROW_DEPTH * row
            
            capture = cv2.imread(str(ITEMS.pop(random.randint(0, len(ITEMS) - 1))))
            
            extent_y, extent_x = capture.shape[:-1]
            
            if extent_y > PARAM_COLLAGE_ROW_DEPTH:
                capture = capture[:PARAM_COLLAGE_ROW_DEPTH, :, :]
                
            if extent_x > PARAM_COLLAGE_COL_DEPTH:
                capture = capture[:, :PARAM_COLLAGE_COL_DEPTH, :]
                
            extent_y, extent_x = capture.shape[:-1]
            
            loc_end_x = loc_begin_x + (PARAM_COLLAGE_COL_DEPTH if extent_x == PARAM_COLLAGE_COL_DEPTH else extent_x)
            loc_end_y = loc_begin_y + (PARAM_COLLAGE_ROW_DEPTH if extent_y == PARAM_COLLAGE_ROW_DEPTH else extent_y)
            
            generated[loc_begin_y:loc_end_y, loc_begin_x:loc_end_x, :] = capture[:, :, :]
            
    path = PARAM_TARGET_FOLDER.joinpath(f"collage_{count}.png")
    cv2.imwrite(str(path), generated)

