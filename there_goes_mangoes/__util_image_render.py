import pathlib as pl
from time import time_ns, sleep

import cv2

PARAM_TARGET_FOLDER_IMG = pl.Path(r"E:\Git\ThereGoesMangoesDataset\images\train")
PARAM_TARGET_FOLDER_DAT = pl.Path(r"E:\Git\ThereGoesMangoesDataset\labels\train")
PARAM_OUTPUT_FOLDER_REN = pl.Path(r"E:\Git\ThereGoesMangoesDataset\render\train")

TARGETS = [x.stem for x in PARAM_TARGET_FOLDER_IMG.iterdir()]

color_dict = {
    0: (127, 0, 0),
    1: (0, 127, 0),
    2: (0, 0, 127),
    3: (255, 255, 0),
    4: (0, 255, 255)
}

color_name = {
    0: "carabao",
    1: "flower",
    2: "indian",
    3: "wet_carabao",
    4: "wet_indian",
}

THICKNESS = 5

FAILURES = {}

begin = time_ns()
for index, name in enumerate(TARGETS):
    print(f"Processing {index + 1} / {len(TARGETS)} @ {(time_ns() - begin) / 1000000000:.4f}s", end="\r")

    image = PARAM_TARGET_FOLDER_IMG.joinpath(f"{name}.png")
    image = cv2.imread(image.as_posix())

    height, width, _ = image.shape

    try:
        data = open(PARAM_TARGET_FOLDER_DAT.joinpath(f"{name}.txt")).readlines()

        for dtp in data:
            dtp = dtp.split(" ")

            cls = int(dtp[0])

            cx = float(dtp[1])
            cy = float(dtp[2])
            bw = float(dtp[3])
            bh = float(dtp[4])

            if any([x > 1 for x in [cx, cy, bw, bh]]):
                raise RuntimeError(f"Broken data file with datapoints {dtp}")

            rw = bw / 2
            rh = bh / 2

            bx = int((cx - rw) * width)
            by = int((cy - rh) * height)
            ex = int((cx + rw) * width)
            ey = int((cy + rh) * height)

            image = cv2.rectangle(image, (bx, by), (ex, ey), color_dict[cls], thickness=THICKNESS)
            image = cv2.putText(image, color_name[cls], (bx, by - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color=color_dict[cls], thickness=2)

        cv2.imwrite(PARAM_OUTPUT_FOLDER_REN.joinpath(f"{name}.png").as_posix(), image)
    except Exception as exc:
        FAILURES[name] = str(exc)

print(f"Finished processing {len(TARGETS) - len(FAILURES)} / {len(TARGETS)} after {(time_ns() - begin) / 1000000000:.4f}s")

if len(FAILURES) > 0:
    print("Failure details:")
    for name, failure in FAILURES.items():
        print(f"\t> {name}: `{failure}`")
