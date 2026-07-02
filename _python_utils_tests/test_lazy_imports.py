"""Tests for the lazy-import machinery that keeps `import python_utils` light
(PEP 562 `__getattr__`/`__dir__` in the package, deferred ``asyncio`` in
``python_utils.time``).
"""

import collections.abc
import os
import subprocess
import sys

import pytest

import python_utils


def _run_clean(code: str) -> subprocess.CompletedProcess[str]:
    """Run ``code`` in a fresh interpreter and return the result."""
    # Run in a fresh interpreter: the test session itself has long since
    # imported asyncio/typing_extensions, so in-process checks are useless.
    env = {**os.environ, 'PYTHONPATH': os.pathsep.join(sys.path)}
    return subprocess.run(
        [sys.executable, '-c', code],
        capture_output=True,
        text=True,
        env=env,
    )


def test_package_lazy_attribute_access() -> None:
    """Resolve submodule and exported names via ``__getattr__``."""
    # Submodule access and exported-name access both resolve via __getattr__.
    aio = python_utils.aio
    assert python_utils.aio is aio  # repeated access returns the cached module
    assert callable(python_utils.acount)
    assert isinstance(python_utils.__version__, str)
    missing = 'definitely_not_a_real_attribute'
    with pytest.raises(AttributeError):
        getattr(python_utils, missing)


def test_bare_import_stays_light() -> None:
    """Keep a bare import free of asyncio and typing_extensions."""
    # Importing the package must not eagerly pull in heavy/optional deps.
    result = _run_clean(
        'import sys, python_utils\n'
        "assert 'asyncio' not in sys.modules, "
        "sorted(m for m in sys.modules if m.startswith('asyncio'))\n"
        "assert 'typing_extensions' not in sys.modules\n"
    )
    assert result.returncode == 0, result.stderr


def test_importing_time_submodule_avoids_asyncio() -> None:
    """Import ``python_utils.time`` without importing asyncio."""
    # Importing python_utils.time for its synchronous helpers must not import
    # asyncio; the async helpers import it lazily inside their own bodies.
    result = _run_clean(
        'import sys, python_utils.time\n'
        "assert 'asyncio' not in sys.modules, "
        "sorted(m for m in sys.modules if m.startswith('asyncio'))\n"
    )
    assert result.returncode == 0, result.stderr


def test_first_access_caches_into_module_dict() -> None:
    """Cache the first lazy access into the module dict."""
    # PEP 562 __getattr__ runs once: the resolved object is cached in the
    # module namespace so subsequent lookups skip __getattr__ entirely.
    module = python_utils.time
    assert python_utils.__dict__['time'] is module

    func = python_utils.format_time
    assert python_utils.__dict__['format_time'] is func


def test_dir_lists_lazy_submodules() -> None:
    """List lazy submodules and ``__all__`` names via ``dir``."""
    # Lazy submodules that are not in __all__ (e.g. ``containers`` and
    # ``exceptions``) must still be discoverable via ``dir``; tools such as
    # ``import_global`` intersect requested names with ``dir(module)``.
    names = set(dir(python_utils))
    assert {'containers', 'exceptions'} <= names
    assert set(python_utils.__all__) <= names


def test_star_import_resolves_all_names() -> None:
    """Bind every ``__all__`` name via a package star-import."""
    # `from python_utils import *` goes through __getattr__ for every name in
    # __all__; none may raise AttributeError, and all must be bound.
    namespace: dict[str, object] = {}
    exec('from python_utils import *', namespace)  # noqa: S102
    missing = set(python_utils.__all__) - set(namespace)
    assert not missing


@pytest.mark.asyncio
async def test_aio_timeout_generator_default_iterable() -> None:
    """Default the iterable to ``aio.acount`` when omitted."""
    # With no iterable the generator defaults to ``aio.acount`` -- exercising
    # the lazy ``aio``/``asyncio`` import and the None-resolution branch.
    count = 0
    generator: collections.abc.AsyncGenerator[object, None] = (
        python_utils.aio_timeout_generator(timeout=0.05, interval=0.0)
    )
    async for _ in generator:
        count += 1
        if count >= 2:
            break

    assert count == 2

    # Sanity: the re-exported type alias still resolves through the package.
    assert python_utils.types.AsyncGenerator is not None
