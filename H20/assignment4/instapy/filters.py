from .python_color2gray import python_color2gray as p_c2g
from .python_color2sepia import python_color2sepia as p_c2s
from .numpy_color2gray import numpy_color2gray as numpy_c2g
from .numpy_color2sepia import numpy_color2sepia as numpy_c2s
from .numba_color2gray import numba_color2gray as numba_c2g
from .numba_color2sepia import numba_color2sepia as numba_c2s
from .grayscale import load_image
import cv2

def  grayscale_image(input_filename, output_filename=None):
    img, shape = load_image(input_filename)
    processed = numpy_c2g(img, shape)
    if output_filename:
        cv2.imwrite(output_filename, processed)
    return processed

def  sepia_image(input_filename, output_filename=None):
    img, shape = load_image(input_filename)
    processed = numpy_c2s(img, shape)
    if output_filename:
        cv2.imwrite(output_filename, processed)
    return processed
