import yaml
import json
import pathlib as pl
from sklearn.model_selection import train_test_split
import shutil
import typing

# name of the dataset
DATASET_NAME = "mango_detection"

print(f"Processing dataset: {DATASET_NAME}")

# data source folder
PARAM_TARGET_SOURCE = str(pl.Path(__file__).parents[1].joinpath("data/buffer"))

# data output folder
PARAM_TARGET_OUTPUT = str(pl.Path(__file__).parents[1].joinpath("data/output"))

PARAM_TARGET_SOURCE = pl.Path(PARAM_TARGET_SOURCE)
PARAM_TARGET_OUTPUT = pl.Path(PARAM_TARGET_OUTPUT)

# check source directory

# require `classes.txt` file
path = PARAM_TARGET_SOURCE.joinpath("classes.txt")
if not path.exists():
    raise RuntimeError(f"Required file `classes.txt` [{path.as_posix()}] not found.")
file = open(path, "r")

# acquire class names
classnames: typing.Dict[int, str] = {ii: x[:-1] for ii, x in enumerate(file.readlines())}
print(f"Found {len(classnames)} classes.")
for ii, cls in classnames.items():
    print(f"\t{ii}: {cls}")

# require `images` and `labels` folders
imagepath = PARAM_TARGET_SOURCE.joinpath("images")
if not imagepath.exists() and not imagepath.is_dir():
    raise RuntimeError(f"Required folder `images` [{imagepath.as_posix()}] not found.")
labelpath = PARAM_TARGET_SOURCE.joinpath("labels")
if not labelpath.exists() and not labelpath.is_dir():
    raise RuntimeError(f"Required folder `labels` [{labelpath.as_posix()}] not found.")

# acquire images and labels paths
images: typing.List[pl.Path] = [x for x in imagepath.iterdir()]
labels: typing.List[pl.Path] = [x for x in labelpath.iterdir()]
if len(images) != len(labels):
    raise RuntimeError(f"Mismatch of images (n: {len(images)}) and labels (n: {len(labels)})")

# integrity check
for ii, imp in enumerate(images):
    if imp.stem != labels[ii].stem:
        raise RuntimeError(f"Bad match detected with image {imp.stem} and label {labels[ii].stem}.")

# Training dataset size ratio
PARAM_DATA_TRAIN_SIZE = 0.75

# Validation dataset size ratio
PARAM_DATA_VAL_SIZE = 0.99

# Testing dataset size ratio
PARAM_DATA_TEST_SIZE = 1 - PARAM_DATA_VAL_SIZE

# ensure integrity with rebuild
del labels
labels = []

for item in images:
    
    label = labelpath.joinpath(item.stem + ".txt")
    if not label.exists():
        raise RuntimeError(f"Data integrity ensure failed with image [{item.as_posix()}], no matching label [{label.as_posix()}] found.")
    labels.append(label)

# build datasets
print(f"Building with {PARAM_DATA_TRAIN_SIZE:.2f}:({PARAM_DATA_VAL_SIZE:.2f}:{PARAM_DATA_TEST_SIZE:.2f}) ratios.")

TRAIN_DATASET_IMAGE, VAL_DATASET_IMAGE, TRAIN_DATASET_LABEL, VAL_DATASET_LABEL = train_test_split(images, labels, train_size=PARAM_DATA_TRAIN_SIZE)
VAL_DATASET_IMAGE, TEST_DATASET_IMAGE, VAL_DATASET_LABEL, TEST_DATASET_LABEL = train_test_split(VAL_DATASET_IMAGE, VAL_DATASET_LABEL, train_size=PARAM_DATA_VAL_SIZE)

print(f"Actual size {len(TRAIN_DATASET_IMAGE):.0f}:({len(VAL_DATASET_IMAGE):.0f}:{len(TEST_DATASET_IMAGE):.0f}) ratios.")

