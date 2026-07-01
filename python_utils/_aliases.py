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

#: A namespace mapping, e.g. ``locals()``/``globals()`` (name -> value).
Scope = dict[str, Any]
#: A :data:`Scope`, or ``None`` when no namespace is supplied.
OptionalScope = Scope | None
#: Any plain (non-decimal) number: an ``int`` or a ``float``.
Number = int | float
#: A :data:`Number` or a :class:`decimal.Decimal`, for precise arithmetic.
DecimalNumber = Number | decimal.Decimal
#: An exception class (not an instance), e.g. ``ValueError``.
ExceptionType = type[Exception]
#: One exception class or a tuple of them, as accepted by ``except``.
ExceptionsType = tuple[ExceptionType, ...] | ExceptionType
#: Text-like data: ``str`` or ``bytes``.
StringTypes = str | bytes

#: A time interval expressed as a ``timedelta`` or a number of seconds.
delta_type = datetime.timedelta | int | float
#: Anything :func:`~python_utils.time.format_time` can render: a duration, a
#: date/datetime, a numeric/str timestamp, or ``None``.
timestamp_type = (
    datetime.timedelta
    | datetime.date
    | datetime.datetime
    | str
    | int
    | float
    | None
)
