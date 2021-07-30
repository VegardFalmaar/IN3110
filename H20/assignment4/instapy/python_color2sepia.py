import numpy as np

def python_color2sepia(src, shape):
    dst = convolve(src, shape)
    np.clip(dst, None, 255, out=dst)
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
    dst = np.zeros(shape)
    H, W, C = shape
    for h in range(H):
        for w in range(W):
            BGR = [0.0]*3
            for c in range(C):
                for i in range(3):
                    BGR[c] += sep_mat_BGR[c, i]*src[h, w, i]
            for c in range(C):
                dst[h, w, c] = BGR[c]
    return dst

sepia_matrix = np.array([
    [0.393, 0.769, 0.189],
    [0.349, 0.686, 0.168],
    [0.272, 0.534, 0.131]
])
sep_mat_BGR = sepia_matrix[::-1, ::-1]

if __name__ == '__main__':
    import cv2, sys
    from grayscale import report, load_image, img_path

    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            # Alternative decorator syntax
            python_color2sepia = report(n)(python_color2sepia)
        except ValueError:
            msg = 'Argument must be a number.\n'
            msg += 'Reverting to normal run without timing.'
            print(msg)

    fname = 'rain.jpg'
    img, shape = load_image(img_path + fname)
    sepia = python_color2sepia(img, shape)
    cv2.imwrite(img_path + 'python_' + fname.replace('.', '_sepia.'), sepia)
