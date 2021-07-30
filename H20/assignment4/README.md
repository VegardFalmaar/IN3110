# IN3110 Assignment 4

To time the code and generate the reports, run
```
python3 time.py
```
This will average the computing time for each function over 5 runs and compare to the results for the other functions. 

The tests of the functions are designed to be run from within the `instapy` directory with
```
pytest -v
```
The `-v` flag for verbosity is optional. The tests pass in python 3.6.9 with numba 0.51.1 and numpy 1.19.1. However, there are some warning messages related to jit. The lines in the test functions related to these warnings are marked with a comment. 

The `instapy` package can be installed from within this directory with
```
pip3 install .
```
This allows you to import `grayscale_image` and `sepia_image` system wide with
```
from instapy.filters import grayscale_image
from instapy.filters import sepia_image
```
or similar. To uninstall the package, run
```
pip3 uninstall instapy
```
