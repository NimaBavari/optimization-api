import pytest

from optimization_lib import efficient, naive

# test constants
PRIMARY_EXPECTED = 198


# fixtures
@pytest.fixture
def lists():
    return [[2, 3, 4, 5, 6], [1, 7, 4], [2, 5, 3], [1, 1]]


@pytest.fixture
def f():
    return lambda x: x**3


@pytest.fixture
def modulo_quot():
    return 200


def test_naive_algo(lists, modulo_quot, f):
    res = naive(lists, modulo_quot, f)
    assert res == PRIMARY_EXPECTED


def test_efficient_algo(lists, modulo_quot, f):
    res = efficient(lists, modulo_quot, f)
    assert res == PRIMARY_EXPECTED
