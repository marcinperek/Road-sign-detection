# Road sign detection

Goal of this project is to train a model to detect road signs and later deploy it on Raspberry Pi.

Currently the project trains YOLOv10 model, in the future it will be replaced by a TensorFlow Lite model.

## Getting started
1. Clone the repository.
2. Create a virtual environment and install dependencies:
    ```bash
    uv sync
    ```
3. If needed, adjust paths in `config.toml` file.

## Dataset creation
Put the raw images in `images/raw` folder according to the folder structure below.
Run
```bash
uv run images-rename
```
to rename the images.

Then run
```bash
uv run images-crop
```
to open a GUI for cropping the images.

After cropping open the `images/unlabeled` folder in LabelImg, label the images and save annotations in Pascal VOC format in `images/labeled`.

To convert the dataset to YOLO format run
```bash
uv run images-to-yolo
```

To check how much images are labeled for each class run
```bash
uv run check-classes
```

## Image processing pipeline
Folder structure:
```
images/
├─ raw/             - raw images for the dataset
├─ renamed/         - images with numbered filenames
├─ unlabeled/       - cropped images
├─ labeled/         - labeled images, TensorFlow ready
└─ yolo_dataset/    - dataset in YOLO format
```

Pipeline steps:

1. Collect raw images.
2. Rename images to `[number].png` format.
3. Crop images to 640x640
4. Label images using LabelImg and save in Pascal VOC format.

Additional YOLO steps:

5. Organize YOLO dataset structure for training.
6. Convert Pascal VOC annotations to YOLO format.