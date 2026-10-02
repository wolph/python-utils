"""Tests for the import helpers in ``python_utils.import_``."""

import collections.abc
import pathlib
import sys

import pytest

from python_utils import import_, types

#: Top-level name of the package that the ``nested_module`` fixture creates.
NESTED_PACKAGE: str = 'python_utils_spam'


@pytest.fixture
def nested_module(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> collections.abc.Iterator[str]:
    """Create ``python_utils_spam.eggs.bacon`` and yield its dotted name."""
    package: pathlib.Path = tmp_path / NESTED_PACKAGE
    subpackage: pathlib.Path = package / 'eggs'
    subpackage.mkdir(parents=True)
    (package / '__init__.py').write_text('', encoding='utf-8')
    (subpackage / '__init__.py').write_text('', encoding='utf-8')
    (subpackage / 'bacon.py').write_text("ham = 'ham'\n", encoding='utf-8')
    monkeypatch.setattr(sys, 'path', [str(tmp_path), *sys.path])

    yield f'{NESTED_PACKAGE}.eggs.bacon'

    imported: list[str] = [
        name for name in sys.modules if name.split('.')[0] == NESTED_PACKAGE
    ]
    for name in imported:
        del sys.modules[name]


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


def test_import_global_nested_module(nested_module: str) -> None:
    """Import a dotted name whose last module nothing imported before."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__name__': __name__}
    assert nested_module not in sys.modules
    import_.import_global(nested_module, locals_=locals_, globals_=globals_)
    assert globals_['ham'] == 'ham'


def test_import_global_missing_nested_module(nested_module: str) -> None:
    """Keep the ``ImportError`` for a nested module that does not exist."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__name__': __name__}
    error: types.Any = import_.import_global(
        f'{nested_module}.sausage',
        exceptions=ImportError,
        locals_=locals_,
        globals_=globals_,
    )
    assert type(error) is ImportError
    assert str(error) == f'No module named {nested_module}.sausage'


def test_import_global_attribute_of_non_module() -> None:
    """Report a path through an object that is not a module as missing."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__name__': __name__}
    error: types.Any = import_.import_global(
        'os.environ.spam',
        exceptions=ImportError,
        locals_=locals_,
        globals_=globals_,
    )
    assert type(error) is ImportError
    assert str(error) == 'No module named os.environ.spam'
