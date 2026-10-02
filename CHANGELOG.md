# Changelog

## 4.1.0 - 2026-10-02

- Keep `UniqueList` membership in sync when replacing an indexed item, and
  leave membership unchanged when the index is out of range, contributed by
  @shkyyy18 in PR #51.
- Keep `UniqueList` membership in sync for slice assignment, `extend`, `pop`,
  `remove`, `clear`, `+=` and `*=`, so `extend` and `+=` no longer add
  duplicates and removed values can be added again.
- Accept one-shot iterables in `UniqueList` slice assignment, allow a slice to
  reuse the values it replaces, and reject a slice that repeats a value.
- Make `copy.copy` and `copy.deepcopy` of a `UniqueList` return a working copy
  with its own membership.
- Leave `UniqueList` membership unchanged when `insert` fails, and answer `in`
  for an unhashable value the way a `list` does.
- Make `CastedDict` and `LazyCastedDict` load from `pickle` on every protocol,
  including pickles written by 4.0.1, and stop `copy.copy` and `copy.deepcopy`
  from casting the stored values a second time.
- Cast what `setdefault` and `|=` store in a `CastedDict` or `LazyCastedDict`.
  A `None` default is stored as it is.
- Cast the key of a `LazyCastedDict` once when it is stored. It was cast twice.
- Let keyword arguments win over the mapping in `update` and the constructor
  of the casted dicts, as `dict` does.
- Make `!=` the opposite of `==` for `SliceableDeque`, and compare unequal to a
  set when an item is unhashable.
- Remove the iterable of mappings from the `DictUpdateArgs` type alias. The
  code never accepted that shape.
- Log the traceback in `Logged.exception()`, and name the caller in every
  record of `Logged` instead of `logger.py`. Code that passed `stacklevel=2`
  to work around the wrong caller now points one frame too high.
- Stop `Logurud` from crashing on a message with a brace in it. A message
  without arguments is logged as written, so braces that were doubled to avoid
  the crash now show doubled.
- Keep the value of a class that combines `Logged` or `Logurud` with a type
  such as `int` or `str`.
- Use the whole match in `to_int` and `to_float` for a pattern without a
  group, and never return a negative power from `scale_1024`.
- Count every day once in `timesince`, describe a negative timedelta by its
  size, and accept a timezone-aware datetime.
- Keep an acronym whole before an underscore or a digit in
  `camel_to_underscore`, so `HTTP_OK` becomes `http_ok`.
- Let `import_global` import a nested module that nothing imported before.
- Cancel the pending item of `abatcher` when the consumer stops early. A
  source that is an async generator ends at that point, where a leaked task
  used to take its next item.
- Restart the interval of `abatcher` after a full batch, and accept an
  iterator whose `__anext__` returns a future.
- Accept a plain function as `on_timeout` in `aio_generator_timeout_detector`.
- Truncate `format_time` exactly for a precision below one second, and print
  the placeholder for `nan`.
- Limit the first sleep of `timeout_generator` and `aio_timeout_generator` to
  `maximum_interval`.
- Let `acount` count down to a `stop` with a negative step.
- Log a skipped call of `sample` through the logger of its module instead of
  the root logger, which installed a handler on it.
- Keep the name, docstring and signature of a function under `listify`, and
  leave the annotations of the wrapped function alone in `wraps_classmethod`.
- Return the value of `total_seconds()` from `timedelta_to_seconds` for a
  duration with a fraction.
- Correct docstrings that described something else than the code does, among
  them `to_str` returning `bytes` and the timeouts that read `0` as none.
- Run the timing tests on a fake clock, so they no longer depend on sleep
  accuracy, and ship `conftest.py` in the sdist.

## 4.0.1 - 2026-08-30

- Allow `uv_build` 0.12.x, contributed by @felixonmars in PR #49.
- Keep the `python_utils.types` export list unique.
- Delay newly published dependencies and development tools by 14 days before resolution.
