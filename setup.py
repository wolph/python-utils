import os
from setuptools import setup

if os.path.isfile('README.rst'):
    long_description = open('README.rst').read()
else:
    long_description = 'See http://pypi.python.org/pypi/python-utils/'

setup(
    name = 'python-utils',
    version = '1.0',
    author = 'Rick van Hattem',
    author_email = 'Rick.van.Hattem@Fawo.nl',
    description = '''Python Utils is a module with some convenient utilities
        not included with the standard Python install''',
    url='https://github.com/WoLpH/python-utils',
    license = 'BSD',
    packages=['python_utils'],
    long_description=long_description,
#    test_suite='nose.collector',
#    setup_requires=['nose'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
    ],
)
