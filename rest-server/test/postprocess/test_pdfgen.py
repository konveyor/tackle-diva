import json
from pathlib import Path
import pytest
from diva_server.postprocess.pdfgen import convert


@pytest.fixture
def in_file() -> Path:
    p = Path(__file__).parent.parent / \
        'fixtures/diva_output-1/transaction_summary.dot'
    return p


@pytest.fixture
def out_file() -> Path:
    p = Path(__file__).parent.parent / \
        'fixtures/rest_output/transaction_summary.pdf'
    return p


def test_main(in_file: Path, out_file: Path) -> None:
    assert in_file.exists()
    convert(in_file=in_file, out_file=out_file)
