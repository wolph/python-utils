# CI Lint Stability Design

## Problem

CI resolved Ruff 0.16.5 instead of the Ruff 0.15.20 used by the previous successful run. Ruff 0.16.0 introduced RUF068, which reports duplicate entries in `__all__`. The existing `python_utils.types.__all__` list contains duplicate `SupportsIndex` and `TracebackType` entries.

The duplicates do not change import behavior, but they are unnecessary public API declarations and now fail the lint job. After that check is repaired, Ruff 0.16 also tries to format Python code blocks in Markdown and rejects six existing documentation files. The CI toolchain resolves current compatible versions, so new checks and target file types can appear between runs.

## Design

Remove the second occurrence of `SupportsIndex` and `TracebackType` from `python_utils.types.__all__`. Do not suppress RUF068 or pin Ruff to an older release because the diagnostic identifies a real source defect.

Add one regression test that imports `python_utils.types`, compares the length of `__all__` with the length of `set(__all__)`, and reports the duplicate names when the assertion fails. The test protects the public export list independently of the installed Ruff version.

Keep the existing `[tool.uv] exclude-newer = "14 days"` setting. It delays newly published dependency and tool versions long enough for early regressions to surface elsewhere, while allowing CI to exercise current tooling after the delay. It is a buffer, not a lock.

Add `extend-exclude = ['*.md']` to the root `ruff.toml` so Ruff remains responsible for Python source and does not rewrite deliberately aligned documentation examples. Ruff gives the dedicated configuration file precedence over `[tool.ruff]` in `pyproject.toml`. The documentation build remains responsible for validating Markdown.

## Scope

Change only:

- `python_utils/types.py` to remove the two duplicate exports.
- `_python_utils_tests/test_types.py` to enforce unique exports.
- `ruff.toml` to exclude Markdown from Ruff's lint and formatting discovery.

Do not change GitHub Actions, tox runners, dependency ranges, documentation content, or the repository policy that excludes `uv.lock`.

## Verification

Use Ruff 0.16.5 to reproduce RUF068 before the source change. Run the new regression test before the source change and confirm that it fails with the duplicate names. After the source change, run the regression test and confirm that the lint environment reaches the Markdown formatting failure. Add the explicit Markdown exclusion, then run the lint tox environment and the full tox suite supported by the installed interpreters. Finally, inspect the working tree to confirm that unrelated files remain untouched.
