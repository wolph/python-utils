def import_global(name, modules=None, exceptions=None, locals_=None, globals_=None):
    '''Import the requested items into the global scope
    
    WARNING! this method _will_ overwrite your global scope
    If you have a variable named "path" and you call import_global('sys')
    it will be overwritten with sys.path
    
    name -- the name of the module to import, e.g. sys
    modules -- the modules to import, use None for everything
    exception -- the exception to catch, e.g. ImportError
    locals_ -- the `locals()` method (in case you need a different scope)
    globals_ -- the `globals()` method (in case you need a different scope)
    '''
    try:
        frame = None
        if not locals_ or not globals_:
            import inspect
            frame = inspect.stack()[1][0]
            globals_, locals_ = frame.f_globals, frame.f_locals

        try:
            name = name.split('.')
            module = __import__(name[0], globals_, locals_, name[1:])

            if not modules:
                modules = getattr(module, '__all__', dir(module))
            else:
                modules = set(modules).intersection(dir(module))

            for k in set(dir(module)).intersection(modules):
                if k and k[0] != '_':
                    globals_[k] = getattr(module, k)
        except exceptions, e:
            return e
    finally:
        del name, modules, exceptions, locals_, globals_, frame

