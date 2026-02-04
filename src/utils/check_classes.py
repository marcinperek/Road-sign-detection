import os
import xml.etree.ElementTree as ET
from termcolor import colored

from utils.config import load_config

def check_classes():
    config = load_config("config.toml")
    path = config["images"]["labeled_path"]
    all_files = os.listdir(path)

    classes = {name: 0 for name in config["images"]["classes"]}
    labeled = 0
    images = 0
    target = config["images"]["min_per_class"]

    for file in all_files:
        if os.path.splitext(file)[1] == ".xml":
            labeled += 1
            tree = ET.parse(os.path.join(path, file))
            for obj in tree.getroot().findall("object"):
                name_elem = obj.find("name")
                if name_elem is not None and name_elem.text:
                    text = name_elem.text
                    if text not in classes:
                        print(colored(f"Wrong class: {text} in file {file}", "red"))
                    else:
                        classes[text] += 1

        elif os.path.splitext(file)[1] == ".png":
            images += 1

    if labeled < images:
        print(colored(f"Missing labels for {images - labeled} images", "red"))
    else:
        print(colored("All images labeled", "green"))

    for i in list(classes):
        if classes[i] == 0:
            print(colored(f"{i}: {classes[i]}", "red"))
        elif classes[i] >= target:
            print(colored(f"{i}: {classes[i]}", "green"))
        else:
            print(f"{i}: ", colored(classes[i], "red"), f"(lacking {target - classes[i]})")


if __name__ == "__main__":
    check_classes()