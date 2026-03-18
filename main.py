from rembg import remove
from PIL import Image
import numpy as np
import random

def main():
    color_shifts = [(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 100, 100), (100, 0, 100), (100, 100, 0)]
    image = Image.open("images/test/output.png").convert("RGBA")
    data = np.array(image, dtype=np.int16)

    shift = color_shifts[random.randint(0,5)]
    data[..., :3] = (data[..., :3] + shift) % 256

    new_img = Image.fromarray(data.astype(np.uint8), "RGBA")

    new_img.save("changed.png")
if __name__ == '__main__':
    main()