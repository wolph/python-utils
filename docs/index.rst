Python Utils
============

.. image:: _static/banner.svg
   :alt: Python Utils — the fast, fully-typed stdlib helpers you keep rewriting
   :width: 720px

|

.. image:: https://img.shields.io/pypi/v/python-utils.svg
   :target: https://pypi.python.org/pypi/python-utils
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/python-utils.svg
   :target: https://pypi.python.org/pypi/python-utils
   :alt: Supported Python versions

.. image:: https://github.com/WoLpH/python-utils/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/WoLpH/python-utils/actions/workflows/ci.yml
   :alt: CI status

.. image:: https://coveralls.io/repos/github/WoLpH/python-utils/badge.svg?branch=develop
   :target: https://coveralls.io/github/WoLpH/python-utils?branch=develop
   :alt: Coverage status

**Python Utils** is a collection of small, battle-tested functions and classes
that make everyday Python patterns shorter, safer and faster. No sprawling
framework, no heavy dependencies — just the helpers you find yourself rewriting
in project after project, packaged once and typed to the hilt.

Highlights:

- 🪶 **Zero-cost imports** — :doc:`PEP 562 lazy loading <guide/performance>` means
  ``import python_utils`` pulls in nothing until you touch a helper.
- ⚡ **Async-native** — ``acount``, ``abatcher`` and timeout/stall detectors for
  ``async for``.
- 📦 **Smart containers** — self-casting dicts, duplicate-proof lists, a
  sliceable deque.
- 🔢 **Forgiving converters** — numbers out of messy strings, byte scaling, range
  remapping with ``Decimal`` precision.
- 🎯 **Fully typed & 100% covered** — ships ``py.typed`` and passes mypy,
  basedpyright *and* pyrefly in strict mode.

New here? Start with :doc:`getting-started`.

.. toctree::
   :maxdepth: 2
   :caption: Guides
   :hidden:

   getting-started
   guide/async
   guide/containers
   guide/conversions-and-formatting
   guide/performance
   whats-new
   usage

.. toctree::
   :maxdepth: 4
   :caption: API reference
   :hidden:

   python_utils

Indices and tables
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
