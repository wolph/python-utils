"""
This module initializes the `python_utils` package by importing various
submodules and functions.

Imports are performed lazily (PEP 562): nothing is imported when you ``import
python_utils``; each submodule/function is loaded on first access. This keeps
``import python_utils`` cheap and, in particular, avoids eagerly importing
``asyncio`` (via the async helpers) for consumers that only need the
synchronous utilities.

Submodules::

    aio
    converters
    decorators
    formatters
    generators
    import_
    logger
    terminal
    time
    types

Functions::

    acount
    remap
    scale_1024
    to_float
    to_int
    to_str
    to_unicode
    listify
    set_attributes
    raise_exception
    reraise
    camel_to_underscore
    timesince
    abatcher
    batcher
    import_global
    get_terminal_size
    aio_generator_timeout_detector
    aio_generator_timeout_detector_decorator
    aio_timeout_generator
    delta_to_seconds
    delta_to_seconds_or_none
    format_time
    timedelta_to_seconds
    timeout_generator

Classes::

    CastedDict
    LazyCastedDict
    UniqueList
    Logged
    LoggerBase
"""

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:  # pragma: no cover
    # Eager imports for type checkers only; the runtime equivalents are loaded
    # lazily by ``__getattr__`` below. Names appear in ``__all__`` so they are
    # treated as re-exports (not unused imports).
    from . import (
        aio,
        converters,
        decorators,
        formatters,
        generators,
        import_,
        logger,
        terminal,
        time,
        types,
    )
    from .__about__ import __version__
    from .aio import acount
    from .containers import CastedDict, LazyCastedDict, UniqueList
    from .converters import (
        remap,
        scale_1024,
        to_float,
        to_int,
        to_str,
        to_unicode,
    )
    from .decorators import listify, set_attributes
    from .exceptions import raise_exception, reraise
    from .formatters import camel_to_underscore, timesince
    from .generators import abatcher, batcher
    from .import_ import import_global
    from .logger import Logged, LoggerBase
    from .terminal import get_terminal_size
    from .time import (
        aio_generator_timeout_detector,
        aio_generator_timeout_detector_decorator,
        aio_timeout_generator,
        delta_to_seconds,
        delta_to_seconds_or_none,
        format_time,
        timedelta_to_seconds,
        timeout_generator,
    )

#: Submodules that can be accessed as ``python_utils.<name>``.
_SUBMODULES: frozenset[str] = frozenset(
    {
        'aio',
        'containers',
        'converters',
        'decorators',
        'exceptions',
        'formatters',
        'generators',
        'import_',
        'logger',
        'terminal',
        'time',
        'types',
    }
)

#: Exported name -> submodule it lives in.
_NAME_TO_MODULE: dict[str, str] = {
    '__version__': '__about__',
    'acount': 'aio',
    'CastedDict': 'containers',
    'LazyCastedDict': 'containers',
    'UniqueList': 'containers',
    'remap': 'converters',
    'scale_1024': 'converters',
    'to_float': 'converters',
    'to_int': 'converters',
    'to_str': 'converters',
    'to_unicode': 'converters',
    'listify': 'decorators',
    'set_attributes': 'decorators',
    'raise_exception': 'exceptions',
    'reraise': 'exceptions',
    'camel_to_underscore': 'formatters',
    'timesince': 'formatters',
    'abatcher': 'generators',
    'batcher': 'generators',
    'import_global': 'import_',
    'Logged': 'logger',
    'LoggerBase': 'logger',
    'get_terminal_size': 'terminal',
    'aio_generator_timeout_detector': 'time',
    'aio_generator_timeout_detector_decorator': 'time',
    'aio_timeout_generator': 'time',
    'delta_to_seconds': 'time',
    'delta_to_seconds_or_none': 'time',
    'format_time': 'time',
    'timedelta_to_seconds': 'time',
    'timeout_generator': 'time',
}


def __getattr__(name: str) -> _typing.Any:
    """Lazily import a submodule or exported name on first access (PEP 562).

    Args:
        name: Attribute requested on the ``python_utils`` package.

    Returns:
        The imported submodule or object. It is cached in ``globals()`` so
        this hook runs only once per name.

    Raises:
        AttributeError: If ``name`` is not a known submodule or export.
    """
    if name in _SUBMODULES:
        module = _importlib.import_module(f'.{name}', __name__)
    elif name in _NAME_TO_MODULE:
        module = _importlib.import_module(
            f'.{_NAME_TO_MODULE[name]}', __name__
        )
        value = getattr(module, name)
        globals()[name] = value  # cache so __getattr__ runs only once
        return value
    else:
        raise AttributeError(f'module {__name__!r} has no attribute {name!r}')

    globals()[name] = module
    return module


def __dir__() -> list[str]:
    """List all eager and lazily-available names (for tab-completion)."""
    return sorted(
        set(globals()) | set(__all__) | _SUBMODULES | set(_NAME_TO_MODULE)
    )


__all__ = [
    'CastedDict',
    'LazyCastedDict',
    'Logged',
    'LoggerBase',
    'UniqueList',
    '__version__',
    'abatcher',
    'acount',
    'aio',
    'aio_generator_timeout_detector',
    'aio_generator_timeout_detector_decorator',
    'aio_timeout_generator',
    'batcher',
    'camel_to_underscore',
    'converters',
    'decorators',
    'delta_to_seconds',
    'delta_to_seconds_or_none',
    'format_time',
    'formatters',
    'generators',
    'get_terminal_size',
    'import_',
    'import_global',
    'listify',
    'logger',
    'raise_exception',
    'remap',
    'reraise',
    'scale_1024',
    'set_attributes',
    'terminal',
    'time',
    'timedelta_to_seconds',
    'timeout_generator',
    'timesince',
    'to_float',
    'to_int',
    'to_str',
    'to_unicode',
    'types',
]
