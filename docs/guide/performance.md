# 🪶 Performance: lazy imports

`import python_utils` is intentionally *cheap*. The package uses
[PEP 562](https://peps.python.org/pep-0562/) module-level `__getattr__` so that
**nothing** is imported when you import the package — each submodule and each
exported name is loaded on first access, then cached.

## Why it matters

Utility libraries are often imported everywhere, including in code paths that only
need one or two synchronous helpers. Eagerly importing every submodule would drag
in `asyncio` (via the async helpers) and other machinery you may never use,
inflating startup time and memory. Lazy loading keeps the import graph minimal.

In particular:

- Only need the synchronous helpers? `asyncio` is never imported.
- Even `typing_extensions` is deferred, so the base import stays tiny.

## See it for yourself

```python
import sys
import python_utils

'asyncio' in sys.modules             # False
'typing_extensions' in sys.modules   # False

python_utils.acount                  # touches `aio`, which imports asyncio...
'asyncio' in sys.modules             # True
```

## How it works

The package `__init__` maps every public name to the submodule that defines it and
resolves them on demand:

```python
def __getattr__(name):
    # look up which submodule provides `name`, import it lazily,
    # cache the result in globals() so __getattr__ runs only once,
    # and return it.
    ...
```

Type checkers and IDEs still see everything: the same names are declared under a
`typing.TYPE_CHECKING` block and listed in `__all__`, so autocompletion and static
analysis work exactly as if the imports were eager. `__dir__` is implemented too,
so `dir(python_utils)` and tab-completion list every lazily-available name.

## Practical tips

- Import what you use directly (`python_utils.to_int`) — the first access pays the
  one-time import cost for that module only.
- Importing from a submodule (`from python_utils import converters`) is equally
  lazy with respect to the *other* submodules.
- The cost is paid once per process; subsequent accesses are plain attribute
  lookups.
