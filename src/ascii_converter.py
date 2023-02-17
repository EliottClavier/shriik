from multiprocessing.dummy import Array
from tokenize import String
from typing import Any
from PIL import Image

class AsciiConverter:

    image_path: String = ""
    img: Image = None 
    pixels: Any = None
    ascii_image: String = None
    new_width: int = 200
    chars: Array = ["B","S","#","&","@","$","%","*","!",":","."]
    
    def launch_workflow(self, image_path, image_name) -> None:
        self.get_image(image_path)
        self.configure_image()
        self.convert()
        self.write_image(image_name)

    def get_image(self, image_path) -> None:
        self.img = Image.open(image_path)

    def configure_image(self) -> None:
        width, height = self.img.size
        aspect_ratio = height/width
        # * 0.55 car un caractère ne fait pas la taille d'un carré, donc la hauteur doit prendre moins de ligne que la largeur
        new_height = aspect_ratio * self.new_width * 0.55

        self.img = self.img.resize((self.new_width, int(new_height)))
        self.img = self.img.convert('L')
        self.pixels = self.img.getdata()

    def convert(self) -> None:
        new_pixels = [self.chars[pixel//25] for pixel in self.pixels]
        new_pixels = ''.join(new_pixels)

        new_pixels_count = len(new_pixels)

        self.ascii_image = [new_pixels[index:index + self.new_width] for index in range(0, new_pixels_count, self.new_width)]
        self.ascii_image = "\n".join(self.ascii_image)

    def write_image(self, image_name) -> None:
        print("Writing image...")
        with open(f"{image_name}.txt", "w") as f:
            f.write(self.ascii_image)
            f.close()
        print("Image written.")

    def copy_ascii_image_clipboard(self) -> String:
        return self.ascii_image