"""Tests for the decorators in ``python_utils.decorators``."""

import inspect
import logging
import typing
from unittest import mock

import pytest

from python_utils import decorators

T = typing.TypeVar('T')


@pytest.fixture
def random(monkeypatch: pytest.MonkeyPatch) -> mock.MagicMock:
    """Patch ``decorators.random.random`` and return the mock."""
    random_mock = mock.MagicMock()
    monkeypatch.setattr(
        'python_utils.decorators.random.random', random_mock, raising=True
    )
    return random_mock


def test_sample_called(random: mock.MagicMock) -> None:
    """Call the wrapped function when the sampled roll passes."""
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
    """Skip the wrapped function when the sampled roll fails."""
    demo_function = mock.MagicMock()
    decorated = decorators.sample(0.5)(demo_function)
    random.return_value = 0.5
    decorated()
    random.return_value = 1.0
    decorated()
    assert demo_function.call_count == 0


def test_sample_leaves_root_logger_alone(
    random: mock.MagicMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Skip a call without configuring the root logger."""
    root: logging.Logger = logging.getLogger()
    handlers: list[logging.Handler] = []
    # A root logger without handlers is what an application starts with.
    # `logging.debug()` installs a handler on it, a module logger does not.
    monkeypatch.setattr(root, 'handlers', handlers)
    random.return_value = 1.0

    decorators.sample(0.5)(mock.MagicMock())()

    assert handlers == []


def test_sample_logs_on_module_logger(
    random: mock.MagicMock, caplog: pytest.LogCaptureFixture
) -> None:
    """Report a skipped call on the logger of the module."""
    random.return_value = 1.0

    with caplog.at_level(logging.DEBUG):
        decorators.sample(0.5)(mock.MagicMock())()

    names: list[str] = [record.name for record in caplog.records]
    assert names == ['python_utils.decorators']
    assert 'Skipped execution' in caplog.records[0].getMessage()


def test_listify_keeps_metadata() -> None:
    """Keep the name, docstring and signature of the decorated function."""

    @decorators.listify(collection=list)
    def numbers(count: int = 3) -> typing.Iterator[int]:
        """Yield ``count`` numbers."""
        yield from range(count)

    assert numbers() == [0, 1, 2]
    assert numbers.__name__ == 'numbers'
    assert numbers.__doc__ == 'Yield ``count`` numbers.'
    assert list(inspect.signature(numbers).parameters) == ['count']


class SomeClass:
    """A sample class with classmethods for wrapping tests."""

    @classmethod
    def some_classmethod(cls, arg: T) -> T:
        """Return the argument unchanged (generic classmethod)."""
        return arg

    @classmethod
    def some_annotated_classmethod(cls, arg: int) -> int:
        """Return the integer argument unchanged."""
        return arg


def test_wraps_classmethod() -> None:
    """Forward calls through a wrapped classmethod."""
    some_class = SomeClass()
    some_class.some_classmethod = mock.MagicMock()  # type: ignore[method-assign]
    wrapped_method = decorators.wraps_classmethod(SomeClass.some_classmethod)(
        some_class.some_classmethod
    )
    wrapped_method(123)
    some_class.some_classmethod.assert_called_with(123)


def test_wraps_annotated_classmethod() -> None:
    """Forward calls through a wrapped annotated classmethod."""
    some_class = SomeClass()
    some_class.some_annotated_classmethod = mock.MagicMock()  # type: ignore[method-assign]
    wrapped_method = decorators.wraps_classmethod(
        SomeClass.some_annotated_classmethod
    )(some_class.some_annotated_classmethod)
    wrapped_method(123)
    some_class.some_annotated_classmethod.assert_called_with(123)


def test_wraps_classmethod_leaves_wrapped_annotations_alone() -> None:
    """Drop ``self`` for the wrapper without touching the wrapped method."""

    def wrapped(self: SomeClass, arg: int) -> int:
        """Return the argument unchanged, as a regular method would."""
        return arg

    def wrapper(cls: type[SomeClass], arg: int) -> int:
        """Return the argument unchanged, as a classmethod would."""
        return arg

    result: typing.Callable[..., int] = decorators.wraps_classmethod(wrapped)(
        wrapper
    )

    assert wrapped.__annotations__ == {
        'self': SomeClass,
        'arg': int,
        'return': int,
    }
    assert result.__annotations__ == {'arg': int, 'return': int}
    assert result.__annotations__ is not wrapped.__annotations__


def test_wraps_classmethod_keeps_wrapper_annotations() -> None:
    """Keep the wrapper's annotations if the wrapped method has none."""

    def wrapped(self: SomeClass, arg: int) -> int:
        """Return the argument unchanged, as a regular method would."""
        return arg

    def wrapper(cls: type[SomeClass], arg: int) -> int:
        """Return the argument unchanged, as a classmethod would."""
        return arg

    # To the interpreter this is a method that was written without
    # annotations. The type checkers still get to see them.
    wrapped.__annotations__ = {}

    result: typing.Callable[..., int] = decorators.wraps_classmethod(wrapped)(
        wrapper
    )

    assert result.__annotations__ == {
        'cls': type[SomeClass],
        'arg': int,
        'return': int,
    }
