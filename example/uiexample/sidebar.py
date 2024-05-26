import tkinter as tk
from tkinter import ttk

class SideBar(ttk.Frame):
    def __init__(self, parent, change_scaling_event):
        super().__init__(parent)
        self.change_scaling_event = change_scaling_event
        self.grid_rowconfigure(2, weight=1)

        # Label
        self.logo_label = ttk.Label(self, text="Tkinter Project")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Seperator 
        self.seperator = ttk.Separator(self)
        self.seperator.grid(row=1, column=0, pady=10, sticky="nsew")

        # Logging Text
        self.frame = ttk.Frame(self)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.text = tk.Text(self.frame, wrap="word", width=30)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.text.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.text.config(yscrollcommand=self.scrollbar_y.set)

        # Clear loggging text button
        self.button = ttk.Button(
            self, text="Clear Logging", command=lambda: self.text.delete("1.0", tk.END)
        )
        self.button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Seperator 
        self.seperator = ttk.Separator(self)
        self.seperator.grid(row=4, column=0, pady=10, sticky="nsew")

        # Scaling
        self.scaling_label = ttk.Label(self, text="UI Scaling", anchor="center")
        self.scaling_label.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.options2 = ["80%", "90%", "100%", "110%", "120%"]
        self.selected_scale = tk.StringVar(self)
        self.scaling_optionemenu = ttk.OptionMenu(
            self,
            self.selected_scale,
            *self.options2,
            command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.selected_scale.set(self.options2[2])

    def log(self, message):
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
