"Analyze SQL files (especially FK relations)"
from contextlib import nullcontext
from dataclasses import asdict, dataclass, field
from functools import partial
from glob import iglob
from logging import getLogger
from pathlib import Path
from tempfile import TemporaryDirectory

from antlr4 import ParseTreeWalker
from rich.pretty import pretty_repr
from typer import Option, Typer
from yaml import safe_dump, safe_load

from .. import reinit_logger, sprint_
from ..preprocess import preprocess_file
from ..util import parse, process_pool, timer
from . import PHYSICAL_INFO_FILE, SCHEMA_INFO_FILE
from .schema_analyzer import AnalysisResult, FKAnalyzer

app = Typer()
_logger = getLogger(__name__)


@dataclass
class SchemaInfo:
    """
    dataclass for storing overall schema info.
    """
    schema: str
    root_dir: str
    root_dir_fullpath: str
    # physical information (including file splitting)
    physical_info: dict = None
    files: list[dict] = field(init=False, default_factory=list)


def analyze_file(file_name: str, in_dir: Path, out_dir: Path,
                 preprocess: bool = False,
                 silent: bool = False, verbose: int = 0) -> AnalysisResult:
    """
    Analyze a single file in a directory and write results.

    If preprocess is True, input file is preprocessed, that is, encoding is changed.
    """
    sprint = partial(sprint_, silent)  # pylint: disable=unused-variable

    if preprocess:
        cm = TemporaryDirectory()
    else:
        cm = nullcontext(None)

    with cm as tempdir:
        if tempdir is not None:
            _logger.debug(tempdir)
            preprocess_file(in_dir=in_dir, out_dir=tempdir, file=file_name,
                            silent=silent, verbose=verbose)
            infile = Path(tempdir)/file_name
        else:
            infile = in_dir/file_name

        # parsing
        tree, parser = parse(infile, silent=silent, verbose=verbose)
        ist = parser.getTokenStream()  # ist is valid after cm is closed?

        # analyzing
        _logger.info("analyzing file %s...", infile)
        walker = ParseTreeWalker()
        # PLSQLAnalyzer(parser, ist, ignore_physprop=IGNORE_PHYSPROP)
        analyzer = FKAnalyzer(
            parser=parser, input_stream=ist, arg_ctor={
                "sub_path": file_name,
            }
        )
        _logger.info("walking parse tree...")
        walker.walk(analyzer, tree)
        _logger.info("successfully walked.")
        result: AnalysisResult = analyzer.result

        _logger.debug("analysis result:")
        _logger.debug(pretty_repr(asdict(result)))
        return result


def analyze_dir(schema_name: str, in_dir: Path, out_dir: Path, preprocess: bool = False,
                silent: bool = False, verbose: int = 0):
    "Analyze files in a directory and write results."
    with timer() as t:
        sprint = partial(sprint_, silent)
        sprint(
            f"analyzing SQL files of schema '{schema_name}' (preprocess = {preprocess})...")
        _logger.info("input dir = %s", in_dir.resolve())
        _logger.info("output dir = %s", out_dir.resolve())
        if not out_dir.exists():
            _logger.info("  create output directory %s", out_dir)
            out_dir.mkdir(parents=True)

        info = SchemaInfo(schema=schema_name, root_dir=str(
            in_dir), root_dir_fullpath=str(in_dir.resolve()))
        _logger.info("reading phyisical info...")
        with open(in_dir/PHYSICAL_INFO_FILE, mode="r", encoding="utf-8") as f:
            phyisical_info = safe_load(f)
            _logger.debug("physical info:")
            _logger.debug(phyisical_info)
        info.physical_info = phyisical_info['files']

        _logger.info("scanning files")
        g = partial(analyze_file, in_dir=in_dir, out_dir=out_dir, preprocess=preprocess,
                    silent=silent, verbose=verbose)
        # iterate by file (TODO: parallelize)
        with process_pool() as pp:
            iter_results = pp.imap_unordered(
                g, iglob('**/*.sql', root_dir=in_dir, recursive=True))
            n_files = 0
            results = list(iter_results)

        info.files = results
        _logger.debug("analysis results:")
        _logger.debug(asdict(info))

        # summarize
        n_files = len(info.files)
        n_tables = sum([len(file_entry.tables) for file_entry in info.files])
        n_FKs = sum([len(table.FKs)
                    for file_entry in info.files for table in file_entry.tables])

        # write result
        sprint(f"\n{n_files} file(s) are analyzed.")
        sprint(f"  {n_tables} table(s) are defined")
        sprint(f"  {n_FKs} FK/PK relations are found")
        sprint("")

        schema_info_file = out_dir/SCHEMA_INFO_FILE
        with open(schema_info_file, mode="w", encoding="utf-8") as f:
            safe_dump(asdict(info), stream=f)
        sprint(f"analysis result {schema_info_file.resolve()} has been saved.")
        sprint(f"({t.sec_str()})")


@app.command()
def cli_main(
    schema_name: str = Option(
        "schema",
        "-n", "--schema-name",
        help="Schema name to be analyzed."),
    in_dir: Path = Option(
        None,
        "-i", "--in-dir",
        help="directory of the analysis target."),
    out_dir: Path = Option(
        None, "-o", "--out-dir",
        help="Directory for the analysis results. It will be created if not exist."),
    in_file: str = Option(
        None,
        "-f", "--in-file",
        help="Process a single file. this value is a sub-path under the input directory."),
    preprocess: bool = Option(
        False,
        help="if true, preprocessing (encoding conversion to UTF-8, and uppercase conversion) will be performed on each file."
    ),
    silent: bool = Option(
        False,
        "--silent", "-s",
        help="Output nothing to console. This sets log level to CRITICAL."
    ),
    verbose: int = Option(
        0,
        "--verbose", "-v",
        help="Control log level. By default greater level than WARNING will be shown."
        "Specifying '-v' shows INFO and higher level logs and '-vv' shows DEBUG and higher ones. "
        "If you specify '-s', log level is set to CRITICAL.",
        count=True
    )
):
    """
    CLI entrypoint of schema analysis.
    """
    reinit_logger(_logger, silent=silent, verbose=verbose,
                  tool_name="Schema analyzer from SQL sources")
    sprint = partial(sprint_, silent)
    if in_file:
        analyze_file(in_dir=in_dir, file_name=in_file, out_dir=out_dir,
                     preprocess=preprocess,
                     silent=silent, verbose=verbose)
    else:
        analyze_dir(schema_name=schema_name, in_dir=in_dir, out_dir=out_dir, preprocess=preprocess,
                    silent=silent, verbose=verbose)
    sprint("[green][OK] analysis completed.[/]")


if __name__ == "__main__":
    app()
