import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math


class TopLevelWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x100")
        self.title("Toplevel Window")
        self.label = tk.Label(self, text="This is a poweerful toplevel window").pack(
            expand=True
        )
        self.button = ttk.Button(self, text="Close", command=self.destroy).pack(
            expand=True
        )


class Ball:
    def __init__(self, canvas, x, y, dx, dy):
        self.canvas = canvas
        self.id = canvas.create_oval(x * 0.1, y * 0.0, x * 0.2, y * 0.1, fill="red")
        self.dx = dx
        self.dy = dy

    def move(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        if x1 + self.dx < 0 or x2 + self.dx > self.canvas.winfo_width():
            self.dx *= -1
        if y1 + self.dy < 0 or y2 + self.dy > self.canvas.winfo_height():
            self.dy *= -1
        self.canvas.move(self.id, self.dx, self.dy)
        self.canvas.after(50, self.move)


class Page5(ttk.Frame):
    def __init__(self, parent, log_event):
        super().__init__(parent)
        self.log_event = log_event
        self.parent = parent

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Treeview
        # Add attributes show="tree" to hide the heading row,
        # show="headings" to hide the heading column
        self.tree = ttk.Treeview(self)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree["columns"] = ("one", "two")

        self.tree.heading("#0", text="State", anchor="w")
        self.tree.heading("one", text="City", anchor="w")
        self.tree.heading("two", text="Road", anchor="w")

        self.tree.column("#0", width=100, minwidth=100, stretch=True, anchor="w")
        self.tree.column("#1", width=100, minwidth=100, stretch=True, anchor="w")
        self.tree.column("one", width=100, minwidth=100, stretch=True, anchor="w")
        self.tree.column("two", width=100, minwidth=100, stretch=True, anchor="w")

        tw = self.tree.insert("", index=tk.END, text="Taiwan")
        my = self.tree.insert("", index=tk.END, text="Malaysia")

        self.tree.insert(
            tw,
            index=tk.END,
            text="Taipei",
            values=("Shilin", "Night Market"),
            tags="tag1",
        )
        self.tree.insert(tw, index=tk.END, text="Taichung", values=("Central", "TRA"))
        self.tree.insert(
            tw, index=tk.END, text="Kaohsiung", values="Xinzuoying", tags="tag1"
        )

        self.tree.insert(
            my,
            index=tk.END,
            text="Kuala Lumpur",
            values=("Bukit Bintang", "Jalan Alor"),
        )
        self.tree.insert(
            my,
            index=tk.END,
            text="Selangor",
            values=("Puchong", "Jalan Wawasan"),
            tags="tag1",
        )

        self.tree.tag_configure("tag1", background="lightblue")
        self.log_event("All items in treeview: " + str(self.tree.get_children()))
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=1, column=0, sticky="nsew")
        self.frame1.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame1.grid_rowconfigure(0, weight=1)

        self.button_info = ttk.Button(self.frame1, text="Info", command=self.show_info)
        self.button_info.grid(row=1, column=0, sticky="nsew")

        self.button_delete = ttk.Button(self.frame1, text="Delete", command=self.delete)
        self.button_delete.grid(row=1, column=1, sticky="nsew")

        self.button_run = ttk.Button(self.frame1, text="Run", command=self.run)
        self.button_run.grid(row=1, column=2, sticky="nsew")

        # Top level window
        self.button_top = ttk.Button(
            self.frame1, text="Top Level", command=self.open_window
        )
        self.button_top.grid(row=1, column=3, sticky="nsew")

        # Canvas
        self.frame2 = ttk.Frame(self)
        self.frame2.grid(row=2, column=0, sticky="nsew")
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.canvas = tk.Canvas(self.frame2)
        self.canvas.grid(row=0, column=0, rowspan=6, sticky="nsew")

        self.button1 = ttk.Button(self.frame2, text="Line Styles", command=self.event1)
        self.button1.grid(row=0, column=1, sticky="nsew")

        self.button2 = ttk.Button(self.frame2, text="Geometry", command=self.event2)
        self.button2.grid(row=1, column=1, sticky="nsew")

        self.button3 = ttk.Button(self.frame2, text="Stipple", command=self.event3)
        self.button3.grid(row=2, column=1, sticky="nsew")

        self.button4 = ttk.Button(self.frame2, text="Shapes", command=self.event4)
        self.button4.grid(row=3, column=1, sticky="nsew")

        self.button5 = ttk.Button(self.frame2, text="Drawing", command=self.event5)
        self.button5.grid(row=4, column=1, sticky="nsew")

        self.button6 = ttk.Button(self.frame2, text="Fragments", command=self.event6)
        self.button6.grid(row=5, column=1, sticky="nsew")

    def open_window(self):
        window = TopLevelWindow(self)
        # To make sure only one top level window is open at a time
        window.grab_set()

    def on_tree_select(self, event):
        selected_iid = self.tree.selection()[0]
        text = self.tree.item(selected_iid, "text")
        self.log_event("Selected item: " + str(text))

    def show_info(self):
        selected_iid = self.tree.selection()
        text = ""
        for iid in selected_iid:
            text += str(self.tree.item(iid))
        messagebox.showinfo("Item Info: ", text)

    def delete(self):
        selected_iid = self.tree.selection()
        for iid in selected_iid:
            self.tree.delete(iid)

    def run(self):
        last = len(self.tree.get_children()[0])
        first = self.tree.get_children()[0]
        self.tree.move(first, "", last - 1)

    def event1(self):
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        x1 = width / 10
        x2 = width - x1
        y1 = height / 10
        y2 = height - y1
        x = (x2 - x1) / 5
        y = (y2 - y1) / 4

        self.canvas.create_line(x1, y1, x1, y2)
        self.canvas.create_line(x2, y1, x2, y2)

        caps = ["round", "projecting", "butt"]
        joins = ["round", "bevel", "miter"]
        for i in range(3):
            self.canvas.create_line(
                x1, y1 + i * y, x2, y1 + i * y, width=8, capstyle=caps[i]
            )
            self.canvas.create_line(
                x1 + 2 * x * i,
                y1 + 3 * y,
                x1 + 2 * x * i + x,
                y1 + 3 * y,
                x1 + 2 * x * i,
                y1 + 4 * y,
                width=8,
                joinstyle=joins[i],
            )

    def event2(self):
        self.canvas.delete("all")
        width = 320
        height = 240
        x_center, y_center, r = width / 2, height / 2, 100
        x, y = [], []

        for i in range(12):
            x.append(x_center + r * math.cos(30 * i * math.pi / 180))
            y.append(y_center + r * math.sin(30 * i * math.pi / 180))

        for i in range(12):
            for j in range(12):
                self.canvas.create_line(x[i], y[i], x[j], y[j])

    def event3(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        self.canvas.create_line(0, 50, width, 50, width=40, stipple="gray25")
        self.canvas.create_line(0, 100, width, 100, width=40, stipple="questhead")
        self.canvas.create_line(0, 150, width, 150, width=40, stipple="info")

    def event4(self):
        self.canvas.delete("all")
        x = self.canvas.winfo_width()
        y = self.canvas.winfo_height()
        self.canvas.create_rectangle(
            x * 0.1, y * 0.1, x * 0.3, y * 0.2, fill="lightblue"
        )
        self.canvas.create_arc(
            x * 0.4, y * 0.1, x * 0.5, y * 0.2, extent=180, style=tk.ARC
        )
        self.canvas.create_arc(
            x * 0.6, y * 0.1, x * 0.7, y * 0.2, extent=240, style=tk.CHORD
        )
        self.canvas.create_arc(
            x * 0.8, y * 0.1, x * 0.9, y * 0.2, start=10, extent=120, style=tk.PIESLICE
        )
        self.canvas.create_oval(
            x * 0.1,
            y * 0.4,
            x * 0.3,
            y * 0.6,
            fill="lightblue",
            outline="gray",
            width=3,
        )
        self.canvas.create_polygon(
            x * 0.4, y * 0.4, x * 0.5, y * 0.5, x * 0.6, y * 0.4, width=3, fill=""
        )
        self.canvas.create_text(x * 0.1, y * 0.8, text="CSIE in NCUE")
        self.canvas.create_text(
            x * 0.4,
            y * 0.8,
            text="CSIE in NCUE",
            fill="blue",
            font=("Old English Text MT", 20),
        )
        self.canvas.create_text(
            x * 0.7,
            y * 0.8,
            text="CSIE in NCUE",
            fill="blue",
            font=("華康新綜藝體 Std W7", 20),
        )
        ball = Ball(self.canvas, x, y, 1, 1)
        ball.move()

    def event5(self):
        def paint(event):
            x1, y1 = (event.x, event.y)
            x2, y2 = (event.x, event.y)
            self.canvas.create_oval(x1, y1, x2, y2, fill="blue")

        self.canvas.delete("all")
        self.canvas.bind("<B1-Motion>", paint)


    def sierpinski(self, order, p1, p2, p3):
            
        def drawLine(p1, p2):
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], tags="myline")

        def midpoint(p1, p2):
            p = [0, 0]
            p[0] = (p1[0] + p2[0]) / 2
            p[1] = (p1[1] + p2[1]) / 2
            return p
        
        if order == 0:
            drawLine(p1, p2)
            drawLine(p2, p3)
            drawLine(p3, p1)
        else:
            p12 = midpoint(p1, p2)
            p23 = midpoint(p2, p3)
            p31 = midpoint(p3, p1)

        self.sierpinski(order - 1, p1, p12, p31)
        self.sierpinski(order - 1, p12, p2, p23)
        self.sierpinski(order - 1, p31, p23, p3)



    def event6(self):
        self.canvas.delete("all")
        x = self.canvas.winfo_width()
        y = self.canvas.winfo_height()

        self.sierpinski(3, (x * 0.1, y * 0.1), (x * 0.9, y * 0.1), (x * 0.5, y * 0.9))

