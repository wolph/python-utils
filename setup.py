import os
import typing

import setuptools

# To prevent importing about and thereby breaking the coverage info we use this
# exec hack
about: typing.Dict[str, str] = {}
with open('python_utils/__about__.py') as fp:
    exec(fp.read(), about)

if os.path.isfile('README.rst'):
    long_description = open('README.rst').read()
else:
    long_description = 'See http://pypi.python.org/pypi/python-utils/'

if __name__ == '__main__':
    setuptools.setup(
        python_requires='>3.6.0',
        name='python-utils',
        version=about['__version__'],
        author=about['__author__'],
        author_email=about['__author_email__'],
        description=about['__description__'],
        url=about['__url__'],
        license='BSD',
        packages=setuptools.find_packages(exclude=[
            '_python_utils_tests', '*.__pycache__']),
        long_description=long_description,
        tests_require=['pytest'],
        extras_require={
            'loguru': [
                'loguru',
            ],
            'docs': [
                'mock',
                'sphinx',
                'python-utils',
            ],
            'tests': [
                'flake8',
                'pytest',
                'pytest-cov',
                'pytest-mypy',
                'pytest-asyncio',
                'sphinx',
                'types-setuptools',
                'loguru',
            ],
        },
        classifiers=['License :: OSI Approved :: BSD License'],
    )
