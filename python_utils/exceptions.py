import typing


def raise_exception(
    exception_class: typing.Type[Exception],
    *args: typing.Any,
    **kwargs: typing.Any,
) -> typing.Callable:
    '''
    Returns a function that raises an exception of the given type with the
    given arguments.

    >>> raise_exception(ValueError, 'spam')('eggs')
    Traceback (most recent call last):
        ...
    ValueError: spam
    '''

    def raise_(*args_: typing.Any, **kwargs_: typing.Any) -> typing.Any:
        raise exception_class(*args, **kwargs)

    return raise_


def reraise(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
    raise
