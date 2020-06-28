import sys

def print_info(fn):
    """Print number of lines, words and characters 
    of file with filename given as argument.
    """
    info = [0]*3    # lines, words, chars
    with open(fn, 'r') as infile:
        for line in infile:
            info[0] += 1
            words = line.split()
            info[1] += len(words)
            string = ''.join(words)
            info[2] += len(string)
    print(' '.join([str(num) for num in info]) + ' ' + fn)

for fn in sys.argv[1:]:
    if fn[-4:] == '.pdf':
        print(f'Cant\'t display information for {fn}.')
    else:
        print_info(fn)
