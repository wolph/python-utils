# mypy: disable-error-code=misc
import pytest

from python_utils.loguru import Logurud

loguru = pytest.importorskip('loguru')


def test_logurud() -> None:
    class MyClass(Logurud):
        pass

    my_class = MyClass()
    my_class.debug('debug')
    my_class.info('info')
    my_class.warning('warning')
    my_class.error('error')
    my_class.critical('critical')
    my_class.exception('exception')
    my_class.log(0, 'log')
