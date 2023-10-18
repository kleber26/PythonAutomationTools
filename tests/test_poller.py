import time
from typing import Any, Dict

import pytest

from src.poller import Poller


def test_until_true_times_out() -> None:
    never_returns_true = lambda: False
    timeout = 0.5

    start = time.perf_counter()
    success = Poller.until_true(never_returns_true, timeout=timeout)
    end = time.perf_counter()
    assert not success, 'Should return False if polling times out!'

    duration = end - start
    assert duration > timeout, \
        f'Poller.until_true() took {duration} but the timeout was {timeout}'


def test_until_true_does_not_time_out() -> None:
    returns_true = lambda: True
    timeout = 0.5

    start = time.perf_counter()
    success = Poller.until_true(returns_true, timeout=timeout)
    end = time.perf_counter()
    assert success, 'Poller.until_true() should have returned True!'

    duration = end - start
    assert duration < timeout, \
        f'Poller.until_true() took {duration} but it should take less than {timeout}'


def test_receive_args() -> None:
    returns_something = lambda x: True

    timeout = 0.5

    start = time.perf_counter()
    something: Dict[str, Any] = {'x': 'bolinha'}
    success = Poller.until_true(returns_something, timeout=timeout, **something)
    end = time.perf_counter()
    assert success, 'Poller.until_true() should have returned True!'

    duration = end - start
    assert duration < timeout, \
        f'Poller.until_true() took {duration} but it should take less than {timeout}'


def test_receive_multiple_args() -> None:
    def any_function(param1: str, param2: float) -> bool:
        return True

    timeout = 0.5

    start = time.perf_counter()
    params: Dict[str, Any] = {'param1': 'rtr', 'param2': 3.14}
    success = Poller.until_true(any_function, timeout=timeout, **params)
    end = time.perf_counter()
    assert success, 'Poller.until_true() should have returned True!'

    duration = end - start
    assert duration < timeout, \
        f'Poller.until_true() took {duration} but it should take less than {timeout}'


def test_throws_without_kwargs() -> None:
    def any_function(param1: str) -> bool:
        return True

    timeout = 0.5
    params: Dict[str, Any] = {}
    with pytest.raises(TypeError):
        Poller.until_true(any_function, timeout=timeout, **params)


def test_throws_without_enough_kwargs() -> None:
    def any_function(param1: str, param2: float) -> bool:
        return True

    timeout = 0.5
    params: Dict[str, Any] = {'param1': 'rtr'}
    with pytest.raises(TypeError):
        Poller.until_true(any_function, timeout=timeout, **params)
