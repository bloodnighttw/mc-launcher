# Source: https://stackoverflow.com/questions/71726458/how-to-change-whole-apps-theme-when-used-within-class-tkinter-ttkthemes-them
# Offical Documentation: https://docs.python.org/3/library/tkinter.ttk.html#scrollable-widget-options

# ttk and tk are basically similar, but ttk have extension for themes

"""
Sidebar: Debug Console
Page 1: Main Menu, Switch Version
Page 2: Skins
Page 3: Settings
Page 4: About us, Help, Support

"""

import tkinter as tk
import tkinter.ttk as ttk

from index import all_version
from .sidebar import SideBar
from .page1 import Page1
from .page2 import Page2
from .page3 import Page3
from .page4 import Page4
import json

from .ttkthemes.themed_style import ThemedStyle


class Main(tk.Tk):

    def __init__(self, skin_preview,token, user_profile):
        # Initialization
        super().__init__()
        self.SETTINGS_PATH = "settings.json"
        self.settings_data = {}
        with open(self.SETTINGS_PATH, "r") as file:
            self.settings_data = json.load(file)

        self.skin_preview = skin_preview
        self.style = ThemedStyle()

        # Configure Window
        self.title("Themes")
        self.default_width = 1100
        self.default_height = 580
        self.geometry(f"{self.default_width}x{self.default_height}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Notebook
        self.my_notebook = ttk.Notebook(self)
        self.my_notebook.grid(row=0, column=1, sticky="nsew")

        self.sidebar_frame = SideBar(self)
        self.page1 = Page1(self, self.my_notebook, [i["id"] for i in all_version if i["type"] == "release"],token,user_profile)
        self.page2 = Page2(self, self.my_notebook, user_profile)
        self.page3 = Page3(self, self.my_notebook)
        self.page4 = Page4(self, self.my_notebook)

        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.my_notebook.add(self.page1, text="    Games     ")
        self.my_notebook.add(self.page2, text="    Skin      ")
        self.my_notebook.add(self.page3, text="   Settings   ")
        self.my_notebook.add(self.page4, text="   About Us   ")

        # Root bindings (Press CTRL + E to exit)
        self.bind("<Control-e>", lambda e: self.destroy())

    def logging(self, message):
        # Used for logging, pass one string parameter as message
        self.sidebar_frame.log(message)

    def settings(self, *args):
        """
        Read or write settings.json file.

        First argument: key
        Second argument(optional): value

        Passing key only will return the value;
        passing key and value will set the value.
        """
        if len(args) == 1:
            # with open(self.SETTINGS_PATH, 'r') as file:
            #     self.data = json.load(file)
            return self.settings_data[args[0]]
        elif len(args) == 2:
            # self.data = {args[0]: args[1]}
            self.settings_data[args[0]] = args[1]
            with open(self.SETTINGS_PATH, "w") as file:
                json.dump(self.settings_data, file)
