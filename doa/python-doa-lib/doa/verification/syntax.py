"Perform syntax verification."
from dataclasses import asdict, dataclass, field
from functools import partial
from glob import iglob
from logging import getLogger
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import Optional

from rich import box
from rich.pretty import pretty_repr
from rich.table import Table
from typer import Option, Typer
from yaml import safe_dump, safe_load

from .. import console, reinit_logger, sprint_
from ..util import timer
from . import SYN_VERIFICATION_FILE

app = Typer()
_logger = getLogger(__name__)


@dataclass
class FileVerification:
    """
    Dataclass to store verification results for a file.
    """
    file: str  # file path (relative to root_dir) of files before splitting
    cp: str = None
    returncode: int = None
    stdout: str = None
    stderr: str = None


@dataclass
class SyntaxVerification:
    """
    Dataclass to store results of syntax verification.
    """
    root_dir: str  # root directory, that is specified by "in_dir", of input files.
    root_dir_fullpath: str  # full path (= abs path) of the root directory.
    # file path (relative to root_dir) of files before splitting
    files: list[FileVerification] = field(init=False, default_factory=list)


def verify_file(in_dir: Path, file_name: str, out_dir: Path,
                silent: bool = False, verbose: int = 0) -> FileVerification:
    """
    Analyze a single file in a directory and write results.

    If preprocess is True, input file is preprocessed, that is, encoding is changed.
    """
    sprint = partial(sprint_, silent)  # pylint: disable=unused-variable

    infile: Path = in_dir/file_name
    _logger.info("analyzing %s (%s)...", file_name, infile.resolve())

    # connection = psycopg2.connect()
    # connection.close()

    # args = ["psql", "-c", "\\a \\l"]
    args = ["psql", "--set", "ON_ERROR_STOP=on", "-f", str(infile.resolve())]
    completed_process: CompletedProcess = run(  # pylint: disable=subprocess-run-check
        args=args, text=True, capture_output=True)
    _logger.info(completed_process)

    info = FileVerification(
        file=file_name,
        returncode=completed_process.returncode,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr,
        cp=repr(completed_process)
    )

    #
    # write back split files
    #
    # _logger.info("%s statement(s) found", analyzer.len_statements())
    # oom = len(str(analyzer.len_statements()))
    # outfile: Path = out_dir/ file_name
    # for i, text in enumerate(analyzer.statements_text()):
    #     _logger.debug(text)
    #     outfile = base_outfile.with_stem(
    #         f"{base_outfile.stem}_{str(i).zfill(oom)}")  # like "bar/foo.sql" -> "bar/foo_000.sql"
    #     # _logger.info(outfile)
    #     info.split_files.append(str(outfile.relative_to(Path(out_dir))))
    #     with open(outfile, mode="w", encoding="utf-8") as f:
    #         f.write(text)
    #         _logger.info("split file %s has been writen",
    #                      outfile.resolve())
    # sprint(f"split files saved in {out_dir.resolve()}.")
    return info


def verify_dir(in_dir: Path, out_dir: Path, init_command: str = None,
               silent: bool = False, verbose: int = 0):
    "Verify SQL files in a directory and write results."
    with timer() as t:
        sprint = partial(sprint_, silent)
        _logger.info("input dir = %s", in_dir.resolve())
        _logger.info("output dir = %s", out_dir.resolve())

        if not out_dir.exists():
            _logger.info("  create output directory %s", out_dir)
            out_dir.mkdir(parents=True)

        _logger.info("initializing database...")
        # delete public schema and recreate it.
        cp = run(args=["psql", "-c", "drop schema public cascade; create schema public;"],
                 capture_output=True, text=True, check=True)
        _logger.info(cp)
        if init_command:
            _logger.info("executing init command: %s", init_command)
            cp = run(args=["psql", "-c", init_command],
                     capture_output=True, text=True, check=True)
            _logger.info(cp)

        sprint(
            f"starting syntax verification for files in {in_dir.resolve()}...")
        info = SyntaxVerification(root_dir=str(in_dir),
                                  root_dir_fullpath=str(in_dir.resolve()))

        g = partial(verify_file, in_dir=in_dir, out_dir=out_dir,
                    silent=silent, verbose=verbose)
        # iterate by file 
        for f in sorted(iglob('**/*.sql', root_dir=in_dir, recursive=True)):
            _logger.debug("file = %s", f)
            info.files.append(g(file_name=f))

        # compute stat
        n_files = len(info.files)
        n_success = len(list(filter(lambda x: x.returncode == 0, info.files)))
        n_fail = n_files-n_success

        # print
        sprint("")
        sprint(f"Number of converted SQLs (for Postgres): {n_files}")
        sprint("Syntax verification results:")
        sprint(f"  Success: {n_success} ({n_success/n_files : .2%})")
        sprint(f"  Failure: {n_fail} ({n_fail/n_files : .2%})")

        # sprint("")
        # sprint("Number of PK/FK relationships: N/A")
        # sprint("Semantics verification results:")
        # sprint("  (skipped)")

        # save
        outfile = out_dir/SYN_VERIFICATION_FILE
        with open(outfile, mode="w", encoding="utf-8") as f:
            _logger.debug(asdict(info))
            safe_dump(asdict(info), stream=f)
            sprint("")
            sprint(
                f"verification results {outfile.resolve()} has been saved.")
        sprint(f"({t.sec_str()})")


