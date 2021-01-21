from python_utils import import_


def test_import_globals_relative_import():
    for i in range(-1, 5):
        relative_import(i)


def relative_import(level):
    locals_ = {}
    globals_ = {'__name__': 'python_utils.import_'}
    import_.import_global('.formatters', locals_=locals_, globals_=globals_)
    import pprint
    pprint.pprint(globals_)
    assert 'camel_to_underscore' in globals_


def test_import_globals_without_inspection():
    locals_ = {}
    globals_ = {'__name__': __name__}
    import_.import_global(
        'python_utils.formatters', locals_=locals_, globals_=globals_)
    assert 'camel_to_underscore' in globals_


def test_import_globals_single_method():
    locals_ = {}
    globals_ = {'__name__': __name__}
    import_.import_global(
        'python_utils.formatters', ['camel_to_underscore'], locals_=locals_,
        globals_=globals_)
    assert 'camel_to_underscore' in globals_


def test_import_globals_with_inspection():
    import_.import_global('python_utils.formatters')
    assert 'camel_to_underscore' in globals()


def test_import_globals_missing_module():
    import_.import_global(
        'python_utils.spam', exceptions=ImportError, locals_=locals())
    assert 'camel_to_underscore' in globals()


def test_import_locals_missing_module():
    import_.import_global(
        'python_utils.spam', exceptions=ImportError, globals_=globals())
    assert 'camel_to_underscore' in globals()

