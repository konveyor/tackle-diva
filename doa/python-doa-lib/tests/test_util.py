"tests for .util package."
from time import sleep

from pytest import raises
from doa.util import timer


def test_timer_normal():
    "test of timer for normal execution."
    # pylint: disable=invalid-name
    with timer() as t:
        x = 5/2
        sleep(1)
        print(x)
        delta = t.sec()
        assert 0.95 < delta < 1.05


def test_timer_exception():
    "test of timer for exception capturing in context body"
    with raises(ZeroDivisionError):
        # pylint: disable=invalid-name
        with timer() as t:
            x = 5/0
            print(x)
            print(t.sec_str())
