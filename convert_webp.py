from sys import argv
from glob import glob
from os import path
from os import unlink

from PIL import Image


def convert_if_no_existing_file(file: str, verbose: bool):
    new_path = file.strip('webp') + 'png'
    if not path.exists(new_path):
        img = Image.open(file).convert('RGB')
        img.save(new_path, 'png')
        unlink(file)
        if verbose:
            print(file, '->', new_path)


if len(argv) < 2:
    print("Need a folder path")
    exit(1)

image_folder = argv[1]
webps = glob(path.join(image_folder, '*.webp'))

for webp in webps:
    convert_if_no_existing_file(webp, True)
