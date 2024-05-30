import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import itertools
import os

# 1920x1080

class ImageSlider:
    def __init__(self, root, image_paths):
        self.root = root
        self.root.title("Image Slider Animation")

        self.canvas = Canvas(root)
        self.canvas.pack(fill='both', expand=True)

        self.images = [Image.open(img_path) for img_path in image_paths]
        self.image_index = 0
        self.current_image_tk = None
        self.current_image_id = None

        self.root.bind('<Configure>', self.resize_canvas)

        self.root.after(2000, self.slide_images)

    def resize_canvas(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.update_image()

    def update_image(self):
        image = self.images[self.image_index]
        resized_image = self.resize_image(image, self.canvas_width, self.canvas_height)
        self.current_image_tk = ImageTk.PhotoImage(resized_image)
        
        if self.current_image_id:
            self.canvas.delete(self.current_image_id)

        self.current_image_id = self.canvas.create_image(
            self.canvas_width // 2, self.canvas_height // 2, image=self.current_image_tk
        )

    def resize_image(self, image, canvas_width, canvas_height):
        img_width, img_height = image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))
        return image.resize(new_size)

    def slide_images(self):
        next_image_index = (self.image_index + 1) % len(self.images)
        self.animate_image(self.images[next_image_index])
        self.image_index = next_image_index
        self.root.after(4000, self.slide_images)

    def animate_image(self, next_image):
        next_image_tk = ImageTk.PhotoImage(self.resize_image(next_image, self.canvas_width, self.canvas_height))
        
        for offset in itertools.chain(range(0, self.canvas_width + 1, 20)):
            self.canvas.move(self.current_image_id, -20, 0)
            new_image_id = self.canvas.create_image(
                self.canvas_width - offset, self.canvas_height // 2, image=next_image_tk
            )
            self.root.update()
            self.canvas.delete(new_image_id)
        
        self.canvas.delete(self.current_image_id)
        self.current_image_id = self.canvas.create_image(
            self.canvas_width // 2, self.canvas_height // 2, image=next_image_tk
        )
        self.current_image_tk = next_image_tk

def create_window():
    root = tk.Tk()
    image_paths = []
    for path in os.listdir("ui/img"):
        image_paths.append(os.path.join("ui/img", path))
        # image_paths.append(path)
    ImageSlider(root, image_paths)
    root.mainloop()

if __name__ == "__main__":
    create_window()
