"Split SQL files by each statement."
from contextlib import nullcontext
from dataclasses import asdict, dataclass, field
from functools import partial
from glob import iglob
from logging import getLogger
from pathlib import Path
from tempfile import TemporaryDirectory

from antlr4 import ParseTreeWalker
from typer import Option, Typer
from yaml import safe_dump

from .. import reinit_logger, sprint_
from ..preprocess import preprocess_dir
from ..util import parse, process_pool, timer
from . import PHYSICAL_INFO_FILE
from .split_helper import SplitHelper

app = Typer()
_logger = getLogger(__name__)


@dataclass
class FileSplitInfo:
    """
    Dataclass to store parent and child files by splitting.
    """
    file: str  # file path (relative to root_dir) of files before splitting
    split_files: list[str] = field(
        init=False, default_factory=list)  # path of split files


@dataclass
class PhysicalInfo:
    """
    Dataclass to store physical (= file splitting) info.
    """
    root_dir: str  # root directory, that is specified by "in_dir", of input files.
    root_dir_fullpath: str  # full path (= abs path) of the root directory.
    # file path (relative to root_dir) of files before splitting
    files: list[FileSplitInfo] = field(init=False, default_factory=list)


def split_file(file_name: str,
               in_dir: Path, out_dir: Path,
               silent: bool = False, verbose: int = 0) -> FileSplitInfo:
    """
    Analyze a single file in a directory and write results.

    If preprocess is True, input file is preprocessed, that is, encoding is changed.
    """
    sprint = partial(sprint_, silent)  # pylint: disable=unused-variable

    infile = in_dir/file_name

    # parsing
    tree, parser = parse(infile, silent=silent, verbose=verbose)
    ist = parser.getTokenStream()  # ist is valid after cm is closed?

    # analyzing
    _logger.info("analyzing file %s...", infile)
    walker = ParseTreeWalker()
    # PLSQLAnalyzer(parser, ist, ignore_physprop=IGNORE_PHYSPROP)
    analyzer = SplitHelper(parser=parser, input_stream=ist)
    _logger.info("walking parse tree...")
    walker.walk(analyzer, tree)
    _logger.info("successfully walked.")

    #
    # write back split files
    #
    _logger.info("%s statement(s) found", analyzer.len_statements())
    info = FileSplitInfo(file=file_name)
    oom = len(str(analyzer.len_statements()))
    # _logger.info("oom = %d", oom)
    base_outfile = Path(out_dir)/file_name
    # _logger.info(base_outfile.stem)
    for i, text in enumerate(analyzer.statements_text()):
        # _logger.info(str(i).zfill(oom))
        _logger.debug(text)
        outfile = base_outfile.with_stem(
            # like "bar/foo.sql" -> "bar/foo_000.sql"
            f"{base_outfile.stem}_{str(i).zfill(oom)}")
        # _logger.info(outfile)
        info.split_files.append(str(outfile.relative_to(Path(out_dir))))
        with open(outfile, mode="w", encoding="utf-8") as f:
            f.write(text)
            _logger.info("split file %s has been writen",
                         outfile.resolve())
    # sprint(f"split files saved in {out_dir.resolve()}.")
    return info


def split_dir(in_dir: Path, out_dir: Path, preprocess: bool = True,
              silent: bool = False, verbose: int = 0):
    "Split files in a directory and write split ones."
    with timer() as t:
        sprint = partial(sprint_, silent)
        sprint(
            f"splitting files in {in_dir.resolve()} (preprocess = {preprocess})...")

        # if needed to preprocess,
        # create tempdir and save the pre-processing result
        if preprocess:
            cm = TemporaryDirectory()  # pylint: disable=invalid-name
        else:
            cm = nullcontext(None)  # pylint: disable=invalid-name

        with cm as tempdir:
            org_in_dir = in_dir  # save original directory

            if tempdir is not None:  # i.e. need to preprocess
                _logger.debug(tempdir)
                preprocess_dir(in_dir=in_dir, out_dir=tempdir,
                               silent=silent, verbose=verbose)
                in_dir = Path(tempdir)
                sprint("")
                sprint("splitting...")

            _logger.info("input dir = %s", in_dir.resolve())
            _logger.info("output dir = %s", out_dir.resolve())
            if not out_dir.exists():
                _logger.info("  create output directory %s", out_dir)
                out_dir.mkdir(parents=True)
            info = PhysicalInfo(root_dir=str(org_in_dir),
                                root_dir_fullpath=str(org_in_dir.resolve()))

            # pylint:disable=invalid-name
            g = partial(split_file, in_dir=in_dir, out_dir=out_dir,
                        silent=silent, verbose=verbose)
            # iterate by file (TODO: parallelize)
            with process_pool() as pp:
                _results = pp.imap_unordered(
                    g, iglob('**/*.sql', root_dir=in_dir, recursive=True))
                info.files = list(_results)

        num_files = len(info.files)
        num_split_files = sum([len(a_file.split_files)
                              for a_file in info.files])
        sprint(
            f"original {num_files} file(s) are split into {num_split_files} files, "
            f"saved in {out_dir.resolve()}.")
        split_info_file = out_dir/PHYSICAL_INFO_FILE
        with open(split_info_file, mode="w", encoding="utf-8") as f:
            _logger.info(asdict(info))
            safe_dump(asdict(info), stream=f, indent=4)
        sprint(f"split info saved in {split_info_file.resolve()}.")
        sprint(f"({t.sec_str()})")


@app.command()
def cli_main(
    in_dir: Path = Option(None, "-i", "--in-dir",
                          help="directory of the files to be split."),
    out_dir: Path = Option(None, "-o", "--out-dir",
                           help="directory for the split files. It will be created if not exist."),
    silent: bool = Option(
        False,
        "--silent",
        "-s",
        help="Output nothing to console. This sets log level to CRITICAL."
    ),
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
    Split SQL files by each statement.
    """
    reinit_logger(_logger, silent=silent, verbose=verbose,
                  tool_name="SQL file splitter")
    sprint = partial(sprint_, silent)
    split_dir(in_dir=in_dir, out_dir=out_dir,
              preprocess=True, silent=silent, verbose=verbose)
    sprint("[green][OK] split completed.[/]")


if __name__ == "__main__":
    app()
