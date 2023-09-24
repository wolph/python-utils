from unittest.mock import MagicMock

import pytest

from python_utils.decorators import sample, wraps_classmethod


@pytest.fixture
def random(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock()
    monkeypatch.setattr(
        'python_utils.decorators.random.random', mock, raising=True
    )
    return mock


def test_sample_called(random: MagicMock):
    demo_function = MagicMock()
    decorated = sample(0.5)(demo_function)
    random.return_value = 0.4
    decorated()
    random.return_value = 0.0
    decorated()
    args = [1, 2]
    kwargs = {'1': 1, '2': 2}
    decorated(*args, **kwargs)
    demo_function.assert_called_with(*args, **kwargs)
    assert demo_function.call_count == 3


def test_sample_not_called(random: MagicMock):
    demo_function = MagicMock()
    decorated = sample(0.5)(demo_function)
    random.return_value = 0.5
    decorated()
    random.return_value = 1.0
    decorated()
    assert demo_function.call_count == 0


class SomeClass:
    @classmethod
    def some_classmethod(cls, arg):  # type: ignore
        return arg  # type: ignore

    @classmethod
    def some_annotated_classmethod(cls, arg: int) -> int:
        return arg


def test_wraps_classmethod():  # type: ignore
    some_class = SomeClass()
    some_class.some_classmethod = MagicMock()
    wrapped_method = wraps_classmethod(  # type: ignore
        SomeClass.some_classmethod  # type: ignore
    )(  # type: ignore
        some_class.some_classmethod  # type: ignore
    )
    wrapped_method(123)
    some_class.some_classmethod.assert_called_with(123)  # type: ignore


def test_wraps_annotated_classmethod():  # type: ignore
    some_class = SomeClass()
    some_class.some_annotated_classmethod = MagicMock()
    wrapped_method = wraps_classmethod(SomeClass.some_annotated_classmethod)(
        some_class.some_annotated_classmethod
    )
    wrapped_method(123)  # type: ignore
    some_class.some_annotated_classmethod.assert_called_with(123)
