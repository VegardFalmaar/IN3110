import numpy as np
import cv2
from blur_1 import load_image
import timeit
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

    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        number = 50
        res1 = timeit.timeit(stmt=f'blurred = blur_image(fname)', 
                    setup='from __main__ import fname; from blur_1 import blur_image',
                    number=3)
        res2 = timeit.timeit(stmt=f'blurred = blur_image(fname)', 
                    setup='from __main__ import blur_image, fname',
                    number=number)
        _, shape = load_image(fname)
        text = [f'Size of image: {shape}',
                f'Total time for 3 and {number} runs:\n',
                ('{:^10s}'*2).format('blur_1', 'blur_2'),
                '-'*20,
                ('{:^10.5f}'*2).format(res1, res2),
                ('{:^10.5f}'*2).format(res1/3, res2/number)]

        with open('report2.txt', 'w') as outfile:
            [outfile.write(line + '\n') for line in text]
