"""
This module provides various utility decorators for Python functions
and methods.

The decorators include:

1. `set_attributes`: Sets attributes on functions and classes.
2. `listify`: Converts any generator to a list or other collection.
3. `sample`: Limits calls to a function based on a sample rate.
4. `wraps_classmethod`: Wraps classmethods with type info from a
   regular method.

Each decorator is designed to enhance the functionality of Python
functions and methods in a simple and reusable manner.
"""

import collections.abc
import contextlib
import functools
import logging
import random
import typing

_T = typing.TypeVar('_T')
_P = typing.ParamSpec('_P')


def set_attributes(
    **kwargs: typing.Any,
) -> collections.abc.Callable[..., typing.Any]:
    """Decorator to set attributes on functions and classes.

    A common usage for this pattern is the Django Admin where
    functions can get an optional short_description. To illustrate:

    Example from the Django admin using this decorator:
    https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display

    Our simplified version:

    >>> @set_attributes(short_description='Name')
    ... def upper_case_name(self, obj):
    ...     return ('%s %s' % (obj.first_name, obj.last_name)).upper()

    The standard Django version:

    >>> def upper_case_name(obj):
    ...     return ('%s %s' % (obj.first_name, obj.last_name)).upper()

    >>> upper_case_name.short_description = 'Name'

    """

    def _set_attributes(
        function: collections.abc.Callable[_P, _T],
    ) -> collections.abc.Callable[_P, _T]:
        """Attach the captured ``kwargs`` as attributes on ``function``."""
        for key, value in kwargs.items():
            setattr(function, key, value)
        return function

    return _set_attributes


def listify(
    collection: collections.abc.Callable[
        [collections.abc.Iterable[_T]], collections.abc.Collection[_T]
    ] = list,
    allow_empty: bool = True,
) -> collections.abc.Callable[
    [collections.abc.Callable[..., collections.abc.Iterable[_T] | None]],
    collections.abc.Callable[..., collections.abc.Collection[_T]],
]:
    """
    Convert any generator to a list or other type of collection.

    >>> @listify()
    ... def generator():
    ...     yield 1
    ...     yield 2
    ...     yield 3

    >>> generator()
    [1, 2, 3]

    >>> @listify()
    ... def empty_generator():
    ...     pass

    >>> empty_generator()
    []

    >>> @listify(allow_empty=False)
    ... def empty_generator_not_allowed():
    ...     pass

    >>> empty_generator_not_allowed()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ... `allow_empty` is `False`

    >>> @listify(collection=set)
    ... def set_generator():
    ...     yield 1
    ...     yield 1
    ...     yield 2

    >>> set_generator()
    {1, 2}

    >>> @listify(collection=dict)
    ... def dict_generator():
    ...     yield 'a', 1
    ...     yield 'b', 2

    >>> dict_generator()
    {'a': 1, 'b': 2}
    """

    def _listify(
        function: collections.abc.Callable[
            ..., collections.abc.Iterable[_T] | None
        ],
    ) -> collections.abc.Callable[..., collections.abc.Collection[_T]]:
        """Materialize ``function``'s result into ``collection``."""

        def __listify(
            *args: typing.Any, **kwargs: typing.Any
        ) -> collections.abc.Collection[_T]:
            """Call ``function`` and gather its result into ``collection``."""
            result: collections.abc.Iterable[_T] | None = function(
                *args, **kwargs
            )
            if result is None:
                if allow_empty:
                    return collection(iter(()))
                else:
                    raise TypeError(
                        f'{function} returned `None` and `allow_empty` '
                        'is `False`'
                    )
            else:
                return collection(result)

        return __listify

    return _listify


def sample(
    sample_rate: float,
) -> collections.abc.Callable[
    [collections.abc.Callable[_P, _T]],
    collections.abc.Callable[_P, _T | None],
]:
    """
    Limit calls to a function based on given sample rate.
    Number of calls to the function will be roughly equal to
    sample_rate percentage.

    Usage:

    >>> @sample(0.5)
    ... def demo_function(*args, **kwargs):
    ...     return 1

    Calls to *demo_function* will be limited to 50% approximately.
    """

    def _sample(
        function: collections.abc.Callable[_P, _T],
    ) -> collections.abc.Callable[_P, _T | None]:
        """Wrap ``function`` so it only runs on a sampled fraction of calls."""

        @functools.wraps(function)
        def __sample(*args: _P.args, **kwargs: _P.kwargs) -> _T | None:
            """Run ``function`` with probability ``sample_rate``, else skip."""
            if random.random() < sample_rate:
                return function(*args, **kwargs)
            else:
                logging.debug(
                    'Skipped execution of %r(%r, %r) due to sampling',
                    function,
                    args,
                    kwargs,
                )
                return None

        return __sample

    return _sample


def wraps_classmethod(
    wrapped: collections.abc.Callable[typing.Concatenate[typing.Any, _P], _T],
) -> collections.abc.Callable[
    [
        collections.abc.Callable[typing.Concatenate[typing.Any, _P], _T],
    ],
    collections.abc.Callable[typing.Concatenate[typing.Any, _P], _T],
]:
    """Like ``functools.wraps``, but for wrapping classmethods.

    Copies the wrapped method's metadata (name, docstring and annotations) onto
    the wrapper, so a classmethod wrapper carries the type information of the
    regular method it stands in for.

    Args:
        wrapped: The method whose metadata should be copied onto the wrapper.

    Returns:
        A decorator that updates its wrapper with ``wrapped``'s metadata.
    """

    def _wraps_classmethod(
        wrapper: collections.abc.Callable[
            typing.Concatenate[typing.Any, _P], _T
        ],
    ) -> collections.abc.Callable[typing.Concatenate[typing.Any, _P], _T]:
        """Copy ``wrapped``'s metadata onto ``wrapper`` and return it."""
        # For some reason `functools.update_wrapper` fails on some test
        # runs but not while running actual code
        with contextlib.suppress(AttributeError):
            wrapper = functools.update_wrapper(
                wrapper,
                wrapped,
                assigned=tuple(
                    a
                    for a in functools.WRAPPER_ASSIGNMENTS
                    if a != '__annotations__'
                ),
            )
        if annotations := getattr(wrapped, '__annotations__', {}):
            # Drop `self`: the wrapper is a classmethod, so it takes no `self`.
            annotations.pop('self', None)
            wrapper.__annotations__ = annotations

        return wrapper

    return _wraps_classmethod
