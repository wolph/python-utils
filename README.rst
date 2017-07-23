Useful Python Utils
==============================================================================

.. image:: https://travis-ci.org/WoLpH/python-utils.svg?branch=master
  :target: https://travis-ci.org/WoLpH/python-utils

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

 - `six` any recent version

Installation:
------------------------------------------------------------------------------

The package can be installed through `pip` (this is the recommended method):

    pip install python-utils
    
Or if `pip` is not available, `easy_install` should work as well:

    easy_install python-utils
    
Or download the latest release from Pypi (https://pypi.python.org/pypi/python-utils) or Github.

Note that the releases on Pypi are signed with my GPG key (https://pgp.mit.edu/pks/lookup?op=vindex&search=0xE81444E9CE1F695D) and can be checked using GPG:

     gpg --verify python-utils-<version>.tar.gz.asc python-utils-<version>.tar.gz

Quickstart
------------------------------------------------------------------------------

This module makes it easy to execute common tasks in Python scripts such as
converting text to numbers and making sure a string is in unicode or bytes
format.

Examples
------------------------------------------------------------------------------

To extract a number from nearly every string:

.. code-block:: python

    from python_utils import converters

    number = converters.to_int('spam15eggs')
    assert number == 15

    number = converters.to_int('spam')
    assert number == 0

    number = converters.to_int('spam', default=1)
    assert number == 1

    number = converters.to_float('spam1.234')

To do a global import programmatically you can use the `import_global`
function. This effectively emulates a `from ... import *`

.. code-block:: python

    from python_utils.import_ import import_global

    # The following is  the equivalent of `from some_module import *`
    import_global('some_module')

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

