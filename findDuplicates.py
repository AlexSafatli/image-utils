import imagehash
from PIL import Image

from sys import argv
from glob import glob
from os import path


if len(argv) < 2:
    print("Need a folder path")
    exit(1)

image_folder = argv[1]
jpgs = glob(path.join(image_folder, '*.jpg'))
pngs = glob(path.join(image_folder, '*.png'))
images = jpgs
jpgs.extend(pngs)
image_hashes = {}
dupes = []

for image_file in images:
    with Image.open(image_file) as img:
        img_hash = imagehash.average_hash(img, hash_size=8)
        if img_hash in image_hashes:
            print('Duplicate {}\n found for Image {}!\n'.format(
                image_file, image_hashes[img_hash]))
            dupes.append(image_file)
