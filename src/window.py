from tkinter import *
from tkinter import messagebox

from src.ascii_converter import AsciiConverter

import sys
from os import path

class Window:

    window: Tk = None
    ascii_converter: AsciiConverter = AsciiConverter()

    previous_ascii_image: StringVar = None

    def __init__(self):
        try:
            if len(sys.argv) > 1:
                self.write_base_window()
            else:
                raise FileNotFoundError("No image path provided")
        except Exception as e:
            self.exception_catcher(e)

    def exception_catcher(self, e) -> None:
        messagebox.showerror("Error", e)

    def write_base_window(self) -> None:
        self.window = Tk()
        self.window.title("Shriik's Image Converter")

        self.previous_ascii_image = StringVar()
                
        ascii_button = Button(self.window, text="Convert to ASCII", command=self.convert_ascii)
        ascii_button.grid(column=1, row=1, padx=(100, 100), pady=(100, 100))

        previous_ascii_image = Label(self.window, textvariable=self.previous_ascii_image, font=("Courier", 5))
        previous_ascii_image.grid(column=2, row=1, padx=(10, 100), pady=(100, 100))

        if path.exists("./ascii/ascii_image.txt"):
            with open("./ascii/ascii_image.txt", "r") as f:
                self.previous_ascii_image.set(f.read())
                f.close()

        self.window.mainloop()
    
    def convert_ascii(self) -> None:
        self.ascii_converter.launch_workflow(sys.argv[1], "ascii_image")
        with open("./ascii/ascii_image.txt", "r") as f:
            self.previous_ascii_image.set(f.read())
            f.close()