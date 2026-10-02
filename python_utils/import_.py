"""
This module provides utilities for importing modules and handling exceptions.

Classes:
    DummyError(Exception):
        A custom exception class used as a default for exception handling.

Functions:
    import_global(name, modules=None, exceptions=DummyError, locals_=None,
        globals_=None, level=-1):
        Imports the requested items into the global scope, with support for
        relative imports and custom exception handling.
"""

import importlib
import types
import typing

from python_utils import _aliases


class DummyError(Exception):
    """A custom exception class used as a default for exception handling."""


#: Backwards-compatible legacy alias for ``DummyError``.
DummyException = DummyError


def _get_attribute(module: typing.Any, attr: str, name: str) -> typing.Any:
    """Return ``module.attr``, importing it as a submodule when needed.

    A submodule only becomes an attribute of its parent once something has
    imported it.

    Args:
        module: The module, or other object, to take the attribute from.
        attr: The name of the attribute or submodule.
        name: The full dotted name that is being imported, for the error.

    Returns:
        The attribute or the imported submodule.

    Raises:
        ImportError: When ``module`` has no such attribute or submodule. An
            error that the submodule raises while it is imported is passed
            on as it is, a missing dependency included.
    """
    try:
        return getattr(module, attr)
    except AttributeError as error:
        if not isinstance(module, types.ModuleType):
            # The same error as for a missing module, as it always was.
            raise ImportError(  # noqa: TRY004
                f'No module named {name}'
            ) from error

    submodule: str = f'{module.__name__}.{attr}'
    try:
        return importlib.import_module(submodule)
    except ModuleNotFoundError as error:
        missing: str = error.name or ''
        if missing != submodule and not submodule.startswith(f'{missing}.'):
            # The submodule exists and one of its own imports is missing.
            raise

        raise ImportError(f'No module named {name}') from error


def import_global(  # noqa: C901
    name: str,
    modules: list[str] | None = None,
    exceptions: _aliases.ExceptionsType = DummyError,
    locals_: _aliases.OptionalScope = None,
    globals_: _aliases.OptionalScope = None,
    level: int = -1,
) -> typing.Any:  # sourcery skip: hoist-if-from-if
    """Import the requested items into the global scope.

    WARNING! this method _will_ overwrite your global scope
    If you have a variable named `path` and you call `import_global('sys')`
    it will be overwritten with `sys.path`

    Args:
        name (str): the name of the module to import, e.g. sys
        modules (list[str]): the names to import from the module, use None
            for everything. An empty list also imports everything. A single
            name needs a list as well, a bare string is read as a collection
            of one-character names. Names that start with an underscore are
            never imported.
        exceptions (Exception): the exception to catch, e.g. ImportError
        locals_: the `locals()` method (in case you need a different scope)
        globals_: the `globals()` method (in case you need a different scope)
        level (int): the level to import from, this can be used for
        relative imports
    """
    frame = None
    name_parts: list[str] = name.split('.')
    modules_set: set[str] = set()
    try:
        # If locals_ or globals_ are not given, autodetect them by inspecting
        # the current stack
        if locals_ is None or globals_ is None:
            import inspect

            frame = inspect.stack()[1][0]

            if locals_ is None:
                locals_ = frame.f_locals

            if globals_ is None:
                globals_ = frame.f_globals

        try:
            # Relative imports are supported (from .spam import eggs)
            if not name_parts[0]:
                name_parts = name_parts[1:]
                level = 1

            # raise IOError((name, level))
            module = __import__(
                name=name_parts[0] or '.',
                globals=globals_,
                locals=locals_,
                fromlist=name_parts[1:],
                level=max(level, 0),
            )

            # Make sure we get the right part of a dotted import (i.e.
            # spam.eggs should return eggs, not spam)
            for attr in name_parts[1:]:
                module = _get_attribute(module, attr, '.'.join(name_parts))

            # If no list of modules is given, autodetect from either __all__
            # or a dir() of the module
            if not modules:
                modules_set = set(getattr(module, '__all__', dir(module)))
            else:
                modules_set = set(modules).intersection(dir(module))

            # Add all items in modules to the global scope
            for k in set(dir(module)).intersection(modules_set):
                if k and k[0] != '_':
                    globals_[k] = getattr(module, k)
        except exceptions as e:
            return e
    finally:
        # Clean up, just to be sure
        del (  # pyrefly: ignore[unsupported-delete]
            name,
            name_parts,
            modules,
            modules_set,
            exceptions,
            locals_,
            globals_,
            frame,
        )
