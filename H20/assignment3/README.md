# IN3110 Assignment 3

# Word count

`wc.py` is a script that reads the content of a file whose name is given as an input parameter. The number of lines, number of words and number of word characters in the file are then printed to the terminal. The script can be ran with the `*` argument as shown below.
```
python3 wc.py README.md # prints n. of lines, words and chars for README.md
python3 wc.py *         # prints the info of all files in the current dir
python3 wc.py *.py      # prints the info of all .py files in the current dir
```
The `*` of course works with all text files, not just python files.

# Array

The code for the `Array` class is found in `Array.py`. The file `test_Array.py` contains unit tests for the class. The tests are written with pytest and can be run with a simple
```
py.test
```
while in this directory. 

All tests pass with Python 3.6.9 and pytest-5.2.2. I have not had access to other computers with pytest installed to test the code elsewhere. 