# create output sub-directories
imagepath = PARAM_TARGET_OUTPUT.joinpath("images")
imagepath.mkdir(parents=True, exist_ok=True)
imagepath.joinpath("train").mkdir(parents=True, exist_ok=True)
imagepath.joinpath("val").mkdir(parents=True, exist_ok=True)
imagepath.joinpath("test").mkdir(parents=True, exist_ok=True)
labelpath = PARAM_TARGET_OUTPUT.joinpath("labels")
labelpath.mkdir(parents=True, exist_ok=True)
labelpath.joinpath("train").mkdir(parents=True, exist_ok=True)
labelpath.joinpath("val").mkdir(parents=True, exist_ok=True)
labelpath.joinpath("test").mkdir(parents=True, exist_ok=True)

# process training datasets
print("Processing training dataset: ", end="")
for num, iitem in enumerate(TRAIN_DATASET_IMAGE):
    
    iname = iitem.name
    ipath = imagepath.joinpath("train").joinpath(iname)
    
    litem = TRAIN_DATASET_LABEL[num]
    lname = litem.name
    lpath = labelpath.joinpath("train").joinpath(lname)
    
    if iitem.stem != TRAIN_DATASET_LABEL[num].stem:
        raise RuntimeError(f"Data integrity check fail with image [{iitem.as_posix()}] and label [{litem.as_posix()}].")
    
    # copy files over
    shutil.copyfile(iitem, ipath)
    shutil.copyfile(litem, lpath)
print("Ok")
    
# process validation datasets
print("Processing validation dataset: ", end="")
for num, iitem in enumerate(VAL_DATASET_IMAGE):
    
    iname = iitem.name
    ipath = imagepath.joinpath("val").joinpath(iname)
    
    litem = VAL_DATASET_LABEL[num]
    lname = litem.name
    lpath = labelpath.joinpath("val").joinpath(lname)
    
    if iitem.stem != VAL_DATASET_LABEL[num].stem:
        raise RuntimeError(f"Data integrity check fail with image [{iitem.as_posix()}] and label [{litem.as_posix()}].")
    
    # copy files over
    shutil.copyfile(iitem, ipath)
    shutil.copyfile(litem, lpath)
print("Ok")

# process testing datasets
print("Processing testing dataset: ", end="")
for num, iitem in enumerate(TEST_DATASET_IMAGE):
    
    iname = iitem.name
    ipath = imagepath.joinpath("test").joinpath(iname)
    
    litem = TEST_DATASET_LABEL[num]
    lname = litem.name
    lpath = labelpath.joinpath("test").joinpath(lname)
    
    if iitem.stem != TEST_DATASET_LABEL[num].stem:
        raise RuntimeError(f"Data integrity check fail with image [{iitem.as_posix()}] and label [{litem.as_posix()}].")
    
    # copy files over
    shutil.copyfile(iitem, ipath)
    shutil.copyfile(litem, lpath)
print("Ok")

# Write output files
print("Writing output files: ", end="")

json.dump(
    {
        "name": DATASET_NAME,
        "path": PARAM_TARGET_OUTPUT.as_posix(),
        "train": imagepath.joinpath("train").relative_to(PARAM_TARGET_OUTPUT).as_posix(),
        "val": imagepath.joinpath("val").relative_to(PARAM_TARGET_OUTPUT).as_posix(),
        "test": imagepath.joinpath("test").relative_to(PARAM_TARGET_OUTPUT).as_posix(),
        "names": classnames
    },
    open(
        PARAM_TARGET_OUTPUT.joinpath(f"yolo_{DATASET_NAME}.json"),
        "w+"
    )
)

yaml.dump(
    {
        "name": DATASET_NAME,
        "path": PARAM_TARGET_OUTPUT.as_posix(),
        "train": imagepath.joinpath("train").relative_to(PARAM_TARGET_OUTPUT).as_posix(),
        "val": imagepath.joinpath("val").relative_to(PARAM_TARGET_OUTPUT).as_posix(),
        "test": imagepath.joinpath("test").relative_to(PARAM_TARGET_OUTPUT).as_posix(),
        "names": classnames
    },
    open(
        PARAM_TARGET_OUTPUT.joinpath(f"yolo_{DATASET_NAME}.yaml"),
        "w+"
    )
)
print("Ok")

print("Finished processing.")
