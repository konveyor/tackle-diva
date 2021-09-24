import pytest
from pathlib import Path
from diva_server.impl import new_app


@pytest.fixture
def out_dir() -> str:
    yield str(Path(__file__).parent.parent / "fixtures" / "rest_output")


def test_new_app(out_dir: str):
    res = new_app(id='day_trader',
                  source={
                      "github_url": "https://github.com/WASdev/sample.daytrader7.git"},
                  name='Java EE7: DayTrader Sample', out_dir=out_dir)
