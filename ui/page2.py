import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import os

'''
Switch Skin
'''

class Page2(ttk.Frame):
    def __init__(self, main, parent):

        # Initialization
        super().__init__()
        self.main = main
        self.parent = parent
        self.skin_path = main.settings('skin_path')

        # Main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame 1
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        # 自己用

        # Frame 2
        self.frame2 = ttk.Frame(self)
        self.frame2.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.frame2.columnconfigure(0, weight=1)

        self.label_skin = ttk.Label(self.frame2, text=f"Skin: {self.skin_path} ")
        self.label_skin.grid(row=0, column=0, sticky="ew")
        # self.label_skin.configure(background="red")

        self.button_skin = ttk.Button(self.frame2, text="Choose Other Skin", command=self.event_skin)
        self.button_skin.grid(row=0, column=1, sticky="ew", padx=10)

        self.button_skin_preview = ttk.Button(self.frame2, text="Preview Skin", command=self.event_skin_preview)
        self.button_skin_preview.grid(row=0, column=2, sticky="ew", padx=10)

    def event_skin_preview(self):
        self.main.skin_preview(self.skin_path)

    def event_skin(self):
        self.new_skin_path = filedialog.askopenfilename(initialdir="skin/skins")
        if self.new_skin_path:
            self.new_skin_path = os.path.basename(self.new_skin_path)
            self.main.settings('skin_path', self.new_skin_path)
            self.skin_path = self.new_skin_path
            self.main.logging(f"Skin changed to {self.new_skin_path}")
            self.label_skin.configure(text=f"Skin: {self.skin_path} ")