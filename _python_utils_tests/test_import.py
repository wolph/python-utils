"""Tests for the import helpers in ``python_utils.import_``."""

import collections.abc
import pathlib
import sys
from types import ModuleType

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
    (subpackage / 'needy.py').write_text(
        'import python_utils_missing_dependency\n', encoding='utf-8'
    )
    (subpackage / 'broken.py').write_text(
        "raise AttributeError('broken on purpose')\n", encoding='utf-8'
    )
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


def test_import_global_nested_module_missing_dependency(
    nested_module: str,
) -> None:
    """Show the missing dependency of a nested module that does exist."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__name__': __name__}
    with pytest.raises(ModuleNotFoundError) as raised:
        import_.import_global(
            f'{NESTED_PACKAGE}.eggs.needy', locals_=locals_, globals_=globals_
        )

    assert raised.value.name == 'python_utils_missing_dependency'


def test_import_global_nested_module_import_error(nested_module: str) -> None:
    """Show the error that a nested module raises while it is imported."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__name__': __name__}
    with pytest.raises(AttributeError, match='broken on purpose'):
        import_.import_global(
            f'{NESTED_PACKAGE}.eggs.broken', locals_=locals_, globals_=globals_
        )


def test_import_global_looks_an_attribute_up_once(
    nested_module: str, tmp_path: pathlib.Path
) -> None:
    """Ask a module for an attribute once, also when it computes it."""
    lazy: pathlib.Path = tmp_path / NESTED_PACKAGE / 'eggs' / 'lazy.py'
    lazy.write_text(
        'calls = []\n\n\n'
        'def __getattr__(name):\n'
        "    if name == 'computed':\n"
        '        calls.append(name)\n'
        '        return calls\n'
        '    raise AttributeError(name)\n',
        encoding='utf-8',
    )
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__name__': __name__}
    import_.import_global(
        f'{NESTED_PACKAGE}.eggs.lazy.computed',
        locals_=locals_,
        globals_=globals_,
    )

    assert sys.modules[f'{NESTED_PACKAGE}.eggs.lazy'].calls == ['computed']


def test_import_global_missing_below_detached_module(
    nested_module: str, tmp_path: pathlib.Path
) -> None:
    """Name the requested module when a module has another name itself."""
    detached: pathlib.Path = tmp_path / NESTED_PACKAGE / 'eggs' / 'detached.py'
    detached.write_text(
        "import types\n\nspam = types.ModuleType('python_utils_detached')\n",
        encoding='utf-8',
    )
    name: str = f'{NESTED_PACKAGE}.eggs.detached.spam.sausage'
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__name__': __name__}
    error: types.Any = import_.import_global(
        name, exceptions=ImportError, locals_=locals_, globals_=globals_
    )

    assert type(error) is ImportError
    assert str(error) == f'No module named {name}'


@pytest.mark.parametrize(
    'names', [None, ['virtual', 'none', '_private', 'missing']]
)
def test_import_global_lazy_module_exports(
    monkeypatch: pytest.MonkeyPatch, names: list[str] | None
) -> None:
    """Read declared and explicit exports through module __getattr__."""
    module_name = 'python_utils_lazy_export_fixture'
    module = ModuleType(module_name)
    calls: dict[str, int] = {}

    def lookup(name: str) -> types.Any:
        """Provide public names that are deliberately absent from dir()."""
        calls[name] = calls.get(name, 0) + 1
        if name == 'virtual':
            return 42
        if name == 'none':
            return None
        raise AttributeError(name)

    module.__dict__['__getattr__'] = lookup
    module.__dict__['__all__'] = ['virtual', 'none', '_private', 'missing']
    monkeypatch.setitem(sys.modules, module_name, module)
    scope: dict[str, types.Any] = {}
    import_.import_global(module_name, names, locals_={}, globals_=scope)
    assert scope == {'virtual': 42, 'none': None}
    assert calls['virtual'] == calls['none'] == 1


@pytest.mark.parametrize('error', [ImportError, RuntimeError])
def test_import_global_skips_failing_lazy_exports(
    monkeypatch: pytest.MonkeyPatch, error: type[Exception]
) -> None:
    """Skip a lazy export that fails to resolve, as 4.x did."""
    module_name = 'python_utils_failing_lazy_fixture'
    module = ModuleType(module_name)

    def lookup(name: str) -> types.Any:
        """Serve one working and one failing lazy export."""
        if name == 'working':
            return 1
        if name == 'broken':
            raise error('optional dependency missing')
        raise AttributeError(name)

    module.__dict__['__getattr__'] = lookup
    module.__dict__['__all__'] = ['eager', 'working', 'broken']
    module.__dict__['eager'] = 0
    monkeypatch.setitem(sys.modules, module_name, module)
    scope: dict[str, types.Any] = {}
    result = import_.import_global(module_name, locals_={}, globals_=scope)
    assert result is None
    assert scope == {'eager': 0, 'working': 1}