def dump_file(infile: Optional[Path] = None, show_all: bool = False, verbose: int = 0) -> None:
    """
    Dump the verification result file.
    """
    sprint = partial(sprint_, False)
    sprint(f"reading result file {infile}...")
    _logger.info("infile = %s", infile)
    _logger.info("  fullpath = %s", infile.resolve())
    with open(infile, mode="r", encoding="utf-8")as f:
        result = safe_load(f)
        _logger.info("successfully loaded and parsed.")
    _logger.debug(pretty_repr(result, indent_size=2))
    result_files: list = result['files'] if show_all else filter(
        lambda e: e['returncode'] != 0, result['files'])

    count = 0
    with console.pager(styles=True):
        for info in result_files:
            console.rule(info['file'])
            _logger.debug(info)
            info_file = (
                Path(result['root_dir_fullpath'])/info['file']).resolve()
            sprint(f"file = {info_file}")
            return_code = info['returncode']

            # show in table
            table = Table(box=box.MINIMAL, highlight=True,
                          leading=True, show_header=False)
            table.add_column("type", style="white dim")
            table.add_column("content", overflow="fold")
            # table.add_row("file", str(info_file))
            table.add_row(
                "return code", f"{return_code} ({'[green]OK[/]' if return_code==0 else '[red]ERROR[/]'})")
            table.add_row("strandard out", info['stdout'])
            table.add_row("strandard error", info['stderr'])
            sprint(table)
            count += 1

    if count == 0:
        sprint("")
        sprint("[cyan]No errors![/]")
        sprint("")


@app.command(name="dump")
def dump_result(
    in_dir: Optional[Path] = Option(None, "-i", "--in-dir",
                                    file_okay=False, dir_okay=True, exists=True,
                                    help="Directory where the result file is located. The file 'syntax-verification.yaml' under the specified directory will be read."),
    in_file: Optional[Path] = Option(None, "-f", "--file",
                                     file_okay=True, dir_okay=False, exists=True,
                                     help="Name of the result file."),
    show_all: bool = Option(False, "-a", "--all",
                            help="if set, show all entries inclufing successful ones."),
    verbose: int = Option(
        0,
        "--verbose",
        "-v",
        help="""
        Control log level. By default greater level than WARNING will be shown.
        Specifying '-v' shows INFO and higher level logs and '-vv' shows DEBUG and higher ones.
        If you specify '-s', log level is set to CRITICAL.
        """,
        count=True
    )
) -> None:
    """
    Dump the result of syntactic verification.

    By default it only shows error entries but it can be changed to show all entries by specifying '--all' option.
    """
    reinit_logger(_logger, silent=False, verbose=verbose,
                  tool_name="Syntax verification result dumper")
    sprint = partial(sprint_, False)
    if in_dir is not None:
        infile = in_dir / SYN_VERIFICATION_FILE
    else:
        infile = in_file
    dump_file(infile=infile, show_all=show_all, verbose=verbose)
    sprint("[green][OK] successfully displayed.[/]")


@app.command(name="run")
def cli_main(
    in_dir: Path = Option(
        None, "-i", "--in-dir",
        help="directory of the target SQL files."),
    out_dir: Path = Option(
        None, "-o", "--out-dir",
        help="directory for the result files. It will be created if not exist."),
    init_command: str = Option(
        None,
        help="psql command to initialize database."),
    silent: bool = Option(
        False,
        "--silent",
        "-s",
        help="Output nothing to console. This also sets log level to CRITICAL."
    ),
    verbose: int = Option(
        0,
        "--verbose",
        "-v",
        help="""
        Control log level. By default greater level than WARNING will be shown.
        Specifying '-v' shows INFO and higher level logs and '-vv' shows DEBUG and higher ones.
        If you specify '-s', log level is set to CRITICAL.
        """,
        count=True
    )
):
    """
    Perform syntax verification.
    """
    reinit_logger(_logger, silent=silent, verbose=verbose,
                  tool_name="Syntax verifier")
    sprint = partial(sprint_, silent)
    verify_dir(in_dir=in_dir, out_dir=out_dir,
               init_command=init_command, silent=silent, verbose=verbose)
    sprint("[green][OK] syntax verification completed.[/]")


if __name__ == "__main__":
    app()
