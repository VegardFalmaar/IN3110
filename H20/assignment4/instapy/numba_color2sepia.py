from numba import jit
import numpy as np
from .python_color2sepia import convolve

convolve = jit(nopython=True)(convolve)

def numba_color2sepia(src, shape):
    dst = convolve(src, shape)
    np.clip(dst, None, 255, out=dst)
    dst = dst.astype('uint8')
    return dst

if __name__ == '__main__':
    import cv2, sys
    from grayscale import load_image, report, img_path

    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            # Alternative decorator syntax
            numba_color2sepia = report(n)(numba_color2sepia)
        except ValueError:
            msg = 'Argument must be a number. '
            msg += 'Reverting to normal run without timing.'
            print(msg)

    fname = 'rain.jpg'
    img, shape = load_image(img_path + fname)
    sepia = numba_color2sepia(img, shape)
    cv2.imwrite(img_path + 'numba_' + fname.replace('.', '_sepia.'), sepia)
