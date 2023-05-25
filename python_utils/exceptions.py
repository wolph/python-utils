from . import types


def raise_exception(
    exception_class: types.Type[Exception],
    *args: types.Any,
    **kwargs: types.Any,
) -> types.Callable[..., None]:
    '''
    Returns a function that raises an exception of the given type with the
    given arguments.

    >>> raise_exception(ValueError, 'spam')('eggs')
    Traceback (most recent call last):
        ...
    ValueError: spam
    '''

    def raise_(*args_: types.Any, **kwargs_: types.Any) -> types.Any:
        raise exception_class(*args, **kwargs)

    return raise_


def reraise(*args: types.Any, **kwargs: types.Any) -> types.Any:
    raise
