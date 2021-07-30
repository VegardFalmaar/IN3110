import pytest
import numpy as np
from .python_color2gray import python_color2gray as p_c2g
from .python_color2sepia import python_color2sepia as p_c2s
from .numpy_color2gray import numpy_color2gray as numpy_c2g
from .numpy_color2sepia import numpy_color2sepia as numpy_c2s
from .numba_color2gray import numba_color2gray as numba_c2g
from .numba_color2sepia import numba_color2sepia as numba_c2s
from .grayscale import load_image

def test_grayscale_filter():
    shape = (10, 10, 3)
    img = np.random.randint(256, size=shape, dtype='uint8')
    gray1 = p_c2g(img, shape)
    gray2 = numpy_c2g(img, shape)
    np.testing.assert_array_equal(gray1, gray2)

    # these two lines are responsible for the warning in pytest
    gray3 = numba_c2g(img, shape)
    np.testing.assert_array_equal(gray1, gray3)

    assert gray1.shape == (10, 10)
    idx = (5, 5)
    comp = gray1[idx]
    pixel = img[idx]
    expected = pixel[0]*0.07 + pixel[1]*0.72 + pixel[2]*0.21
    expected = min(255, int(expected))
    assert comp == expected

def test_sepia_filter(): 
    shape = (10, 10, 3)
    img = np.random.randint(256, size=shape, dtype='uint8')
    sepia1 = p_c2s(img, shape)
    sepia2 = numpy_c2s(img, shape)
    np.testing.assert_array_equal(sepia1, sepia2)

    # these two lines are responsible for the warning in pytest
    sepia3 = numba_c2s(img, shape)
    np.testing.assert_array_equal(sepia1, sepia3)

    assert sepia1.shape == (10, 10, 3)
    idx = (5, 5)
    comp = sepia1[idx]
    expected = np.zeros(3)
    pixel = img[idx]

    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sep_mat_BGR = sepia_matrix[::-1, ::-1]

    for i in range(3):
        expected = 0
        for j in range(3):
            expected += sep_mat_BGR[i, j]*pixel[j]
        expected = min(255, int(expected))
        assert comp[i] == expected
