# CI Lint Stability Design

## Problem

CI resolved Ruff 0.16.5 instead of the Ruff 0.15.20 used by the previous successful run. Ruff 0.16.0 introduced RUF068, which reports duplicate entries in `__all__`. The existing `python_utils.types.__all__` list contains duplicate `SupportsIndex` and `TracebackType` entries.

The duplicates do not change import behavior, but they are unnecessary public API declarations and now fail the lint job. The CI toolchain resolves current compatible versions, so new checks can appear between runs.

## Design

Remove the second occurrence of `SupportsIndex` and `TracebackType` from `python_utils.types.__all__`. Do not suppress RUF068 or pin Ruff to an older release because the diagnostic identifies a real source defect.

Add one regression test that imports `python_utils.types`, compares the length of `__all__` with the length of `set(__all__)`, and reports the duplicate names when the assertion fails. The test protects the public export list independently of the installed Ruff version.

Keep the existing `[tool.uv] exclude-newer = "14 days"` setting. It delays newly published dependency and tool versions long enough for early regressions to surface elsewhere, while allowing CI to exercise current tooling after the delay. It is a buffer, not a lock.

## Scope

Change only:

- `python_utils/types.py` to remove the two duplicate exports.
- `_python_utils_tests/test_types.py` to enforce unique exports.

Do not change GitHub Actions, tox runners, dependency ranges, or the repository policy that excludes `uv.lock`.

## Verification

Use Ruff 0.16.5 to reproduce RUF068 before the source change. Run the new regression test before the source change and confirm that it fails with the duplicate names. After the source change, run the regression test, the lint tox environment, and the full tox suite supported by the installed interpreters. Finally, inspect the working tree to confirm that unrelated files remain untouched.
