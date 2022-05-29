import abc
import functools
import logging

__all__ = ['Logged']

import typing


class LoggerBase(abc.ABC):
    '''Class which automatically adds logging utilities to your class when
    interiting. Expects `logger` to be a logging.Logger or compatible instance.

    Adds easy access to debug, info, warning, error, exception and log methods

    >>> class MyClass(LoggerBase):
    ...     logger = logging.getLogger(__name__)
    ...
    ...     def __init__(self):
    ...         Logged.__init__(self)

    >>> my_class = MyClass()
    >>> my_class.debug('debug')
    >>> my_class.info('info')
    >>> my_class.warning('warning')
    >>> my_class.error('error')
    >>> my_class.exception('exception')
    >>> my_class.log(0, 'log')
    '''

    # Being a tad lazy here and not creating a Protocol.
    # The actual classes define the correct type anyway
    logger: typing.Any

    @classmethod
    def __get_name(cls, *name_parts: str) -> str:
        return '.'.join(n.strip() for n in name_parts if n.strip())

    @classmethod
    @functools.wraps(logging.debug)
    def debug(cls, msg: str, *args: typing.Any, **kwargs: typing.Any):
        cls.logger.debug(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.info)
    def info(cls, msg: str, *args: typing.Any, **kwargs: typing.Any):
        cls.logger.info(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.warning)
    def warning(cls, msg: str, *args: typing.Any, **kwargs: typing.Any):
        cls.logger.warning(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.error)
    def error(cls, msg: str, *args: typing.Any, **kwargs: typing.Any):
        cls.logger.error(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.exception)
    def exception(cls, msg: str, *args: typing.Any, **kwargs: typing.Any):
        cls.logger.exception(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.log)
    def log(cls, lvl: int, msg: str, *args: typing.Any, **kwargs: typing.Any):
        cls.logger.log(lvl, msg, *args, **kwargs)


class Logged(LoggerBase):
    '''Class which automatically adds a named logger to your class when
    interiting

    Adds easy access to debug, info, warning, error, exception and log methods

    >>> class MyClass(Logged):
    ...     def __init__(self):
    ...         Logged.__init__(self)

    >>> my_class = MyClass()
    >>> my_class.debug('debug')
    >>> my_class.info('info')
    >>> my_class.warning('warning')
    >>> my_class.error('error')
    >>> my_class.exception('exception')
    >>> my_class.log(0, 'log')

    >>> my_class._Logged__get_name('spam')
    'spam'
    '''

    logger: logging.Logger  # pragma: no cover

    @classmethod
    def __get_name(cls, *name_parts: str) -> str:
        return LoggerBase._LoggerBase__get_name(*name_parts)  # type: ignore

    def __new__(cls, *args, **kwargs):
        cls.logger = logging.getLogger(
            cls.__get_name(cls.__module__, cls.__name__)
        )
        return super(Logged, cls).__new__(cls)
