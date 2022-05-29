Useful Python Utils
==============================================================================

.. image:: https://github.com/WoLpH/python-utils/actions/workflows/main.yml/badge.svg?branch=master
  :target: https://github.com/WoLpH/python-utils/actions/workflows/main.yml

.. image:: https://coveralls.io/repos/WoLpH/python-utils/badge.svg?branch=master
  :target: https://coveralls.io/r/WoLpH/python-utils?branch=master

Python Utils is a collection of small Python functions and
classes which make common patterns shorter and easier. It is by no means a
complete collection but it has served me quite a bit in the past and I will
keep extending it.

One of the libraries using Python Utils is Django Utils.

Documentation is available at: https://python-utils.readthedocs.org/en/latest/

Links
-----

 - The source: https://github.com/WoLpH/python-utils
 - Project page: https://pypi.python.org/pypi/python-utils
 - Reporting bugs: https://github.com/WoLpH/python-utils/issues
 - Documentation: https://python-utils.readthedocs.io/en/latest/
 - My blog: https://wol.ph/

Requirements for installing:
------------------------------------------------------------------------------

For the Python 3+ release (i.e. v3.0.0 or higher) there are no requirements.
For the Python 2 compatible version (v2.x.x) the `six` package is needed.

Installation:
------------------------------------------------------------------------------

The package can be installed through `pip` (this is the recommended method):

.. code-block:: bash

    pip install python-utils
    
Or if `pip` is not available, `easy_install` should work as well:

.. code-block:: bash

    easy_install python-utils
    
Or download the latest release from Pypi (https://pypi.python.org/pypi/python-utils) or Github.

Note that the releases on Pypi are signed with my GPG key (https://pgp.mit.edu/pks/lookup?op=vindex&search=0xE81444E9CE1F695D) and can be checked using GPG:

.. code-block:: bash

     gpg --verify python-utils-<version>.tar.gz.asc python-utils-<version>.tar.gz

Quickstart
------------------------------------------------------------------------------

This module makes it easy to execute common tasks in Python scripts such as
converting text to numbers and making sure a string is in unicode or bytes
format.

Examples
------------------------------------------------------------------------------

Automatically converting a generator to a list, dict or other collections
using a decorator:

.. code-block:: pycon

    >>> @decorators.listify()
    ... def generate_list():
    ...     yield 1
    ...     yield 2
    ...     yield 3
    ...
    >>> generate_list()
    [1, 2, 3]

    >>> @listify(collection=dict)
    ... def dict_generator():
    ...     yield 'a', 1
    ...     yield 'b', 2

    >>> dict_generator()
    {'a': 1, 'b': 2}

Retrying until timeout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To easily retry a block of code with a configurable timeout, you can use the
`time.timeout_generator`:

.. code-block:: pycon

    >>> for i in time.timeout_generator(10):
    ...     try:
    ...         # Run your code here
    ...     except Exception as e:
    ...         # Handle the exception

Formatting of timestamps, dates and times
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Easy formatting of timestamps and calculating the time since:

.. code-block:: pycon

    >>> time.format_time('1')
    '0:00:01'
    >>> time.format_time(1.234)
    '0:00:01'
    >>> time.format_time(1)
    '0:00:01'
    >>> time.format_time(datetime.datetime(2000, 1, 2, 3, 4, 5, 6))
    '2000-01-02 03:04:05'
    >>> time.format_time(datetime.date(2000, 1, 2))
    '2000-01-02'
    >>> time.format_time(datetime.timedelta(seconds=3661))
    '1:01:01'
    >>> time.format_time(None)
    '--:--:--'

    >>> formatters.timesince(now)
    'just now'
    >>> formatters.timesince(now - datetime.timedelta(seconds=1))
    '1 second ago'
    >>> formatters.timesince(now - datetime.timedelta(seconds=2))
    '2 seconds ago'
    >>> formatters.timesince(now - datetime.timedelta(seconds=60))
    '1 minute ago'

Converting your test from camel-case to underscores:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> camel_to_underscore('SpamEggsAndBacon')
    'spam_eggs_and_bacon'

Attribute setting decorator. Very useful for the Django admin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A convenient decorator to set function attributes using a decorator:

.. code-block:: pycon

    You can use:
    >>> @decorators.set_attributes(short_description='Name')
    ... def upper_case_name(self, obj):
    ...     return ("%s %s" % (obj.first_name, obj.last_name)).upper()

    Instead of:
    >>> def upper_case_name(obj):
    ...     return ("%s %s" % (obj.first_name, obj.last_name)).upper()

    >>> upper_case_name.short_description = 'Name'

This can be very useful for the Django admin as it allows you to have all
metadata in one place.

Scaling numbers between ranges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> converters.remap(500, old_min=0, old_max=1000, new_min=0, new_max=100)
    50

    # Or with decimals:
    >>> remap(decimal.Decimal('250.0'), 0.0, 1000.0, 0.0, 100.0)
    Decimal('25.0')

Get the screen/window/terminal size in characters:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> terminal.get_terminal_size()
    (80, 24)

That method supports IPython and Jupyter as well as regular shells, using
`blessings` and other modules depending on what is available.

Extracting numbers from nearly every string:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> converters.to_int('spam15eggs')
    15
    >>> converters.to_int('spam')
    0
    >>> number = converters.to_int('spam', default=1)
    1

Doing a global import of all the modules in a package programmatically:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To do a global import programmatically you can use the `import_global`
function. This effectively emulates a `from ... import *`

.. code-block:: python

    from python_utils.import_ import import_global

    # The following is  the equivalent of `from some_module import *`
    import_global('some_module')

Automatically named logger for classes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Or add a correclty named logger to your classes which can be easily accessed:

.. code-block:: python

    class MyClass(Logged):
        def __init__(self):
            Logged.__init__(self)

    my_class = MyClass()

    # Accessing the logging method:
    my_class.error('error')

    # With formatting:
    my_class.error('The logger supports %(formatting)s',
                   formatting='named parameters')

    # Or to access the actual log function (overwriting the log formatting can
    # be done n the log method)
    import logging
    my_class.log(logging.ERROR, 'log')

Alternatively loguru is also supported. It is largely a drop-in replacement for the logging module which is a bit more convenient to configure:

First install the extra loguru package:

.. code-block:: bash

    pip install 'python-utils[loguru]'

.. code-block:: python

    class MyClass(Logurud):
        ...

Now you can use the `Logurud` class to make functions such as `self.info()`
available. The benefit of this approach is that you can add extra context or
options to you specific loguru instance (i.e. `self.logger`):

Convenient type aliases and some commonly used types:

.. code-block:: python

    # For type hinting scopes such as locals/globals/vars
    Scope = Dict[str, Any]
    OptionalScope = O[Scope]

    # Note that Number is only useful for extra clarity since float
    # will work for both int and float in practice.
    Number = U[int, float]
    DecimalNumber = U[Number, decimal.Decimal]

    # To accept an exception or list of exceptions
    ExceptionType = Type[Exception]
    ExceptionsType = U[Tuple[ExceptionType, ...], ExceptionType]

    # Matching string/bytes types:
    StringTypes = U[str, bytes]
