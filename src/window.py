import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd

from PIL import ImageTk, Image

import shutil
import requests

from src.ascii_converter import AsciiConverter

from os import path

import sv_ttk

class Window(tk.Tk):

    ascii_converter: AsciiConverter = AsciiConverter()
    previous_image: tk.Label = None
    previous_ascii_image: tk.StringVar = None
    previous_ascii_image_label: tk.Label = None
    url_entry: ttk.Entry = None
    accepted_formats: tuple = ("jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "ico", "svg", "raw")

    def __init__(self):
        super().__init__()
        self.write_base_window()

    def exception_catcher(self, e) -> None:
        tk.messagebox.showerror("Error", e)

    def write_base_window(self) -> None:        
        # Theme
        sv_ttk.set_theme("dark")

        for i in range(3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        # Title
        self.title("Shriik")
        self.state('zoomed')

        self.previous_ascii_image = tk.StringVar()

        # Row 0
        title_label = ttk.Label(self, text="Shriik's Image Converter", font=("Arial", 25))
        title_label.grid(column=0, columnspan=3, row=0, padx=(10, 10), pady=(10, 10))

        # Row 1
        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.insert(0, 'Enter an image URL')
        self.url_entry.grid(column=0, row=1, padx=(10, 10), pady=(10, 10))
        self.url_entry.bind("<Return>", lambda e: self.convert_ascii(self.url_entry.get()))

        or_label = ttk.Label(self, text="OR", font=("Arial", 20))
        or_label.grid(column=1, row=1, padx=(10, 10), pady=(10, 10))

        open_button = ttk.Button(self, text='Open image file', command=self.select_file)
        open_button.grid(column=2, row=1, padx=(10, 10), pady=(10, 10))
     
        # Row 2
        if path.exists("./ascii_image.txt"):
            with open("./ascii_image.txt", "r") as f:
                content = f.read()
                f.seek(0)
                width = len(f.readlines()[0])

                arrow = ttk.Label(self, text="🡒", font=("Arial", 150))
                arrow.grid(column=1, row=2, padx=(10, 10), pady=(10, 10))

                self.previous_ascii_image_label = ttk.Label(self, textvariable=self.previous_ascii_image)
                self.previous_ascii_image_label.grid(column=2, row=2, padx=(10, 10), pady=(10, 10))

                self.previous_ascii_image_label.config(font=("Courier", int(500/width)))
                self.previous_ascii_image.set(content)
                f.close()

            self.update_previous_image()
    
    def update_previous_image(self) -> None:
        # Display previous image
        if path.exists("./previous_image.txt"):
            with open("./previous_image.txt", "r") as f:
                f.seek(0)
                content = f.read()
                if content:
                    self.update()
                    if self.previous_image:
                        self.previous_image.grid_forget()
                    old_path = content
                    image = Image.open(old_path)
                    image = ImageTk.PhotoImage(image.resize(
                        (self.previous_ascii_image_label.winfo_width(), self.previous_ascii_image_label.winfo_height())
                        , Image.ANTIALIAS
                    ))
                    self.previous_image = tk.Label(self, image=image)
                    self.previous_image.image = image
                    self.previous_image.grid(column=0, row=2, padx=(10, 10), pady=(10, 10))
                f.close()

    def select_file(self):
        filetypes = (('Image files', f'*.{accepted_format}') for accepted_format in self.accepted_formats)

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if filename:
            self.convert_ascii(filename, False)

    def convert_ascii(self, path, from_internet=True) -> None:
        img_format = path.split('.')[-1]

        if img_format.lower() in self.accepted_formats:
            image_name = path.split('/')[-1]

            if from_internet:
                res = requests.get(path, stream = True)
                
                if res.status_code == 200:
                    with open(f"./images/{image_name}", 'wb') as f:
                        shutil.copyfileobj(res.raw, f)
                    print(f"Image sucessfully downloaded: {image_name}")
                else:
                    self.exception_catcher("Image couldn't be retrieved")
                    return

            if from_internet:
                self.ascii_converter.launch_workflow(f"./images/{image_name}", "ascii_image")
            else:
                self.ascii_converter.launch_workflow(path, "ascii_image")
            
            with open("./ascii_image.txt", "r") as f:
                content = f.read()
                f.seek(0)
                width = len(f.readlines()[0])
                arrow = ttk.Label(self, text="🡒", font=("Arial", 150))
                arrow.grid(column=1, row=2, padx=(10, 10), pady=(10, 10))

                self.previous_ascii_image_label = ttk.Label(self, textvariable=self.previous_ascii_image)
                self.previous_ascii_image_label.grid(column=2, row=2, padx=(10, 10), pady=(10, 10))
                self.previous_ascii_image_label.config(font=("Courier", int(500/width)))
                self.previous_ascii_image.set(content)
                f.close()

            with open(f"previous_image.txt", 'wb') as f:
                f.write(path.encode())
                f.close()

            self.update_previous_image()
        else:
            self.exception_catcher(f"Format {img_format} not accepted")