"""Tests for the logging mixins in ``python_utils.logger``."""

import logging

import pytest

from python_utils import logger


def records_of(
    caplog: pytest.LogCaptureFixture, name: str
) -> list[logging.LogRecord]:
    """Return the captured records of the logger called ``name``."""
    return [record for record in caplog.records if record.name == name]


def test_exception_logs_traceback(caplog: pytest.LogCaptureFixture) -> None:
    """Attach the active exception to the record, like ``logging`` does."""

    class Spam(logger.Logged):
        pass

    spam: Spam = Spam()
    name: str = Spam.logger.name
    with caplog.at_level(logging.DEBUG, logger=name):
        try:
            int('eggs')
        except ValueError:
            spam.exception('bacon')

    record: logging.LogRecord = records_of(caplog, name)[-1]
    assert record.exc_info is not None
    assert record.exc_info[0] is ValueError


def test_exception_without_traceback(caplog: pytest.LogCaptureFixture) -> None:
    """Leave the traceback out when ``exc_info`` is switched off."""

    class Spam(logger.Logged):
        pass

    spam: Spam = Spam()
    name: str = Spam.logger.name
    with caplog.at_level(logging.DEBUG, logger=name):
        try:
            int('eggs')
        except ValueError:
            spam.exception('bacon', exc_info=False)

    record: logging.LogRecord = records_of(caplog, name)[-1]
    assert not record.exc_info


def test_records_name_the_caller(caplog: pytest.LogCaptureFixture) -> None:
    """Report the calling function in every record, not the mixin."""

    class Spam(logger.Logged):
        pass

    spam: Spam = Spam()
    name: str = Spam.logger.name
    with caplog.at_level(logging.DEBUG, logger=name):
        spam.debug('debug')
        spam.info('info')
        spam.warning('warning')
        spam.error('error')
        spam.critical('critical')
        spam.exception('exception')
        spam.log(logging.INFO, 'log')

    records: list[logging.LogRecord] = records_of(caplog, name)
    assert len(records) == 7
    assert {record.funcName for record in records} == {
        'test_records_name_the_caller'
    }
    assert {record.filename for record in records} == {'test_logged.py'}


def log_one_frame_up(spam: logger.Logged) -> None:
    """Log a record that points at the caller of this helper."""
    spam.info('eggs', stacklevel=2)


def test_stacklevel_counts_from_the_caller(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Count an explicit ``stacklevel`` from the calling function."""

    class Spam(logger.Logged):
        pass

    spam: Spam = Spam()
    name: str = Spam.logger.name
    with caplog.at_level(logging.DEBUG, logger=name):
        log_one_frame_up(spam)

    record: logging.LogRecord = records_of(caplog, name)[-1]
    assert record.funcName == 'test_stacklevel_counts_from_the_caller'


class Bacon:
    """A base class whose ``__new__`` needs the constructor arguments."""

    value: int

    def __new__(cls, value: int) -> 'Bacon':
        """Store ``value`` on the new instance."""
        self: Bacon = super().__new__(cls)
        self.value = value
        return self


def test_new_forwards_arguments_to_builtin() -> None:
    """Keep the value of a built-in type that is created in ``__new__``."""

    class LoggedInt(logger.Logged, int):
        pass

    class LoggedStr(logger.Logged, str):
        pass

    number: LoggedInt = LoggedInt(5)
    octal: LoggedInt = LoggedInt('7', base=8)
    text: LoggedStr = LoggedStr('spam')
    assert number == 5
    assert octal == 7
    assert text == 'spam'


def test_new_forwards_arguments_to_base() -> None:
    """Pass the constructor arguments on to the next ``__new__``."""

    class Eggs(logger.Logged, Bacon):
        pass

    eggs: Eggs = Eggs(5)
    assert eggs.value == 5
    assert Eggs.logger.name.endswith('.Eggs')


def test_new_accepts_arguments_for_init() -> None:
    """Keep accepting arguments that only ``__init__`` uses."""

    class Spam(logger.Logged):
        def __init__(self, value: int, name: str = 'spam') -> None:
            """Store both arguments on the instance."""
            self.value: int = value
            self.name: str = name

    spam: Spam = Spam(1, name='eggs')
    assert (spam.value, spam.name) == (1, 'eggs')


class Singleton:
    """A base class whose ``__new__`` takes no constructor arguments."""

    instance: 'Singleton | None' = None

    def __new__(cls) -> 'Singleton':
        """Create the one instance on the first call and reuse it after."""
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance


def test_new_falls_back_without_arguments() -> None:
    """Keep working with a base ``__new__`` that takes no arguments."""

    class Config(logger.Logged, Singleton):
        def __init__(self, path: str = 'defaults.ini') -> None:
            """Store the path on the instance."""
            self.path: str = path

    config: Config = Config('settings.ini')
    assert config.path == 'settings.ini'
    assert Config('other.ini') is config


def test_new_reports_the_first_error() -> None:
    """Raise the error of the forwarded call when no call works."""

    class Eggs(logger.Logged, Bacon):
        def __init__(self, *args: int) -> None:
            """Accept any number of arguments."""

    # The message is the interpreter's own and differs on PyPy.
    with pytest.raises(TypeError):
        Eggs(1, 2)


def test_logger_is_created_at_first_instance() -> None:
    """Create the logger of a class when it is first instantiated.

    ``logging.config.dictConfig`` disables every logger that exists when it
    runs. A logger that is created when the class is defined would be gone
    for an application that configures logging after its imports.
    """

    class LateSpam(logger.Logged):
        pass

    name: str = f'{LateSpam.__module__}.LateSpam'
    assert name not in logging.Logger.manager.loggerDict
    assert 'logger' not in vars(LateSpam)

    LateSpam()
    assert name in logging.Logger.manager.loggerDict
    assert LateSpam.logger.name == name


def test_subclass_inherits_class_body_logger() -> None:
    """Let a subclass use the logger from the class body of its parent."""
    custom: logging.Logger = logging.getLogger('python_utils.tests.custom')

    class Parent(logger.Logged):
        logger = custom

    class Child(Parent):
        pass

    assert Child.logger is custom
    Child()
    assert Child.logger.name.endswith('.Child')
