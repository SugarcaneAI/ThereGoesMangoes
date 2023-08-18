import pathlib as pl
from time import time_ns, sleep

import cv2
import numpy as np

PARAM_TARGET_FOLDER: pl.Path = pl.Path(r"E:\Git\ThereGoesMangoes\data\wet")
PARAM_OUTPUT_FOLDER: pl.Path = pl.Path(r"E:\Git\ThereGoesMangoes\data\wet")

PARAM_MAX_SIDE_SIZE = 640

FILES = [x for x in PARAM_TARGET_FOLDER.iterdir()]

begin = time_ns()
for index, imagepth in enumerate(FILES):
    print(f"Processing {index + 1} / {len(FILES)} @ {(time_ns() - begin) / 1000000000:.4f}s", end="\r")

    image = cv2.imread(imagepth.as_posix())

    height, width,_ = image.shape

    max_side = height if height >= width else width
    sratio = PARAM_MAX_SIDE_SIZE / max_side

    fx = height / max_side * sratio
    fy = width / max_side * sratio

    image = cv2.resize(image, None, fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)

    name = PARAM_OUTPUT_FOLDER.joinpath(imagepth.name)
    cv2.imwrite(name.as_posix(), image)

    while not name.exists():
        sleep(0.01)
