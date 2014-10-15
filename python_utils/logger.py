import logging
import functools

__all__ = ['Logged']


class Logged(object):
    '''Class which automatically adds a named logger to your class when
    interiting

    Adds easy access to debug, info, warning, error, exception and log methods

    >>> class MyClass(Logged):
    ...     def __init__(self):
    ...         Logged.__init__(self)
    >>> my_class = MyClass()
    >>> my_class.debug('debug')
    >>> my_class.info('info')
    >>> my_class.warning('warning')
    >>> my_class.error('error')
    >>> my_class.exception('exception')
    >>> my_class.log(0, 'log')
    '''
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(
            self.__get_name(__name__, self.__class__.__name__))

    def __get_name(self, *name_parts):
        return '.'.join(n.strip() for n in name_parts if n.strip())

    @functools.wraps(logging.debug)
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    @functools.wraps(logging.info)
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    @functools.wraps(logging.warning)
    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    @functools.wraps(logging.error)
    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    @functools.wraps(logging.exception)
    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    @functools.wraps(logging.log)
    def log(self, lvl, msg, *args, **kwargs):
        self.logger.log(lvl, msg, *args, **kwargs)

