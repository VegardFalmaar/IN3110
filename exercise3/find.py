import sys
import os

string, dr = sys.argv[1:]
fnames = []
for root, dr, files in os.walk(dr, topdown=True):
    for fname in files:
        if string in fname:
            full_fname = os.path.join(root, fname)
            fnames.append(full_fname)
fnames.sort()
for fname in fnames:
    print(fname)
