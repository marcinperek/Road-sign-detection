import os
import random
from tqdm import trange

from utils.config import load_config


def main():
    config = load_config("config.toml")

    YOLO_PATH = os.path.join(config["images"]["yolo_dataset_path"])

    image_files = [
        f for f in os.listdir(YOLO_PATH) if f.endswith(".png") or f.endswith(".jpg")
    ]

    file_num = len(image_files)
    if config["dataset"]["test_split"] > 0:
        train_num = int(file_num * config["dataset"]["train_split"])
        val_num = int(file_num * config["dataset"]["val_split"])
    else:
        train_num = int(file_num * config["dataset"]["train_split"])
        val_num = file_num - train_num

    os.makedirs(os.path.join(YOLO_PATH, "images", "train"), exist_ok=True)
    os.makedirs(os.path.join(YOLO_PATH, "images", "validation"), exist_ok=True)
    os.makedirs(os.path.join(YOLO_PATH, "labels", "train"), exist_ok=True)
    os.makedirs(os.path.join(YOLO_PATH, "labels", "validation"), exist_ok=True)
    if config["dataset"]["test_split"] > 0:
        os.makedirs(os.path.join(YOLO_PATH, "images", "test"), exist_ok=True)
        os.makedirs(os.path.join(YOLO_PATH, "labels", "test"), exist_ok=True)
        
    random.shuffle(image_files)
    for i in trange(train_num, desc="Moving training images"):
        file = image_files[i]
        image_idx = os.path.splitext(file)[0]
        os.rename(
            os.path.join(YOLO_PATH, file),
            os.path.join(YOLO_PATH, "images", "train", file),
        )
        os.rename(
            os.path.join(YOLO_PATH, f"{image_idx}.txt"),
            os.path.join(YOLO_PATH, "labels", "train", f"{image_idx}.txt"),
        )

    for i in trange(train_num, train_num + val_num, desc="Moving validation images"):
        file = image_files[i]
        image_idx = os.path.splitext(file)[0]
        os.rename(
            os.path.join(YOLO_PATH, file),
            os.path.join(YOLO_PATH, "images", "validation", file),
        )
        os.rename(
            os.path.join(YOLO_PATH, f"{image_idx}.txt"),
            os.path.join(YOLO_PATH, "labels", "validation", f"{image_idx}.txt"),
        )

    if config["dataset"]["test_split"] > 0:
        for i in trange(train_num + val_num, file_num, desc="Moving test images"):
            file = image_files[i]
            image_idx = os.path.splitext(file)[0]
            os.rename(
                os.path.join(YOLO_PATH, file),
                os.path.join(YOLO_PATH, "images", "test", file),
            )
            os.rename(
                os.path.join(YOLO_PATH, f"{image_idx}.txt"),
                os.path.join(YOLO_PATH, "labels", "test", f"{image_idx}.txt"),
            )


if __name__ == "__main__":
    main()
