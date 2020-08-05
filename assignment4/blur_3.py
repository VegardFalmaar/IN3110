import numpy as np
import cv2
from numba import jit
from blur_1 import load_image

@jit(nopython=True)
def convolve(src, dst, shape):
    """Blur the image given as parameter using slow pure-python approach.
    input:
        fname: str, 
            the path to the image to blur
    output:
        dst: nd-array of dimensions (H, W, 3), where
                H is the height of the picture (pixels) and
                W is the width of the picture (pixels),
            The blurred image
    """
    H, W, C = shape
    for h in range(1, H+1):
        dst_h = h - 1
        for w in range(1, W+1):
            dst_w = w - 1
            for c in range(C):
                dst[dst_h, dst_w, c] = (src[h, w, c] + src[h-1, w, c] + src[h+1, w, c]
                            + src[h, w-1, c] + src[h, w+1, c]
                            + src[h-1, w-1, c] + src[h-1, w+1, c]
                            + src[h+1, w-1, c] + src[h+1, w+1, c])/9
    return dst
    
def blur_image(fname):
    src, shape = load_image(fname)
    dst = np.zeros(shape) # zeros of floats to support division later
    blurred = convolve(src, dst, shape)
    blurred = blurred.astype('uint8')
    return blurred

if __name__ == '__main__':
    fname = 'beatles.jpg'
    blurred = blur_image(fname)
    cv2.imwrite('beatles_blurred_3.jpg', blurred)
