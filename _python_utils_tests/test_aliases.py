"""The lightweight alias module must define the public type aliases without
pulling in typing_extensions, so importers stay light.
"""

import os
import subprocess
import sys


def test_aliases_do_not_import_typing_extensions() -> None:
    """Importing ``_aliases`` must not pull in typing_extensions."""
    code = (
        'import sys, python_utils._aliases\n'
        "assert 'typing_extensions' not in sys.modules\n"
    )
    result = subprocess.run(
        [sys.executable, '-c', code],
        capture_output=True,
        text=True,
        env={**os.environ, 'PYTHONPATH': os.pathsep.join(sys.path)},
    )
    assert result.returncode == 0, result.stderr


def test_aliases_values() -> None:
    """Check the alias values and the ``__all__`` contents."""
    from python_utils import _aliases

    assert _aliases.Number == (int | float)
    assert _aliases.delta_type == (
        __import__('datetime').timedelta | int | float
    )
    assert set(_aliases.__all__) == {
        'Scope',
        'OptionalScope',
        'Number',
        'DecimalNumber',
        'ExceptionType',
        'ExceptionsType',
        'StringTypes',
        'delta_type',
        'timestamp_type',
    }


def test_types_reexports_aliases_identically() -> None:
    """Re-export every ``_aliases`` name identically via ``types``."""
    from python_utils import _aliases, types

    for name in _aliases.__all__:
        assert getattr(types, name) is getattr(_aliases, name), name


def test_types_still_exposes_datetime_and_decimal() -> None:
    """Keep ``datetime`` and ``decimal`` as ``types`` module attributes."""
    # Backwards compatibility: on 3.x these leaked as module attributes via
    # module-level imports, so `from python_utils.types import datetime` and
    # attribute access both worked. Moving the aliases into _aliases must not
    # drop them.
    import datetime
    import decimal

    from python_utils import types

    assert types.datetime is datetime
    assert types.decimal is decimal


def test_types_still_exposes_typing_extensions_surface() -> None:
    """The ``types`` facade still re-exports ``Self``."""
    # The facade must keep re-exporting typing_extensions (e.g. Self).
    # ``hasattr`` (not ``types.Self``) avoids basedpyright's
    # reportUnknownMemberType, since the wildcard re-export has no static type.
    from python_utils import types

    assert hasattr(types, 'Self')
