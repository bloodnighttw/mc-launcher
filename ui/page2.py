import tkinter as tk
import os
from tkinter import ttk

'''
Switch Skin
'''

class Page2(ttk.Frame):
    def __init__(self, parent, log_event, skin_preview):
        super().__init__()
        self.parent = parent
        self.log_event = log_event
        self.skin_preview = skin_preview

        # main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.btn = ttk.Button(self, text="Change Skin", command=self.change_skin)
        self.btn.grid(row=0, column=0, sticky="ew")

    def change_skin(self):
        print(os.getcwd())
        self.log_event("Switching skin")
        self.skin_preview("0ac346c7ace6165c.png")
        # self.skin_preview("536761a2ea3c651f.png")
        # test = SkinWin("0ac346c7ace6165c.png")
        # test1 = SkinWin("536761a2ea3c651f.png")