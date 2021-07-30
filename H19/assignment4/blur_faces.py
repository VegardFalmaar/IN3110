import numpy as np
import matplotlib.pyplot as plt
from blur_3 import convolve
import cv2, time

def blur_beyond_recognition(fname):
    image = cv2.imread(fname)
    faces = recognize_faces(image)
    i = 0
    while len(faces) > 0:
        image, rectangles = blur_faces(image, faces)
        faces = recognize_faces(image)
        if i%5 == 0:
            cv2.imwrite(f'blurred_faces/blur_{i}.jpg', rectangles)
        i += 1

def recognize_faces(image): 
    faceCascade = cv2.CascadeClassifier(
        'haarcascade_frontalface_default.xml'
    )
    faces = faceCascade.detectMultiScale(
        image,
        scaleFactor=1.025,
        minNeighbors=5,
        minSize=(30, 30)
    )
    num = len(faces)
    word = 'face' if num == 1 else 'faces'
    print(f'Found {num} {word}!')
    return faces

def blur_faces(image, faces): 
    rectangles = image.copy()
    for (x, y, w, h) in faces:
        rectangles = cv2.rectangle(rectangles, 
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2)
        image = blur_section(image, (x, y, w, h))
    return image, rectangles

def blur_section(image, (x, y, w, h)):
    """Blur the section of the image given as parameter using numpy vectorized operations.
    input:
        image: str, 
            the path to the image to blur
    output:
        dst: nd-array of dimensions (H, W, 3), where
                H is the height of the picture (pixels) and
                W is the width of the picture (pixels),
            The blurred image
    """
    shape = (y + h - 1, x + w - 1, 3)
    start = (y, x)
    image = image.astype('uint32')
    dst = image.copy()
    blurred = convolve(image, dst, shape, start=start, shift=0)
    blurred = blurred.astype('uint8')
    return blurred

fname = 'beatles.jpg'
blur_beyond_recognition(fname)
