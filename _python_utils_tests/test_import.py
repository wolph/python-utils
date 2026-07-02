"""Tests for the import helpers in ``python_utils.import_``."""

from python_utils import import_, types


def test_import_globals_relative_import() -> None:
    """Resolve relative imports across several levels."""
    for i in range(-1, 5):
        relative_import(i)


def relative_import(level: int) -> None:
    """Import ``.formatters`` relatively into a fake module dict."""
    locals_: types.Dict[str, types.Any] = {}
    globals_ = {'__name__': 'python_utils.import_'}
    import_.import_global('.formatters', locals_=locals_, globals_=globals_)
    assert 'camel_to_underscore' in globals_


def test_import_globals_without_inspection() -> None:
    """Import a module without inspecting the caller frame."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__name__': __name__}
    import_.import_global(
        'python_utils.formatters', locals_=locals_, globals_=globals_
    )
    assert 'camel_to_underscore' in globals_


def test_import_globals_single_method() -> None:
    """Import only the single named attribute."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__name__': __name__}
    import_.import_global(
        'python_utils.formatters',
        ['camel_to_underscore'],
        locals_=locals_,
        globals_=globals_,
    )
    assert 'camel_to_underscore' in globals_


def test_import_globals_with_inspection() -> None:
    """Infer the target globals from the caller frame."""
    import_.import_global('python_utils.formatters')
    assert 'camel_to_underscore' in globals()


def test_import_globals_missing_module() -> None:
    """Ignore ``ImportError`` for a missing module (locals_)."""
    import_.import_global(
        'python_utils.spam', exceptions=ImportError, locals_=locals()
    )
    assert 'camel_to_underscore' in globals()


def test_import_locals_missing_module() -> None:
    """Ignore ``ImportError`` for a missing module (globals_)."""
    import_.import_global(
        'python_utils.spam', exceptions=ImportError, globals_=globals()
    )
    assert 'camel_to_underscore' in globals()
