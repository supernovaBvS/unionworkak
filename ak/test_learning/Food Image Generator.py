import tkinter as tk
from PIL import ImageTk, Image

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Food Image Generator")
        self.root.geometry("400x400")

        self.food_class = tk.StringVar()
        self.food_class.set("apple")

        self.food_class_label = tk.Label(self.root, text="Enter food class:")
        self.food_class_label.pack()

        self.food_class_entry = tk.Entry(self.root, textvariable=self.food_class)
        self.food_class_entry.pack()

        self.generate_button = tk.Button(self.root, text="Generate", command=self.generate_image)
        self.generate_button.pack()

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

    def generate_image(self):
        food_class = self.food_class.get()
        image_path = f"{food_class}.jpg"
        image = Image.open(image_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)

        self.image_label.configure(image=photo)
        self.image_label.image = photo

app = App()
app.root.mainloop()
