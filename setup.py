"""
Setup script for the python-utils package.

This script uses setuptools to package the python-utils library. It reads
metadata from the `python_utils/__about__.py` file and the `README.rst` file to
populate the package information. The script also defines the package
requirements and optional dependencies for different use cases such as logging,
documentation, and testing.
"""

import pathlib

import setuptools

# pyright: reportUnknownMemberType=false

# To prevent importing about and thereby breaking the coverage info we use this
# exec hack
about: dict[str, str] = {}
with open('python_utils/__about__.py') as fp:
    exec(fp.read(), about)

_readme_path = pathlib.Path(__file__).parent / 'README.rst'
if _readme_path.exists() and _readme_path.is_file():
    long_description = _readme_path.read_text()
else:
    long_description = 'See http://pypi.python.org/pypi/python-utils/'

if __name__ == '__main__':
    setuptools.setup(
        python_requires='>=3.9.0',
        name='python-utils',
        version=about['__version__'],
        author=about['__author__'],
        author_email=about['__author_email__'],
        description=about['__description__'],
        url=about['__url__'],
        license='BSD',
        packages=setuptools.find_packages(
            exclude=['_python_utils_tests', '*.__pycache__'],
        ),
        package_data={'python_utils': ['py.typed']},
        long_description=long_description,
        install_requires=['typing_extensions>3.10.0.2'],
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
                'ruff',
                'pyright',
                'pytest',
                'pytest-cov',
                'pytest-mypy',
                'pytest-asyncio',
                'sphinx',
                'types-setuptools',
                'loguru',
                'loguru-mypy',
                'mypy-ipython',
                'blessings',
            ],
        },
        classifiers=['License :: OSI Approved :: BSD License'],
    )
