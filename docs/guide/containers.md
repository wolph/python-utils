# 📦 Smart containers

Drop-in replacements for `dict` and `list` that add type casting, uniqueness and
slicing — while staying ordinary `dict`/`list` subclasses you can pass anywhere.

## `CastedDict` — cast keys and values on the way in

Give it a key cast and a value cast (either may be `None` to skip). Every
assignment — including `update` and construction — is cast eagerly, so what you
store is already the right type:

```python
from python_utils import containers

d = containers.CastedDict(int, int)
d['3'] = '4'
d.update({'5': '6'})
d                       # {3: 4, 5: 6}
```

Use the subscription syntax to keep type checkers happy:

```python
d: containers.CastedDict[int, int] = containers.CastedDict(int, int)
```

## `LazyCastedDict` — cast values only when read

Same idea, but values are stored raw and cast on access. Handy when casting is
expensive and you only read a subset of the keys. Note that values are **not**
cached, so the cast runs on every read:

```python
from python_utils import containers

d = containers.LazyCastedDict(int, int)
d['3'] = '4'
d.update({'5': '6'})

d                       # {3: '4', 5: '6'}   <- values still raw
d[3]                    # 4                   <- cast on access
list(d.values())        # [4, 6]
```

## `UniqueList` — a list that rejects duplicates

By default duplicates are silently ignored; set `on_duplicate='raise'` to turn
them into errors instead. Uniqueness is enforced across `append`, `insert`,
`extend` and item assignment, backed by an internal `set` for O(1) membership
tests:

```python
from python_utils import containers

u = containers.UniqueList(1, 2, 3)
u.append(2)             # ignored
u                       # [1, 2, 3]

strict = containers.UniqueList(1, 2, 3, on_duplicate='raise')
strict.append(2)        # ValueError: Duplicate value: 2
```

## `SliceableDeque` — a deque you can slice

A `collections.deque` keeps fast appends and pops at both ends but doesn't
support slicing. `SliceableDeque` adds it, plus friendly equality against lists,
tuples and sets:

```python
from python_utils import containers

s = containers.SliceableDeque([1, 2, 3, 4, 5])
s[1:4]                  # SliceableDeque([2, 3, 4])
s[::-1]                 # SliceableDeque([5, 4, 3, 2, 1])
s == [1, 2, 3, 4, 5]    # True
```

See the {doc}`API reference <../python_utils>` for every method and overload.
