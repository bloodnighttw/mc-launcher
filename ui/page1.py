import concurrent
import json
import platform
import subprocess
import tkinter as tk
import urllib
from tkinter import ttk
import threading
import os
from tkinter import Canvas
from PIL import Image, ImageTk
import itertools

from index import all_version, token, user_profile
from minecraft.asset import get_version_info, get_index_list, get_client_url, get_asset_list, \
    get_libraries_download_list
from minecraft.auth import check_minecraft_profile

"""
Main Menu
Switch Version

"""

temp = platform.system()

osname = ""
if temp == "Windows":
    osname = "windows"
elif temp == "Darwin":
    osname = "osx"
elif temp == "Linux":
    osname = "linux"


class Page1(ttk.Frame):
    def __init__(self, main, parent, version_list,token, user_profile):
        super().__init__()
        self.main = main
        self.parent = parent
        self.token = token
        self.user_profile = user_profile

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
        self.switch_version = ttk.Combobox(self.frame2, values=version_list)
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
        self.progressbar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10)
        self.progressbar.grid_remove()  # Hide progressbar

    def download(self, i, count=0, total=1):
        self.progressbar['value'] = (count / total) * 100
        if not os.path.exists(os.path.dirname(f"temp/{i['path']}")):
            os.makedirs(os.path.dirname(f"temp/{i['path']}"))
        elif os.path.exists(f"temp/{i['path']}"):
            return
        self.main.logging(f"Download {i['url']} to temp/{i['path']}")
        urllib.request.urlretrieve(i["url"], f"temp/{i['path']}")

    def button_start_event(self, *args):
        self.main.logging("Launching Minecraft...")
        threading.Thread(target=self.launch_minecraft).start()

    def launch_minecraft(self, *args):
        self.progressbar.grid()  # Show progressbar

        self.progressbar['value'], self.progress_label["text"] = 0, "Loading Version Info..."
        value = self.switch_version.get()
        version_simple_info = None
        for i in all_version:
            if i["id"] == value:
                version_simple_info = i
                break

        version_detail_info = get_version_info(version_simple_info)
        b = get_libraries_download_list(version_detail_info)
        indexes = get_index_list(version_detail_info)
        if not os.path.exists("temp/assets/indexes"):
            os.makedirs("temp/assets/indexes")
        with open(f"temp/assets/indexes/{version_detail_info['assetIndex']['id']}.json", "w") as f:
            f.write(json.dumps(indexes))
        c = get_asset_list(indexes)
        client_url = get_client_url(version_simple_info)

        self.progress_label['text'] = "Downloading Libraries and assets..."

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=11) as executor:  # Download multiple files is io bound, we can use ThreadPoolExecutor to speed up the download speed
            total = len(b) + len(c)
            for count, i in enumerate(b):
                executor.submit(self.download, i, count, total)
            for count, i in enumerate(c):
                executor.submit(self.download, i, len(b) + count, total)

        urllib.request.urlretrieve(client_url, f"temp/{value}.jar")

        div = (os == "windows" and ";" or ":")
        classpath = ""
        for i in b:
            classpath += f"temp/{i['path']}{div}"
        classpath += f"temp/{value}.jar"
        native = "temp/libraries"
        asset = "temp/assets/"



        command = [
            "java",  # Java
            f"-Djava.library.path={native}",
            f"-cp",
            classpath,
            "net.minecraft.client.main.Main",
            "--accessToken",
            self.token,
            "--version",
            version_simple_info['id'],
            "--assetsDir",
            asset,
            "--assetIndex",
            version_detail_info['assetIndex']['id'],
            "--username",
            self.user_profile["name"],
            "--userType",
            "msa",
            "--uuid",
            self.user_profile["id"],
            "--gameDir",
            "temp",
        ]

        self.progress_label['text'] = "Launching Minecraft..."
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                shell=osname == "windows")  # because windows is not posix
        while True:
            line = proc.stdout.readline().decode("utf-8")
            if not line:
                break
            self.main.logging(line)
        self.progress_label['text'] = "Done!"

    def settings_switch_version_event(self, *args):
        value = self.switch_version.get()
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
