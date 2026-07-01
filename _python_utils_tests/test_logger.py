# mypy: disable-error-code=misc
"""Tests for the loguru mixin in ``python_utils.loguru``."""

import pytest

from python_utils import loguru

pytest.importorskip('loguru')


def test_logurud() -> None:
    """Expose all loguru log-level methods on a subclass."""

    class MyClass(loguru.Logurud):
        pass

    my_class = MyClass()
    my_class.debug('debug')
    my_class.info('info')
    my_class.warning('warning')
    my_class.error('error')
    my_class.critical('critical')
    my_class.exception('exception')
    my_class.log(0, 'log')
