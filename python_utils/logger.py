"""
This module provides a base class `LoggerBase` and a derived class `Logged`
for adding logging capabilities to classes. The `LoggerBase` class expects
a `logger` attribute to be a `logging.Logger` or compatible instance and
provides methods for logging at various levels. The `Logged` class
automatically adds a named logger to the class.

Classes:
    LoggerBase:
        A base class that adds logging utilities to a class.
    Logged:
        A derived class that automatically adds a named logger to a class.

Example:
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
"""

from __future__ import annotations

import abc
import collections.abc
import logging
import sys
import types
import typing

if typing.TYPE_CHECKING:
    import typing_extensions

from . import decorators

__all__ = ['Logged']

#: Accepted values for the logging ``exc_info`` parameter: a bool, an
#: ``(type, value, traceback)`` triple, a bare exception instance, or ``None``.
# From the logging typeshed, converted to be compatible with Python 3.8
# https://github.com/python/typeshed/blob/main/stdlib/logging/__init__.pyi
_ExcInfoType: typing.TypeAlias = (
    bool
    | tuple[
        type[BaseException],
        BaseException,
        types.TracebackType | None,
    ]
    | tuple[None, None, None]
    | BaseException
    | None
)
#: Extra frames between ``Logger.exception`` and its caller. Up to Python 3.10
#: ``Logger.exception`` calls ``Logger.error``, and ``logging`` counts that
#: frame against the ``stacklevel``. From Python 3.11 it skips its own frames.
_EXCEPTION_FRAMES: int = int(sys.version_info < (3, 11))
#: Parameter specification capturing a wrapped logger method's arguments.
_P = typing.ParamSpec('_P')
#: Covariant return-type variable for wrapped logger methods.
_T = typing.TypeVar('_T', covariant=True)


