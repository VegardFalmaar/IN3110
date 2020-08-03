import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys

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
    image = cv2.imread(fname)
    src = np.pad(image, ((1, 1), (1, 1), (0, 0)), mode='edge')
    src = src.astype('uint32')

    dst = (src[1:-1, 1:-1, :] + src[:-2, 1:-1, :] + src[2:, 1:-1, :]
                            + src[1:-1, :-2, :] + src[1:-1, 2:, :]
                            + src[:-2, :-2, :] + src[:-2, 2:, :]
                            + src[2:, :-2, :] + src[2:, 2:, :])/9

    dst = dst.astype('uint8')
    return dst
    
fname = 'beatles.jpg'
blurred = blur_image(fname)
cv2.imwrite('beatles_blurred_2.jpg', blurred)

# argparser
if False:
    import blur_1
    slow_blurred = blur_1.blur_image(fname)
    np.testing.assert_array_equal(blurred, slow_blurred)
