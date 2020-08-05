import numpy as np
import cv2
from blur_1 import load_image

def blur_image(fname):
    """Blur the image given as parameter using numpy vectorized operations.
    input:
        fname: str, 
            the path to the image to blur
    output:
        dst: nd-array of dimensions (H, W, 3), where
                H is the height of the picture (pixels) and
                W is the width of the picture (pixels),
            The blurred image
    """
    src, _ = load_image(fname)
    dst = (src[1:-1, 1:-1, :] + src[:-2, 1:-1, :] + src[2:, 1:-1, :]
                            + src[1:-1, :-2, :] + src[1:-1, 2:, :]
                            + src[:-2, :-2, :] + src[:-2, 2:, :]
                            + src[2:, :-2, :] + src[2:, 2:, :])/9
    dst = dst.astype('uint8')
    return dst
    
if __name__ == '__main__':
    fname = 'beatles.jpg'
    blurred = blur_image(fname)
    cv2.imwrite('beatles_blurred_2.jpg', blurred)
