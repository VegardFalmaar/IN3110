
class Array:
    # Assignment 3.3  

    def __init__(self, shape, *values):
        """
        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n 
                elements will have shape = (n,).
            *values: The values in the array. These should all be the same 
                data type. Either numeric or boolean.

        Raises:
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """
        if isinstance(values[0], (tuple, list)):
            values = values[0]
        length = shape[0]
        if len(shape) > 1:
            for e in shape[1:]:
                length *= e
        if not length == len(values):
            raise ValueError(
                f'Shape {shape} does not match number of values {len(values)}.')
        if length == 0:
            raise ValueError('Cannot initialize empty array')
        data_type = type(values[0])
        for e in values[1:]:
            if not type(e) == data_type:
                raise ValueError(
                    f'Types {data_type} and {type(e)} can not be combined.')

        self.values = values
        self.shape = shape
        self.data_type = data_type
        self.tolerance = 1E-8

    def __getitem__(self, index):
        """Return the item of the array given by idx.

        Args:
            index (int, tuple of ints): index to the element

        Returns:
            element: the element at the provided index of the array.
        """
        if len(self.shape) == 1:
            return self.values[index]
        else:
            return Array((self.shape[1:]), self.values[index*self.shape[1]:(index+1)*self.shape[1]])

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.
        """
        if len(self.shape) == 1:
            out =  '[' + ', '.join([str(e) for e in self.values]) + ']'
        elif len(self.shape) == 2:
            out = '['
            for i in range(self.shape[0]):
                out += '['
                for j in range(self.shape[1]):
                    out += f'{self[i][j]}, '
                out = out[:-2]
                out += '],\n '
            out = out[:-3] + ']'
        return out

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        Args:
            other (Array, float, int): The array or number to add element-wise 
                to this array.

        Returns:
            Array: the sum as a new array.

        """
        if isinstance(other, (int, float)):
            return Array(self.shape, [e + other for e in self.values])
        elif type(self) == type(other):
            if self.data_type == other.data_type:
                if self.shape == other.shape:
                    return Array(self.shape, 
                            [i + e for i, e in zip(self.values, other.values)])
                else:
                    msg = f'Add/subtract failed: Shape {self.shape} does not ' +\
                            f'match shape {other.shape}'
                    raise ValueError(msg)
            else:
                msg = 'Add/subtract failed: Cannot combine elements of ' +\
                        f'types {self.data_type}, {other.data_type}'
                raise ValueError(msg)
        else:
            return NotImplemented

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        Args:
            other (Array, float, int): The array or number to add element-wise 
                to this array.

        Returns:
            Array: the sum as a new array.
        """
        return self + other

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        Args:
            other (Array, float, int): The array or number to subtract
                element-wise from this array.

        Returns:
            Array: the difference as a new array.
        """
        return self + (-other)

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        Args:
            other (Array, float, int): The array or number being subtracted
                from.

        Returns:
            Array: the difference as a new array.
        """
        print('rsub called')
        return (-self) + other 

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        Args:
            other (Array, float, int): The array or number to multiply
                element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.
        """
        if isinstance(other, (int, float)):
            return Array(self.shape, [e * other for e in self.values])
        elif type(self) == type(other):
            if self.data_type == other.data_type:
                if self.shape == other.shape:
                    return Array(self.shape, 
                            [i * e for i, e in zip(self.values, other.values)])
                else:
                    msg = f'Multiplication failed: Shape {self.shape} does ' +\
                            f'not match shape {other.shape}'
                    raise ValueError(msg)
            else:
                msg = 'Multiplication failed: Cannot combine elements of ' +\
                        f'types {self.data_type}, {other.data_type}'
                raise ValueError(msg)
        else:
            return NotImplemented

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        Args:
            other (Array, float, int): The array or number to multiply
                element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.
        """
        return self*other

    def __neg__(self):
        """Tells the class how to interpret -Array.
        
        Returns:
            Array: new array with all the signs flipped
        """
        if self.data_type == float or self.data_type == int:
            return Array(self.shape, [-i for i in self.values])
        else:
            raise ValueError(
                f'Cannot interpret negative values of objects of type {self.data_type}')

    def __pow__(self, exp):
        """Tells the class how to interpret Array**exp.

        Args:
            exp (int, float, Array): the exponent
        
        Returns:
            Array: new array with all the elements raise to power exp.
        """
        if isinstance(exp, (int, float)):
            if (self.data_type == float or self.data_type == int):
                return Array(self.shape, [i**exp for i in self.values])
            else:
                raise ValueError(
                    f'Cannot raise values of objects of type {self.data_type} to a higher power')
        elif (type(self) == type(exp)) and (self.shape == exp.shape):
            return Array(self.shape, [i**e for i, e in zip(self.values, exp.values)])


    def __eq__(self, other):
        """Compares an Array with another Array.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal. False otherwise.
        """
        if type(other) != type(self):
            return False
        if (self.shape != other.shape) or (self.data_type != other.data_type):
            return False
        for i, e in zip(self.values, other.values):
            if isinstance(i, float):
                if abs(i - e) > self.tolerance:
                    return False
            elif i != e:
                return False
        return True

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        Args:
            other (Array, float, int): The array or number to compare with this
                array.

        Returns:
            Array: An array of booleans with True where the two arrays match
                and False where they do not.
                   Or if `other` is a number, it returns True where the array
                is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        if isinstance(other, int):
            for i in self.values:
                if i != other:
                    return False
            return True
        elif isinstance(other, float):
            for i in self.values:
                if abs(i - other) > self.tolerance:
                    return False
            return True
        elif type(self) == type(other):
            if (self.shape != other.shape):
                raise ValueError(f'Shape{self.shape} does not match {other.shape}.')
            elif (self.data_type != other.data_type):
                return False
            for i, e in zip(self.values, other.values):
                if isinstance(i, float) and abs(i - e) > self.tolerance:
                    return False
                elif i != e:
                    return False
            return True
        else:
            return NotImplemented
    
    def mean(self):
        """Computes the mean of the array

        Returns:
            float: The mean of the array values.
        """
        if not ((self.data_type == int) or (self.data_type == float)):
            raise ValueError(
                'Cannot compute the mean of array with types {self.data_type}.')
        return sum(self.values)/sum(self.shape)

    def variance(self):
        """Computes the variance of the array

        Only needs to work for numeric data types.
        The variance is computed as: mean((x - x.mean())**2)

        Returns:
            float: The mean of the array values.
        """
        return ((self - self.mean())**2).mean()

    def min_element(self):
        """Returns the smallest value of the array.

        Returns:
            float: The value of the smallest element in the array.

        """
        if not ((self.data_type == int) or (self.data_type == float)):
            raise ValueError(
                'Cannot compute the mean of array with types {self.data_type}.')
        min_e = self.values[0]
        for e in self.values[1:]:
            if e < min_e:
                min_e = e
        return float(min_e)
