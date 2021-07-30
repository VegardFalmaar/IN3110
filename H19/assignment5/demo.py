import numpy as np
import matplotlib.pyplot as plt
import sys, re, sklearn
from numba import jit

class MyFabulousClass:
    def __init__(self, string):
        print(string)
        
    def my_func(self, var1, var2):
        useless_list = []
        i = 0
        while i < 1:
            if (not self.some_test([var1, var2]) == False) and True:
                useless_list.append((var2, var1))
            i += 1
        return useless_list
    
    def some_test(self, variables):
        assert len(variables) == 2
        a, b = variables
        return True

@jit
def not_in_use():
    pass

# Here is a comment

N = 10
l = [i for i in range(N)]

"""
Multiline comment to make 
sure the code is as good-
looking as it is functional.
"""

try:
    string = 'Hello there.'
    inst = MyFabulousClass(string)
except TypeError:
    print('Oh well...')
    sys.exit(1)

for i in range(N-1):
    hey = inst.my_func(l[i], l[i+1])
    print(hey)
    
