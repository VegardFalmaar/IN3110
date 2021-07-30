from instapy.python_color2gray import python_color2gray as p_c2g
from instapy.python_color2sepia import python_color2sepia as p_c2s
from instapy.numpy_color2gray import numpy_color2gray as numpy_c2g
from instapy.numpy_color2sepia import numpy_color2sepia as numpy_c2s
from instapy.numba_color2gray import numba_color2gray as numba_c2g
from instapy.numba_color2sepia import numba_color2sepia as numba_c2s
from instapy.grayscale import report, load_image
import cv2

img_path = 'images/'
rep_path = 'reports/'
fname = 'rain.jpg'

funcs = [
    [p_c2g, numpy_c2g, numba_c2g],
    [p_c2s, numpy_c2s, numba_c2s]
]
methods = ['python', 'numpy', 'numba']
filters = ['grayscale', 'sepia']

for i in range(2):
    for j in range(3):
        print('Timing', methods[j], filters[i])
        func = report(5, rep_path)(funcs[i][j])
        img, shape = load_image(img_path + fname)
        gray = func(img, shape)
        save_fname = methods[j] + '_' + fname.replace('.', '_' + filters[i] + '.')
        cv2.imwrite(img_path + save_fname, gray)
