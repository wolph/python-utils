"""Configuration file for the Sphinx documentation builder."""

from __future__ import annotations

from datetime import date

from python_utils import __about__

# -- Project information ------------------------------------------------------

project = 'Python Utils'
author = __about__.__author__
copyright = f'{date.today().year}, {author}'  # noqa: A001

# The full version, including alpha/beta/rc tags.
release = __about__.__version__
version = '.'.join(release.split('.')[:2])

# -- General configuration ----------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'myst_parser',
]

napoleon_google_docstring = True
napoleon_numpy_docstring = False

autodoc_typehints = 'description'
# `loguru` is an optional dependency (the `loguru` extra); mock it so the docs
# build can import and document `python_utils.loguru` without it installed.
autodoc_mock_imports = ['loguru']

templates_path = ['_templates']
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    # Local skill/session artifacts that are not part of the published docs.
    'superpowers',
    'superpowers/**',
]

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# -- HTML output --------------------------------------------------------------

html_theme = 'furo'
