import cv2, time, os

def compare_results(fname, mean_elapsed):
    with open(fname, 'r') as infile:
        t = infile.readlines()[3]
        t = t.split()[0]
        t = float(t)
    algo = fname.split('.')[0]
    if '/' in algo:
        algo = os.path.split(algo)[1]
    algo = algo.replace('_report_', '_')
    line = f'{algo} takes {t/mean_elapsed:.3f} times as long'
    return line

def report(n, rep_path):
    def n_func(func):
        def nn_func(img, shape):
            mean_elapsed = 0
            for i in range(n):
                start = time.time()
                res = func(img, shape)
                stop = time.time()
                elapsed = stop - start
                mean_elapsed += elapsed
            mean_elapsed /= n
            fname = func.__name__.replace('_', '_report_') + '.txt'
            lines = [
                f'Timing: {func.__name__}',
                f'Shape: {shape}',
                f'Average runtime over {n} runs:',
                f'   {mean_elapsed:.4f} seconds'
            ]

            # add comparison with other algos if the resulst exist
            algos = ['python', 'numpy', 'numba']
            algos.remove(func.__name__.split('_')[0])
            for algo in algos:
                other_fname = rep_path + '_'.join([algo] + fname.split('_')[1:])
                if os.path.isfile(other_fname):
                    lines.append(compare_results(other_fname, mean_elapsed))
                else:
                    print('No result file called', other_fname)

            # write the report to file
            with open(rep_path + fname, 'w') as outfile:
                for line in lines:
                    outfile.write(line + '\n')

            return res
        return nn_func
    return n_func

def load_image(fname):
    image = cv2.imread(fname)
    shape = image.shape
    image = image.astype('uint8')
    return image, shape
