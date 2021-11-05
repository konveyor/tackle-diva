import json
from pathlib import Path

import pytest
from diva_server.postprocess.analysis import main


@pytest.fixture
def in_file() -> Path:
    p = Path(__file__).parent.parent / \
        'fixtures/diva_output-1/transaction.json'
    return p


@pytest.fixture
def out_file() -> Path:
    p = Path(__file__).parent.parent / \
        'fixtures/rest_output/transaction_summary.dot'
    return p


def test_main(in_file: Path, out_file: Path) -> None:
    assert in_file.exists()
    json.load(open(in_file))  # check if it can be loaded as a JSON file.
    main(input_file=in_file, output_file=out_file)
