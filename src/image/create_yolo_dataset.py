import os
import shutil
from tqdm import tqdm

from image.voc_to_yolo import main as voc_to_yolo
from image.train_test_split import main as train_val_split
from utils.config import load_config


def main():
    config = load_config("config.toml")

    LABELED_PATH = os.path.join(config["images"]["labeled_path"])
    YOLO_PATH = os.path.join(config["images"]["yolo_dataset_path"])

    print("Converting to YOLO dataset...")

    all_files = os.listdir(LABELED_PATH)
    voc_to_yolo(LABELED_PATH, YOLO_PATH)

    for file in tqdm(all_files, desc="Copying images"):
        if os.path.splitext(file)[1] in [".png", ".jpg"]:
            shutil.copy(os.path.join(LABELED_PATH, file), os.path.join(YOLO_PATH, file))
    
    train_val_split()

    print("Done")


if __name__ == "__main__":
    main()