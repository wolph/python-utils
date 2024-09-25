"""
This module provides type definitions and utility functions for type hinting.

It includes:
- Shorthand for commonly used types such as Optional and Union.
- Type aliases for various data structures and common types.
- Importing all types from the `typing` and `typing_extensions` modules.
- Importing specific types from the `types` module.

The module also configures Pyright to ignore wildcard import warnings.
"""
# pyright: reportWildcardImportFromLibrary=false
# ruff: noqa: F405

import datetime
import decimal
from re import Match, Pattern
from types import *  # pragma: no cover  # noqa: F403
from typing import *  # pragma: no cover  # noqa: F403

# import * does not import these in all Python versions
# Quickhand for optional because it gets so much use. If only Python had
# support for an optional type shorthand such as `SomeType?` instead of
# `Optional[SomeType]`.
# Since the Union operator is only supported for Python 3.10, we'll create a
# shorthand for it.
from typing import (
    IO,
    BinaryIO,
    Optional as O,  # noqa: N817
    TextIO,
    Union as U,  # noqa: N817
)

from typing_extensions import *  # type: ignore[no-redef,assignment] # noqa: F403

Scope = Dict[str, Any]
OptionalScope = O[Scope]
Number = U[int, float]
DecimalNumber = U[Number, decimal.Decimal]
ExceptionType = Type[Exception]
ExceptionsType = U[Tuple[ExceptionType, ...], ExceptionType]
StringTypes = U[str, bytes]

delta_type = U[datetime.timedelta, int, float]
timestamp_type = U[
    datetime.timedelta,
    datetime.date,
    datetime.datetime,
    str,
    int,
    float,
    None,
]

__all__ = [
    'OptionalScope',
    'Number',
    'DecimalNumber',
    'delta_type',
    'timestamp_type',
    # The types from the typing module.
    # Super-special typing primitives.
    'Annotated',
    'Any',
    'Callable',
    'ClassVar',
    'Concatenate',
    'Final',
    'ForwardRef',
    'Generic',
    'Literal',
    'SupportsIndex',
    'Optional',
    'ParamSpec',
    'ParamSpecArgs',
    'ParamSpecKwargs',
    'Protocol',
    'Tuple',
    'Type',
    'TypeVar',
    'Union',
    # ABCs (from collections.abc).
    'AbstractSet',
    'ByteString',
    'Container',
    'ContextManager',
    'Hashable',
    'ItemsView',
    'Iterable',
    'Iterator',
    'KeysView',
    'Mapping',
    'MappingView',
    'MutableMapping',
    'MutableSequence',
    'MutableSet',
    'Sequence',
    'Sized',
    'ValuesView',
    'Awaitable',
    'AsyncIterator',
    'AsyncIterable',
    'Coroutine',
    'Collection',
    'AsyncGenerator',
    'AsyncContextManager',
    # Structural checks, a.k.a. protocols.
    'Reversible',
    'SupportsAbs',
    'SupportsBytes',
    'SupportsComplex',
    'SupportsFloat',
    'SupportsIndex',
    'SupportsInt',
    'SupportsRound',
    # Concrete collection types.
    'ChainMap',
    'Counter',
    'Deque',
    'Dict',
    'DefaultDict',
    'List',
    'OrderedDict',
    'Set',
    'FrozenSet',
    'NamedTuple',  # Not really a type.
    'TypedDict',  # Not really a type.
    'Generator',
    # Other concrete types.
    'BinaryIO',
    'IO',
    'Match',
    'Pattern',
    'TextIO',
    # One-off things.
    'AnyStr',
    'cast',
    'final',
    'get_args',
    'get_origin',
    'get_type_hints',
    'is_typeddict',
    'NewType',
    'no_type_check',
    'no_type_check_decorator',
    'NoReturn',
    'overload',
    'runtime_checkable',
    'Text',
    'TYPE_CHECKING',
    'TypeAlias',
    'TypeGuard',
    'TracebackType',
    # Types from the `types` module.
    'FunctionType',
    'LambdaType',
    'CodeType',
    'MappingProxyType',
    'SimpleNamespace',
    'GeneratorType',
    'CoroutineType',
    'AsyncGeneratorType',
    'MethodType',
    'BuiltinFunctionType',
    'BuiltinMethodType',
    'WrapperDescriptorType',
    'MethodWrapperType',
    'MethodDescriptorType',
    'ClassMethodDescriptorType',
    'ModuleType',
    'TracebackType',
    'FrameType',
    'GetSetDescriptorType',
    'MemberDescriptorType',
    'new_class',
    'resolve_bases',
    'prepare_class',
    'DynamicClassAttribute',
    'coroutine',
]
