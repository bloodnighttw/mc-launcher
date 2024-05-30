import tkinter as tk
from tkinter import ttk
import threading
import time
from tkinter import Canvas
from PIL import Image, ImageTk
import itertools
import os

"""
Main Menu
Switch Version

"""


class Page1(ttk.Frame):
    def __init__(self, main, parent):
        super().__init__()
        self.main = main
        self.parent = parent

        # Main Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        self.img_slider = ImageSlider(self.frame1)
        self.img_slider.canvas.grid(row=0, column=0, sticky="nsew")

        # Layout 2
        self.frame2 = ttk.Frame(self)
        self.frame2.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frame2.grid_rowconfigure((0, 1, 2), weight=1)
        self.frame2.grid_columnconfigure(0, weight=1)

        # HongWei:

        # self.settings_switch_version_values = (...)
        self.switch_version = ttk.Combobox(self.frame2, values=["1.16.5", "1.17.1"])
        self.switch_version.grid(row=0, column=0, sticky="ew")

        self.button_start = ttk.Button(
            self.frame2, text="Launch", command=self.button_start_event
        )
        self.switch_version.bind(
            "<<ComboboxSelected>>", self.settings_switch_version_event
        )
        # self.settings_switch_version.current(self.settings_switch_version_values.index(self.main.settings("switch_version")))
        self.button_start.grid(row=0, column=1, sticky="ew", padx=10)

        self.progress_label = ttk.Label(self.frame2, text="Welcome Back")
        self.progress_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.progressbar = ttk.Progressbar(self.frame2, value=0)
        self.progressbar.grid(row=2, column=0, columnspan=2, sticky="ew" , padx=10)
        self.progressbar.grid_remove() # Hide progressbar

    def button_start_event(self, *args):
        self.logging("Launching Minecraft...")
        threading.Thread(target=self.launch_minecraft).start()

    def launch_minecraft(self, *args):
        self.progressbar.grid() # Show progressbar
        checkpoints = [
            ("Initializing...", 20),
            ("Loading modules...", 40),
            ("Connecting to database...", 60),
            ("Fetching data...", 80),
            ("Finalizing...", 100)
        ]

        # Progressbar Simulating
        for message, progress in checkpoints:
            time.sleep(1)
            self.progressbar['value'] = progress
            self.progress_label['text'] = message

        self.progress_label['text'] = "Load Complete"

    def settings_switch_version_event(self, *args):
        value = self.settings_switch_version.get()
        # self.main.settings("switch_version", value)
        self.main.logging("Switch to version ...")


# Canvas

class ImageSlider:
    def __init__(self, main):
        self.image_paths = [os.path.join("ui/img", path) for path in os.listdir("ui/img")]
        self.main = main

        self.canvas = Canvas(main)

        self.images = [Image.open(img_path) for img_path in self.image_paths]
        self.image_index = 0
        self.current_image_tk = None
        self.current_image_id = None

        self.main.bind('<Configure>', self.resize_canvas)

        self.main.after(2000, self.slide_images)

    def resize_canvas(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.update_image()

    def update_image(self):
        image = self.images[self.image_index]
        resized_image = self.resize_image(image, self.canvas_width, self.canvas_height)
        self.current_image_tk = ImageTk.PhotoImage(resized_image)
        
        if self.current_image_id:
            self.canvas.delete(self.current_image_id)

        self.current_image_id = self.canvas.create_image(
            self.canvas_width // 2, self.canvas_height // 2, image=self.current_image_tk
        )

    def resize_image(self, image, canvas_width, canvas_height):
        img_width, img_height = image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))
        return image.resize(new_size)

    def slide_images(self):
        next_image_index = (self.image_index + 1) % len(self.images)
        self.animate_image(self.images[next_image_index])
        self.image_index = next_image_index
        self.main.after(4000, self.slide_images)

    def animate_image(self, next_image):
        next_image_tk = ImageTk.PhotoImage(self.resize_image(next_image, self.canvas_width, self.canvas_height))
        
        for offset in itertools.chain(range(0, self.canvas_width + 1, 20)):
            self.canvas.move(self.current_image_id, -20, 0)
            new_image_id = self.canvas.create_image(
                self.canvas_width - offset, self.canvas_height // 2, image=next_image_tk
            )
            self.main.update()
            self.canvas.delete(new_image_id)
        
        self.canvas.delete(self.current_image_id)
        self.current_image_id = self.canvas.create_image(
            self.canvas_width // 2, self.canvas_height // 2, image=next_image_tk
        )
        self.current_image_tk = next_image_tk
