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
