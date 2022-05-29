from unittest.mock import MagicMock

import pytest

from python_utils.decorators import sample


@pytest.fixture
def random(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("python_utils.decorators.random.random", mock, raising=True)
    return mock


def test_sample_called(random):
    demo_function = MagicMock()
    decorated = sample(0.5)(demo_function)    
    random.return_value = 0.4
    decorated()
    random.return_value = 0.0
    decorated()
    args = [1, 2]
    kwargs = {"1": 1, "2": 2}
    decorated(*args, **kwargs)
    demo_function.assert_called_with(*args, **kwargs)
    assert demo_function.call_count == 3


def test_sample_not_called(random):
    demo_function = MagicMock()
    decorated = sample(0.5)(demo_function)
    random.return_value = 0.5
    decorated()
    random.return_value = 1.0
    decorated()
    assert demo_function.call_count == 0