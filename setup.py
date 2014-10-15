import os
import setuptools

import python_utils
if os.path.isfile('README.rst'):
    long_description = open('README.rst').read()
else:
    long_description = 'See http://pypi.python.org/pypi/python-utils/'

setuptools.setup(
    name='python-utils',
    version=python_utils.__version__,
    author=python_utils.__author__,
    author_email=python_utils.__author_email__,
    description=python_utils.__description__,
    url='https://github.com/WoLpH/python-utils',
    license='BSD',
    packages=setuptools.find_packages(),
    long_description=long_description,
    test_suite='nose.collector',
    classifiers=['License :: OSI Approved :: BSD License'],
)

