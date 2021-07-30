from Array import Array
import pytest

@pytest.mark.parametrize('a,b,c,d,e,f', 
        [(0, -3, 4, 3, 2, 1), 
            (-1.0, 7.0, -0.1, 3.9, 90.2, 1.3), 
            (False, True, True, False, True, False)])
def test_print_data_types(a, b, c, d, e, f):
    arr = Array((3,), a, b, c)
    assert str(arr) == f'[{a}, {b}, {c}]'
    arr = Array((2, 3), a, b, c, d, e, f)
    assert str(arr) == f'[[{a}, {b}, {c}],\n [{d}, {e}, {f}]]'

@pytest.mark.parametrize('a,b,c',
        [(0, -3, 4), (-1.0, 7.0, -0.1), (True, True, False)])
def test_instantiation_list(a, b, c):
    assert Array((3,), a, b, c) == Array((3,), [a, b, c])
    assert Array((2,), a, b) == Array((2,), [a, b])

@pytest.mark.parametrize('a,b,c',
        [(0, -3, 4), (-1.0, 7.0, -0.1), (True, True, False)])
def test_bad_instantiation_size(a, b, c):
    with pytest.raises(ValueError):
        assert Array((0,), a, b, c)
        assert Array((1,), a, b)
        assert Array((4,), a, b, c)
        assert Array((3, 2), a, b, c)
        assert Array((2, 2), a, b, c)

@pytest.mark.parametrize('a,b,c,d,e,f',
        [(0, -3.0, 4, 4, 3.8, 3), 
            (-1.0, 7, True, False, 3.4, 1), 
            (True, 0.1, False, True, 2, 54)])
def test_bad_instantiation_values(a, b, c, d, e, f):
    with pytest.raises(ValueError):
        assert Array((3,), a, b, c)
        assert Array((3,), a, b, c)
        assert Array((3,), a, b, c)
        assert Array((3, 2), a, b, c, d, e, f)
        assert Array((2, 3), a, b, c, d, e, f)

@pytest.mark.parametrize('a', [0, 45])
@pytest.mark.parametrize('b', [42, -543])
@pytest.mark.parametrize('c', [1, -43])
@pytest.mark.parametrize('d', [-234, -3])
@pytest.mark.parametrize('e', [-12, 34])
@pytest.mark.parametrize('f', [54, -3])
def test_addition_integers(a, b, c, d, e, f):
    assert (Array((4,), a, b, c, d) + Array((4,), d, a, b, c)) == Array((4,), a+d, b+a, c+b, d+c)
    assert (Array((2,), a, b) + Array((2,), c, d)) + Array((2,), b, c) == Array((2,), a+b+c, b+d+c)
    assert a + Array((3,), b, c, d) == Array((3,), a+b, a+c, a+d)
    assert Array((3,), b, c, d) + a == Array((3,), a+b, a+c, a+d)
    assert a + Array((2, 2), b, c, d, e) == Array((2, 2), a+b, a+c, a+d, a+e)
    assert Array((2, 2), b, c, d, e) + a == Array((2, 2), a+b, a+c, a+d, a+e)
    assert Array((2, 3), a, b, c, d, e, f) + Array((2, 3), f, a, b, c, d, e) == Array((2, 3), a+f, b+a, c+b, d+c, e+d, f+e)

@pytest.mark.parametrize('a', [0.0, 1.2345])
@pytest.mark.parametrize('b', [42.3, -543.12])
@pytest.mark.parametrize('c', [1.5, -43.7])
@pytest.mark.parametrize('d', [-234.23, -3.09])
@pytest.mark.parametrize('e', [234.2, 432.1])
@pytest.mark.parametrize('f', [-12.3, -4.2])
def test_addition_floats(a, b, c, d, e, f):
    assert (Array((4,), a, b, c, d) + Array((4,), d, a, b, c)) == Array((4,), a+d, b+a, c+b, d+c)
    assert (Array((2,), a, b) + Array((2,), c, d)) + Array((2,), b, c) == Array((2,), a+b+c, b+d+c)
    assert a + Array((3,), b, c, d) == Array((3,), a+b, a+c, a+d)
    assert Array((3,), b, c, d) + a == Array((3,), a+b, a+c, a+d)
    assert a + Array((2, 2), b, c, d, e) == Array((2, 2), a+b, a+c, a+d, a+e)
    assert Array((2, 2), b, c, d, e) + a == Array((2, 2), a+b, a+c, a+d, a+e)
    assert Array((2, 3), a, b, c, d, e, f) + Array((2, 3), f, a, b, c, d, e) == Array((2, 3), a+f, b+a, c+b, d+c, e+d, f+e)

