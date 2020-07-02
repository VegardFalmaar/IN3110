The implementation of the "Complex" class for representing complex
numbers is in the file "complex.py".

There are two files containing tests of the implementation:

In "test_complex_direct.py" there are direct tests of various use
cases for the class, calculated manually.

In "test_complex_property.py" there are tests running multiple 
times with random input checking the properties of addition, 
subtraction and multiplication. Conjugation and equality are
also tested here.

The intended way to run all tests in the project is with pytest.
Simply run "pytest" while in this directory.
"pytest -v" gives a more verbose output listing all the separate tests.
