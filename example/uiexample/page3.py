# Source: https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22

import tkinter as tk
from tkinter import ttk


class Page3(ttk.Frame):
    def __init__(self, parent, log_event):
        self.parent = parent
        super().__init__()

        # main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        # layout manager using pack
        self.frame_layout_normal = tk.LabelFrame(self, text="pack")
        self.frame_layout_normal.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.label1 = tk.Label(
            self.frame_layout_normal, text="label1 (bottom, fill='x')", bg="lightblue"
        )
        self.label2 = tk.Label(
            self.frame_layout_normal, text="label2 (right, fill='y')", bg="lightgreen"
        )
        self.label3 = tk.Label(
            self.frame_layout_normal,
            text="label3 (right, expand=True)",
            bg="lightyellow",
        )
        self.label4 = tk.Label(
            self.frame_layout_normal, text="label4 (place)", bg="lightgray"
        )
        self.label1.pack(side="bottom", fill="x")
        self.label2.pack(side="right", fill="y")
        self.label3.pack(side="right", expand=True)
        self.label4.place(relx=0.5, y=30, width=100, height=30)

        # Layout manager using grid
        self.frame_layout_grid = tk.LabelFrame(self, text="grid")
        self.frame_layout_grid.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_layout_grid.grid_rowconfigure((0, 1), weight=1)
        self.frame_layout_grid.grid_rowconfigure((0, 1, 2), weight=1)

        self.labelA = tk.Label(
            self.frame_layout_grid, text="labelA, (0,1,ew)", bg="lightblue"
        )
        self.labelB = tk.Label(
            self.frame_layout_grid, text="labelB, (0,0,nw)", bg="lightgreen"
        )
        self.labelC = tk.Label(
            self.frame_layout_grid,
            text="labelC, (1,0,colspan=2,nsew)",
            bg="lightyellow",
        )
        self.labelD = tk.Label(
            self.frame_layout_grid, text="labelD, place", bg="lightgray"
        )

        self.labelA.grid(row=0, column=1, sticky="ew")
        self.labelB.grid(row=0, column=0, stick="nw")
        self.labelC.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.labelD.place(x=10, rely=0.5, width=100, height=30)

       
