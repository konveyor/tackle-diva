"""
CLI entry point of the toolchain that is called from outside the container.
"""
from functools import partial
from logging import getLogger
from pathlib import Path

from typer import Option, Typer

from . import reinit_logger, sprint_
from .cli_pipeline.conversion import run_convert_pipeline
from .util import timer

app = Typer()
_logger = getLogger(__name__)


def run_verification_pipeline(
        # pylint: disable=unused-argument
        in_dir: Path, out_dir: Path,
        schema_info_file: Path,
        silent: bool = False, verbose: int = 0):
    "Verification pipeline."
    # TODO: to be implemented


@app.command()
def cli_main(
    app_name: str = Option(..., "-n", "--app-name",
                           help="Application name to be analyzed."),
    in_dir: Path = Option(None, "-i", "--in-dir",
                          help="directory of the target SQL files."),
    out_dir: Path = Option(
        None, "-o", "--out-dir",
        help="directory for the result files. It will be created if not exist."),
    convert: bool = Option(
        True,
        help="If set to True, performs conversion before verification."),
    schema_info_file: Path = Option(
        None,
        "--schema-file", "-f",
        help="Path to the file of schema analysis result (by default 'schema-info.yaml') file."
    ),
    init_command: str = Option(
        None,
        help="psql command to initialize database."),
    use_rules: bool = Option(
        True, help="Use horizontal rules of Rich library to separate output."),
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
    Run DOA toolchain.
    """
    reinit_logger(_logger, silent=silent, verbose=verbose,
                  tool_name="Toolchain")
    sprint = partial(sprint_, silent)
    with timer() as t:  # pylint: disable=invalid-name
        if convert:
            run_convert_pipeline(app_name=app_name,
                                 in_dir=in_dir,
                                 out_dir=out_dir,
                                 init_command=init_command, use_rules=use_rules,
                                 silent=silent, verbose=verbose)
        else:
            run_verification_pipeline(
                in_dir=in_dir, out_dir=out_dir,
                schema_info_file=schema_info_file,
                silent=silent, verbose=verbose)
        sprint(f"[green][OK] toolchain completed. ({t.sec_str()})[/]")


if __name__ == "__main__":
    app()
