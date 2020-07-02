from complex import Complex as C

def test_addition():
    assert (C(1, 2) + C(3, 5) == C(4, 7))
    assert (C(0, 2) + C(0, 1) == C(0, 3))
    assert (C(1, 0) + C(3, 5) == C(4, 5))
    assert (C(1, -1) + C(-4, 5) == C(-3, 4))
    assert (C(1, 3) + 3 == C(4, 3))
    assert (C(1, 3) + (-3) == C(-2, 3))
    assert (5 + C(1, 3) == C(6, 3))
    assert ((-9) + C(1, 3) == C(-8, 3))

def test_subtraction(): 
    assert (C(3, 5) - C(3, 5) == C(0, 0))
    assert (C(3, 5) - C(1, 2) == C(2, 3))
    assert (C(0, 2) - C(0, 1) == C(0, 1))
    assert (C(1, 0) - C(3, 5) == C(-2, -5))
    assert (C(1, -1) - C(-4, 5) == C(5, -6))
    assert (C(1, 3) - 3 == C(-2, 3))
    assert (C(1, 3) - (-3) == C(4, 3))
    assert (5 - C(1, 3) == C(4, -3))
    assert ((-9) - C(1, 3) == C(-10, -3))

def test_multiplication():
    # C number * complex number
    assert (C(1, 2) * C(3, 5) == C(-7, 11))
    assert (C(0, 2) * C(0, 1) == C(-2, 0))
    assert (C(1, 0) * C(3, 5) == C(3, 5))
    assert (C(1, -1) * C(-4, 5) == C(1, 9))
    # C number * constant
    assert (2 * C(3, 5) == C(6, 10))
    assert (C(2, -1) * (-3) == C(-6, 3))

def test_conjugate():
    assert (C(1, 2).conjugate() == C(1, -2))
    assert (C(0, 1).conjugate() == C(0, -1))
    assert (C(-5, 0).conjugate() == C(-5, 0))
    assert (C(-1, -2).conjugate() == C(-1, 2))

def test_modulus():
    assert (C(3, 4).modulus() == 5)
    assert (C(3, -4).modulus() == 5)
    assert (C(-5, -12).modulus() == 13)

def test_equality():
    assert (C(-2, 1) == C(-2, 1))
    assert (C(0, 0) == C(0, 0))
    assert not (C(1, 2) == C(5, -2))

