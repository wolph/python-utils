# 🔢 Conversions & formatting

Forgiving converters and human-friendly formatters for the messy, real-world data
you get from users, files and APIs.

## Numbers out of strings

`to_int` and `to_float` never raise on bad input — they return a `default`
(itself `0` by default). Opt into regexp extraction to pull the first number out
of surrounding text:

```python
from python_utils import converters

converters.to_int('abc')                    # 0
converters.to_int('spam15eggs', regexp=True) # 15
converters.to_int('nope', default=-1)        # -1

converters.to_float('pi is 3.14', regexp=True)  # 3.14
```

`regexp=True` uses a sensible built-in pattern; pass your own `str` or compiled
`re.Pattern` for full control (the last capture group is used).

## Text and bytes

`to_str` and `to_unicode` normalise between `str` and `bytes` with configurable
encoding and error handling:

```python
from python_utils import converters

converters.to_unicode(b'a')   # 'a'
converters.to_str('a')        # b'a'
```

## `scale_1024` — human-readable sizes

Scale a number by powers of 1024 and get back both the scaled value and the
power, ready to index into a list of prefixes (`['', 'Ki', 'Mi', ...]`):

```python
from python_utils import converters

converters.scale_1024(1, 3)       # (1.0, 0)   -> 1 B
converters.scale_1024(2048, 3)    # (2.0, 1)   -> 2 KiB
```

## `remap` — move a value between ranges

Linearly remap a value from one range to another. Pass a `decimal.Decimal`
anywhere and the whole computation is done in `Decimal` to avoid floating-point
error; otherwise it follows Python's usual `int`/`float` promotion:

```python
import decimal
from python_utils import converters

converters.remap(500, 0, 1000, 0, 100)                # 50
converters.remap(46.0, 0.0, 100.0, -80.0, 10.0)       # -38.6  (46% volume -> dB)
converters.remap(decimal.Decimal('250.0'), 0.0, 1000.0, 0.0, 100.0)
# Decimal('25.0')
```

## `camel_to_underscore` & `apply_recursive`

Convert CamelCase to snake_case, and apply any string transform to every key of a
(possibly nested) mapping:

```python
from python_utils import formatters

formatters.camel_to_underscore('SpamEggsAndBacon')   # 'spam_eggs_and_bacon'

formatters.apply_recursive(
    formatters.camel_to_underscore,
    {'SpamEggs': {'FooBar': 1}},
)                                                    # {'spam_eggs': {'foo_bar': 1}}
```

## `timesince` & `format_time`

`timesince` gives a Django-style "time ago" string; `format_time` renders
timedeltas, datetimes, dates and raw seconds uniformly:

```python
import datetime
from python_utils import formatters, time

now = datetime.datetime.now()
formatters.timesince(now - datetime.timedelta(seconds=61))   # '1 minute and 1 second ago'

time.format_time(1)                                          # '0:00:01'
time.format_time(datetime.timedelta(seconds=3661))           # '1:01:01'
time.format_time(datetime.datetime(2000, 1, 2, 3, 4, 5))     # '2000-01-02 03:04:05'
time.format_time(None)                                       # '--:--:--'
```

See the {doc}`API reference <../python_utils>` for every parameter.