def test_import_global_ignores_names_that_are_not_strings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Skip entries of ``modules`` and ``__all__`` that are not names."""
    module_name = 'python_utils_odd_all_fixture'
    module = ModuleType(module_name)
    module.__dict__['__all__'] = ['eggs', 1]
    module.__dict__['eggs'] = 1
    monkeypatch.setitem(sys.modules, module_name, module)
    scope: dict[str, types.Any] = {}
    import_.import_global(module_name, locals_={}, globals_=scope)
    assert scope == {'eggs': 1}

    names: types.Any = ['sep', 1, b'sep']
    scope = {}
    import_.import_global('os', names, locals_={}, globals_=scope)
    assert list(scope) == ['sep']


def test_import_global_requested_name_needs_an_export(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Leave a catch-all ``__getattr__`` alone for undeclared names."""
    module_name = 'python_utils_catch_all_fixture'
    module = ModuleType(module_name)
    calls: list[str] = []

    def lookup(name: str) -> str:
        """Answer every name, as a lazy submodule loader would."""
        calls.append(name)
        return f'auto-{name}'

    module.__dict__['__getattr__'] = lookup
    monkeypatch.setitem(sys.modules, module_name, module)
    scope: dict[str, types.Any] = {}
    import_.import_global(module_name, ['eggs'], locals_={}, globals_=scope)
    assert scope == {}
    assert 'eggs' not in calls


@pytest.fixture
def deep_package(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> collections.abc.Iterator[str]:
    """Create ``testrel.nested.deeper`` with importable helper modules."""
    package: pathlib.Path = tmp_path / 'testrel'
    nested: pathlib.Path = package / 'nested'
    deeper: pathlib.Path = nested / 'deeper'
    deeper.mkdir(parents=True)
    (package / '__init__.py').write_text('', encoding='utf-8')
    (nested / '__init__.py').write_text('', encoding='utf-8')
    (deeper / '__init__.py').write_text('', encoding='utf-8')
    (package / 'helper.py').write_text('value = 42\n', encoding='utf-8')
    (nested / 'inner.py').write_text(
        "inner_value = 'inner'\n", encoding='utf-8'
    )
    monkeypatch.setattr(sys, 'path', [str(tmp_path), *sys.path])

    yield 'testrel'

    imported: list[str] = [
        name for name in sys.modules if name.split('.')[0] == 'testrel'
    ]
    for name in imported:
        del sys.modules[name]


def test_import_globals_relative_import_two_dots(deep_package: str) -> None:
    """Resolve ``..helper`` two levels up, to ``testrel.helper`` (#73)."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__package__': 'testrel.nested'}
    import_.import_global('..helper', locals_=locals_, globals_=globals_)
    assert globals_['value'] == 42


def test_import_globals_relative_import_three_dots(deep_package: str) -> None:
    """Resolve ``...helper`` three levels up, to ``testrel.helper`` (#73)."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {
        '__package__': 'testrel.nested.deeper'
    }
    import_.import_global('...helper', locals_=locals_, globals_=globals_)
    assert globals_['value'] == 42


def test_import_globals_relative_import_one_dot(deep_package: str) -> None:
    """Keep resolving a single leading dot one level up (#73 control)."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__package__': 'testrel.nested'}
    import_.import_global('.inner', locals_=locals_, globals_=globals_)
    assert globals_['inner_value'] == 'inner'


def test_import_globals_relative_import_dots_only(deep_package: str) -> None:
    """Reject a dots-only name, which names no module to import (#73)."""
    locals_: types.Dict[str, types.Any] = {}
    globals_: types.Dict[str, types.Any] = {'__package__': 'testrel.nested'}
    with pytest.raises(ImportError):
        import_.import_global('..', locals_=locals_, globals_=globals_)


def test_import_globals_relative_import_dots_only_exception(
    deep_package: str,
) -> None:
    """Keep raising ModuleNotFoundError for a dots-only name, as 4.2.0 did."""
    globals_: types.Dict[str, types.Any] = {
        '__package__': 'testrel.nested.deeper'
    }
    error = import_.import_global(
        '...',
        exceptions=ModuleNotFoundError,
        locals_={},
        globals_=globals_,
    )
    assert isinstance(error, ModuleNotFoundError)


def test_import_globals_relative_import_beyond_top_level(
    deep_package: str,
) -> None:
    """Raise ModuleNotFoundError above the top-level package, as 4.2.0 did."""
    globals_: types.Dict[str, types.Any] = {
        '__package__': 'testrel.nested.deeper'
    }
    with pytest.raises(ModuleNotFoundError, match='beyond top-level'):
        import_.import_global('....helper', locals_={}, globals_=globals_)


def test_import_globals_empty_name() -> None:
    """Keep raising IndexError for an empty name, as 4.2.0 did."""
    with pytest.raises(IndexError):
        import_.import_global('', locals_={}, globals_={'__package__': ''})


def test_import_globals_relative_import_trailing_dot(
    deep_package: str,
) -> None:
    """Raise ModuleNotFoundError for ``..helper.``, as 4.2.0 did."""
    globals_: types.Dict[str, types.Any] = {'__package__': 'testrel.nested'}
    with pytest.raises(ModuleNotFoundError):
        import_.import_global('..helper.', locals_={}, globals_=globals_)
