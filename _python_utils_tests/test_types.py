"""Regression tests for the public ``python_utils.types`` facade."""

import collections
import sys

from python_utils import types


def test_types_all_entries_are_unique() -> None:
    """Export every public name once."""
    counts: collections.Counter[str] = collections.Counter(types.__all__)
    duplicates: list[str] = sorted(
        name for name, count in counts.items() if count > 1
    )

    assert duplicates == []


def test_types_all_entries_exist() -> None:
    """Resolve every name in ``__all__`` so star imports keep working."""
    missing: list[str] = [
        name for name in types.__all__ if not hasattr(types, name)
    ]

    assert missing == []


def test_types_star_import() -> None:
    """Import the public facade with ``from python_utils.types import *``."""
    namespace: dict[str, object] = {}
    exec('from python_utils.types import *', namespace)  # noqa: S102

    assert set(types.__all__) <= namespace.keys()


def test_types_all_keeps_removed_typing_names_in_place() -> None:
    """Keep the 4.1.4 order of ``__all__`` where the names still exist."""
    removed_in_315: list[str] = ['ByteString', 'no_type_check_decorator']
    if sys.version_info >= (3, 15):
        assert not set(removed_in_315) & set(types.__all__)
        return

    # Each name sits in its alphabetical slot, not appended at the end.
    assert types.__all__.index('ByteString') == (
        types.__all__.index('BuiltinMethodType') + 1
    )
    assert types.__all__.index('no_type_check_decorator') == (
        types.__all__.index('no_type_check') + 1
    )
