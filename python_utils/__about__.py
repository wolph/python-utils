"""
This module contains metadata about the `python-utils` package.

Attributes:
    __package_name__ (str): The name of the package.
    __author__ (str): The author of the package.
    __author_email__ (str): The email of the author.
    __description__ (str): A brief description of the package.
    __url__ (str): The URL of the package's repository.
    __version__ (str): The current version, read from the installed metadata.
"""

from __future__ import annotations

from importlib import metadata

#: Distribution name as published on PyPI.
__package_name__: str = 'python-utils'
#: Primary author's name.
__author__: str = 'Rick van Hattem'
#: Primary author's contact email.
__author_email__: str = 'Wolph@wol.ph'
#: One-line description of the package.
__description__: str = (
    'Python Utils is a module with some convenient utilities not included '
    'with the standard Python install'
)
#: Canonical project/repository URL.
__url__: str = 'https://github.com/WoLpH/python-utils'

try:
    # `[project].version` in pyproject.toml is the single source of truth;
    # read it back at runtime so the two never drift.
    __version__: str = metadata.version(__package_name__)
except metadata.PackageNotFoundError:  # pragma: no cover
    # Not installed (e.g. running straight from a source checkout).
    __version__ = '0.0.0'
