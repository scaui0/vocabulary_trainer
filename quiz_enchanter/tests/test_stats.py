from stats import Tries


def test_quote():
    assert Tries(1, 1).quote == 50
    assert Tries(3, 1).quote == 75
    assert Tries(1, 1).quote == Tries(5, 5).quote


def test_compare():
    assert Tries(1, 1) == Tries(1, 1)
    assert Tries(1, 5) != Tries(2, 5)
    assert Tries(1, 5) < Tries(2, 5)
    assert Tries(1, 5) <= Tries(1, 5)
    assert Tries(4, 5) > Tries(3, 5)
    assert Tries(4, 5) >= Tries(4, 5)


def test_state_add():
    assert Tries(1, 0) + Tries(1, 0) == Tries(2, 0)
    assert Tries(0, 1) + Tries(1, 0) == Tries(1, 1)


def test_state_sub():
    assert Tries(1, 0) - Tries(1, 0) == Tries(0, 0)
    assert Tries(5, 2) - Tries(2, 2) == Tries(3, 0)


def test_state_mul():
    assert Tries(1, 0) * 5 == Tries(5, 0)
    assert 5 * Tries(0, 1) == Tries(0, 5)


def test_state_truediv():
    assert Tries(2, 4) / 2 == Tries(1, 2)


def test_state_floordiv():
    assert Tries(2, 4) // 2 == Tries(1, 2)


def test_state_mod():
    assert Tries(2, 4) % 2 == Tries(0, 0)
    assert Tries(3, 5) % 2 == Tries(1, 1)


def test_from_json():
    assert Tries.from_json(dict(right_tries=1, wrong_tries=2), []) == Tries(1, 2)


def test_to_json():
    assert Tries(1, 2).json == dict(right_tries=1, wrong_tries=2)
