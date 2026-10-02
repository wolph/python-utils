# mypy: disable-error-code=misc
"""Tests for the loguru mixin in ``python_utils.loguru``."""

import collections.abc

import loguru as loguru_lib
import pytest

from python_utils import loguru

pytest.importorskip('loguru')

#: Messages that ``str.format`` rejects or would rewrite.
BRACE_MESSAGES: tuple[str, ...] = (
    'payload {"spam": 1}',
    'set {1, 2}',
    'unbalanced {',
    'positional {}',
)


@pytest.fixture
def messages() -> collections.abc.Iterator[list[str]]:
    """Collect the text of every record loguru emits during a test."""
    collected: list[str] = []
    sink_id: int = loguru_lib.logger.add(collected.append, format='{message}')
    yield collected
    loguru_lib.logger.remove(sink_id)


def test_logurud() -> None:
    """Expose all loguru log-level methods on a subclass."""

    class MyClass(loguru.Logurud):
        pass

    my_class = MyClass()
    my_class.debug('debug')
    my_class.info('info')
    my_class.warning('warning')
    my_class.error('error')
    my_class.critical('critical')
    my_class.exception('exception')
    my_class.log(0, 'log')


@pytest.mark.parametrize('message', BRACE_MESSAGES)
def test_logurud_message_with_braces(
    messages: list[str], message: str
) -> None:
    """Log a message that contains braces exactly as it was given."""

    class MyClass(loguru.Logurud):
        pass

    my_class: loguru.Logurud = MyClass()
    my_class.info(message)
    assert messages == [f'{message}\n']


def test_logurud_braces_in_every_method(messages: list[str]) -> None:
    """Accept a message with braces in every log-level method."""

    class MyClass(loguru.Logurud):
        pass

    message: str = 'payload {"spam": 1}'
    my_class: loguru.Logurud = MyClass()
    my_class.debug(message)
    my_class.info(message)
    my_class.warning(message)
    my_class.error(message)
    my_class.critical(message)
    my_class.exception(message)
    my_class.log(20, message)
    assert len(messages) == 7
    assert all(logged.startswith(message) for logged in messages)


def test_logurud_keeps_explicit_extra() -> None:
    """Keep passing an explicit ``extra`` on to the loguru record."""

    class MyClass(loguru.Logurud):
        pass

    extras: list[dict[str, object]] = []
    sink_id: int = loguru_lib.logger.add(
        lambda message: extras.append(dict(message.record['extra'])),
        format='{message}',
    )
    try:
        my_class: loguru.Logurud = MyClass()
        my_class.info('spam')
        my_class.info('spam', extra={'eggs': 1})
    finally:
        loguru_lib.logger.remove(sink_id)

    assert extras == [{}, {'extra': {'eggs': 1}}]


def test_logurud_new_forwards_arguments() -> None:
    """Keep the value of a built-in type that is created in ``__new__``."""

    class LoggedInt(loguru.Logurud, int):
        pass

    number: loguru.Logurud = LoggedInt(5)
    octal: loguru.Logurud = LoggedInt('7', base=8)
    assert isinstance(number, int)
    assert isinstance(octal, int)
    assert number == 5
    assert octal == 7


def test_logurud_new_accepts_arguments_for_init() -> None:
    """Keep accepting arguments that only ``__init__`` uses."""

    class MyClass(loguru.Logurud):
        def __init__(self, value: int, name: str = 'spam') -> None:
            """Store both arguments on the instance."""
            self.value: int = value
            self.name: str = name

    my_class: loguru.Logurud = MyClass(1, name='eggs')
    assert isinstance(my_class, MyClass)
    assert (my_class.value, my_class.name) == (1, 'eggs')
