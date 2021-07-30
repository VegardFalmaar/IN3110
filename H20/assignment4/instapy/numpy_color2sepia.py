import numpy as np
from .python_color2sepia import sep_mat_BGR

def numpy_color2sepia(src, shape):
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
    dst = np.matmul(sep_mat_BGR, src[..., np.newaxis])
    dst = np.squeeze(dst)
    np.clip(dst, None, 255, out=dst)
    dst = dst.astype('uint8')
    return dst

if __name__ == '__main__':
    import cv2, sys
    from grayscale import report, load_image, img_path

    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            # Alternative decorator syntax
            numpy_color2sepia = report(n)(numpy_color2sepia)
        except ValueError:
            msg = 'Argument must be a number.\n'
            msg += 'Reverting to normal run without timing.'
            print(msg)

    fname = 'rain.jpg'
    img, shape = load_image(img_path + fname)
    sepia = numpy_color2sepia(img, shape)
    cv2.imwrite(img_path + 'numpy_' + fname.replace('.', '_sepia.'), sepia)
