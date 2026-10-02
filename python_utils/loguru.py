"""
This module provides a `Logurud` class that integrates the `loguru` logger
with the base logging functionality defined in `logger_module.LoggerBase`.

Classes:
    Logurud: A class that extends `LoggerBase` and uses `loguru` for logging.

Usage example:
    >>> from python_utils.loguru import Logurud
    >>> class MyClass(Logurud):
    ...     def __init__(self):
    ...         Logurud.__init__(self)
    >>> my_class = MyClass()
    >>> my_class.logger.info('This is an info message')
"""

from __future__ import annotations

import collections.abc
import typing

import loguru

from . import logger as logger_module

__all__ = ['Logurud']


class Logurud(logger_module.LoggerBase):
    """
    A class that extends `LoggerBase` and uses `loguru` for logging.

    Attributes:
        logger (loguru.Logger): The `loguru` logger instance.
    """

    logger: loguru.Logger

    @classmethod
    def _log_kwargs(
        cls,
        exc_info: object,
        stack_info: bool,
        stacklevel: int,
        extra: collections.abc.Mapping[str, object] | None,
    ) -> dict[str, typing.Any]:
        """Forward only an explicit ``extra`` to the `loguru` logger.

        `loguru` runs ``str.format`` over the message as soon as a call has
        any arguments. The `logging` keyword arguments would turn every
        message with a brace in it into a broken format string, so they are
        left out. An ``extra`` that the caller passed is still forwarded, as
        it always reached the `loguru` record.

        Args:
            exc_info: Ignored, `loguru` does not take this argument.
            stack_info: Ignored, `loguru` does not take this argument.
            stacklevel: Ignored, `loguru` does not take this argument.
            extra: Forwarded when it is not ``None``.

        Returns:
            The keyword arguments for the `loguru` logger.
        """
        if extra is None:
            return {}

        return {'extra': extra}

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> Logurud:
        """
        Creates a new instance of `Logurud` and initializes the `loguru`
        logger.

        Args:
            *args (typing.Any): Variable length argument list.
            **kwargs (typing.Any): Arbitrary keyword arguments.

        Returns:
            Logurud: A new instance of `Logurud`.
        """
        # `logger` is already declared at class scope; assign without
        # re-annotating to avoid an obscured-declaration error.
        cls.logger = loguru.logger.opt(depth=1)
        return logger_module._create_instance(  # pyright: ignore[reportPrivateUsage]
            super().__new__, cls, args, kwargs
        )
