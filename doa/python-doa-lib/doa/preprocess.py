"""
preprocessor of SQL files before analysis.
"""
import pipes
from functools import partial
from glob import iglob
from logging import getLogger
from os import makedirs
from pathlib import Path
from subprocess import CompletedProcess, run

from more_itertools import ilen
from typer import Option, Typer

from . import reinit_logger, sprint_
from .util import process_pool

_logger = getLogger(__name__)
app = Typer()


def preprocess_file(file: str, in_dir: str | Path = None, out_dir: str | Path = None,
                    verbose: int = 0, silent: bool = False) -> None:
    """
    Preprocess a single file.

    file names before and after preprocessing: {in_dir}/{file} -> {out_dir}/{file}
    """
    sprint = partial(sprint_, silent)  # pylint: disable=unused-variable

    _logger.debug("in_dir = %s", in_dir)
    _logger.debug("out_dir = %s", out_dir)
    _logger.debug("file = %s", file)

    if isinstance(in_dir, str):
        _logger.debug("converting in_dir to Path")
        in_dir = Path(in_dir)
    if isinstance(out_dir, str):
        _logger.debug("converting out_dir to Path")
        out_dir = Path(out_dir)
    makedirs(out_dir, exist_ok=True)

    _logger.info("preprocessing input file %s...", (in_dir/file).resolve())

    cp: CompletedProcess = run(   # pylint: disable=invalid-name
        ["nkf", "-g", str(in_dir/file)], text=True, capture_output=True, check=True)
    _logger.info("input file encoding (guessed) = %s", cp.stdout)
    _logger.info("converting to UTF-8 and LF...")
    # use Template.copy() method:
    t = pipes.Template()  # pylint: disable=invalid-name

    # if debug is set to True, debug message is shown on stdout and stderr.
    # out:   nkf -w -d <test2.txt |
    # out:   tr a-z A-Z >/tmp/out/test2.txt
    # err:   + tr a-z A-Z
    # err:   + nkf -w -d
    if verbose >= 2:
        t.debug(True)

    # defined pipeline reads from stdin and writes to stdout
    # convert to UTF-8, convert unix linebreaks (\n)
    t.append("nkf -w -d", "--")
    t.append("tr a-z A-Z", "--")  # convert to uppercase
    t.copy(str(in_dir/file), str(out_dir/file))

    sprint(
        f"preprocessed file {(out_dir/file).resolve()} has been saved.")


def preprocess_dir(
    in_dir: Path, out_dir: Path,
        verbose: int = 0, silent: bool = False) -> None:
    "Preprocess files in a directory and write out them to another directory."
    sprint = partial(sprint_, silent)
    if isinstance(in_dir, str):
        in_dir = Path(in_dir)
    if isinstance(out_dir, str):
        out_dir = Path(out_dir)
    _logger.info("input dir = %s", in_dir.resolve())
    _logger.info("output dir = %s", out_dir.resolve())
    if not out_dir.exists():
        _logger.info("  create output directory %s", out_dir)
        out_dir.mkdir(parents=True)
    sprint(f"preprocessing files in {in_dir.resolve()}...")

    # pylint:disable=invalid-name
    g = partial(preprocess_file, in_dir=in_dir, out_dir=out_dir,
                silent=True, verbose=verbose)
    # iterate by file (TODO: parallelize)
    with process_pool() as pp:
        result = pp.imap_unordered(
            g, iglob('**/*.sql', root_dir=in_dir, recursive=True))
        sprint(
            f"{ilen(result)} files are preprocessed and saved in {out_dir.resolve()}.")


@app.command()
def cli_main(
    in_dir: Path = Option(None, "-i", "--in-dir",
                          help="directory of the input file."),
    out_dir: Path = Option(None, "-o", "--out-dir",
                           help="directory of the output file. It will be created if not exist."),
    basename: str = Option(
        None, "-f", help="basename of the input/output file."),
    silent: bool = Option(False, "--silent", "-s",
                          help="Output nothing to console. This sets log level to CRITICAL."),
    verbose: int = Option(
        0,
        "--verbose",
        "-v",
        help="Control log level. By default greater level than WARNING will be shown."
        "Specifying '-v' shows INFO and higher level logs and '-vv' shows DEBUG and higher ones. "
        "If you specify '-s', log level is set to CRITICAL.",
        count=True
    )
):
    """
    CLI entrypoint of preprocessing.

    File names before and after preprocessing: {in_dir}/{basename} -> {out_dir}/{basename}
    """
    reinit_logger(_logger, silent=silent, verbose=verbose)
    if basename:
        preprocess_file(in_dir=in_dir, out_dir=out_dir,
                        file=basename, verbose=verbose, silent=silent)
    else:
        preprocess_dir(in_dir=in_dir, out_dir=out_dir,
                       verbose=verbose, silent=silent)
    sprint = partial(sprint_, silent)
    sprint("[green][OK] preproceessing completed.[/]")


if __name__ == "__main__":
    app()
    # # creates a file for input. This is not directly related to pipes, just a sample file.
    # with open("test.txt", "w", encoding="utf-8") as f:
    #     f.write("shin saito\n齋藤 新\n")
    # with open("test2.txt", "w", encoding="sjis") as f:
    #     f.write("shin saito\n齋藤 新\n")

    # preprocess_file(".", "/tmp/out", file="test2.txt", debug=False)
