# Contributing to python-utils

Bug reports, code and documentation contributions are welcome. You can help this
project also by using the development version and by reporting any bugs you might encounter

## 1. Reporting bugs
It's important to provide following details when submitting a bug
- Python version
- python-utils version
- OS details

If possible also provide a minimum reproducible working code.
## 2. Contributing Code and Docs

Before working on a new feature or a bug, please browse [existing issues](https://github.com/WoLpH/python-utils/issues)
to see whether it has previously been discussed.

If your change alters python-util's behaviour or interface, it's a good idea to
discuss it before you start working on it.

If you are fixing an issue, the first step should be to create a test case that
reproduces the incorrect behaviour. That will also help you to build an
understanding of the issue at hand.

Make sure to add relevant tests and update documentation in order to get
your PRs merged. We strictly adhere to 100% code coverage. 

### Development Environment

#### Getting the code

Go to <https://github.com/WoLpH/python-utils> and fork the project repository.

```bash
# Clone your fork
$ git clone git@github.com:<YOU>/python-utils.git

# Enter the project directory
$ cd python-utils

# Create a branch for your changes
$ git checkout -b my_awesome_branch
```

#### Testing
Before submitting any PR make sure your code passes all the tests.

To run the full test-suite, make sure you have `tox` installed and run the following command:

```bash
$ tox
```

Or to speed it up (replace 8 with your number of cores), run:

```bash
$ tox -p8
```

During development I recommend using pytest directly and installing the package in development mode.

Create virtual environment and activate
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```
Install test requirements
```bash
$ cd python-utils
$ pip install -e ".[tests]"
```
Run tests
```bash
$ py.test
```

Note that this won't run `flake8` yet, so once all the tests succeed you can run `flake8` to check for code style errors.

```bash
$ flake8
```
