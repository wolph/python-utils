import re


def to_int(input_, default=0, exception=(ValueError, TypeError), regexp=None):
    '''
    Convert the given input to an integer or return default

    When trying to convert the exceptions given in the exception parameter
    are automatically catched and the default will be returned.

    The regexp parameter allows for a regular expression to find the digits
    in a string.
    When True it will automatically match any digit in the string.
    When a (regexp) object (has a search method) is given, that will be used.
    WHen a string is given, re.compile will be run over it first

    The last group of the regexp will be used as value

    >>> to_int('abc')
    0
    >>> to_int('1')
    1
    >>> to_int('abc123')
    0
    >>> to_int('123abc')
    0
    >>> to_int('abc123', regexp=True)
    123
    >>> to_int('123abc', regexp=True)
    123
    >>> to_int('abc123abc', regexp=True)
    123
    >>> to_int('abc123abc456', regexp=True)
    123
    >>> to_int('abc123', regexp=re.compile('(\d+)'))
    123
    >>> to_int('123abc', regexp=re.compile('(\d+)'))
    123
    >>> to_int('abc123abc', regexp=re.compile('(\d+)'))
    123
    >>> to_int('abc123abc456', regexp=re.compile('(\d+)'))
    123
    >>> to_int('abc123', regexp='(\d+)')
    123
    >>> to_int('123abc', regexp='(\d+)')
    123
    >>> to_int('abc', regexp='(\d+)')
    0
    >>> to_int('abc123abc', regexp='(\d+)')
    123
    >>> to_int('abc123abc456', regexp='(\d+)')
    123
    >>> to_int('1234', default=1)
    1234
    >>> to_int('abc', default=1)
    1
    >>> to_int('abc', regexp=123)
    Traceback (most recent call last):
    ...
    TypeError: unknown argument for regexp parameter
    '''

    if regexp is True:
        regexp = re.compile('(\d+)')
    elif isinstance(regexp, basestring):
        regexp = re.compile(regexp)
    elif hasattr(regexp, 'search'):
        pass
    elif regexp is not None:
        raise TypeError('unknown argument for regexp parameter')

    try:
        if regexp:
            match = regexp.search(input_)
            if match:
                input_ = match.groups()[-1]
        return int(input_)
    except exception:
        return default


def to_float(input_, default=0, exception=(ValueError, TypeError), regexp=None):
    '''
    Convert the given input_ to an integer or return default

    When trying to convert the exceptions given in the exception parameter
    are automatically catched and the default will be returned.

    The regexp parameter allows for a regular expression to find the digits
    in a string.
    When True it will automatically match any digit in the string.
    When a (regexp) object (has a search method) is given, that will be used.
    WHen a string is given, re.compile will be run over it first

    The last group of the regexp will be used as value

    >>> '%.2f' % to_float('abc')
    '0.00'
    >>> '%.2f' % to_float('1')
    '1.00'
    >>> '%.2f' % to_float('abc123.456', regexp=True)
    '123.46'
    >>> '%.2f' % to_float('abc123', regexp=True)
    '123.00'
    >>> '%.2f' % to_float('abc0.456', regexp=True)
    '0.46'
    >>> '%.2f' % to_float('abc123.456', regexp=re.compile('(\d+\.\d+)'))
    '123.46'
    >>> '%.2f' % to_float('123.456abc', regexp=re.compile('(\d+\.\d+)'))
    '123.46'
    >>> '%.2f' % to_float('abc123.46abc', regexp=re.compile('(\d+\.\d+)'))
    '123.46'
    >>> '%.2f' % to_float('abc123abc456', regexp=re.compile('(\d+(\.\d+|))'))
    '123.00'
    >>> '%.2f' % to_float('abc', regexp='(\d+)')
    '0.00'
    >>> '%.2f' % to_float('abc123', regexp='(\d+)')
    '123.00'
    >>> '%.2f' % to_float('123abc', regexp='(\d+)')
    '123.00'
    >>> '%.2f' % to_float('abc123abc', regexp='(\d+)')
    '123.00'
    >>> '%.2f' % to_float('abc123abc456', regexp='(\d+)')
    '123.00'
    >>> '%.2f' % to_float('1234', default=1)
    '1234.00'
    >>> '%.2f' % to_float('abc', default=1)
    '1.00'
    >>> '%.2f' % to_float('abc', regexp=123)
    Traceback (most recent call last):
    ...
    TypeError: unknown argument for regexp parameter
    '''

    if regexp is True:
        regexp = re.compile('(\d+(\.\d+|))')
    elif isinstance(regexp, basestring):
        regexp = re.compile(regexp)
    elif hasattr(regexp, 'search'):
        pass
    elif regexp is not None:
        raise TypeError('unknown argument for regexp parameter')

    try:
        if regexp:
            match = regexp.search(input_)
            if match:
                input_ = match.group(1)
        return float(input_)
    except exception:
        return default


