"""
This module provides utility functions for raising and reraising exceptions.

Functions::

    raise_exception(exception_class, *args, **kwargs):
        Returns a function that raises an exception of the given type with
        the given arguments.

    reraise(*args, **kwargs):
        Reraises the current exception.
"""

import collections.abc
import typing


def raise_exception(
    exception_class: type[Exception],
    *args: typing.Any,
    **kwargs: typing.Any,
) -> collections.abc.Callable[..., None]:
    """
    Returns a function that raises an exception of the given type with the
    given arguments.

    >>> raise_exception(ValueError, 'spam')('eggs')
    Traceback (most recent call last):
        ...
    ValueError: spam
    """

    def raise_(*args_: typing.Any, **kwargs_: typing.Any) -> typing.Any:
        """Raise ``exception_class`` with the captured args."""
        raise exception_class(*args, **kwargs)

    return raise_


def reraise(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
    """
    Reraises the current exception.

    This function seems useless, but it can be useful when you need to pass
    a callable to another function that raises an exception.
    """
    raise
