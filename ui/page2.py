import tkinter as tk
from tkinter import ttk

'''
Switch Skin
'''

class Page2(ttk.Frame):
    def __init__(self, parent, log_event):
        self.parent = parent
        super().__init__()

        # main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # show cursors
        self.frame_cursor = tk.LabelFrame(self, text="Cursors")
        self.frame_cursor.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        cursorList = [
            "arrow",
            "double_arrow",
            "man",
            "sizing",
            "based_arrow_down",
            "draft_large",
            "middlebutton",
            "spider",
            "based_arrow_up",
            "draft_small",
            "mouse",
            "spraycan",
            "boat",
            "draped_box",
            "pencil",
            "star",
            "bogosity",
            "exchange",
            "pirate",
            "target",
            "bottom_left_corner",
            "fleur",
            "plus",
            "tcross",
            "bottom_right_corner",
            "gobbler",
            "question_arrow",
            "top_left_arrow",
            "bottom_side",
            "gumby",
            "right_ptr",
            "top_left_corner",
            "bottom_tee",
            "hand1",
            "right_side",
            "top_right_corner",
            "box_spiral",
            "hand2",
            "right_tee",
            "top_side",
            "center_ptr",
            "heart",
            "rightbutton",
            "top_tee",
            "circle",
            "icon",
            "rtl_logo",
            "trek",
            "clock",
            "iron_cross",
            "sailboat",
            "ul_angle",
            "coffee_mug",
            "left_ptr",
            "sb_down_arrow",
            "umbrella",
            "cross",
            "left_side",
            "sb_h_double_arrow",
            "ur_angle",
            "cross_reverse",
            "left_tee",
            "sb_left_arrow",
            "watch",
            "crosshair",
            "leftbutton",
            "sb_right_arrow",
            "xterm",
            "diamond_cross",
            "ll_angle",
            "sb_up_arrow",
            "X_cursor",
            "dot",
            "lr_angle",
            "sb_v_double_arrow",
            "dotbox",
            "shuttle",
        ]

        for i, cursor in enumerate(cursorList):
            self.frame_cursor.rowconfigure(i // 7, weight=1)
            self.frame_cursor.columnconfigure(i % 7, weight=1)
            ttk.Label(
                self.frame_cursor, text=cursor, cursor=cursor, relief="raised"
            ).grid(row=i // 7, column=i % 7, sticky="nsew", padx=5, pady=5)

        # show labels and bitmaps
        self.frame_label = tk.LabelFrame(self, text="Labels and bitmaps")
        self.frame_label.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.label = tk.Label(
            self.frame_label,
            text="This is a Tkinter Label",
            bg="black",
            fg="white",
            width=200,
        )
        self.label["wraplength"] = 100
        self.label["bitmap"] = "info"
        self.label["compound"] = "left"  # Sets the bitmap to left
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.bitmap = [
            "error",
            "hourglass",
            "info",
            "questhead",
            "question",
            "warning",
            "gray12",
            "gray25",
            "gray50",
            "gray75",
        ]
        for i, bit in enumerate(self.bitmap):
            tk.Label(self.frame_label, text=bit, bitmap=bit).grid(
                row=i + 1, column=0, padx=5, pady=5
            )  # The bitmap are packed in sequence
