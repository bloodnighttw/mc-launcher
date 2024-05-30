import tkinter as tk
from tkinter import ttk
import os

"""
Settings


Naming Format

self.label_<...> = ttk.Label(self.frame, text="...")
self.label_<...>.grid(...)

self.settings_<...>_values = (...)
self.settings_<...> = ttk.Combobox(
    self.frame, values=self.settings_<...>_values, state="readonly"
)
self.settings_<...>.bind(
    "<<ComboboxSelected>>", self.settings_<...>_event
)
self.settings_<...>.current(self.settings_<...>_values.index(self.main.settings("<...>")))
self.settings_<...>.grid(...)

def settings_<...>_event(self, *args):
    value = self.settings_<...>.get()
    self.main.settings("<...>", value)
    self.main.logging(...)

"""


class Page3(ttk.Frame):
    def __init__(self, main, parent):
        super().__init__()
        self.main = main
        self.parent = parent

        # Main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        """
        Frame 1
        """

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame1.grid_columnconfigure((0, 1), weight=1)

        # Font Style
        self.label_font_style = ttk.Label(self.frame1, text="Font")
        self.label_font_style.grid(row=0, column=0, sticky="nsw")

        self.settings_font_style_values = (
            "Minecraft",
            "MinecraftTen",
            "Arial",
            "Calibri",  # 93
            "Consolas",  # 119
            "Microsoft JhengHei",  # 221
            "Times New Roman",  # 332
        )
        self.settings_font_style = ttk.Combobox(
            self.frame1, values=self.settings_font_style_values, state="readonly"
        )
        self.settings_font_style.bind(
            "<<ComboboxSelected>>", self.settings_font_style_event
        )
        self.settings_font_style.current(
            self.settings_font_style_values.index(self.main.settings("font"))
        )
        self.settings_font_style.grid(row=0, column=1, sticky="nsew")

        # Font Size
        self.label_font_size = ttk.Label(self.frame1, text="Font Size")
        self.label_font_size.grid(row=1, column=0, sticky="nsw")

        self.settings_font_size_values = ("small", "medium", "large")
        self.settings_font_size = ttk.Combobox(
            self.frame1, values=self.settings_font_size_values, state="readonly"
        )
        self.settings_font_size.bind(
            "<<ComboboxSelected>>", self.settings_font_size_event
        )
        self.settings_font_size.current(
            self.settings_font_size_values.index(self.main.settings("font_size"))
        )
        self.settings_font_size.grid(row=1, column=1, sticky="nsew")

        """
        Frame 2
        """
        self.frame2 = ttk.Frame(self)
        self.frame2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.frame2.columnconfigure((0, 1), weight=1)

        # Windows Style Settings
        self.label_windows_style = ttk.Label(self.frame2, text="Windows Style")
        self.label_windows_style.grid(row=1, column=0, sticky="nsw")

        self.settings_windows_style_values = ("black", "arc", "calm", "ubuntu", "vista")
        self.settings_windows_style = ttk.Combobox(
            self.frame2, values=self.settings_windows_style_values, state="readonly"
        )
        self.settings_windows_style.bind(
            "<<ComboboxSelected>>", self.settings_windows_style_event
        )
        self.settings_windows_style.current(
            self.settings_windows_style_values.index(self.main.settings("window_style"))
        )
        self.settings_windows_style.grid(row=1, column=1, sticky="nsew")

        # Windows Size Settings
        self.label_windows_size = ttk.Label(self.frame2, text="Windows Size")
        self.label_windows_size.grid(row=0, column=0, sticky="nsw")

        self.settings_windows_size_values = ("small", "medium", "large", "full")
        self.settings_windows_size = ttk.Combobox(
            self.frame2, values=self.settings_windows_size_values, state="readonly"
        )
        self.settings_windows_size.bind(
            "<<ComboboxSelected>>", self.settings_windows_size_event
        )
        self.settings_windows_size.current(
            self.settings_windows_size_values.index(self.main.settings("window_size"))
        )
        self.settings_windows_size.grid(row=0, column=1, sticky="nsew")

        # Run initialization on widget
        self.settings_windows_size_event()
        self.settings_windows_style_event()
        self.settings_font_size_event()
        self.settings_font_style_event()

    def settings_font_style_event(self, *args):
        value = self.settings_font_style.get()
        self.main.settings("font", value)
        size = self.settings_font_size.get()
        font_sizes = {"small": 8, "medium": 12, "large": 16}
        self.main.style.configure(".", font=(value, font_sizes[size]))
        self.main.logging(f"Settings: changed font to {value}")

    def settings_font_size_event(self, *args):
        value = self.settings_font_size.get()
        self.main.settings("font_size", value)
        style = self.settings_font_style.get()
        font_sizes = {"small": 8, "medium": 12, "large": 16}
        self.main.style.configure(".", font=(style, font_sizes[value]))
        self.main.logging(f"Settings: changed font size to {value}")

    def settings_windows_style_event(self, *args):
        value = self.settings_windows_style.get()
        self.main.settings("window_style", value)
        self.main.style.theme_use(value)
        self.main.logging(f"Settings: changed windows style to {value}")

    def settings_windows_size_event(self, *args):
        value = self.settings_windows_size.get()
        self.main.settings("window_size", value)
        if value == "full":
            self.main.attributes("-fullscreen", True)
            return
        self.main.attributes("-fullscreen", False)
        ratio = {"small": 0.8, "medium": 1, "large": 1.2}
        scale = ratio[value]
        self.main.wm_geometry(
            f"{int(self.main.default_width*scale)}x{int(self.main.default_height*scale)}"
        )
        self.main.logging(f"Settings: changed windows size to {value}")
