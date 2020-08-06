import numpy as np
import cv2, sys, timeit
from numba import jit
from blur_1 import load_image

@jit(nopython=True)
def convolve(src, dst, shape, start=(1, 1), shift=1):
    """Blur the image given as parameter using python accelerated by numba.
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
    for h in range(start[0], H+1):
        dst_h = h - shift
        for w in range(start[1], W+1):
            dst_w = w - shift
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

    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        number = 50
        res1 = timeit.timeit(stmt=f'blurred = blur_image(fname)', 
                    setup='from __main__ import fname; from blur_1 import blur_image',
                    number=3)
        res2 = timeit.timeit(stmt=f'blurred = blur_image(fname)', 
                    setup='from __main__ import fname; from blur_2 import blur_image',
                    number=number)
        res3 = timeit.timeit(stmt=f'blurred = blur_image(fname)', 
                    setup='from __main__ import fname, blur_image',
                    number=number)
        _, shape = load_image(fname)
        text = [f'Size of image: {shape}',
                f'Total and average time for 3, {number} and {number} runs:\n',
                ('{:^10s}'*3).format('blur_1', 'blur_2', 'blur_3'),
                '-'*30,
                ('{:^10.5f}'*3).format(res1, res2, res3),
                ('{:^10.5f}'*3).format(res1/3, res2/number, res3/number)]

        with open('report3.txt', 'w') as outfile:
            [outfile.write(line + '\n') for line in text]
