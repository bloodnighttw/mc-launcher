import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string


class Page4(ttk.Frame):
    def __init__(self, parent, log_event):
        super().__init__(parent)
        self.log_event = log_event
        self.parent = parent

        # Initialization
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 3), weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.bind("<Control-KeyPress-i>", self.entry_prev)
        self.bind("<Return>", self.keyboard_enter)
        self.buffer_entry = ["", ""]  # Buffer for entry
        self.buffer = []  # Buffer for undo and redo

        # First frame section
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame1.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.label_name = ttk.Label(self.frame1, text="Name:")
        self.label_name.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.label_score = ttk.Label(self.frame1, text="Score:")
        self.label_score.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.str_name = tk.StringVar()
        self.entry_name = ttk.Entry(self.frame1, textvariable=self.str_name)
        self.entry_name.grid(
            row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.str_score = tk.StringVar()
        self.entry_score = ttk.Entry(self.frame1, textvariable=self.str_score)
        self.entry_score.grid(
            row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.button_undo = ttk.Button(self.frame1, text="Undo", command=self.undo)
        self.button_undo["state"] = "disabled"
        self.button_undo.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        self.button_redo = ttk.Button(self.frame1, text="Redo", command=self.redo)
        self.button_redo["state"] = "disabled"
        self.button_redo.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

        self.button_add = ttk.Button(self.frame1, text="Add", command=self.add)
        self.button_add.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.button_add = ttk.Button(self.frame1, text="Search", command=self.search)
        self.button_add.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.button_add = ttk.Button(self.frame1, text="Delete", command=self.delete)
        self.button_add.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        self.button_add = ttk.Button(self.frame1, text="Update", command=self.update)
        self.button_add.grid(row=2, column=3, padx=10, pady=10, sticky="ew")

        # Second frame section
        self.frame2 = ttk.Frame(self)
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.frame2.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.option_sort_name = tk.StringVar()
        self.option_sort = tk.BooleanVar()  # True: ascending
        self.option_show_deleted = tk.BooleanVar()  # True: show deleted items

        self.radio_sort_name = ttk.Radiobutton(
            self.frame2,
            text="Sort by Name",
            variable=self.option_sort_name,
            value="name",
            command=self.showlists,
        )
        self.radio_sort_name.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.radio_sort_score = ttk.Radiobutton(
            self.frame2,
            text="Sort by Score",
            variable=self.option_sort_name,
            value="score",
            command=self.showlists,
        )
        self.radio_sort_score.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.radio_sort_name = ttk.Radiobutton(
            self.frame2,
            text="Ascending",
            variable=self.option_sort,
            value=False,
            command=self.showlists,
        )
        self.radio_sort_name.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.radio_sort_score = ttk.Radiobutton(
            self.frame2,
            text="Descending",
            variable=self.option_sort,
            value=True,
            command=self.showlists,
        )
        self.radio_sort_score.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        self.radio_sort_name = ttk.Checkbutton(
            self.frame2,
            text="Show Deleted",
            variable=self.option_show_deleted,
            command=self.showlists,
        )
        self.radio_sort_name.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

        self.option_sort_name.set("name")
        self.option_sort.set(False)
        self.option_show_deleted.set(False)

        # Third frame section
        self.frame3 = ttk.Frame(self)
        self.frame3.grid(row=2, column=0, sticky="nsew")
        self.frame3.grid_rowconfigure(0, weight=1)
        self.frame3.grid_columnconfigure(0, weight=1)

        self.scrollbar_x = ttk.Scrollbar(self.frame3, orient="horizontal")
        self.scrollbar_x.grid(row=1, column=0, sticky="swe")

        self.scrollbar_y = ttk.Scrollbar(self.frame3, orient="vertical")
        self.scrollbar_y.grid(row=0, column=1, sticky="nse")

        self.lists = []  # Used to store current items
        self.deleted = []  # Used to store deleted items
        self.listbox = tk.Listbox(
            self.frame3,
            xscrollcommand=self.scrollbar_x.set,
            yscrollcommand=self.scrollbar_y.set,
            selectmode="extended",
        )
        self.listbox.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_x.config(command=self.listbox.xview)
        self.scrollbar_y.config(command=self.listbox.yview)

        # Fourth frame section
        self.frame4 = ttk.Frame(self)
        self.frame4.grid(row=3, column=0, sticky="nsew")
        self.frame4.grid_columnconfigure((0, 1), weight=1)

        self.button_generate = ttk.Button(
            self.frame4, text="Generate data", command=self.generate
        )
        self.button_generate.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.label_select = ttk.Label(self.frame4, text="Selected Score:")
        self.label_select.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.scale = ttk.Scale(
            self.frame4, from_=0, to=100, orient="horizontal", command=self.update_scale
        )
        self.scale.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.scale.set(0)

    # When enter is pressed, decide whether to add or update
    def keyboard_enter(self, *args):
        entry_name = self.entry_name.get()
        for i in range(len(self.lists)):
            if self.lists[i][0] == entry_name:
                self.update()
                return
        self.add()

    # Generate 15 random listbox items
    def generate(self):
        for _ in range(15):
            name = "".join(random.choices(string.ascii_letters, k=3))
            score = str(random.randint(0, 100))
            self.str_name.set(name)
            self.str_score.set(score)
            self.add()

    def redo(self):
        for item in self.buffer:
            if item[2] == "add":
                self.lists.append([item[0], item[1]])
            elif item[2] == "delete":
                for i in range(len(self.lists)):
                    if self.lists[i][0] == item[0]:
                        self.lists.pop(i)
                        self.deleted.append([item[0], item[1]])
                        break
            elif item[2] == "update":
                for i in range(len(self.lists)):
                    if self.lists[i][0] == item[0]:
                        self.lists[i][1] = item[1]
                        break

        self.showlists()
        self.button_redo["state"] = tk.DISABLED
        self.button_undo["state"] = tk.NORMAL

    def undo(self):
        for item in self.buffer:
            if item[2] == "add":
                for i in range(len(self.lists)):
                    if self.lists[i][0] == item[0]:
                        self.lists.pop(i)
                        break
            elif item[2] == "delete":
                for i in range(len(self.deleted)):
                    if self.deleted[i][0] == item[0]:
                        self.deleted.pop(i)
                        self.lists.append([item[0], item[1]])
                        break
            elif item[2] == "update":
                for i in range(len(self.lists)):
                    if self.lists[i][0] == item[0]:
                        temp = self.lists[i][1]
                        self.lists[i][1] = item[1]
                        item[1] = temp
                        break

        self.showlists()
        self.button_redo["state"] = tk.NORMAL
        self.button_undo["state"] = tk.DISABLED

    # Use to update entry when CTRL + I is pressed
    def update_entry(self, *args):
        self.buffer_entry = [str(self.str_name.get()), str(self.str_score.get())]
        print(self.buffer_entry)  ##
        self.str_name.set("")
        self.str_score.set("")

    # Use to toggle previous entry
    def entry_prev(self, *args):
        temp = [self.str_name.get(), self.str_score.get()]
        self.str_name.set(self.buffer_entry[0])
        self.str_score.set(self.buffer_entry[1])
        self.buffer_entry = temp

    # Use to update listbox after making changes
    def showlists(self, threshold=0):
        # Sort based on option
        self.lists.sort(
            key=lambda x: x[0] if self.option_sort_name.get() == "name" else int(x[1]),
            reverse=self.option_sort.get(),
        )

        # Add to list box
        self.listbox.delete(0, tk.END)
        for i in range(len(self.lists)):
            if int(self.lists[i][1]) >= threshold:
                self.listbox.insert(tk.END, self.lists[i][0] + " - " + self.lists[i][1])

        # Show deleted items
        if self.option_show_deleted.get():
            self.deleted.sort(
                key=lambda x: x[0] if self.option_sort_name.get() == "name" else x[1],
                reverse=self.option_sort.get(),
            )
            for i in range(len(self.deleted)):
                if int(self.lists[i][1]) >= threshold:
                    self.listbox.insert(
                        tk.END, f"Deleted: {self.deleted[i][0]} - {self.deleted[i][1]}"
                    )

    # Add new item to lists
    def add(self):
        name = self.str_name.get()
        score = self.str_score.get()

        if not score.isdigit():
            messagebox.showerror("Error", "Score must be a digit")
            self.update_entry()
            return
        if int(score) < 0 or int(score) > 100:
            messagebox.showerror("Error", "Score must be between 0 and 100")
            self.update_entry()
            return
        for i in range(len(self.lists)):
            if self.lists[i][0] == name:
                messagebox.showerror("Error", "Name already exists!")
                self.update_entry()
                return
        self.lists.append([name, score])

        # Add to buffer for redo
        self.buffer.clear()
        self.buffer.append([name, score, "add"])
        self.button_undo["state"] = tk.NORMAL

        self.showlists()
        self.update_entry()

    # Search for item from list
    def search(self):
        name = self.entry_name.get()
        for i in range(len(self.lists)):
            if self.lists[i][0] == name:
                messagebox.showinfo(
                    f"Search Result", f"{self.lists[i][0]} - {self.lists[i][1]}"
                )
                return
        messagebox.showinfo("Search Result", f"Name {name} not found!")
        self.update_entry()

    # Delete item from list
    def delete(self):
        # A list to delete multiple items
        names = []

        # Delete from entry
        entry__name = self.str_name.get()
        name_found = False
        if entry__name:
            for i in range(len(self.lists)):
                if self.lists[i][0] == entry__name:
                    names.append(entry__name)
                    name_found = True
                    break
            if not name_found:
                messagebox.showerror("Error", f"Name {entry__name} not found!")

        # Delete from selection
        selected_indiced = self.listbox.curselection()
        for i in selected_indiced:
            name = self.listbox.get(i).split(" - ")[0]
            names.append(name)

        self.buffer.clear()
        # Delete from listbox
        for name in names:
            for i in range(len(self.lists)):
                if self.lists[i][0] == name:
                    self.deleted.append(self.lists[i])

                    # Add to buffer for redo
                    self.buffer.append([name, self.lists[i][1], "delete"])
                    self.lists.pop(i)
                    self.button_undo["state"] = tk.NORMAL
                    break

        self.showlists()
        self.update_entry()

    # Update the score from the list
    def update(self):
        # Update scores with the given name
        name = self.str_name.get()
        score = self.str_score.get()
        old_score = None
        if not score.isdigit():
            messagebox.showerror("Error", "Score must be a digit")
            self.update_entry()
            return
        if int(score) < 0 or int(score) > 100:
            messagebox.showerror("Error", "Score must be between 0 and 100")
            self.update_entry()
            return
        name_found = False
        for i in range(len(self.lists)):
            if self.lists[i][0] == name:
                old_score = self.lists[i][1]
                self.lists[i][1] = score
                name_found = True
                break
        if not name_found:
            messagebox.showerror("Error", f"Name {name} not found!")

        # Add to buffer for redo
        self.buffer.clear()
        if old_score is not None:
            self.buffer.append([name, old_score, "update"])
            self.button_undo["state"] = tk.NORMAL

        self.showlists()
        self.update_entry()

    # Update the scale when the scale has changed
    def update_scale(self, *args):
        threshold = self.scale.get()
        self.label_select["text"] = "Selected Score: " + str(int(threshold))
        self.showlists(threshold)
        pass
