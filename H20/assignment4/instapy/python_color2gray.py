import numpy as np

def python_color2gray(src, shape):
    dst = convolve(src, shape)
    dst = dst.astype('uint8')
    return dst

def convolve(src, shape):
    """Grayscale the image given as parameter using slow pure-python approach.
    input:
        src: nd-array of dimensions (H, W, C), where
                H is the height of the picture (pixels),
                W is the width of the picture (pixels),
                C is the number of color channels (3),
            The image to grayscale
        shape: tuple
            The shape of src

    output:
        dst: nd-array like src
            The grayscaled image
    """
    # zeros of floats to support the weighted colour values
    H, W, C = shape
    dst = np.zeros((H, W))
    weights = [0.07, 0.72, 0.21]
    for h in range(H):
        for w in range(W):
            tot = 0
            for c in range(C):
                tot += src[h, w, c]*weights[c]
            dst[h, w] = tot
    return dst

if __name__ == '__main__':
    import cv2, sys
    from grayscale import report, load_image, img_path

    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            # Alternative decorator syntax
            python_color2gray = report(n)(python_color2gray)
        except ValueError:
            msg = 'Argument must be a number. '
            msg += 'Reverting to normal run without timing.'
            print(msg)

    fname = 'rain.jpg'
    img, shape = load_image(img_path + fname)
    gray = python_color2gray(img, shape)
    cv2.imwrite(img_path + 'python_' + fname.replace('.', '_grayscale.'), gray)
