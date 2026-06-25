import typing
from unittest import mock

import pytest

from python_utils import decorators

T = typing.TypeVar('T')


@pytest.fixture
def random(monkeypatch: pytest.MonkeyPatch) -> mock.MagicMock:
    random_mock = mock.MagicMock()
    monkeypatch.setattr(
        'python_utils.decorators.random.random', random_mock, raising=True
    )
    return random_mock


def test_sample_called(random: mock.MagicMock) -> None:
    demo_function = mock.MagicMock()
    decorated = decorators.sample(0.5)(demo_function)
    random.return_value = 0.4
    decorated()
    random.return_value = 0.0
    decorated()
    args = [1, 2]
    kwargs = {'1': 1, '2': 2}
    decorated(*args, **kwargs)
    demo_function.assert_called_with(*args, **kwargs)
    assert demo_function.call_count == 3


def test_sample_not_called(random: mock.MagicMock) -> None:
    demo_function = mock.MagicMock()
    decorated = decorators.sample(0.5)(demo_function)
    random.return_value = 0.5
    decorated()
    random.return_value = 1.0
    decorated()
    assert demo_function.call_count == 0


class SomeClass:
    @classmethod
    def some_classmethod(cls, arg: T) -> T:
        return arg

    @classmethod
    def some_annotated_classmethod(cls, arg: int) -> int:
        return arg


def test_wraps_classmethod() -> None:
    some_class = SomeClass()
    some_class.some_classmethod = mock.MagicMock()  # type: ignore[method-assign]
    wrapped_method = decorators.wraps_classmethod(SomeClass.some_classmethod)(
        some_class.some_classmethod
    )
    wrapped_method(123)
    some_class.some_classmethod.assert_called_with(123)


def test_wraps_annotated_classmethod() -> None:
    some_class = SomeClass()
    some_class.some_annotated_classmethod = mock.MagicMock()  # type: ignore[method-assign]
    wrapped_method = decorators.wraps_classmethod(
        SomeClass.some_annotated_classmethod
    )(some_class.some_annotated_classmethod)
    wrapped_method(123)
    some_class.some_annotated_classmethod.assert_called_with(123)
