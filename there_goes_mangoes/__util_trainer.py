import pathlib as pl

from ultralytics import YOLO

msize = "n"
mname = "nano"
imgsz = 64

PARAM_DATASET_YAML = pl.Path(r"E:\Git\WetThereGoesMangoesDataset\yolo_wet_mango_detection_2.yaml")

model = YOLO(f"yolov8{msize}.pt")
model.train(
    data=PARAM_DATASET_YAML.as_posix(),
    epochs=50,
    batch=16,
    imgsz=imgsz,
    patience=50,
    device="cpu",
    project="mangoes",
    name=f"{mname}-{imgsz}",
    exist_ok=True,
)
# validate
model.val(
    split="test",
    name=f"{mname}-{imgsz}-val",
    exist_ok=True,
)
