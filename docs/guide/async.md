# ⚡ Async helpers

`python_utils` brings `itertools`-style ergonomics to `async for`, plus tools for
sampling and guarding slow async generators. Because of
[lazy imports](performance.md), `asyncio` is only imported once you actually
touch one of these helpers.

## `acount` — an async counter

The async twin of `itertools.count`, with an optional `step`, `delay` (seconds
between yields) and `stop` value:

```python
import asyncio
from python_utils import aio

async def main():
    async for i in aio.acount(stop=3):
        print(i)          # 0, 1, 2

asyncio.run(main())
```

## `abatcher` — batch by size *or* time

`abatcher` wraps an async generator and yields lists of items. Give it a
`batch_size`, an `interval`, or both — it flushes on whichever is reached first.
That makes it ideal for chunking bursty producers without ever stalling a slow
loop.

Batch purely by size:

```python
import asyncio
from python_utils import aio, generators

async def main():
    async for batch in generators.abatcher(aio.acount(stop=10), batch_size=3):
        print(batch)      # [0, 1, 2], [3, 4, 5], [6, 7, 8], [9]

asyncio.run(main())
```

Batch by time interval instead (flush at least every ``interval`` seconds).
`interval` accepts a `datetime.timedelta` or a plain number of seconds:

```python
async for batch in generators.abatcher(source(), interval=0.1):
    ...                   # whatever accumulated in the last 100ms
```

After each yield the interval timer resets from the current time, so a slow,
blocking loop never causes a runaway burst.

There's a synchronous counterpart too:

```python
from python_utils import generators

list(generators.batcher(range(9), 3))   # [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
```

## `aio_timeout_generator` — sample a slow async source

The `async for` twin of {func}`~python_utils.time.timeout_generator`: walk an
async iterable until a timeout elapses, sleeping ``interval`` seconds between
items. The `interval` can grow each round (`interval_multiplier`) up to an
optional `maximum_interval`, giving you exponential backoff for free. The default
iterable is `acount`, so you get an async counter out of the box.

```python
import asyncio
from python_utils import time

async def main():
    # Yield roughly every 0.06s, for at most 0.1s total.
    async for i in time.aio_timeout_generator(timeout=0.1, interval=0.06):
        print(i)          # 0, 1, ...

asyncio.run(main())
```

## `aio_generator_timeout_detector` — fail fast on a stalled generator

Wrap an async generator so that, if it goes quiet for longer than `timeout`
seconds (or exceeds `total_timeout` overall), you find out instead of hanging
forever. By default the underlying `asyncio.TimeoutError` is re-raised; pass an
`on_timeout` callback to handle it your own way.

```python
from python_utils import time

async def slow_source(): ...

guarded = time.aio_generator_timeout_detector(slow_source(), timeout=5)

# Or as a decorator:
@time.aio_generator_timeout_detector_decorator(timeout=5)
async def producer(): ...
```

See the {doc}`API reference <../python_utils>` for the full signatures.
