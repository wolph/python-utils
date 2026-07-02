"""Deterministic import-footprint regression gate.

Each target module is imported in a clean subprocess; a per-target denylist of
heavy modules must be absent from sys.modules afterward. This is the CI
performance guard: it fails the moment an eager heavy import is reintroduced.
"""

import json
import os
import subprocess
import sys

import pytest

# (import target, modules that must be ABSENT from sys.modules afterward)
FOOTPRINT_CASES = [
    ('python_utils', ('typing_extensions', 'asyncio')),
    ('python_utils.time', ('typing_extensions', 'asyncio')),
    ('python_utils.logger', ('typing_extensions',)),
    ('python_utils.converters', ('typing_extensions', 'asyncio')),
    ('python_utils.formatters', ('typing_extensions', 'asyncio')),
    ('python_utils.import_', ('typing_extensions', 'asyncio')),
    ('python_utils.terminal', ('typing_extensions',)),
    ('python_utils.containers', ('typing_extensions', 'asyncio')),
    ('python_utils.decorators', ('typing_extensions', 'asyncio')),
    ('python_utils.exceptions', ('typing_extensions', 'asyncio')),
    # aio, generators legitimately use asyncio; only typing_extensions denied.
    ('python_utils.aio', ('typing_extensions',)),
    ('python_utils.generators', ('typing_extensions',)),
]


def _modules_after_import(target: str) -> set[str]:
    """Return ``sys.modules`` after importing ``target`` cleanly."""
    code = (
        f'import sys, {target}\n'
        'import json\n'
        'print(json.dumps(sorted(sys.modules)))\n'
    )
    result = subprocess.run(
        [sys.executable, '-c', code],
        capture_output=True,
        text=True,
        env={**os.environ, 'PYTHONPATH': os.pathsep.join(sys.path)},
    )
    assert result.returncode == 0, result.stderr

    return set(json.loads(result.stdout))


@pytest.mark.parametrize(('target', 'denied'), FOOTPRINT_CASES)
def test_import_footprint(target: str, denied: tuple[str, ...]) -> None:
    """Importing ``target`` must not pull in denied modules."""
    present = _modules_after_import(target)
    leaked = [m for m in denied if m in present]
    assert not leaked, f'{target} eagerly imported {leaked}'


def test_bare_import_module_count_under_budget() -> None:
    """Keep a bare import under the module-count budget."""
    # Coarse bloat tripwire (denylist above is the real guard). Cap tightened
    # now that __version__ is lazy (importlib.metadata no longer pulled on bare
    # import). Bump only if a new Python version legitimately adds startup
    # modules. Measures modules ADDED by importing python_utils.
    added = len(_modules_after_import('python_utils')) - len(
        _modules_after_import('sys')
    )
    assert added < 40, f'python_utils added {added} modules to sys.modules'


def test_bare_import_does_not_pull_importlib_metadata() -> None:
    """A bare import must not import ``importlib.metadata``."""
    # __version__ is resolved lazily; bare import must not call
    # importlib.metadata.version() (which drags in email/zipfile/json/...).
    present = _modules_after_import('python_utils')
    assert 'importlib.metadata' not in present


def test_version_resolves_correctly() -> None:
    """Resolve ``__version__`` lazily to a non-empty string."""
    import python_utils

    assert isinstance(python_utils.__version__, str)
    assert python_utils.__version__  # non-empty


PUBLIC_CALLABLES_TO_INTROSPECT = [
    ('python_utils.time', 'timeout_generator'),
    ('python_utils.time', 'aio_timeout_generator'),
    ('python_utils.time', 'format_time'),
    ('python_utils.converters', 'remap'),
    ('python_utils.converters', 'to_int'),
    ('python_utils.formatters', 'timesince'),
    ('python_utils.import_', 'import_global'),
]


@pytest.mark.parametrize(('module', 'name'), PUBLIC_CALLABLES_TO_INTROSPECT)
def test_get_type_hints_still_resolves(module: str, name: str) -> None:
    """Resolve type hints without ``NameError`` for public APIs."""
    import importlib
    import typing

    obj = getattr(importlib.import_module(module), name)
    # Must not raise NameError now that type imports moved/changed.
    typing.get_type_hints(obj)
