from time import time, sleep

def time_it(func):
    def new_func(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        stop = time()
        diff = stop - start
        return result, diff
    return new_func

@time_it
def slow_func():
    import random
    t = random.randint(1, 4)
    print(f'Sleeping for {t} seconds...')
    sleep(t)
    return

for _ in range(5):
    _, t = slow_func()
    print(f'Time: {t:.4f} s')
    
class CacheOutput:
    def __init__(self, func):
        self.func = func
        self.params_called = []
        self.results = []

    @time_it
    def __call__(self, *args, **kwargs):
        if (args, kwargs) in self.params_called:
            print('\nshortcut')
            i = self.params_called.index((args, kwargs))
            return self.results[i]
        else:
            print('\nslow')
            result = self.func(*args, **kwargs)
            self.params_called.append((args, kwargs))
            self.results.append(result)
            return result

@CacheOutput
def slow_func(x, add=1):
    sleep(2)
    return x + add

print(slow_func(1))
print(slow_func(2))
print(slow_func(1))
print(slow_func(1, add=3))
print(slow_func(1, add=2))
print(slow_func(1, add=3))
