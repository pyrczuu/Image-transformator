from typing import List
import os
from rembg import remove
from PIL import Image
import numpy as np
import random

def main():
    # idek what those will be
    color_shifts = [(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 100, 100), (100, 0, 100), (100, 100, 0), (200, 55, 0), (55,55, 155)]
    # clock like every 45 deg
    tilt_angles = [0, 45, 90, 135, 180, 225, 270, 315]
    # up, down, left, right and every corner
    pos_shifts = [(0, -300), (300, 0), (-300, 0), (0, 300), (150, -150), (150, 150), (-150, 150), (-150, -150)]

    directory = os.fsencode("images/#3003")
    for file in os.listdir(directory):
        img = Image.open(directory+"/"+file)
        remove(img)

        image = Image.open("images/test/output.png").convert("RGBA")
        data = np.array(image, dtype=np.int16)

        shift = color_shifts[random.randint(0,5)]
        data[..., :3] = (data[..., :3] + shift) % 256

        new_img = Image.fromarray(data.astype(np.uint8), "RGBA")

        new_img.save("changed.png")

def dataAugmentation(dir: str) -> None:
    pass

if __name__ == '__main__':
    main()