from progress.bar import Bar

import base
import image_file

import numpy as np

import os
from sys import argv


IMAGE_FILES = {}


def matrices(directory: str, recursive: bool):
    paths = []
    m = []
    files = base.get_all_file_paths(directory, recursive=recursive)
    with Bar('Converting Images to Tensors in "' + directory + '"',
             max=len(files)) as bar:
        for f in files:
            if not os.path.isdir(f) and f not in IMAGE_FILES:
                img = image_file.ImageFile(f)
                IMAGE_FILES[f] = img
                if img.tensor is not None:
                    m.append(img.tensor)
                    paths.append(f)
            bar.next()
    return m, paths


def mse(a, b):
    err = np.sum((a.astype('float') - b.astype('float')) ** 2)
    err /= float(a.shape[0] * a.shape[1])
    return err


def similarity(sim: int) -> int:
    ref = 200  # normal sens
    if sim == -1:
        ref = 1000  # very low sens
    elif sim == 1:
        ref = 0.025  # extremely sens
    return ref


def determine_image_quality(a: str, b: str):
    a_size = IMAGE_FILES[a].stat.st_size
    b_size = IMAGE_FILES[b].stat.st_size
    if a_size > b_size:
        return a, b
    return b, a


def search_directory(directory: str, recursive=True):
    a_matrices, a_paths = matrices(directory, recursive)
    ans = {}
    found_dupes = []
    lower_qualities = []
    sim = similarity(1)  # allow customizable similarity later

    # Find duplicates in this folder.
    for a_cnt, a_matrix in enumerate(a_matrices):
        for b_cnt, b_matrix in enumerate(a_matrices):
            if b_cnt != 0 and b_cnt > a_cnt != len(a_matrices):
                err = mse(a_matrix, b_matrix)
                if err < sim:
                    a_path = a_paths[a_cnt]
                    b_path = a_paths[b_cnt]
                    a = os.path.basename(a_path)
                    b = os.path.basename(b_path)

                    if a not in found_dupes:
                        found_dupes.append(b)

                    if a in ans.keys():
                        ans[a]['dupes'] += [
                            (b_path, IMAGE_FILES[b_path].stat.st_size*1e-6)]
                    else:
                        high, low = determine_image_quality(a_path, b_path)
                        lower_qualities.append(low)
                        if a not in found_dupes:
                            dupes = [(b_path,
                                      IMAGE_FILES[b_path].stat.st_size*1e-6)]
                            ans[a] = {'fname': a, 'loc': a_path,
                                      'dupes': dupes,
                                      'size':
                                          IMAGE_FILES[a_path].stat.st_size*1e-6}
    return ans, lower_qualities


def main():
    if len(argv) < 2:
        print("Need a folder path")
        exit(1)

    image_folder = argv[1]
    recurse = True
    if len(argv) >= 3:
        recurse = argv[2] == 'True' or argv[2] == 'true'
        print('Recursive:', recurse)
    ans, lowers = search_directory(image_folder, recursive=recurse)
    print('Found', len(ans), 'image(s) with one or more duplicates.')

    if len(lowers) > 0 and base.show_duplicate_image_results_in_window(ans):
        base.delete_images(set(lowers))


if __name__ == '__main__':
    main()
