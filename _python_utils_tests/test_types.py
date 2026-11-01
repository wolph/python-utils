"""Regression tests for the public ``python_utils.types`` facade."""

import collections

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
