import decimal
from typing import *  # pragma: no cover
# import * does not import Pattern
from typing import Pattern

# Quickhand for optional because it gets so much use. If only Python had
# support for an optional type shorthand such as `SomeType?` instead of
# `Optional[SomeType]`.
from typing import Optional as O
# Since the Union operator is only supported for Python 3.10, we'll create a
# shorthand for it.
from typing import Union as U

Scope = Dict[str, Any]
OptionalScope = O[Scope]
Number = U[int, float]
DecimalNumber = U[Number, decimal.Decimal]
ExceptionType = Type[Exception]
ExceptionsType = U[Tuple[ExceptionType, ...], ExceptionType]
StringTypes = U[str, bytes]

assert Pattern

__all__ = [
    'OptionalScope',
    'Number',
    'DecimalNumber',

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
    'Optional',
    'ParamSpec',
    'Protocol',
    'Tuple',
    'Type',
    'TypeVar',
    'Union',

    # ABCs (from collections.abc).
    'AbstractSet',  # collections.abc.Set.
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
    'ParamSpecArgs',
    'ParamSpecKwargs',
    'runtime_checkable',
    'Text',
    'TYPE_CHECKING',
    'TypeAlias',
    'TypeGuard',
]
