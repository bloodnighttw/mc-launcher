# Source: https://stackoverflow.com/questions/71726458/how-to-change-whole-apps-theme-when-used-within-class-tkinter-ttkthemes-them
# Offical Documentation: https://docs.python.org/3/library/tkinter.ttk.html#scrollable-widget-options

# ttk and tk are basically similar, but ttk have extension for themes

# Todo: Alarm, Messagebox, Canvas
# Main: Menu, Notebook, Style, Frame, Bindings, Themes
# Sidebar: Debug information, Text
# Page 1: Widgets - Button, Entry, Variable, Radiobutton, Checkbox,
# Optionmenu, Combobox, Progressbar, Scale, Spinbox, Listbox, Scrollbar
# Page 2: Label - anchor, cursor, bitmap, LabelFrame
# Page 3: Layout - pack (side, fill, expand), grid (row, col)
# Page 4: Midterm
# Page 5: Toplevel, Treeview

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font
from ttkthemes import ThemedStyle
from .sidebar import SideBar
from .page1 import Page1
from .page2 import Page2
from .page3 import Page3
from .page4 import Page4
from .page5 import Page5

class ThemedApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # Configure Window
        self.title("Themes")
        self.default_width = 1100
        self.default_height = 580
        self.geometry(f"{self.default_width}x{self.default_height}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Configure Layout and Notebook
        self.my_notebook = ttk.Notebook(self)
        self.my_notebook.grid(row=0, column=1, sticky="nsew")

        self.sidebar_frame = SideBar(self, change_scaling_event=self.change_scaling)
        self.page1 = Page1(self.my_notebook, log_event=self.logging)
        self.page2 = Page2(self.my_notebook, log_event=self.logging)
        self.page3 = Page3(self.my_notebook, log_event=self.logging)
        self.page4 = Page4(self.my_notebook, log_event=self.logging)
        self.page5 = Page5(self.my_notebook, log_event=self.logging)

        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.my_notebook.add(self.page1, text="Page 1")
        self.my_notebook.add(self.page2, text="Page 2")
        self.my_notebook.add(self.page3, text="Page 3")
        self.my_notebook.add(self.page4, text="Page 4")
        self.my_notebook.add(self.page5, text="Page 5")

        # Configure Menu
        self.my_menu = tk.Menu(self)
        self.config(menu=self.my_menu)

        self.menu_style = tk.Menu(self.my_menu)
        self.my_menu.add_cascade(label="Style", menu=self.menu_style)
        self.style = ThemedStyle()
        for item in sorted(self.style.get_themes()):
            self.menu_style.add_command(
                label=item, command=lambda name=item: self.change_theme(name)
            )

        # Menu first
        self.menu_first = tk.Menu(self.my_menu)
        # Underline does not work on windows
        self.my_menu.add_cascade(label="Menu 1", menu=self.menu_first, underline=0)
        self.menu_first.add_command(label="Label A", underline=6)
        self.menu_first.add_command(label="Label B", underline=6)

        self.submenu = tk.Menu(self.menu_first, tearoff=False)
        self.menu_first.add_cascade(label="Submenu", menu=self.submenu)
        self.submenu.add_command(label="Submenu A", underline=6)
        self.submenu.add_command(label="Submenu B", underline=6)

        self.cb_menu = tk.BooleanVar()
        self.cb_menu.set(True)
        self.menu_first.add_checkbutton(label="Check", variable=self.cb_menu)
        self.menu_first.add_separator()
        self.menu_first.add_command(label="Close", command=self.destroy, underline=0)

        # Menu second
        self.menu_second = tk.Menu(self.my_menu)
        self.my_menu.add_cascade(label="Menu 2", menu=self.menu_second)
        self.families = list(tk_font.families())
        self.families.sort()
        for i, family in enumerate(self.families):
            self.menu_second.add_command(
                label=family + str(i), command=lambda i=i: self.change_font(i)
            )

        # Menu Popup
        self.popupmenu = tk.Menu(self, tearoff=False)
        self.popupmenu.add_command(label="Minimize", command=self.minimizeIcon)
        self.popupmenu.add_command(label="Exit", command=self.destroy)
        self.bind("<Button-3>", self.showPopupMenu)  # Right click

        # Root bindings (Press CTRL + E to exit)
        self.bind("<Control-e>", lambda e: self.destroy())

    def change_theme(self, name):
        self.style.theme_use(name)
        self.logging(f"Changed to theme: {name}")

    def change_scaling(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        self.wm_geometry(
            f"{int(self.default_width*new_scaling_float)}x{int(self.default_height*new_scaling_float)}"
        )
        self.logging(f"Changed to scale: {new_scaling}")

    def logging(self, message):
        self.sidebar_frame.log(message)

    def change_font(self, code):
        print(code)
        print(self.families[code])
        fonts = tk_font.Font(family=self.families[code], size=12)
        self.sidebar_frame.text.configure(font=fonts)

    def minimizeIcon(self):
        self.iconify()

    def showPopupMenu(self, event):
        self.popupmenu.post(event.x_root, event.y_root)
