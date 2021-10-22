import json
from pathlib import Path

import pytest
from diva_server.postprocess.db_extractor import main


@pytest.fixture
def in_file() -> Path:
    p = Path(__file__).parent.parent / \
        'fixtures/diva_output-1/transaction.json'
    return p


@pytest.fixture
def out_file() -> Path:
    p = Path(__file__).parent.parent / \
        'fixtures/rest_output/database.json'
    return p


def test_main(in_file: Path, out_file: Path) -> None:
    assert in_file.exists()
    json.load(open(in_file))  # check if it can be loaded as a JSON file.
    main(in_file=in_file, out_file=out_file, app_path='/app')
