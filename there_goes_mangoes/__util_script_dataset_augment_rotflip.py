import argparse as ap
import pathlib as pl
import typing

import cv2

# Source and Output target folders
PARAM_SOURCE_FOLDER = r"D:\Git\ThereGoesMangoes\data\raw"
PARAM_TARGET_FOLDER = r"D:\Git\ThereGoesMangoes\data\augmented"

PARAM_SOURCE_FOLDER = pl.Path(PARAM_SOURCE_FOLDER)
PARAM_TARGET_FOLDER = pl.Path(PARAM_TARGET_FOLDER)

if not PARAM_TARGET_FOLDER.exists() and not PARAM_TARGET_FOLDER.is_dir():
    PARAM_TARGET_FOLDER.mkdir(exist_ok=True, parents=True)

CLASS_FOLDERS: typing.List[pl.Path] = [x for x in PARAM_SOURCE_FOLDER.iterdir()]
ITEMS: typing.List[typing.Tuple[str, pl.Path]] = []

# Collect all targets
for cls in CLASS_FOLDERS:
    for path in cls.iterdir():
        ITEMS.append((cls.name, path))

# Augment

ii = 0
for (cls, path) in ITEMS:
    
    img = cv2.imread(str(path))
    
    if img is None:
        continue
    
    loc = str(PARAM_TARGET_FOLDER.joinpath(f"mango_{ii}_{cls}_{path.stem}.png"))
    cv2.imwrite(loc, img)
    ii += 1
    
    for rot in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]:
        
        rott = cv2.rotate(img, rot)
        loc = str(PARAM_TARGET_FOLDER.joinpath(f"mango_{ii}_{cls}_{path.stem}.png"))
        cv2.imwrite(loc, rott)
        ii += 1
        
        for flip in [0, 1, -1]:
            
            flipp = cv2.flip(rott, flip)
            loc = str(PARAM_TARGET_FOLDER.joinpath(f"mango_{ii}_{cls}_{path.stem}.png"))
            cv2.imwrite(loc, flipp)
            ii += 1
