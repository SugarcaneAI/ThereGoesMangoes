import pathlib as pl

from ultralytics import YOLO

MODEL_ROOT = pl.Path(r"E:\Git\ThereGoesMangoes\model\_train")

for msize in ["nano", "small", "medium", "large"]:
    for imgsz in [256, 512, 640, 1024]:
        
        MODEL = MODEL_ROOT.joinpath(f"{msize}-{imgsz}")
        
        if not MODEL.exists():
            print(f"Skipping model [{msize}-{imgsz}] as no models were found.")
            continue
            
        if not MODEL.joinpath("weights").joinpath("best_saved_model").exists():
            print("Exporting model to TF Keras format")
            temp = MODEL.joinpath("weights").joinpath("best.pt")
            temp = YOLO(temp).export(format="saved_model", keras=True)
            
        MODEL = MODEL.joinpath("weights").joinpath("best.pt")
        
        print(f"Validating model [{msize}-{imgsz}]")
        MODEL = YOLO(MODEL, task="detect")
        
        print("Validating with validation `val` dataset")
        metrics = MODEL.val(
            data=r"E:\Git\ThereGoesMangoesDataset\yolo_mango_detection.yaml",
            imgsz=imgsz,
            batch=10,
            split="val",
            project="post",
            name=f"{msize}-{imgsz}-val",
            exist_ok=True,
            device="cpu"
        )
        
        print(metrics.box.maps)
        
        print("Validating with testing `test` dataset")
        metrics = MODEL.val(
            data=r"E:\Git\ThereGoesMangoesDataset\yolo_mango_detection.yaml",
            imgsz=imgsz,
            batch=10,
            split="test",
            project="post",
            name=f"{msize}-{imgsz}-test"
        )
        
        print(metrics.box.maps)
