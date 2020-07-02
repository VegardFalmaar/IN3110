from random import randint
from complex import Complex as C

def random_input(func):
    def new_func():
        for i in range(10000):
            a, b, c, d, e, f = [randint(-10, 10) for i in range(6)]
            func(a, b, c, d, e, f)
    return new_func
        
@random_input
def test_add_commutative(a, b, c, d, *_):
    assert (C(a, b) + C(c, d) == C(c, d) + C(a, b))
    assert (C(a, b) + complex(c, d) == C(c, d) + C(a, b))
    assert (C(a, b) + c == c + C(a, b))

@random_input
def test_add_zero(a, b, *_):
    assert (C(a, b) + C(0, 0) == C(a, b))
    assert (C(a, b) + complex(0, 0) == C(a, b))
    assert (C(a, b) + 0 == C(a, b))

@random_input
def test_add1_twice_is_add2(a, b, *_):
    assert (C(a, b) + 1 + 1 == C(a, b) + C(2, 0))
    assert (C(a, b) + complex(0, 1) + complex(0, 1) == C(a, b) + complex(0, 2))

@random_input
def test_sub_not_commutative(a, b, c, d, *_):
    assert (C(a, b) - C(c, d) == -C(c, d) + C(a, b))
    assert (a - C(c, d) == -C(c, d) + a)
    assert (C(a, b) - complex(c, d) == -complex(c, d) + C(a, b))

@random_input
def test_sub_zero(a, b, *_):
    assert (C(a, b) - C(0, 0) == C(a, b))
    assert (C(a, b) - complex(0, 0) == C(a, b))
    assert (C(a, b) - 0 == C(a, b))

@random_input
def test_sub1_twice_is_sub2(a, b, *_):
    assert (C(a, b) - 1 - 1 == C(a, b) - 2)
    assert (C(a, b) - complex(0, 1) - complex(0, 1) == C(a, b) - complex(0, 2))

@random_input
def test_mul_commutative(a, b, c, d, *_):
    assert (C(a, b) * C(c, d) == C(c, d) * C(a, b))
    assert (C(a, b) * c == c * C(a, b))
    assert (C(a, b) * complex(c, d) == complex(c, d) * C(a, b))

@random_input
def test_mul_zero(a, b, *_):
    assert (C(a, b) * C(0, 0) == 0)
    assert (C(a, b) * complex(0, 0) == 0)
    assert (C(a, b) * 0 == 0)

@random_input
def test_mul_assosiative(a, b, c, d, e, f):
    assert ((C(a, b) * C(c, d)) * C(e, f) == C(a, b) * (C(c, d) * C(e, f)))

@random_input
def test_mul_identity(a, b, *_):
    assert (C(a, b) * 1 == C(a, b))

@random_input
def test_mul_distributive(a, b, c, d, e, f):
    assert ((C(a, b) + C(c, d)) * C(e, f) == C(a, b) * C(e, f) + C(c, d) * C(e, f))

@random_input
def test_equality(a, b, *_):
    assert (C(a, b) == C(a, b))
    assert (C(a, b) == complex(a, b))
    assert (C(a, 0) == a)

@random_input
def test_conjugation(a, b, *_):
    assert (C(a, b).conjugate() == C(a, -b))
    assert (C(a, 0).conjugate() == a)
    assert (C(0, a).conjugate() == complex(0, -a)) 
    
"""
import pytest
@pytest.mark.randomize(i1=int, min_num=0, max_num=2, ncalls=5)
def test_generate_int_anns(*args, **kwargs):
    print(args)
    print(kwargs)

@pytest.mark.randomize(i1=int, min_num=0, max_num=4, ncalls=5)
def test_int(i1):
    pass

@pytest.mark.randomize(i1=int, i2=int, i3=int, i4=int, ncalls=20)
def test_add_assosiative(a, b, c, d):
    assert (C(a, b) + C(c, d) == C(c, d) + C(a, b))
    assert (C(a, b) + complex(c, d) == C(c, d) + C(a, b))
    assert (C(a, b) + c == c + C(a, b))

@pytest.mark.randomize(ncalls=20)
def test_add_zero(a: int, b:int):
    assert (C(a, b) + C(0, 0) == C(a, b))
    assert (C(a, b) + complex(0, 0) == C(a, b))
    assert (C(a, b) + 0 == C(a, b))

@pytest.mark.randomize(ncalls=20)
def test_add1_twice_is_add2(a: int, b:int):
    assert (C(a, b) + 1 + 1 == C(a, b) + 2)
    assert (C(a, b) + complex(0, 1) + complex(0, 1) == C(a, b) + complex(0, 2))

@pytest.mark.randomize(ncalls=20)
def test_sub_assosiative(a: int, b:int, c:int, d:int):
    assert not (C(a, b) - C(c, d) == C(c, d) - C(a, b))
    assert (C(a, b) - C(c, d) == -C(c, d) + C(a, b))

"""