@pytest.mark.parametrize('a', [0, 45])
@pytest.mark.parametrize('b', [42, -543])
@pytest.mark.parametrize('c', [1, -43])
@pytest.mark.parametrize('d', [-234, -3])
@pytest.mark.parametrize('e', [-12, 34])
@pytest.mark.parametrize('f', [54, -3])
def test_subtraction_integers(a, b, c, d, e, f):
    assert (Array((4,), a, b, c, d) - Array((4,), d, a, b, c)) == Array((4,), a-d, b-a, c-b, d-c)
    assert (Array((2,), a, b) - Array((2,), c, d)) - Array((2,), b, c) == Array((2,), a-b-c, b-d-c)
    assert a - Array((3,), b, c, d) == Array((3,), a-b, a-c, a-d)
    assert Array((3,), b, c, d) - a == Array((3,), b-a, c-a, d-a)
    assert a - Array((2, 2), b, c, d, e) == Array((2, 2), a-b, a-c, a-d, a-e)
    assert Array((2, 2), b, c, d, e) - a == Array((2, 2), b-a, c-a, d-a, e-a)
    assert Array((2, 3), a, b, c, d, e, f) - Array((2, 3), f, a, b, c, d, e) == Array((2, 3), a-f, b-a, c-b, d-c, e-d, f-e)

@pytest.mark.parametrize('a', [0.0, 1.2345])
@pytest.mark.parametrize('b', [42.3, -543.12])
@pytest.mark.parametrize('c', [1.5, -43.7])
@pytest.mark.parametrize('d', [-234.23, -3.09])
@pytest.mark.parametrize('e', [234.2, 432.1])
@pytest.mark.parametrize('f', [-12.3, -4.2])
def test_subtraction_floats(a, b, c, d, e, f):
    assert (Array((4,), a, b, c, d) - Array((4,), d, a, b, c)) == Array((4,), a-d, b-a, c-b, d-c)
    assert (Array((2,), a, b) - Array((2,), c, d)) - Array((2,), b, c) == Array((2,), a-b-c, b-d-c)
    assert a - Array((3,), b, c, d) == Array((3,), a-b, a-c, a-d)
    assert Array((3,), b, c, d) - a == Array((3,), b-a, c-a, d-a)
    assert a - Array((2, 2), b, c, d, e) == Array((2, 2), a-b, a-c, a-d, a-e)
    assert Array((2, 2), b, c, d, e) - a == Array((2, 2), b-a, c-a, d-a, e-a)
    assert Array((2, 3), a, b, c, d, e, f) - Array((2, 3), f, a, b, c, d, e) == Array((2, 3), a-f, b-a, c-b, d-c, e-d, f-e)

@pytest.mark.parametrize('a', [0, 45])
@pytest.mark.parametrize('b', [42, -543])
@pytest.mark.parametrize('c', [1, -43])
@pytest.mark.parametrize('d', [-234, -3])
@pytest.mark.parametrize('e', [-12, 34])
@pytest.mark.parametrize('f', [54, -3])
def test_multiplication_integers(a, b, c, d, e, f):
    assert a*Array((3,), b, c, d) == Array((3,), a*b, a*c, a*d)
    assert Array((3,), b, c, d) * a == Array((3,), a*b, a*c, a*d)
    assert (Array((4,), a, b, c, d) * Array((4,), d, a, b, c)) == Array((4,), a*d, b*a, c*b, d*c)
    assert a * Array((3, 2), a, b, c, d, e, f) == Array((3, 2), a*a, a*b, a*c, a*d, a*e, a*f)
    assert Array((2, 3), a, b, c, d, e, f) * a == Array((2, 3), a*a, b*a, c*a, d*a, e*a, f*a)
    assert Array((2, 3), a, b, c, d, e, f) * Array((2, 3), f, a, b, c, d, e) == Array((2, 3), a*f, b*a, c*b, d*c, e*d, f*e)

