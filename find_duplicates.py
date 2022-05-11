from progress.bar import Bar
from terminaltables import AsciiTable

import image_file

import numpy as np

import os
from sys import argv


IMAGE_FILES = {}


def check_dir(directory: str) -> str:
    directory += os.sep
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory: " + directory + " does not exist")
    return directory


def matrices(directory: str):
    fnames = []
    m = []
    directory = check_dir(directory)
    img_files = []
    for root, dirs, files in os.walk(directory):
        img_files.extend([os.path.join(root, f) for f in files])
    with Bar('Converting Images to Tensors in "' + directory + '"',
             max=len(img_files)) as bar:
        for f in img_files:
            if not os.path.isdir(f) and f not in IMAGE_FILES:
                img = image_file.ImageFile(f)
                IMAGE_FILES[f] = img
                if img.tensor is not None:
                    m.append(img.tensor)
                    fnames.append(os.path.basename(f))
            bar.next()
    return m, fnames


def mse(a, b):
    err = np.sum((a.astype('float') - b.astype('float')) ** 2)
    err /= float(a.shape[0] * a.shape[1])
    return err


def similarity(sim: int) -> int:
    ref = 200  # normal sens
    if sim == -1:
        ref = 1000  # very low sens
    elif sim == 1:
        ref = 0.05  # extremely sens
    return ref


def determine_image_quality(a: str, b: str):
    a_size = IMAGE_FILES[a].stat.st_size
    b_size = IMAGE_FILES[b].stat.st_size
    if a_size > b_size:
        return a, b
    return b, a


def print_dupes(ans: dict):
    for k in ans:
        table_data = [
            ['File Name', 'Path', 'Size'],
            [ans[k]['fname'], ans[k]['loc'],
             IMAGE_FILES[ans[k]['loc']].stat.st_size]
        ]
        for dupe in ans[k]['dupes']:
            table_data.append([os.path.basename(dupe), dupe,
                               IMAGE_FILES[dupe].stat.st_size])
        print(AsciiTable(table_data).table, end='\n\n')


def print_lower_qualities(li: list):
    table_data = [
        ['File Name', 'Path', 'Size']
    ]
    for f in li:
        img = IMAGE_FILES[f]
        table_data.append([os.path.basename(img.path), img.path,
                           img.stat.st_size])
    print(AsciiTable(table_data).table)


def search_directory(directory: str):
    a_matrices, a_fnames = matrices(directory)
    ans = {}
    lower_qualities = []
    sim = similarity(1)  # allow customizable similarity later

    # Find duplicates in this folder.
    for a_cnt, a_matrix in enumerate(a_matrices):
        for b_cnt, b_matrix in enumerate(a_matrices):
            if b_cnt != 0 and b_cnt > a_cnt != len(a_matrices):
                err = mse(a_matrix, b_matrix)
                if err < sim:
                    a = a_fnames[a_cnt]
                    b = a_fnames[b_cnt]
                    a_path = os.path.join(directory, a)
                    b_path = os.path.join(directory, b)
                    if a in ans.keys():
                        ans[a]['dupes'] += [b_path]
                    else:
                        ans[a] = {'fname': a, 'loc': a_path, 'dupes': [b_path]}
                    high, low = determine_image_quality(a_path, b_path)
                    lower_qualities.append(low)
    return ans, lower_qualities


def delete_images(image_set: set):
    i = 0
    for f in image_set:
        try:
            os.remove(f)
            print('Deleted:', f)
            i += 1
        except:
            pass
    print("\n***\nDeleted", i, "images.")


def main():
    if len(argv) < 2:
        print("Need a folder path")
        exit(1)

    image_folder = argv[1]
    ans, lowers = search_directory(image_folder)
    print_dupes(ans)
    print('Found', len(ans), 'image(s) with one or more duplicates.')

    if len(lowers) > 0:
        print_lower_qualities(lowers)
        ask = input('Delete lower quality images? (y/N)')
        if ask.lower() == 'y' or ask.lower() == 'yes':
            delete_images(set(lowers))


if __name__ == '__main__':
    main()
