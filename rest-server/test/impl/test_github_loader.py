from logging import getLogger
from pathlib import Path

from diva_server.impl import GitHubLoader, SourceLoader

info = getLogger(__name__).info


def test_main():
    """
    test to clone external repository to ./fixture/tmp/ directory.

    Make sure to delete the directory before the test, or the test fails.
    """
    loader: SourceLoader = GitHubLoader({'github_url':
                                         "https://github.com/WASdev/sample.daytrader7.git"})
    in_dir = Path(__file__).parent.parent / 'fixtures/tmp'
    assert not in_dir.exists(), "delete test directory before testing"
    info(str(in_dir))
    loader.load(str(in_dir))
