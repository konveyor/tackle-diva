"test for DOA library."
from doa import __version__


def test_version():
    "test version string."
    assert __version__ == '2.4.0'
