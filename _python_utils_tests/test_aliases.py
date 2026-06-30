"""The lightweight alias module must define the public type aliases without
pulling in typing_extensions, so importers stay light.
"""

import os
import subprocess
import sys


def test_aliases_do_not_import_typing_extensions() -> None:
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
    from python_utils import _aliases, types

    for name in _aliases.__all__:
        assert getattr(types, name) is getattr(_aliases, name), name


def test_types_still_exposes_typing_extensions_surface() -> None:
    # The facade must keep re-exporting typing_extensions (e.g. Self).
    # ``hasattr`` (not ``types.Self``) avoids basedpyright's
    # reportUnknownMemberType, since the wildcard re-export has no static type.
    from python_utils import types

    assert hasattr(types, 'Self')
