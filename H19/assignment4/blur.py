import argparse
import os
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='Blur an image')
parser.add_argument('infile', nargs='?', type=str, 
                    help='the path to the image you would like to blur')
parser.add_argument('outfile', nargs='?', type=str, 
                    help='the path where to save the blurred image')
parser.add_argument('-m', '--method', type=str, metavar='method',
                help='the method to use: "1" for python, "2" for numpy, "3" for numba. Default is "2"')
parser.add_argument('--verify', 
                    help='verify that all three impementations yield the same result',
                    action='store_true')

args = parser.parse_args()

if args.infile:
    infile = args.infile
else:
    infile = input('Path to image: ')
assert os.path.isfile(infile)

if args.outfile:
    outfile = args.outfile
else:
    outfile = input('Path to save image: ')

if not args.method:
    from blur_2 import blur_image
    print('Defaulting to numpy vectorized method')
elif args.method == '1':
    from blur_1 import blur_image
elif args.method == '2':
    from blur_2 import blur_image
elif args.method == '3':
    from blur_3 import blur_image
else:
    raise ValueError(f'Invalid argument to --method: {args.method}.')

blurred = blur_image(infile)
cv2.imwrite(outfile, blurred)

if args.verify:
    print('\nVerifying the three implementations...')
    import blur_1, blur_2, blur_3
    fname = 'beatles.jpg'
    blurred_1 = blur_1.blur_image(fname)
    blurred_2 = blur_2.blur_image(fname)
    blurred_3 = blur_3.blur_image(fname)
    np.testing.assert_array_equal(blurred_1, blurred_2)
    np.testing.assert_array_equal(blurred_1, blurred_3)
    print('All three implementations yield the same result')
