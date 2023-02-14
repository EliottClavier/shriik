import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import shutil
import requests

from src.ascii_converter import AsciiConverter

from os import path

import sv_ttk

class Window(tk.Tk):

    ascii_converter: AsciiConverter = AsciiConverter()
    previous_ascii_image: tk.StringVar = None
    url_entry: ttk.Entry = None

    def __init__(self):
        super().__init__()
        self.write_base_window()

    def exception_catcher(self, e) -> None:
        tk.messagebox.showerror("Error", e)

    def write_base_window(self) -> None:        
        self.title("Shriik's Image Converter")

        self.previous_ascii_image = tk.StringVar()

        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.insert(0, 'Enter an image URL')
        self.url_entry.grid(column=0, row=0, padx=(50, 50), pady=(100, 10))
        self.url_entry.bind("<Return>", lambda e: self.convert_ascii())
     
        previous_ascii_image = ttk.Label(self, textvariable=self.previous_ascii_image, font=("Courier", 5))
        previous_ascii_image.grid(column=0, row=1, padx=(50, 50), pady=(100, 100))

        if path.exists("./ascii/ascii_image.txt"):
            with open("./ascii/ascii_image.txt", "r") as f:
                self.previous_ascii_image.set(f.read())
                f.close()

        sv_ttk.set_theme("dark")
    
    def convert_ascii(self) -> None:
        url = self.url_entry.get()
        img_format = url.split('.')[-1]

        format_accepted = ("jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "ico", "svg", "raw")
        if img_format in format_accepted:
            image_name = url.split('/')[-1]
            res = requests.get(url, stream = True)
            
            if res.status_code == 200:
                with open(f"./images/{image_name}", 'wb') as f:
                    shutil.copyfileobj(res.raw, f)
                print(f"Image sucessfully downloaded: {image_name}")

                self.ascii_converter.launch_workflow(f"./images/{image_name}", "ascii_image")
                with open("./ascii/ascii_image.txt", "r") as f:
                    self.previous_ascii_image.set(f.read())
                    f.close()
            else:
                self.exception_catcher("Image couldn't be retrieved")
        else:
            self.exception_catcher(f"Format {img_format} not accepted")