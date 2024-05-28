import tkinter as tk
from tkinter import ttk

'''
Main Menu
Switch Version
'''

class Page1(ttk.Frame):
    def __init__(self,  main, parent):
        super().__init__(parent)
        self.main = main
        self.parent = parent

        
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1, 2), weight=0)

        # Listbox, Scrollbar
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 0))
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(
            self.frame1,
            selectmode="extended"  # selectmode=multiple
        )
        self.listbox.bind("<<ListboxSelect>>", self.listbox_event)
        for i in range(100):
            self.listbox.insert(tk.END, "*" * i)
        self.listbox.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_x = ttk.Scrollbar(
            self.frame1, orient="horizontal", command=self.listbox.xview
        )
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.scrollbar_y = ttk.Scrollbar(
            self.frame1, orient="vertical", command=self.listbox.yview
        )
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.listbox.config(yscrollcommand=self.scrollbar_y.set)
        self.listbox.config(xscrollcommand=self.scrollbar_x.set)

        # Optionmenu, Combobox, Spinbox
        self.frame2 = ttk.Frame(self, width=250)
        self.frame2.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.frame2.grid_rowconfigure((0, 1, 2), weight=1)

        self.optionmenu_values = ["Value 1", "Value 2", "Value 3"]
        self.optionmenu_variable = tk.StringVar(self)
        self.optionmenu = ttk.OptionMenu(
            self.frame2,
            self.optionmenu_variable,
            *self.optionmenu_values,
            command=self.optionmenu_event,
        )
        self.optionmenu.grid(row=0, padx=20, pady=(10, 5), sticky="ew")

        self.combobox_values = ["Value 1", "Value 2", "Value Long Long Long"]
        self.combobox_variable = tk.StringVar(self)
        self.combobox = ttk.Combobox(
            self.frame2,
            values=self.combobox_values,
            textvariable=self.combobox_variable,
        )
        self.combobox.bind("<<ComboboxSelected>>", self.combobox_event)
        self.combobox.current(0)
        self.combobox.grid(row=1, padx=20, pady=5, sticky="ew")

        self.spinbox = ttk.Spinbox(
            self.frame2, from_=0, to=10
        )
        self.spinbox.set(6)
        self.spinbox.bind("<FocusOut>", self.spinbox_event)
        self.spinbox.grid(row=2, padx=20, pady=5, sticky="ew")

        # Button, Entry, Variable, Radiobutton, Checkbox
        self.frame3 = ttk.Frame(self, width=250)
        self.frame3.grid(
            row=0, column=2, rowspan=2, padx=20, pady=(20, 0), sticky="nsew"
        )
        self.frame3.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.button = ttk.Button(self.frame3, text="Button", command=self.button_event)
        self.button.grid(row=0, padx=20, pady=(20, 10), sticky="ew")

        self.button_disabled = ttk.Button(
            self.frame3, text="Disabled Button", state="disabled"
        )
        self.button_disabled.grid(row=1, padx=20, pady=10, sticky="ew")

        self.entry = ttk.Entry(self.frame3)
        self.entry.grid(row=2, padx=20, pady=10, sticky="ew")

        self.radio_var = tk.IntVar(value=0)
        self.radiobutton = ttk.Radiobutton(
            self.frame3,
            variable=self.radio_var,
            value=0,
            text="Radio Button 1",
            command=self.radiobutton_event,
        )
        self.radiobutton.grid(row=3, pady=10, padx=20, sticky="ew")
        self.radio_button_2 = ttk.Radiobutton(
            self.frame3,
            variable=self.radio_var,
            value=1,
            text="Radio Button 2",
            command=self.radiobutton_event,
        )
        self.radio_button_2.grid(row=4, pady=10, padx=20, sticky="ew")
        self.radio_button_3 = ttk.Radiobutton(
            self.frame3,
            variable=self.radio_var,
            value=2,
            text="Radio Button 3",
            command=self.radiobutton_event,
        )
        self.radio_button_3.grid(row=5, pady=10, padx=20, sticky="ew")

        self.checkbox_1 = ttk.Checkbutton(
            self.frame3, text="Checkbox 1", command=self.checkbox_event_1
        )
        self.checkbox_1.grid(row=6, pady=10, padx=20, sticky="ew")
        self.checkbox_2 = ttk.Checkbutton(
            self.frame3, text="Checkbox 2", command=self.checkbox_event_2
        )
        self.checkbox_2.grid(row=7, pady=10, padx=20, sticky="ew")
        self.checkbox_3 = ttk.Checkbutton(
            self.frame3, text="Checkbox 3", command=self.checkbox_event_3
        )
        self.checkbox_3.grid(row=8, pady=(10, 20), padx=20, sticky="ew")
        self.checkbox_1.state(["selected"])

        # Progressbar, Scale
        self.frame4 = ttk.Frame(self)
        self.frame4.grid(
            row=1, column=0, columnspan=2, padx=(20, 0), pady=20, sticky="sew"
        )
        self.frame4.grid_columnconfigure((0, 2), weight=0)
        self.frame4.grid_columnconfigure(1, weight=1)

        self.label_progressbar_1 = ttk.Label(self.frame4, text="Progressbar")
        self.label_progressbar_1.grid(
            row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nw"
        )
        self.progressbar_1 = ttk.Progressbar(self.frame4)
        self.progressbar_1.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.label_scale = ttk.Label(self.frame4, text="Scale")
        self.label_scale.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nw")
        self.scale = ttk.Scale(
            self.frame4, from_=0, to=100, orient="horizontal", command=self.scale_event
        )
        self.scale.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.label_progressbar_2 = ttk.Label(
            self.frame4, text="Adjust Spinbox"
        )
        self.label_progressbar_2.grid(
            row=2, column=0, padx=(20, 10), pady=(10, 0), sticky="nw"
        )
        self.progressbar_2 = ttk.Progressbar(self.frame4)
        self.progressbar_2.grid(row=2, column=1, padx=10, pady=(10, 20), sticky="ew")

        self.progressbar_3 = ttk.Progressbar(self.frame4, mode="indeterminate", orient="vertical", value=70)
        self.progressbar_3.grid(
            row=0, column=2, rowspan=3, padx=(10, 20), pady=20, sticky="ns"
        )
        self.progressbar_3.start()

        self.progress_value = 0
        self.progress_id = None
        self.update_progress()

    def listbox_event(self, *args):
        indexes = self.listbox.get(self.listbox.curselection())
        var = ""
        for i in indexes:
            var += f"{i}, "
        self.main.logging(f"Listbox chosen {var}")

    def optionmenu_event(self, *args):
        var = self.optionmenu_variable.get()
        print(var, args, *args)  # Debugging info
        self.main.logging(f"Optionmenu chosen {var}")

    def combobox_event(self, *args):
        var = self.combobox.get()
        self.main.logging(f"Combobox chosen {var}")

    def spinbox_event(self, *args):
        var = self.spinbox.get()
        self.main.logging(f"Spinbox changed to {var}")
        if self.progress_value < 100:
            interval = int(self.spinbox.get()) 
            self.after_cancel(self.progress_id)  # Cancel previous after() call
            self.after(interval, self.update_progress)  # Restart progress with new speed  

    def button_event(self):
        self.main.logging("Button Clicked")

    def radiobutton_event(self, *args):
        var = self.radio_var.get()
        self.main.logging(f"Radiobutton chosen {var}")

    def checkbox_event_1(self, *args):
        var = self.checkbox_1.instate(["selected"])
        self.main.logging(f"Checkbox1 chosen {var}")

    def checkbox_event_2(self, *args):
        var = self.checkbox_2.instate(["selected"])
        self.main.logging(f"Checkbox2 chosen {var}")

    def checkbox_event_3(self, *args):
        var = self.checkbox_3.instate(["selected"])
        self.main.logging(f"Checkbox3 chosen {var}")

    def scale_event(self, *args):
        var = self.scale.get()
        self.progressbar_1["value"] = var

    def update_progress(self, *args):
        self.progress_value += 1
        self.progressbar_2["value"] = self.progress_value
        if self.progress_value < 100:
            interval = int(self.spinbox.get())
            self.after(interval, self.update_progress)
        else:
            self.progress_value = 0
            self.progressbar_2["value"] = 0
            interval = int(self.spinbox.get())
            self.after(interval, self.update_progress)   