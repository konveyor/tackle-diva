"""
DOA CLI entrypoint.
"""
from functools import partial
from logging import getLogger
from pathlib import Path
from subprocess import run

from typer import Option, Typer

from . import __app_ver_rich__, __version__, console, reinit_logger, sprint_

# from .dev import app as app_dev

app = Typer()
# app.add_typer(app_dev, name="dev")
_logger = getLogger(__name__)
compose_file = Path(__file__).parent / "compose.yaml"


@app.command()
def convert(
    in_dir: Path = Option(
        None, "-i", "--in-dir",
        help="directory of the target SQL files."),
    out_dir: Path = Option(
        None, "-o", "--out-dir",
        help="directory for the result files. It will be created if not exist."),
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
    "convert SQL files that contain dialect into ones for PostgreSQL"
    reinit_logger(_logger, silent=silent, verbose=verbose)
    sprint = partial(sprint_, silent)

    if not out_dir.exists():
        _logger.info("  create output directory %s", out_dir)
        out_dir.mkdir(parents=True)

    # compose file
    _logger.info(compose_file)

    # mount
    _mount_in = ["-v", f"{in_dir.absolute()}:/opt/in"]
    _mount_out = ["-v", f"{out_dir.absolute()}:/opt/out"]
    _logger.info(_mount_in)
    _logger.info(_mount_out)

    with open(compose_file, mode="r", encoding="utf-8") as f:
        _logger.debug(f.read())
    _args_compose = ["docker", "compose", "-f",
                     compose_file, "run", "--rm"]
    _args_program = ["python",
                     "-m", "doa.cli", "-n", "northwind", "-i", "/opt/in", "-o", "/opt/out"]
    _args = _args_compose + _mount_in + _mount_out + ["app"] + _args_program
    _logger.info(_args)

    run(_args, check=True)
    run(["docker", "compose", "-f", compose_file, "stop"], check=True)


@app.command()
def gen_yaml():
    "generate YAML files of K8s resource definition"


@app.command()
def verify():
    "verify DB schema"
    pass


@app.command()
def version():
    "show version and exit"
    console.print(__app_ver_rich__)


if __name__ == '__main__':
    app()
