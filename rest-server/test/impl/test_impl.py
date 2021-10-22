import json
from logging import DEBUG, debug
from pathlib import Path
from tempfile import TemporaryDirectory, TemporaryFile

import pytest
import yaml
from diva_server.impl import Analyzer, OnDockerAnalyzer, new_app

# def test_new_app() -> None:
#     in_dir, out_dir = new_app(id='day_trader', name="Java EE7: DayTrader Sample", source={
#         "github_url": "https://github.com/WASdev/sample.daytrader7.git"})  # type str, str


@pytest.fixture
def analyzer() -> Analyzer:
    return OnDockerAnalyzer()


@pytest.fixture
def in_dir() -> str:
    return str(Path(__file__).parent/'fixtures'/'sample.daytrader7')


@pytest.fixture
def out_dir() -> str:
    with TemporaryDirectory() as d:
        yield d


def test_analyze(analyzer: Analyzer, in_dir: str, out_dir: str) -> None:
    analyzer.analyze(in_dir, out_dir)
    assert (Path(out_dir)/'contexts.yml').exists()
    with open(Path(out_dir)/'contexts.yml') as f1:
        yaml.safe_load(f1)
    assert (Path(out_dir)/'transaction.yml').exists()
    with open(Path(out_dir)/'transaction.yml') as f2:
        yaml.safe_load(f2)
    assert (Path(out_dir)/'transaction.json').exists()
    with open(Path(out_dir)/'transaction.json') as f3:
        json.load(f3)
