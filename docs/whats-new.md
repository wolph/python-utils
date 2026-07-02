# 🎉 What's new in 4.0

Version 4.0 is a modernization release: the public helpers you already rely on are
unchanged, but the package underneath is faster to import, stricter about types,
and built with a modern toolchain.

The authoritative, per-release changelog lives on the
[GitHub releases page](https://github.com/WoLpH/python-utils/releases). The
highlights:

## 🪶 Lazy imports

`import python_utils` no longer eagerly imports its submodules. Thanks to
[PEP 562](https://peps.python.org/pep-0562/) lazy loading, nothing is imported
until first access — notably `asyncio` and `typing_extensions` stay out of the
import graph until you use a helper that needs them. See the
[performance guide](guide/performance.md).

## 🎯 Strict typing on three checkers

The codebase is verified in strict mode by **mypy**, **basedpyright** *and*
**pyrefly**, and ships `py.typed` so your own type checker picks up the
annotations. Coverage remains at **100%**.

## 🧰 Modern build & tooling

- Built with the **`uv_build`** backend.
- Linted and formatted with **ruff**.
- Git hooks via **lefthook**.
- A **tox** matrix across supported interpreters, with split GitHub Actions CI and
  PyPI Trusted Publishing.
- The source distribution ships the test suite and `tox.ini`, so downstream
  packagers can build and test from the sdist.

## 🐍 Supported Python versions

Python **3.10+** is supported, and the package is tested against current CPython
releases as well as PyPI.

## Handy modules worth a fresh look

- [Async helpers](guide/async.md) — `acount`, `abatcher`, and the timeout/stall
  detectors.
- [Smart containers](guide/containers.md) — `CastedDict`, `LazyCastedDict`,
  `UniqueList`, `SliceableDeque`.

For anything not listed here, consult the
[release notes](https://github.com/WoLpH/python-utils/releases) for the exact
version you're upgrading from.
