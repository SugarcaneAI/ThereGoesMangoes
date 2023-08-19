import pathlib as pl
from time import time_ns, sleep

import cv2

PARAM_TARGET_FOLDER: pl.Path = pl.Path(r"E:\Git\ThereGoesMangoesDataset\items")
PARAM_OUTPUT_FOLDER: pl.Path = pl.Path(r"E:\Git\ThereGoesMangoesDataset\items")

PARAM_MAX_SIDE_SIZE = 640

FILES = [x for x in PARAM_TARGET_FOLDER.iterdir()]
PROCESSED = 0

begin = time_ns()
for index, imagepth in enumerate(FILES):
    print(f"Processing {index + 1} / {len(FILES)} @ {(time_ns() - begin) / 1000000000:.4f}s", end="\r")

    image = cv2.imread(imagepth.as_posix())

    height, width,_ = image.shape

    max_side = height if height >= width else width
    if max_side == PARAM_MAX_SIDE_SIZE:
        continue
    sratio = PARAM_MAX_SIDE_SIZE / max_side

    fy = int(height * sratio)
    fx = int(width * sratio)

    image = cv2.resize(image, (fx, fy), interpolation=cv2.INTER_CUBIC)

    name = PARAM_OUTPUT_FOLDER.joinpath(imagepth.name)
    cv2.imwrite(name.as_posix(), image)

    while not name.exists():
        sleep(0.01)

    PROCESSED += 1

print(f"Finished processing {PROCESSED} / {len(FILES)} after {(time_ns() - begin) / 1000000000:.4f}s")
