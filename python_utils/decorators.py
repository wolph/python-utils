import functools
from . import types


def set_attributes(**kwargs):
    '''Decorator to set attributes on functions and classes

    A common usage for this pattern is the Django Admin where
    functions can get an optional short_description. To illustrate:

    Example from the Django admin using this decorator:
    https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display

    Our simplified version:

    >>> @set_attributes(short_description='Name')
    ... def upper_case_name(self, obj):
    ...     return ("%s %s" % (obj.first_name, obj.last_name)).upper()

    The standard Django version:

    >>> def upper_case_name(obj):
    ...     return ("%s %s" % (obj.first_name, obj.last_name)).upper()

    >>> upper_case_name.short_description = 'Name'

    '''

    def _set_attributes(function):
        for key, value in kwargs.items():
            setattr(function, key, value)
        return function

    return _set_attributes


def listify(collection: types.Callable = list, allow_empty: bool = True):
    '''
    Convert any generator to a list or other type of collection.

    >>> @listify()
    ... def generator():
    ...     yield 1
    ...     yield 2
    ...     yield 3

    >>> generator()
    [1, 2, 3]

    >>> @listify()
    ... def empty_generator():
    ...     pass

    >>> empty_generator()
    []

    >>> @listify(allow_empty=False)
    ... def empty_generator_not_allowed():
    ...     pass

    >>> empty_generator_not_allowed()
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not iterable

    >>> @listify(collection=set)
    ... def set_generator():
    ...     yield 1
    ...     yield 1
    ...     yield 2

    >>> set_generator()
    {1, 2}

    >>> @listify(collection=dict)
    ... def dict_generator():
    ...     yield 'a', 1
    ...     yield 'b', 2

    >>> dict_generator()
    {'a': 1, 'b': 2}
    '''

    def _listify(function):
        @functools.wraps(function)
        def __listify(*args, **kwargs):
            result = function(*args, **kwargs)
            if result is None and allow_empty:
                return []
            return collection(result)

        return __listify

    return _listify
