import pathlib as pl
from time import time_ns, sleep

import cv2
import numpy as np
import pandas as pd

from ultralytics import YOLO

PARAM_MODEL_FOLDER = pl.Path(r"E:\Git\ThereGoesMangoes\model\_train")

print("Discovering models", end="\r")

MODELS = [x.joinpath("weights/best.pt") for x in PARAM_MODEL_FOLDER.iterdir() if x.joinpath("weights/best.pt").exists()]

print(f"Discovered {len(MODELS)} models")
for model in MODELS:
    print(f"\t> {model.parent.parent.stem}")

CONFIDENCE_MAP = {
    "large-640": 0.207,
    "medium-1024": 0.194,
    "medium-640": 0.208,
    "nano-1024": 0.243,
    "nano-640": 0.233,
    "small-1024": 0.204,
    "small-640": 0.203,
}

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

PARAM_TEST_NAME = "val"

PARAM_DATASET_ROOT = pl.Path(r"E:\Git\ThereGoesMangoesDataset")
PARAM_DATASET_IMAGES = PARAM_DATASET_ROOT.joinpath("images").joinpath(PARAM_TEST_NAME)
PARAM_DATASET_LABELS = PARAM_DATASET_ROOT.joinpath("labels").joinpath(PARAM_TEST_NAME)

print("Discovering dataset images and labels", end="\r")
ITEMS = []
for imgpth in PARAM_DATASET_IMAGES.iterdir():
    lblpth = PARAM_DATASET_LABELS.joinpath(f"{imgpth.stem}.txt")
    if lblpth.exists():
        ITEMS.append((imgpth, lblpth))
print(f"Discovered {len(ITEMS)} matched dataset images and labels")

PARAM_OUTPUT_FOLDER_ROOT = pl.Path(r"E:\Git\ThereGoesMangoes\post\_train")

begin = time_ns()
for model_path in MODELS:
    model_name = model_path.parent.parent.stem

    output_dir = PARAM_OUTPUT_FOLDER_ROOT.joinpath(f"{model_name}-{PARAM_TEST_NAME}").joinpath("fragments")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Testing model `{model_name}` using `{PARAM_TEST_NAME}` test.")
    model_begin_time = time_ns()

    model = YOLO(model_path)

    print(f"Model loaded @ {(time_ns() - model_begin_time) / 1000000000:.2f}s")

    results = {
        "target": [],
        "height": [],
        "width": [],
        "space_accuracy": [],
        "space_precision": [],
        "space_recall": [],
        "space_f_score": [],
        "labels": [],
        "detections": [],
        "time": []
    }

    for index, (image_path, label_path) in enumerate(ITEMS):
        print(f"\tProcessing image {index + 1} / {len(ITEMS)} @ {(time_ns() - model_begin_time) / 1000000000:.2f}s")

        image = cv2.imread(image_path.as_posix())

        height, width, _ = image.shape

        results["target"].append(image_path.name)
        results["height"].append(height)
        results["width"].append(width)

        plots = np.zeros((height, width), np.uint8)

        data = open(label_path, "r+").readlines()

        for data_point in data:
            data_point = data_point.split()

            cls = int(data_point[0])

            cx = float(data_point[1])
            cy = float(data_point[2])
            bw = float(data_point[3])
            bh = float(data_point[4])

            rw = bw / 2
            rh = bh / 2

            bx = int((cx - rw) * width)
            by = int((cy - rh) * height)
            ex = int((cx + rw) * width)
            ey = int((cy + rh) * height)

            plots = cv2.rectangle(plots, (bx, by), (ex, ey), color=255, thickness=-1)

        results["labels"].append(len(data))

        dplot = np.zeros((height, width), np.uint8)

        print("\tDetecting from image")

        dtime = time_ns()

        boxes = model(
            image,
            stream=False,
            conf=CONFIDENCE_MAP[model_name],
            verbose=None
        )[0].boxes

        det = {
            "class": [],
            "class_name": [],
            "centroid_x": [],
            "centroid_y": [],
            "box_width": [],
            "box_height": [],
            "confidence": []
        }
        for box in boxes:

            cls = int(box.cls)
            conf = float(box.conf)

            cx, cy, bw, bh = box.xywhn[0]

            cx = float(cx)
            cy = float(cy)
            bw = float(bw)
            bh = float(bh)

            rw = bw / 2
            rh = bh / 2

            bx = int((cx - rw) * width)
            by = int((cy - rh) * height)
            ex = int((cx + rw) * width)
            ey = int((cy + rh) * height)

            dplot = cv2.rectangle(dplot, (bx, by), (ex, ey), color=255, thickness=-1)

            image = cv2.rectangle(image, (bx, by), (ex, ey), color=color_dict[cls], thickness=2)
            image = cv2.putText(image, f"{color_name[cls]} {conf:.2f}", (bx, by - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=color_dict[cls], thickness=2)

            det["class"].append(cls)
            det["class_name"].append(color_name[cls])
            det["centroid_x"].append(cx)
            det["centroid_y"].append(cy)
            det["box_width"].append(bw)
            det["box_height"].append(bh)
            det["confidence"].append(conf)

        results["detections"].append(len(boxes))

        etime = (time_ns() - dtime) / 1000000000
        print(f"\tDetected from image in {etime:.2f}s")

        det = pd.DataFrame(det)
        det.to_csv(output_dir.joinpath(f"{image_path.stem}.csv").as_posix(), index=False)

        results["time"].append(etime)

        tp = np.sum(cv2.bitwise_and(dplot, plots))
        fn = np.sum(cv2.bitwise_xor(dplot, plots))
        fp = np.sum(cv2.bitwise_and(dplot, cv2.bitwise_not(plots)))
        tn = np.sum(cv2.bitwise_xor(dplot, cv2.bitwise_not(plots)))

        acc = (tp + tn) / (tp + tn + fp + fn)
        prc = tp / (tp + fp)
        rec = tp / (tp + fn)
        fsc = 2 * ((prc * rec) / (prc + rec))

        results["space_accuracy"].append(acc)
        results["space_precision"].append(prc)
        results["space_recall"].append(rec)
        results["space_f_score"].append(fsc)

        cv2.imwrite(output_dir.joinpath(image_path.name).as_posix(), image)

    df = pd.DataFrame(results)
    df.to_csv(output_dir.joinpath("_data.csv").as_posix(), index=False)
    print()
