<div align="center">

<img src="https://raw.githubusercontent.com/WoLpH/python-utils/develop/docs/_static/banner.svg" alt="python-utils" width="720">

# ⚡ Python Utils

**The fast, fully-typed stdlib helpers you keep rewriting — in one tiny, zero-dependency package.**

[![PyPI version](https://img.shields.io/pypi/v/python-utils.svg?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/python-utils)
[![Python versions](https://img.shields.io/pypi/pyversions/python-utils.svg?logo=python&logoColor=white)](https://pypi.python.org/pypi/python-utils)
[![CI](https://github.com/WoLpH/python-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/WoLpH/python-utils/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/WoLpH/python-utils/badge.svg?branch=develop)](https://coveralls.io/github/WoLpH/python-utils?branch=develop)
[![Typed](https://img.shields.io/badge/typed-mypy%20%7C%20pyright%20%7C%20pyrefly-blue.svg)](https://github.com/WoLpH/python-utils)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/pypi/l/python-utils.svg)](https://github.com/WoLpH/python-utils/blob/develop/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/python-utils.svg?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/python-utils)

[**Documentation**](https://python-utils.readthedocs.io/en/latest/) ·
[**PyPI**](https://pypi.python.org/pypi/python-utils) ·
[**Source**](https://github.com/WoLpH/python-utils) ·
[**Issues**](https://github.com/WoLpH/python-utils/issues)

</div>

---

Python Utils is a collection of small, battle-tested functions and classes that
make everyday Python patterns shorter, safer and faster. No sprawling framework,
no heavy dependencies — just the helpers you find yourself re-writing in project
after project, packaged once and typed to the hilt.

It has powered production code for years (and is used by libraries such as
[Django Utils](https://pypi.python.org/pypi/django-utils2) and
[progressbar2](https://pypi.python.org/pypi/progressbar2)).

## ✨ Highlights

- 🪶 **Zero-cost imports** — thanks to [PEP 562][pep562] lazy loading, `import
  python_utils` pulls in *nothing* until you actually touch a helper. No
  `asyncio`, no `typing_extensions`, until you ask for them.
- ⚡ **Async-native** — `acount`, `abatcher`, and timeout/stall detectors bring
  `itertools`-style ergonomics to `async for`.
- 📦 **Smart containers** — self-casting dicts, duplicate-proof lists and a
  sliceable deque.
- 🔢 **Forgiving converters** — pull an `int`/`float` out of *any* messy string,
  scale bytes to KiB/MiB, remap values between ranges (with `Decimal` precision).
- ⏱️ **Time & retries** — human-readable durations plus timeout generators for
  sampling slow APIs without hanging.
- 🎯 **Fully typed & 100% covered** — ships `py.typed`, passes **mypy**,
  **basedpyright** *and* **pyrefly** in strict mode, with 100% test coverage.
- 🐍 **Modern & tiny** — Python 3.10+, a single runtime dependency
  (`typing_extensions`), BSD-3 licensed.

## 🗺️ What's inside

| Module | What you get |
| --- | --- |
| [`converters`](https://python-utils.readthedocs.io/en/latest/) | `to_int` · `to_float` · `to_str` · `to_unicode` · `scale_1024` · `remap` |
| [`formatters`](https://python-utils.readthedocs.io/en/latest/) | `camel_to_underscore` · `apply_recursive` · `timesince` |
| [`time`](https://python-utils.readthedocs.io/en/latest/) | `format_time` · `timeout_generator` · `aio_timeout_generator` · `aio_generator_timeout_detector` |
| [`generators`](https://python-utils.readthedocs.io/en/latest/) | `batcher` · `abatcher` (batch by size **or** time interval) |
| [`aio`](https://python-utils.readthedocs.io/en/latest/) | `acount` · `acontainer` — async `itertools` |
| [`containers`](https://python-utils.readthedocs.io/en/latest/) | `CastedDict` · `LazyCastedDict` · `UniqueList` · `SliceableDeque` |
| [`decorators`](https://python-utils.readthedocs.io/en/latest/) | `listify` · `set_attributes` · `sample` · `wraps_classmethod` |
| [`logger`](https://python-utils.readthedocs.io/en/latest/) | `Logged` · `LoggerBase` (+ `Logurud` via the `loguru` extra) |
| [`import_`](https://python-utils.readthedocs.io/en/latest/) | `import_global` — programmatic `from x import *` |
| [`exceptions`](https://python-utils.readthedocs.io/en/latest/) | `raise_exception` · `reraise` |
| [`terminal`](https://python-utils.readthedocs.io/en/latest/) | `get_terminal_size` — works in shells, IPython & Jupyter |
| [`types`](https://python-utils.readthedocs.io/en/latest/) | handy type aliases (`Number`, `Scope`, `StringTypes`, …) |

## 📦 Installation

```bash
pip install python-utils
```

Optional extras:

```bash
pip install 'python-utils[loguru]'   # loguru-backed logging mixin
```

Python **3.10+** is required. The only runtime dependency is
`typing_extensions` (and it's imported lazily).

## 🚀 Quickstart

```python
import python_utils

# Pull a number out of any messy string
python_utils.to_int('listening on port=8080', regexp=True)   # 8080

# Human-readable sizes: (value, power-of-1024)
python_utils.scale_1024(1536, 2)                             # (1.5, 1)  -> 1.5 KiB

# Remap a value between ranges (46% volume -> dB on an AVR)
python_utils.remap(46.0, 0.0, 100.0, -80.0, 10.0)           # -38.6

# "time ago" formatting, Django-style
import datetime
python_utils.timesince(datetime.datetime.now() - datetime.timedelta(seconds=61))
# '1 minute and 1 second ago'
```

Everything is reachable straight off the top-level package (`python_utils.<name>`)
or from its submodule (`python_utils.converters.to_int`) — pick whichever reads
better. Either way, only the modules you touch get imported.

## 🧰 Examples

<details open>
<summary><b>🔢 Converters — numbers out of anything</b></summary>

```python
from python_utils import converters

# Extract digits with a built-in or custom regexp
converters.to_int('spam15eggs', regexp=True)          # 15
converters.to_int('nope', default=-1)                 # -1
converters.to_float('pi is 3.14', regexp=True)        # 3.14

# Scale bytes to a sensible unit (value, power) -> 2.0 KiB
converters.scale_1024(2048, 3)                         # (2.0, 1)

# Linear remap; pass a Decimal anywhere to keep full precision
converters.remap(500, 0, 1000, 0, 100)                # 50
import decimal
converters.remap(decimal.Decimal('250.0'), 0.0, 1000.0, 0.0, 100.0)
# Decimal('25.0')
```

</details>

<details>
<summary><b>📦 Containers — dicts & lists with super-powers</b></summary>

```python
from python_utils import containers

# Keys and values are cast on the way in
d = containers.CastedDict(int, int)
d['3'] = '4'
d.update({'5': '6'})
d                                   # {3: 4, 5: 6}

# A list that silently drops duplicates (or raises, if you prefer)
u = containers.UniqueList(1, 2, 3)
u.append(2)                         # ignored
u                                   # [1, 2, 3]

# A deque you can actually slice
s = containers.SliceableDeque([1, 2, 3, 4, 5])
s[1:4]                              # SliceableDeque([2, 3, 4])
```

</details>

<details>
<summary><b>⚡ Async helpers — <code>itertools</code> for <code>async for</code></b></summary>

```python
from python_utils import aio, generators

# Async counter (optionally with a delay and a stop value)
async def demo():
    async for i in aio.acount(stop=3):
        print(i)                    # 0, 1, 2

# Batch an async stream by size OR time interval — whichever comes first.
# Great for chunking bursty producers without ever stalling a slow loop.
async def batched():
    async for batch in generators.abatcher(aio.acount(stop=10), batch_size=3):
        print(batch)                # [0, 1, 2], [3, 4, 5], [6, 7, 8], [9]

# Sync batching too:
list(generators.batcher(range(9), 3))   # [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
```

</details>

<details>
<summary><b>⏱️ Time & retries — sample slow APIs, format durations</b></summary>

```python
import datetime
from python_utils import time

# Loop over a slow operation, but give up after `timeout` seconds
for i in time.timeout_generator(0.1, interval=0.06):
    ...                             # yields 0, 1, 2 then stops

# Format timedeltas, datetimes and raw seconds uniformly
time.format_time(1)                                         # '0:00:01'
time.format_time(datetime.timedelta(seconds=3661))         # '1:01:01'
time.format_time(datetime.datetime(2000, 1, 2, 3, 4, 5))   # '2000-01-02 03:04:05'
time.format_time(None)                                     # '--:--:--'
```

There's also `aio_timeout_generator` (the `async for` twin) and
`aio_generator_timeout_detector`, which fails fast when an async generator
stalls instead of hanging forever.

</details>

<details>
<summary><b>🔤 Formatters — case conversion & friendly timestamps</b></summary>

```python
from python_utils import formatters

formatters.camel_to_underscore('SpamEggsAndBacon')   # 'spam_eggs_and_bacon'

# Recursively rewrite every key in a nested dict
formatters.apply_recursive(
    formatters.camel_to_underscore,
    {'SpamEggs': {'FooBar': 1}},
)                                                    # {'spam_eggs': {'foo_bar': 1}}
```

</details>

<details>
<summary><b>🎀 Decorators — collect generators, tag functions, sample calls</b></summary>

```python
from python_utils import decorators

# Turn a generator into a concrete collection automatically
@decorators.listify()
def numbers():
    yield 1
    yield 2
    yield 3

numbers()                           # [1, 2, 3]

@decorators.listify(collection=dict)
def pairs():
    yield 'a', 1
    yield 'b', 2

pairs()                             # {'a': 1, 'b': 2}

# Attach metadata to a function (handy for the Django admin)
@decorators.set_attributes(short_description='Name')
def upper_case_name(self, obj):
    return f'{obj.first_name} {obj.last_name}'.upper()

# Only actually run ~10% of the calls
@decorators.sample(0.1)
def maybe_log(msg): ...
```

</details>

<details>
<summary><b>📝 Logging — a correctly-named logger on every class</b></summary>

```python
from python_utils.logger import Logged

class MyClass(Logged):
    def do_work(self):
        self.info('starting %s', 'work')     # stdlib %-style logging args
        self.error('something went wrong')

MyClass().do_work()
```

Prefer [loguru](https://github.com/Delgan/loguru)? Install the extra
(`pip install 'python-utils[loguru]'`) and subclass `Logurud` instead — the same
`self.info(...)` / `self.error(...)` API, backed by loguru so you keep all its
configuration and per-instance context.

</details>

<details>
<summary><b>🖥️ Terminal & 🧩 misc</b></summary>

```python
from python_utils import terminal, import_
from python_utils.exceptions import raise_exception, reraise

# Robust terminal size (tries IPython/Jupyter, shutil, blessings, ioctl, tput…)
terminal.get_terminal_size()                    # e.g. (80, 24)

# Programmatic `from some_module import *`
import_.import_global('os')

# Build a callable that raises — useful as a default/callback
on_error = raise_exception(ValueError, 'boom')
```

</details>

## ⚡ Performance: lazy by default

`import python_utils` is intentionally *cheap*. Every submodule and every export
is wired through a [PEP 562][pep562] `__getattr__`, so nothing is imported until
first access — and then it's cached. In particular:

- Need only the synchronous helpers? `asyncio` is never imported.
- Even `typing_extensions` is deferred, so the import graph stays minimal.

```python
import sys
import python_utils                 # imports basically nothing extra

'asyncio' in sys.modules            # False
python_utils.acount                 # now `aio` (and asyncio) load, on demand
```

See the [performance guide](https://python-utils.readthedocs.io/en/latest/) for
the full story.

## 📚 Documentation

Full API reference and guides live at
**<https://python-utils.readthedocs.io/en/latest/>**.

## 🔗 Links

- 📖 Documentation: <https://python-utils.readthedocs.io/en/latest/>
- 🐙 Source: <https://github.com/WoLpH/python-utils>
- 📦 PyPI: <https://pypi.python.org/pypi/python-utils>
- 🐛 Issues: <https://github.com/WoLpH/python-utils/issues>
- ✍️ Author's blog: <https://wol.ph/>

## 🔒 Security

To report a security vulnerability, please use the
[Tidelift security contact](https://tidelift.com/security). Tidelift will
coordinate the fix and disclosure.

## 🤝 Contributing

Contributions are very welcome! We keep a strict **100% coverage** bar and run
`ruff`, three type checkers and the full test matrix in CI. See
[CONTRIBUTING.md](https://github.com/WoLpH/python-utils/blob/develop/CONTRIBUTING.md)
to get set up.

## 📄 License

BSD-3-Clause — see [LICENSE](https://github.com/WoLpH/python-utils/blob/develop/LICENSE).

[pep562]: https://peps.python.org/pep-0562/
