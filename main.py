from pathlib import Path
from rembg import remove
from PIL import Image
import numpy as np
import random
import cv2

def main():
    dataAugmentation("images/classes", "images/backgrounds", 150)

def dataAugmentation(class_dir, background_dir: str, goal: int) -> None:
    # idek what those will be
    color_shifts = [(100, 0, 0), (-200, 200, 0), (-110, -100, 200),
                    (200, 55, 155), (100, 0, 100), (100, 100, 0),
                    (200, 55, 0), (55, 55, 155)]
    # clock like every 45 deg
    tilt_angles = [0, 45, 90, 135, 180, 225, 270, 315]

    # data set
    class_dir = Path(class_dir)
    if not class_dir.exists():
        raise FileNotFoundError(f"Could not find class directory: {class_dir}")
    background_dir = Path(background_dir)
    if not background_dir.exists():
        raise FileNotFoundError(f"Could not find background directory: {background_dir}")
    # for class
    for class_folder in class_dir.iterdir():
        # amount of files in dir
        if class_folder.is_dir():
            amount = len([f for f in class_folder.iterdir() if f.is_file()])
            while amount < goal:
                for file in class_folder.iterdir():
                    # read and remove background
                    img = Image.open(file).convert('RGBA')
                    img = remove(img)
                    bbox = img.getbbox()
                    if bbox:
                        img = img.crop(bbox)

                    # convert to cv2 format
                    # tilt
                    cv2_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)
                    height, width = cv2_img.shape[:2]
                    center = (width // 2, height // 2)
                    angle = tilt_angles[random.randint(0, 7)]
                    scale = 1.0

                    # bounding box
                    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
                    abs_cos = abs(rotation_matrix[0, 0])
                    abs_sin = abs(rotation_matrix[0, 1])
                    new_w = int(height * abs_sin + width * abs_cos)
                    new_h = int(height * abs_cos + width * abs_sin)

                    rotation_matrix[0, 2] += new_w / 2 - center[0]
                    rotation_matrix[1, 2] += new_h / 2 - center[1]
                    rotated_image = cv2.warpAffine(cv2_img, rotation_matrix, (new_w, new_h))
                    rotated_image = Image.fromarray(cv2.cvtColor(rotated_image, cv2.COLOR_BGRA2RGBA))

                    # back to pil image and color shift
                    data = np.array(rotated_image, dtype=np.int16)

                    color_shift = color_shifts[random.randint(0, 7)]
                    data[..., :3] = np.clip(data[..., :3] + color_shift, 0, 255)
                    color_shifted = Image.fromarray(data.astype(np.uint8), "RGBA")
                    bg_file = background_dir / f"{random.randint(0, 7)}.png"
                    if bg_file.exists():
                        background = Image.open(bg_file)
                    else:
                        raise FileNotFoundError("Could not find background image")

                    # shift
                    bg_w, bg_h = background.size
                    obj_w, obj_h = color_shifted.size

                    target_max_w = int(bg_w * 0.4)
                    target_max_h = int(bg_h * 0.4)

                    scale_factor = min(target_max_w / obj_w, target_max_h / obj_h)
                    new_w = int(obj_w * scale_factor)
                    new_h = int(obj_h * scale_factor)

                    color_shifted = color_shifted.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    obj_w, obj_h = color_shifted.size

                    max_x = max(0, bg_w - obj_w)
                    max_y = max(0, bg_h - obj_h)

                    tx = random.randint(0, max_x)
                    ty = random.randint(0, max_y)

                    background.paste(color_shifted, (tx, ty), color_shifted)
                    background.save(rf"./images/classes/#3003/file{amount}.png")
                    amount += 1

if __name__ == '__main__':
    main()