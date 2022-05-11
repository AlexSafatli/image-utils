import skimage
import numpy as np
import cv2

import os


class ImageFile(object):

    def __init__(self, path: str, px_size=50):
        self.path = path
        self.px_size = px_size
        self.stat = os.stat(path)
        self.tensor = self._get_tensor()

    def _get_tensor(self):
        try:
            img = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8),
                               cv2.IMREAD_UNCHANGED)
            if type(img) == np.ndarray:
                img = img[..., 0:3]
                img = cv2.resize(img, dsize=(self.px_size, self.px_size),
                                 interpolation=cv2.INTER_CUBIC)

                if len(img.shape) == 2:
                    img = skimage.color.gray2rgb(img)
            return img
        except:
            return None