#         def paintTree(depth, x1, y1, length, angle):
#  if depth >= 0:
#  depth-= 1
#  x2 = x1 + int(math.cos(angle) * length)
#  y2 = y1-int(math.sin(angle) * length)
#  drawLine(x1, y1, x2, y2)
#  paintTree(depth, x2, y2, length*sizeRatio, angle+angleValue)
#  paintTree(depth, x2, y2, length*sizeRatio, angle-angleValue)
#  def drawLine(x1, y1, x2, y2):
#  canvas.create_line(x1, y1, x2, y2, tags="myline")
#  def show():
#  canvas.delete("myline")
#  myDepth = depth.get()
#  paintTree(myDepth, myWidth/2, myHeight, myHeight/3, math.pi/2)
#  angleValue= math.pi/4
#  sizeRatio= 0.6


#  defkoch(order, p1, p2):
#  iforder ==0:
#  drawLine(p1, p2)
#  else:
#  dx=p2[0] -p1[0]
#  dy=p2[1] -p1[1]
#  x=[p1[0] + dx/3, p1[1] + dy/ 3]
#  y=[p1[0] + dx*2/3, p1[1] +dy*2/3]
#  z=[(int)((p1[0]+p2[0]) /2
# math.cos(math.radians(30)) *dy/3),
#  (int)((p1[1]+p2[1]) /2 +
#  math.cos(math.radians(30)) *dx/3)]