class LoggerProtocol(typing.Protocol):
    """Structural type for any ``logging.Logger``-compatible logger.

    Objects that provide these methods (such as a ``logging.Logger`` or a
    ``loguru`` logger) can be used as the ``logger`` attribute of a
    ``LoggerBase`` subclass. Only the shape matters; no inheritance required.
    """

    def debug(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``DEBUG`` level."""

    def info(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``INFO`` level."""

    def warning(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``WARNING`` level."""

    def error(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``ERROR`` level."""

    def critical(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``CRITICAL`` level."""

    def exception(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``ERROR`` level, including exception information."""

    def log(
        self,
        level: int,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at the integer ``level``."""


def _create_instance(
    new: collections.abc.Callable[..., _T],
    cls: type[_T],
    args: tuple[typing.Any, ...],
    kwargs: dict[str, typing.Any],
) -> _T:
    """Create an instance with the next ``__new__`` in line.

    The constructor arguments are passed on, so that a class which is created
    in ``__new__`` gets its value, as ``int`` and ``str`` do. A ``__new__``
    that does not take them is called without, the way it always was.

    Args:
        new: The next ``__new__`` in the method resolution order.
        cls: The class to create an instance of.
        args: The positional constructor arguments.
        kwargs: The keyword constructor arguments.

    Returns:
        The new instance.

    Raises:
        TypeError: When ``new`` accepts the arguments in neither form. The
            error is the one for the call with the arguments.
    """
    if new is object.__new__:
        # `object.__new__` takes no arguments, they are for `__init__`.
        return new(cls)

    try:
        return new(cls, *args, **kwargs)
    except TypeError as error:
        try:
            return new(cls)
        except TypeError:
            raise error from None


class LoggerBase(abc.ABC):
    """Class which automatically adds logging utilities to your class when
    inheriting. Expects `logger` to be a logging.Logger or compatible instance.

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
    """

    # I've tried using a protocol to properly type the logger but it gave all
    # sorts of issues with mypy so we're using the lazy solution for now. The
    # actual classes define the correct type anyway
    logger: typing.Any
    # logger: LoggerProtocol

    @classmethod
    def __get_name(  # pyright: ignore[reportUnusedFunction]
        cls, *name_parts: str
    ) -> str:
        """Join the non-empty, stripped ``name_parts`` into a dotted name."""
        return '.'.join(n.strip() for n in name_parts if n.strip())

    @classmethod
    def _log_kwargs(
        cls,
        exc_info: _ExcInfoType,
        stack_info: bool,
        stacklevel: int,
        extra: collections.abc.Mapping[str, object] | None,
    ) -> dict[str, typing.Any]:
        """Build the keyword arguments that every log method forwards.

        Subclasses with a logger that does not take the ``logging`` keyword
        arguments can override this method.

        Args:
            exc_info: Exception information to attach to the record.
            stack_info: Whether to attach the current stack to the record.
            stacklevel: How many frames up the caller of the log method is.
            extra: Extra attributes for the record.

        Returns:
            The keyword arguments for the method of ``cls.logger``.
        """
        return {
            'exc_info': exc_info,
            'stack_info': stack_info,
            # One level more, so the record names the caller of the log
            # method instead of the log method itself.
            'stacklevel': stacklevel + 1,
            'extra': extra,
        }

    @decorators.wraps_classmethod(logging.Logger.debug)
    @classmethod
    def debug(
        cls,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``DEBUG`` level on the class logger."""
        return cls.logger.debug(  # type: ignore[no-any-return]
            msg,
            *args,
            **cls._log_kwargs(exc_info, stack_info, stacklevel, extra),
        )

    @decorators.wraps_classmethod(logging.Logger.info)
    @classmethod
    def info(
        cls,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``INFO`` level on the class logger."""
        return cls.logger.info(  # type: ignore[no-any-return]
            msg,
            *args,
            **cls._log_kwargs(exc_info, stack_info, stacklevel, extra),
        )

    @decorators.wraps_classmethod(logging.Logger.warning)
    @classmethod
    def warning(
        cls,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``WARNING`` level on the class logger."""
        return cls.logger.warning(  # type: ignore[no-any-return]
            msg,
            *args,
            **cls._log_kwargs(exc_info, stack_info, stacklevel, extra),
        )

    @decorators.wraps_classmethod(logging.Logger.error)
    @classmethod
    def error(
        cls,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``ERROR`` level on the class logger."""
        return cls.logger.error(  # type: ignore[no-any-return]
            msg,
            *args,
            **cls._log_kwargs(exc_info, stack_info, stacklevel, extra),
        )

    @decorators.wraps_classmethod(logging.Logger.critical)
    @classmethod
    def critical(
        cls,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``CRITICAL`` level on the class logger."""
        return cls.logger.critical(  # type: ignore[no-any-return]
            msg,
            *args,
            **cls._log_kwargs(exc_info, stack_info, stacklevel, extra),
        )

    @decorators.wraps_classmethod(logging.Logger.exception)
    @classmethod
    def exception(
        cls,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = True,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at ``ERROR`` level with exception info attached."""
        return cls.logger.exception(  # type: ignore[no-any-return]
            msg,
            *args,
            **cls._log_kwargs(
                exc_info,
                stack_info,
                stacklevel + _EXCEPTION_FRAMES,
                extra,
            ),
        )

    @decorators.wraps_classmethod(logging.Logger.log)
    @classmethod
    def log(
        cls,
        level: int,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: collections.abc.Mapping[str, object] | None = None,
    ) -> None:
        """Log ``msg`` at the integer ``level`` on the class logger."""
        return cls.logger.log(  # type: ignore[no-any-return]
            level,
            msg,
            *args,
            **cls._log_kwargs(exc_info, stack_info, stacklevel, extra),
        )


class Logged(LoggerBase):
    """Class which automatically adds a named logger to your class when
    inheriting.

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
    """

    logger: logging.Logger  # pragma: no cover

    @classmethod
    def __get_name(cls, *name_parts: str) -> str:
        """Build the dotted logger name via ``LoggerBase``'s joiner."""
        return typing.cast(
            str,
            LoggerBase._LoggerBase__get_name(*name_parts),  # type: ignore[attr-defined]  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportAttributeAccessIssue]
        )

    def __new__(
        cls, *args: typing.Any, **kwargs: typing.Any
    ) -> typing_extensions.Self:
        """
        Create a new instance of the class and initialize the logger.

        The logger is named using the module and class name.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            An instance of the class.
        """
        cls.logger = logging.getLogger(
            cls.__get_name(cls.__module__, cls.__name__)
        )
        return _create_instance(super().__new__, cls, args, kwargs)
