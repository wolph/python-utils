# 🚀 Getting started

Python Utils is a small collection of typed, dependency-light helpers for the
patterns you keep rewriting: pulling numbers out of strings, batching iterables,
formatting durations, casting dictionaries, and more.

## Installation

```bash
pip install python-utils
```

Optional extras:

```bash
pip install 'python-utils[loguru]'   # loguru-backed logging mixin
```

Python **3.10+** is required. The only runtime dependency is `typing_extensions`,
and even that is imported lazily.

## Lazy by design

Everything is reachable straight off the top-level package, but nothing is
imported until you actually use it (see the
[performance guide](guide/performance.md)):

```python
import python_utils

python_utils.to_int('port=8080', regexp=True)   # 8080
```

You can also import from a submodule when you prefer an explicit namespace — the
result is identical, and only the modules you touch get loaded:

```python
from python_utils import converters

converters.to_int('port=8080', regexp=True)      # 8080
```

## A five-minute tour

```python
import datetime
import python_utils

# Numbers out of anything
python_utils.to_int('spam15eggs', regexp=True)              # 15

# Human-readable sizes: (value, power-of-1024)
python_utils.scale_1024(2048, 3)                            # (2.0, 1)  -> 2 KiB

# Remap a value between ranges (Decimal-safe)
python_utils.remap(46.0, 0.0, 100.0, -80.0, 10.0)          # -38.6

# Friendly durations
python_utils.format_time(datetime.timedelta(seconds=3661))  # '1:01:01'
python_utils.timesince(
    datetime.datetime.now() - datetime.timedelta(seconds=61)
)                                                           # '1 minute and 1 second ago'

# Batch an iterable
list(python_utils.batcher(range(9), 3))                     # [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
```

## Where to next

- [Async helpers](guide/async.md) — `acount`, `abatcher`, timeout & stall
  detectors.
- [Smart containers](guide/containers.md) — `CastedDict`, `UniqueList`,
  `SliceableDeque`.
- [Conversions & formatting](guide/conversions-and-formatting.md) — `to_int`,
  `scale_1024`, `remap`, `camel_to_underscore`, `timesince`.
- [Performance](guide/performance.md) — how lazy imports keep startup cheap.
- [What's new](whats-new.md) — the v4 modernization.
- The full {doc}`API reference <python_utils>`.
