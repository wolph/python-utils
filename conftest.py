"""
Load the shared fixtures for the tests and the doctests.

The fixtures live in the tests package. They are loaded from the repository
root because the doctests in ``python_utils`` need them as well.
"""

pytest_plugins: tuple[str, ...] = ('_python_utils_tests.clock',)
