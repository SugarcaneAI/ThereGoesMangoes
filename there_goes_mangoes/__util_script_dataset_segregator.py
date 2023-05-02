import argparse as ap
import pathlib as pl
import random
import shutil

PARAM_SOURCE_FOLDER = r"D:\Git\ThereGoesMangoes\data\items"
PARAM_TARGET_FOLDER = r"D:\Git\ThereGoesMangoes\data\sets"

PARAM_SOURCE_FOLDER = pl.Path(PARAM_SOURCE_FOLDER)
PARAM_TARGET_FOLDER = pl.Path(PARAM_TARGET_FOLDER)

if not PARAM_TARGET_FOLDER.exists() and not PARAM_TARGET_FOLDER.is_dir():
    PARAM_TARGET_FOLDER.mkdir(exist_ok=True, parents=True)
    
ITEMS = [x for x in PARAM_SOURCE_FOLDER.iterdir()]

while len(ITEMS) > 0:
    for annotator in ["missy", "xen", "bea", "pearl"]:
        apath = PARAM_TARGET_FOLDER.joinpath(annotator)
        
        if not apath.exists():
            apath.mkdir(exist_ok=True, parents=True)
            
        src = ITEMS.pop(random.randint(0, len(ITEMS) - 1))
        dst = apath.joinpath(src.name)
        
        shutil.copyfile(src, dst)
