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

# Kept as public module attributes for backwards compatibility:
# `from python_utils.types import datetime, decimal` worked in 3.x.
import datetime as datetime
import decimal as decimal
from re import Match, Pattern
from types import *  # pragma: no cover  # noqa: F403
from typing import *  # pragma: no cover  # noqa: F403

# `import *` does not import these on all Python versions. `O` / `U` are kept
# as backwards-compatible shorthands; new code should prefer `X | None`.
from typing import (
    IO,
    BinaryIO,
    Optional as O,  # noqa: N817
    TextIO,
    Union as U,  # noqa: N817
)

from typing_extensions import *  # type: ignore[no-redef,assignment] # noqa: F403

# Lightweight aliases live in a stdlib-only module so importers don't pull in
# typing_extensions; re-exported here to keep the public surface unchanged.
# The redundant `X as X` form marks these as intentional re-exports so strict
# type checkers and ruff see `python_utils.types.X` without adding them to
# `__all__` (which would change `from python_utils.types import *`).
from ._aliases import (
    DecimalNumber as DecimalNumber,
    ExceptionType as ExceptionType,
    ExceptionsType as ExceptionsType,
    Number as Number,
    OptionalScope as OptionalScope,
    Scope as Scope,
    StringTypes as StringTypes,
    delta_type as delta_type,
    timestamp_type as timestamp_type,
)

__all__ = [
    'IO',
    'TYPE_CHECKING',
    # ABCs (from collections.abc).
    'AbstractSet',
    # The types from the typing module.
    # Super-special typing primitives.
    'Annotated',
    'Any',
    # One-off things.
    'AnyStr',
    'AsyncContextManager',
    'AsyncGenerator',
    'AsyncGeneratorType',
    'AsyncIterable',
    'AsyncIterator',
    'Awaitable',
    # Other concrete types.
    'BinaryIO',
    'BuiltinFunctionType',
    'BuiltinMethodType',
    'ByteString',
    'Callable',
    # Concrete collection types.
    'ChainMap',
    'ClassMethodDescriptorType',
    'ClassVar',
    'CodeType',
    'Collection',
    'Concatenate',
    'Container',
    'ContextManager',
    'Coroutine',
    'CoroutineType',
    'Counter',
    'DecimalNumber',
    'DefaultDict',
    'Deque',
    'Dict',
    'DynamicClassAttribute',
    'Final',
    'ForwardRef',
    'FrameType',
    'FrozenSet',
    # Types from the `types` module.
    'FunctionType',
    'Generator',
    'GeneratorType',
    'Generic',
    'GetSetDescriptorType',
    'Hashable',
    'ItemsView',
    'Iterable',
    'Iterator',
    'KeysView',
    'LambdaType',
    'List',
    'Literal',
    'Mapping',
    'MappingProxyType',
    'MappingView',
    'Match',
    'MemberDescriptorType',
    'MethodDescriptorType',
    'MethodType',
    'MethodWrapperType',
    'ModuleType',
    'MutableMapping',
    'MutableSequence',
    'MutableSet',
    'NamedTuple',  # Not really a type.
    'NewType',
    'NoReturn',
    'Number',
    'O',
    'Optional',
    'OptionalScope',
    'OrderedDict',
    'ParamSpec',
    'ParamSpecArgs',
    'ParamSpecKwargs',
    'Pattern',
    'Protocol',
    # Structural checks, a.k.a. protocols.
    'Reversible',
    'Sequence',
    'Set',
    'SimpleNamespace',
    'Sized',
    'SupportsAbs',
    'SupportsBytes',
    'SupportsComplex',
    'SupportsFloat',
    'SupportsIndex',
    'SupportsIndex',
    'SupportsInt',
    'SupportsRound',
    'Text',
    'TextIO',
    'TracebackType',
    'TracebackType',
    'Tuple',
    'Type',
    'TypeAlias',
    'TypeGuard',
    'TypeVar',
    'TypedDict',  # Not really a type.
    'U',
    'Union',
    'ValuesView',
    'WrapperDescriptorType',
    'cast',
    'coroutine',
    'delta_type',
    'final',
    'get_args',
    'get_origin',
    'get_type_hints',
    'is_typeddict',
    'new_class',
    'no_type_check',
    'no_type_check_decorator',
    'overload',
    'prepare_class',
    'resolve_bases',
    'runtime_checkable',
    'timestamp_type',
]
