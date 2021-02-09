from sys import argv
from glob import glob
from os import path
from os import rename


def rename_if_no_existing_file(file: str, verbose: bool):
    new_path = file.strip('large').rstrip('_')
    if not path.exists(new_path):
        rename(file, new_path)
        if verbose:
            print(file, '->', new_path)


if len(argv) < 2:
    print("Need a folder path")
    exit(1)

image_folder = argv[1]
jpg_larges = glob(path.join(image_folder, '*.jpg_large'))
png_larges = glob(path.join(image_folder, '*.png_large'))

for jpg in jpg_larges:
    rename_if_no_existing_file(jpg, True)

for png in png_larges:
    rename_if_no_existing_file(png, True)
