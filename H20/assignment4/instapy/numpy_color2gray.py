import numpy as np

def numpy_color2gray(src, shape):
    """Grayscale the image given as parameter using numpy.
    input:
        src: nd-array of dimensions (H, W, C), where
                H is the height of the picture (pixels),
                W is the width of the picture (pixels),
                C is the number of color channels (3),
            The image to grayscale

    output:
        dst: nd-array like src
            The grayscaled image
    """
    weights = np.array([0.07, 0.72, 0.21])
    totals = src*weights
    dst = np.sum(totals, axis=2)
    dst = dst.astype('uint8')
    return dst

if __name__ == '__main__':
    import cv2, sys
    from grayscale import report, load_image, img_path

    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            # Alternative decorator syntax
            numpy_color2gray = report(n)(numpy_color2gray)
        except ValueError:
            msg = 'Argument must be a number. '
            msg += 'Reverting to normal run without timing.'
            print(msg)

    fname = 'rain.jpg'
    img, shape = load_image(img_path + fname)
    gray = numpy_color2gray(img, shape)
    cv2.imwrite(img_path + 'numpy_' + fname.replace('.', '_grayscale.'), gray)
