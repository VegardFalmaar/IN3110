import numpy as np

class Complex:
    def __init__(self, a, b):
        assert isinstance(a, (int, float))
        assert isinstance(b, (int, float))
        self.a, self.b = a, b

    def __str__(self):
        string = f'{self.a} + {self.b}i'
        string = string.replace('+ -', '- ')
        string = string.replace('0 + ', '')
        string = string.replace(' + 0i', '')
        string = string.replace('1i', 'i')
        return string
    
    def __repr__(self):
        return f'<Complex object: {self.__str__()}>'

    # Assignment 3.3

    def conjugate(self):
        self.b *= -1
        return self

    def modulus(self):
        return np.sqrt(self.a**2 + self.b**2)

    def __add__(self, other):
        if isinstance(other, Complex):
            a = self.a + other.a
            b = self.b + other.b
            return Complex(a, b)
        elif isinstance(other, (int, float)):
            a = self.a + other
            return Complex(a, self.b)
        elif isinstance(other, complex):
            a = self.a + other.real
            b = self.b + other.imag
            return Complex(a, b)
        else:
            raise ValueError('Unsupported operand type {type(other)}')

    def __sub__(self, other):
        if isinstance(other, Complex):
            a = self.a - other.a
            b = self.b - other.b
            return Complex(a, b) 
        elif isinstance(other, (int, float)):
            a = self.a - other
            return Complex(a, self.b)
        elif isinstance(other, complex):
            a = self.a - other.real
            b = self.b - other.imag
            return Complex(a, b)
        else:
            raise ValueError('Unsupported operand type {type(other)}')

    def __mul__(self, other):
        if isinstance(other, Complex):
            a = self.a * other.a - self.b * other.b
            b = self.a * other.b + self.b * other.a
            return Complex(a, b)
        elif isinstance(other, (int, float)):
            a = other*self.a
            b = other*self.b
            return Complex(a, b)
        elif isinstance(other, complex):
            a = self.a * other.real - self.b * other.imag
            b = self.a * other.imag + self.b * other.real
            return Complex(a, b)
        else:
            raise ValueError('Unsupported operand type {type(other)}')

    def __eq__(self, other):
        # Add isinstance for different shit here too
        if isinstance(other, Complex):
            return (self.a == other.a and self.b == other.b)
        elif isinstance(other, (int, float)):
            return (self.a == other and self.b == 0)
        elif isinstance(other, complex):
            return (self.a == other.real and self.b == other.imag)
        else:
            raise ValueError('Unsupported operand type {type(other)}')

    # Assignment 3.4
    def __radd__(self, other):
        return self.__add__(other)  # equiv to self + other

    def __rsub__(self, other):
        flipped_sign = Complex(-self.a, -self.b)
        return flipped_sign.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    # Optional, possibly useful methods

    # Allows you to write `-a`
    def __neg__(self):
        return Complex(-self.a, -self.b)

    # Make the `complex` function turn this into Python's version of a complex number
    def __complex__(self):
        return complex(self.a, self.b)

