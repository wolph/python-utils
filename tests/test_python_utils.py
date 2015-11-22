import python_utils


def test_definitions():
    # The setup.py requires this so we better make sure they exist :)
    assert python_utils.__version__
    assert python_utils.__author__
    assert python_utils.__author_email__
    assert python_utils.__description__

