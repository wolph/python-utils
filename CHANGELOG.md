# Changelog

## Unreleased

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

## 4.0.1 - 2026-08-30

- Allow `uv_build` 0.12.x, contributed by @felixonmars in PR #49.
- Keep the `python_utils.types` export list unique.
- Delay newly published dependencies and development tools by 14 days before resolution.
