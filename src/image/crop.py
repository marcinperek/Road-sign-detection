import os
from PIL import Image, ImageTk, ImageEnhance
from tkinter import filedialog
import tkinter as tk

from utils.config import load_config

config = load_config("config.toml")

class CropperApp:
    def __init__(self, root):
        self.root = root
        self.img = None
        self.img_tk = None
        self.rect = None
        self.out_size = (640, 640)
        self.label = None
        self.button_open = None
        self.button_renamed = None
        self.button_crop = None
        self.button_next = None
        self.mask_applied = False
        self.cropped_image = None
        self.file_name = None
        self.current_dir = None

        self.create_window()

    def create_window(self):
        self.root.title("Image Cropper")

        self.label = tk.Label(self.root, text="Select an image to crop")
        self.label.pack(side="top", fill="both", expand=True)

        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", fill="x")

        self.button_open = tk.Button(
            button_frame, text="Open Image", command=self.open_image, bg="lightblue"
        )
        self.button_open.pack(side="left", fill="x", expand=True)

        self.button_renamed = tk.Button(
            button_frame, text="Start in Renamed", command=self.load_renamed_dir, bg="lightcyan"
        )
        self.button_renamed.pack(side="left", fill="x", expand=True)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Select an image", filetypes=[("Image files", "*.jpg;*.png")]
        )
        
        if not path:
            return

        self.file_name = os.path.basename(path)
        self.current_dir = os.path.dirname(path)
        print(f"Selected image: {self.file_name}")

        self.img = Image.open(path)
        self.img_tk = ImageTk.PhotoImage(self.img)

        enhancer = ImageEnhance.Brightness(self.img)
        self.img_grey = ImageTk.PhotoImage(enhancer.enhance(0.3))

        self.canvas.bind("<Motion>", self.update_rectangle)
        self.canvas.bind("<Button-1>", self.select_crop)

        self.display_image()

    def load_renamed_dir(self):
        renamed_path = config["images"]["renamed_path"]
        if not os.path.exists(renamed_path):
            print(f"Renamed path not found: {renamed_path}")
            return

        files = [
            f
            for f in os.listdir(renamed_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if not files:
            print("No images found in renamed folder")
            return

        files.sort()
        first_file = os.path.join(renamed_path, files[0])

        self.file_name = files[0]
        self.current_dir = renamed_path
        print(f"Loading renamed image: {self.file_name}")

        self.img = Image.open(first_file)
        self.img_tk = ImageTk.PhotoImage(self.img)

        enhancer = ImageEnhance.Brightness(self.img)
        self.img_grey = ImageTk.PhotoImage(enhancer.enhance(0.3))

        self.canvas.bind("<Motion>", self.update_rectangle)
        self.canvas.bind("<Button-1>", self.select_crop)

        self.display_image()

    def display_image(self):
        if not self.img:
            raise ValueError("No image loaded")

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        self.canvas.config(width=self.img.width, height=self.img.height)

        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            3, 3, self.out_size[0], self.out_size[1], outline="red", width=2
        )

        self.update_buttons()

    def update_buttons(self):
        if self.label:
            self.label.pack_forget()
        if self.button_open:
            self.button_open.pack_forget()
        if self.button_renamed:
            self.button_renamed.pack_forget()
        if self.button_crop:
            self.button_crop.pack_forget()
        if self.button_next:
            self.button_next.pack_forget()

        if self.img:
            self.button_crop = tk.Button(
                self.root, text="Crop and Save", command=self.crop_and_save, bg="lightgreen"
            )
            self.button_crop.pack(side="left", fill="x", expand=True)

            self.button_next = tk.Button(
                self.root, text="Next", command=self.next_image, bg="lightblue"
            )
            self.button_next.pack(side="left", fill="x", expand=True)
        else:
            self.button_open = tk.Button(
                self.root, text="Open Image", command=self.open_image, bg="lightblue"
            )
            self.button_open.pack(side="left", fill="x", expand=True)

            self.button_renamed = tk.Button(
                self.root, text="Start in Renamed", command=self.load_renamed_dir, bg="lightcyan"
            )
            self.button_renamed.pack(side="left", fill="x", expand=True)

    def update_rectangle(self, event):
        if not self.img or not self.rect:
            raise ValueError("Image or rectangle not initialized")

        x, y = event.x, event.y
        x -= self.out_size[0] // 2
        y -= self.out_size[1] // 2

        x = max(3, min(x, self.img.width - self.out_size[0] - 1))
        y = max(3, min(y, self.img.height - self.out_size[1] - 1))

        if not self.mask_applied:
            self.canvas.coords(
                self.rect, x, y, x + self.out_size[0], y + self.out_size[1]
            )

    def get_crop_area(self, x, y):
        if not self.img or not self.rect:
            raise ValueError("Image or rectangle not initialized")

        return ImageTk.PhotoImage(
            self.img.crop((x, y, x + self.out_size[0], y + self.out_size[1]))
        )

    def select_crop(self, event):
        if not self.img or not self.rect:
            raise ValueError("Image or rectangle not initialized")

        if not self.mask_applied:
            self.mask_applied = True
            self.canvas.create_image(0, 0, image=self.img_grey, anchor=tk.NW)
            x, y = self.canvas.coords(self.rect)[:2]
            self.cropped_image = self.get_crop_area(x, y)
            self.canvas.create_image(x, y, image=self.cropped_image, anchor=tk.NW)
        else:
            self.mask_applied = False
            self.display_image()

    def crop_and_save(self):
        if not self.mask_applied or not self.cropped_image:
            raise ValueError("No cropped image to save")

        save_path = os.path.join(config["images"]["unlabeled_path"], self.file_name)
        if not save_path:
            return
        ImageTk.getimage(self.cropped_image).save(save_path)
        print(f"Cropped image saved to {save_path}")
        self.next_image()

    def next_image(self):
        if not self.file_name or not self.img:
            return
        current_dir = os.path.dirname(self.img.filename)
        files = [
            f
            for f in os.listdir(current_dir)
            if f.lower().endswith((".jpg", ".png"))
        ]
        files.sort()
        try:
            idx = files.index(self.file_name)
        except ValueError:
            idx = -1
        next_idx = (idx + 1) % len(files)
        next_file = os.path.join(current_dir, files[next_idx])
        self.img = Image.open(next_file)
        self.file_name = files[next_idx]
        self.img_tk = ImageTk.PhotoImage(self.img)
        enhancer = ImageEnhance.Brightness(self.img)
        self.img_grey = ImageTk.PhotoImage(enhancer.enhance(0.3))
        self.mask_applied = False
        self.cropped_image = None
        self.display_image()


def main():
    root = tk.Tk()
    app = CropperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
