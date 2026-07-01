"""Tests for the package metadata in ``python_utils.__about__``."""

from python_utils import __about__


def test_definitions() -> None:
    """Ensure the required metadata fields are defined."""
    # The setup.py requires this so we better make sure they exist :)
    assert __about__.__version__
    assert __about__.__author__
    assert __about__.__author_email__
    assert __about__.__description__
