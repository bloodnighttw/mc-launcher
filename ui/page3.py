# Source: https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22

import tkinter as tk
from tkinter import ttk

"""
Settings
"""


class Page3(ttk.Frame):
    def __init__(self, main, parent, log_event):
        super().__init__()
        self.main = main
        self.parent = parent
        self.log_event = log_event

        # main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        """
        Frame 1
        """

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame1.grid_columnconfigure((0, 1), weight=1)

        # Font Settings
        self.label_font = ttk.Label(self.frame1, text="Font")
        self.label_font.grid(row=0, column=0, sticky="nsw")

        self.settings_font_values = (
            "Arial",
            "Times New Roman",
            "Courier New",
            "Verdana",
        )
        self.settings_font = ttk.Combobox(
            self.frame1, values=self.settings_font_values, state="readonly"
        )
        self.settings_font.bind("<<ComboboxSelected>>", self.settings_font_event)
        self.settings_font.current(0)
        self.settings_font.grid(row=0, column=1, sticky="nsew")

        # Font Size
        self.label_font_size = ttk.Label(self.frame1, text="Font Size")
        self.label_font_size.grid(row=1, column=0, sticky="nsw")

        self.settings_font_size_values = ("small", "medium", "large")
        self.settings_font_size = ttk.Combobox(
            self.frame1, values=self.settings_font_size_values, state="readonly"
        )
        self.settings_font_size.bind("<<ComboboxSelected>>", self.settings_font_event)
        self.settings_font_size.current(1)
        self.settings_font_size.grid(row=1, column=1, sticky="nsew")

        """
        Frame 2
        """
        self.frame2 = ttk.Frame(self)
        self.frame2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.frame2.columnconfigure((0, 1), weight=1)

        # Windows Size Settings
        self.label_windows = ttk.Label(self.frame2, text="Windows Size")
        self.label_windows.grid(row=0, column=0, sticky="nsw")

        self.settings_windows_values = ("small", "medium", "large")
        self.settings_windows = ttk.Combobox(
            self.frame2, values=self.settings_windows_values, state="readonly"
        )
        self.settings_windows.bind("<<ComboboxSelected>>", self.settings_windows_event)
        self.settings_windows.current(1)
        self.settings_windows.grid(row=0, column=1, sticky="nsew")

        # Windows Style Settings
        self.label_windows_style = ttk.Label(self.frame2, text="Windows Style")
        self.label_windows_style.grid(row=1, column=0, sticky="nsw")

        self.settings_windows_style_values = ("light", "dark")
        self.settings_windows_style = ttk.Combobox(
            self.frame2, values=self.settings_windows_style_values, state="readonly"
        )
        self.settings_windows_style.bind(
            "<<ComboboxSelected>>", self.settings_windows_event
        )
        self.settings_windows_style.current(0)
        self.settings_windows_style.grid(row=1, column=1, sticky="nsew")

    def settings_font_event(self, *args):
        var = self.settings_font.get()
        self.log_event(f"Settings: changed font to {var}")

    def settings_font_size_event(self, *args):
        var = self.settings_font_size.get()
        self.log_event(f"Settings: changed font size to {var}")

    def settings_windows_event(self, *args):
        var = self.settings_windows.get()
        scale = 0
        if var == "small":
            scale = 0.8
        elif var == "medium":
            scale = 1
        elif var == "large":
            scale = 1.2
        self.main.wm_geometry(
            f"{int(self.main.default_width*scale)}x{int(self.main.default_height*scale)}"
        )
        self.log_event(f"Settings: changed windows size to {var}")

    def settings_windows_style_event(self, *args):
        var = self.settings_windows_style.get()
        self.log_event(f"Settings: changed windows style to {var}")
