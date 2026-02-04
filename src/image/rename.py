import os
from tqdm import tqdm

from utils.config import load_config


config = load_config("config.toml")
RAW_PATH = config["images"]["raw_path"]
RENAMED_PATH = config["images"]["renamed_path"]
LABELED_PATH = config["images"]["labeled_path"]


def rename_images(start_index=0):
    all_files = os.listdir(RAW_PATH)
    index = start_index
    for file in tqdm(all_files, desc="Renaming images"):
        new_name = f"{index}{os.path.splitext(file)[1]}"
        os.rename(
            os.path.join(RAW_PATH, file),
            os.path.join(RENAMED_PATH, new_name)
        )
        index += 1


def find_index():
    labeled_files = os.listdir(LABELED_PATH)
    if not labeled_files:
        return 0
    
    indices = [
        int(os.path.splitext(file)[0])
        for file in labeled_files
        if file.endswith((".png", ".jpg"))
    ]
    return max(indices) + 1 if indices else 0


def main():
    start_index = find_index()
    print(f"Starting index for renaming: {start_index}")
    cont = input("Continue? (Y/n): ")
    if cont.lower() in ("y", "yes", ""):
        rename_images(start_index)
    else:
        print("Renaming aborted.")


if __name__ == "__main__":
    main()