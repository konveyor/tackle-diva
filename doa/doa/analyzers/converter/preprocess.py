"""
preprocessor of SQL files before analysis.
"""
import pipes
from logging import basicConfig, getLogger
from os import makedirs
from pathlib import Path

from rich.logging import RichHandler

_logger = getLogger(__name__)


def preprocess_file(in_dir: str | Path, out_dir: str | Path,
                    file: str, debug: bool = False) -> None:
    """
    Preprocess a single file.

    file names before and after preprocessing: {in_dir}/{file} -> {out_dir}/{file}
    """
    if isinstance(in_dir, str):
        in_dir = Path(in_dir)
    if isinstance(out_dir, str):
        out_dir = Path(out_dir)
    makedirs(out_dir, exist_ok=True)

    _logger.info("preprocessing input file %s...", (in_dir/file).resolve())

    # use Template.copy() method:
    t = pipes.Template()  # pylint: disable=invalid-name

    # if debug is set to True, debug message is shown on stdout and stderr.
    # out:   nkf -w -d <test2.txt |
    # out:   tr a-z A-Z >/tmp/out/test2.txt
    # err:   + tr a-z A-Z
    # err:   + nkf -w -d
    t.debug(debug)

    # defined pipeline reads from stdin and writes to stdout
    # convert to UTF-8, convert unix linebreaks (\n)
    t.append("nkf -w -d", "--")
    t.append("tr a-z A-Z", "--")  # convert to uppercase
    t.copy(str(in_dir/file), str(out_dir/file))

    _logger.info(
        "successfully preprocessed and written to %s.", (out_dir/file).resolve())


if __name__ == "__main__":
    basicConfig(level="INFO", format="%(message)s",
                datefmt="[%X]", handlers=[RichHandler()])

    # creates a file for input. This is not directly related to pipes, just a sample file.
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write("shin saito\n齋藤 新\n")
    with open("test2.txt", "w", encoding="sjis") as f:
        f.write("shin saito\n齋藤 新\n")

    preprocess_file(".", "/tmp/out", file="test2.txt", debug=False)