@pytest.mark.parametrize('a', [0.0, 1.2345])
@pytest.mark.parametrize('b', [42.3, -543.12])
@pytest.mark.parametrize('c', [1.5, -43.7])
@pytest.mark.parametrize('d', [-234.23, -3.09])
@pytest.mark.parametrize('e', [234.2, 432.1])
@pytest.mark.parametrize('f', [-12.3, -4.2])
def test_multiplication_floats(a, b, c, d, e, f):
    assert a*Array((3,), b, c, d) == Array((3,), a*b, a*c, a*d)
    assert Array((3,), b, c, d) * a == Array((3,), a*b, a*c, a*d)
    assert (Array((4,), a, b, c, d) * Array((4,), d, a, b, c)) == Array((4,), a*d, b*a, c*b, d*c)
    assert a * Array((3, 2), a, b, c, d, e, f) == Array((3, 2), a*a, a*b, a*c, a*d, a*e, a*f)
    assert Array((2, 3), a, b, c, d, e, f) * a == Array((2, 3), a*a, b*a, c*a, d*a, e*a, f*a)
    assert Array((2, 3), a, b, c, d, e, f) * Array((2, 3), f, a, b, c, d, e) == Array((2, 3), a*f, b*a, c*b, d*c, e*d, f*e)

@pytest.mark.parametrize('a', [0, 45])
@pytest.mark.parametrize('b', [42, -543])
@pytest.mark.parametrize('c', [1, -43])
@pytest.mark.parametrize('d', [-234, -3])
@pytest.mark.parametrize('e', [-234, -3])
@pytest.mark.parametrize('f', [-12, 34])
def test_equality_integers(a, b, c, d, e, f):
    assert (Array((2,), a, b) == Array((2,), c, d)) == (a == c and b == d)
    assert (Array((4,), a, b, c, d) == Array((4,), a, b, c, d))
    assert not (Array((3,), a, b, c) == Array((4,), a, b, c, d))
    assert not (Array((4,), a, b, c, d) == a)
    assert Array((3, 2), a, b, c, d, e, f) == Array((3, 2), a, b, c, d, e, f)
    assert not Array((3, 2), a, b, c, d, e, f) == Array((2, 3), a, b, c, d, e, f)

@pytest.mark.parametrize('a', [0.0, 1.2345])
@pytest.mark.parametrize('b', [42.3, -543.12])
@pytest.mark.parametrize('c', [1.5, -43.7])
@pytest.mark.parametrize('d', [-234.23, -3.09])
@pytest.mark.parametrize('e', [-12.3, -4.2])
@pytest.mark.parametrize('f', [42.3, -543.12])
def test_equality_floats(a, b, c, d, e, f):
    assert (Array((2,), a, b) == Array((2,), c, d)) == (abs(a - c) < 1E-8 and abs(b - d) < 1E-8)
    assert (Array((4,), a, b, c, d) == Array((4,), a, b, c, d))
    assert not (Array((3,), a, b, c) == Array((4,), a, b, c, d))
    assert not (Array((4,), a, b, c, d) == a)
    assert Array((3, 2), a, b, c, d, e, f) == Array((3, 2), a, b, c, d, e, f)
    assert not Array((3, 2), a, b, c, d, e, f) == Array((2, 3), a, b, c, d, e, f)

@pytest.mark.parametrize('a', [True, False])
@pytest.mark.parametrize('b', [True, False])
@pytest.mark.parametrize('c', [True, False])
@pytest.mark.parametrize('d', [True, False])
@pytest.mark.parametrize('e', [False, False])
@pytest.mark.parametrize('f', [True, True])
def test_equality_booleans(a, b, c, d, e, f):
    assert (Array((2,), a, b) == Array((2,), c, d)) == (a == c and b == d)
    assert (Array((4,), a, b, c, d) == Array((4,), a, b, c, d))
    assert not (Array((3,), a, b, c) == Array((4,), a, b, c, d))
    assert not (Array((4,), a, b, c, d) == a)
    assert Array((3, 2), a, b, c, d, e, f) == Array((3, 2), a, b, c, d, e, f)
    assert not Array((3, 2), a, b, c, d, e, f) == Array((2, 3), a, b, c, d, e, f)

@pytest.mark.parametrize('a', [0, 45, -2])
@pytest.mark.parametrize('b', [42, -543, 2])
@pytest.mark.parametrize('c', [1, -43, 654])
@pytest.mark.parametrize('d', [-234, -3, -24])
def test_is_equal_integers(a, b, c, d):
    assert (Array((2,), a, b).is_equal(Array((2,), c, d))) == (a == c and b == d)
    assert (Array((4,), a, b, c, d).is_equal(Array((4,), a, b, c, d)))
    assert Array((3,), a, a, a).is_equal(a)
    assert Array((3, 2), a, a, a, a, a, a).is_equal(a)
    assert Array((2, 2), a, b, c, d).is_equal(Array((2, 2), a, b, c, d))
    assert Array((2, 2), a, b, c, d).is_equal(Array((2, 2), c, d, a, b)) == Array((2,), a, b).is_equal(Array((2,), c, d))

