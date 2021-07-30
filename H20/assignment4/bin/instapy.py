import argparse, os, cv2, sys
import numpy as np

parser = argparse.ArgumentParser(description='Apply filter to an image')
parser.add_argument('-f', '--file', type=str,
                    help='the filename of the image to apply filter to')
parser.add_argument('-o', '--out', type=str,
                    help='the output filename')
parser.add_argument('-se', '--sepia',
                    help='select sepia filter',
                    action='store_true')
parser.add_argument('-g', '--gray',
                    help='select gray filter',
                    action='store_true')
# parser.add_argument('-sc', '--scale', type=str,
                    # help='scale factor to resize image')
parser.add_argument('-i', '--implementation', type=str, 
        choices=['python', 'numpy', 'numba'],
        help='the implementation to use')

args = parser.parse_args()

try:
    infile = args.infile
except AttributeError:
    infile = input('Name of image: ')
while not os.path.isfile(infile):
    infile = input('Name of image: ')

try:
    outfile = args.outfile
except AttributeError:
    outfile = input('Name of the output image: ')

if args.gray:
    if args.implementation == 'python':
        from instapy.python_color2gray import python_color2gray as process
    elif args.implementation == 'numpy':
        from instapy.numpy_color2gray import numpy_color2gray as process
    elif args.implementation == 'numba':
        from instapy.numba_color2gray import numba_color2gray as process
    else:
        print('Defaulting to numpy')
        from instapy.numpy_color2gray import numpy_color2gray as process
elif args.sepia:
    if args.implementation == 'python':
        from instapy.python_color2sepia import python_color2sepia as process
    elif args.implementation == 'numpy':
        from instapy.numpy_color2sepia import numpy_color2sepia as process
    elif args.implementation == 'numba':
        from instapy.numba_color2sepia import numba_color2sepia as process
    else:
        print('Defaulting to numpy')
        from instapy.numpy_color2sepia import numpy_color2sepia as process
else:
    msg = 'Please provide a filter argument.\n'
    msg += 'Run \'python3 instapy.py -h\' for directions'
    print(msg)
    sys.exit(1)

img, shape = load_image(infile)
img = process(img, shape)
cv2.imwrite(outfile, img)
