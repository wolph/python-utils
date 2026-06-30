"""Lightweight, stdlib-only type aliases shared across python_utils.

These live here (rather than in ``python_utils.types``) so internal modules can
import them without dragging in ``typing_extensions``. ``python_utils.types``
re-exports everything defined here, so the public names are unchanged.
"""

from __future__ import annotations

import datetime
import decimal
from typing import Any

__all__ = [
    'DecimalNumber',
    'ExceptionType',
    'ExceptionsType',
    'Number',
    'OptionalScope',
    'Scope',
    'StringTypes',
    'delta_type',
    'timestamp_type',
]

Scope = dict[str, Any]
OptionalScope = Scope | None
Number = int | float
DecimalNumber = Number | decimal.Decimal
ExceptionType = type[Exception]
ExceptionsType = tuple[ExceptionType, ...] | ExceptionType
StringTypes = str | bytes

delta_type = datetime.timedelta | int | float
timestamp_type = (
    datetime.timedelta
    | datetime.date
    | datetime.datetime
    | str
    | int
    | float
    | None
)