@pytest.mark.parametrize('a', [0.0, 1.2345, -2.45])
@pytest.mark.parametrize('b', [42.3, -543.12, 2.0])
@pytest.mark.parametrize('c', [1.5, -43.7, 654.54])
@pytest.mark.parametrize('d', [-234.23, -3.09, -24.1])
def test_is_equal_floats(a, b, c, d):
    assert (Array((2,), a, b).is_equal(Array((2,), c, d))) == (a == c and b == d)
    assert (Array((4,), a, b, c, d).is_equal(Array((4,), a, b, c, d)))
    assert Array((3,), a, a, a).is_equal(a)
    assert Array((3, 2), a, a, a, a, a, a).is_equal(a)
    assert Array((2, 2), a, b, c, d).is_equal(Array((2, 2), a, b, c, d))
    assert Array((2, 2), a, b, c, d).is_equal(Array((2, 2), c, d, a, b)) == Array((2,), a, b).is_equal(Array((2,), c, d))

@pytest.mark.parametrize('a', [True, False, False])
@pytest.mark.parametrize('b', [True, False, False])
@pytest.mark.parametrize('c', [True, False, False])
@pytest.mark.parametrize('d', [True, False, False])
def test_is_equal_booleans(a, b, c, d):
    assert (Array((2,), a, b).is_equal(Array((2,), c, d))) == (a == c and b == d)
    assert (Array((4,), a, b, c, d).is_equal(Array((4,), a, b, c, d)))
    assert Array((3,), a, a, a).is_equal(a)
    assert Array((3, 2), a, a, a, a, a, a).is_equal(a)
    assert Array((2, 2), a, b, c, d).is_equal(Array((2, 2), a, b, c, d))
    assert Array((2, 2), a, b, c, d).is_equal(Array((2, 2), c, d, a, b)) == Array((2,), a, b).is_equal(Array((2,), c, d))

@pytest.mark.parametrize('a', [0, 45, -2])
@pytest.mark.parametrize('b', [42, -543, 2])
@pytest.mark.parametrize('c', [1, -43, 654])
@pytest.mark.parametrize('d', [-234, -3, -24])
def test_mean_integers(a, b, c, d):
    assert abs(Array((4,), a, b, c, d).mean() - (a + b + c + d)/4) < 1E-8
    assert abs(Array((2, 2), a, b, c, d).mean() - (a + b + c + d)/4) < 1E-8

@pytest.mark.parametrize('a', [0.0, 1.2345, -2.45])
@pytest.mark.parametrize('b', [42.3, -543.12, 2.0])
@pytest.mark.parametrize('c', [1.5, -43.7, 654.54])
@pytest.mark.parametrize('d', [-234.23, -3.09, -24.1])
def test_mean_floats(a, b, c, d):
    assert (Array((4,), a, b, c, d).mean() - (a + b + c + d)/4) < 1E-8
    assert abs(Array((2, 2), a, b, c, d).mean() - (a + b + c + d)/4) < 1E-8

@pytest.mark.parametrize('a, b, c, d',
        [(1, 2, 3, 23), (-67, -23, 0, 23), (0, 234, 43, 1)])
def test_min_element_integers(a, b, c, d):
    assert Array((3,), a, b, c).min_element() == a
    assert Array((3,), b, a, c).min_element() == a
    assert Array((3,), b, c, a).min_element() == a
    assert Array((2, 2), d, b, c, a).min_element() == a
    assert Array((2, 2), a, b, c, a).min_element() == a

@pytest.mark.parametrize('a, b, c, d',
        [(1.1, 2.1, 3.9, 10.3), (-67.0, -23.2, 0.2, 10.3), (0.3, 234.4, 43.7, 0.4)])
def test_min_element_floats(a, b, c, d):
    assert Array((3,), a, b, c).min_element() == a
    assert Array((3,), b, a, c).min_element() == a
    assert Array((3,), b, c, a).min_element() == a
    assert Array((2, 2), d, b, c, a).min_element() == a
    assert Array((2, 2), a, b, c, a).min_element() == a
