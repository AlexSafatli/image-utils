from progress.bar import Bar

import skimage
import numpy as np
import cv2
import os

from sys import argv


def check_dir(directory: str) -> str:
    directory += os.sep
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory: " + directory + " does not exist")
    return directory


def matrices(directory: str, px_size=50):
    fnames = []
    m = []
    directory = check_dir(directory)
    files = [fname for fname in os.listdir(directory)]
    with Bar('Converting Images to Tensors in "' + directory + '"',
             max=len(files)) as bar:
        for fname in files:
            f = os.path.join(directory, fname)
            if not os.path.isdir(f):
                try:
                    img = cv2.imdecode(np.fromfile(f, dtype=np.uint8),
                                       cv2.IMREAD_UNCHANGED)
                    if type(img) == np.ndarray:
                        img = img[..., 0:3]
                        img = cv2.resize(img, dsize=(px_size, px_size),
                                         interpolation=cv2.INTER_CUBIC)

                        if len(img.shape) == 2:
                            img = skimage.color.gray2rgb(img)
                        m.append(img)
                        fnames.append(fname)
                except:
                    pass
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


def determine_image_quality(a_dir: str, b_dir: str, a, b):
    a_dir = check_dir(a_dir)
    b_dir = check_dir(b_dir)
    a_size = os.stat(a_dir + a).st_size
    b_size = os.stat(b_dir + b).st_size
    if a_size > b_size:
        return os.path.join(a_dir, a), os.path.join(b_dir, b)
    return os.path.join(b_dir, b), os.path.join(a_dir, a)


def print_images(a, b):
    print("""Duplicate files:\n{} and \n{}

    """.format(a, b))


def search_directory(directory: str, px_size=50):
    a_matrices, a_fnames = matrices(directory, px_size)
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
                    print_images(str("..." + directory[-35:]) +
                                 "/" + a, str("..." + directory[-35:]) +
                                 "/" + b)
                    if a in ans.keys():
                        ans[a]['dupes'] += [os.path.join(directory, b)]
                    else:
                        ans[a] = {'loc': os.path.join(directory, a),
                                  'dupes': [os.path.join(directory, b)]}
                    high, low = determine_image_quality(directory, directory,
                                                        a, b)
                    lower_qualities.append(low)
    return ans, lower_qualities


def delete_images(image_set: set):
    i = 0
    for f in image_set:
        try:
            os.remove(f)
            print('Deleted:', f, end='\r')
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
    print('Found', len(ans), 'image(s) with one or more duplicates.')

    if len(lowers) > 0:
        ask = input('Delete lower quality images? (y/N)')
        if ask.lower() == 'y' or ask.lower() == 'yes':
            delete_images(set(lowers))


if __name__ == '__main__':
    main()
