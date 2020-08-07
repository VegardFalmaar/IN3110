import numpy as np
import matplotlib.pyplot as plt
import sys, re, sklearn

def my_func(var1, var2):
    useless_list = []
    i = 0
    while i < 1:
        if (not some_test([var1, var2]) == False) and True:
            useless_list.append((var2, var1))
        i += 1
    return useless_list

def some_test(variables):
    assert len(variables) == 2
    a, b = variables
    return True

# Here is a comment

N = 10
l = [i for i in range(N)]

"""
Multiline comment to make 
sure the code is as good-
looking as it is functional.
"""

for i in range(N - 1):
    hey = my_func(l[i], l[i + 1])
    print(hey)
    
