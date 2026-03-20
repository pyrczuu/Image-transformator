from typing import List
import os
from rembg import remove
from PIL import Image
import numpy as np
import random

def main():
    pass

def dataAugmentation(class_dir, background_dir: str, goal: int) -> None:
    # idek what those will be
    color_shifts = [(100, 0, 0), (0, 100, 0), (0, 0, 100),
                    (100, 100, 100), (100, 0, 100), (100, 100, 0),
                    (200, 55, 0), (55, 55, 155)]
    # clock like every 45 deg
    tilt_angles = [0, 45, 90, 135, 180, 225, 270, 315]
    # up, down, left, right and every corner
    pos_shifts = [(0, -300), (300, 0), (-300, 0),
                  (0, 300), (150, -150), (150, 150),
                  (-150, 150), (-150, -150)]

    # data set
    class_dir = os.fsencode(class_dir)
    background_dir = os.fsencode(background_dir)
    # for class
    for d in os.listdir(class_dir):
        # ammount of files in dir
        ammount = len([name for name in os.listdir(d) if os.path.isfile(os.path.join(d, name))])
        while ammount < goal:
            for file in os.listdir(d):
                img = Image.open(class_dir + "/" + file)
                remove(img)

                image = Image.open("images/test/output.png").convert("RGBA")
                data = np.array(image, dtype=np.int16)

                color_shift = color_shifts[random.randint(0, 7)]
                data[..., :3] = (data[..., :3] + color_shift) % 256

                new_img = Image.fromarray(data.astype(np.uint8), "RGBA")

                new_img.save("file" + ammount + ".png")
                ammount += 1

if __name__ == '__main__':
    main()