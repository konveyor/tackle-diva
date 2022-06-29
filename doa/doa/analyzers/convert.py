"""
SQL converter. Wrapper script of module sqal.doa.
"""
from logging import getLogger
from pathlib import Path

from rich.text import Text
from rich import print as rprint
from sqal.doa import main as convert
from typer import Option, Typer
from wasabi import Printer

from . import __version__

app = Typer()
msg = Printer()
logger = getLogger(__name__)


def main(app_name: str, in_dir: Path, out_dir: Path, lang: str) -> None:
    """
    Analyzes SQL files and convert them.

    This is the main logic called from cli_main().
    """
    # msg.good(f'DOA SQL converter v{__version__}')
    rprint(Text.assemble((f'DOA SQL converter v{__version__}', "cyan")))

    logger.info('setting up...')
    logger.info(f'  application name = {app_name}')
    logger.info(f'  input directory = {in_dir}')
    logger.info(f'  output directory = {out_dir}')
    if not out_dir.exists():
        logger.warning('  creating output directory')
        out_dir.mkdir(parents=True)

    if lang:
        rprint(f'converting SQL files, from "{lang}" to "PostgreSQL"...')
        convert(app_name=app_name, in_dir=in_dir, out_dir=out_dir,
                stat_dir=out_dir/"stat", use_debug_listener=True)
        rprint()
        rprint(Text.assemble(("[OK] successfully converted.", "green")))


@app.command()
def cli_main(
    # repo_url: str = Argument(...,
    #                          help="repository URL of tatget application."),
    app_name: str = Option(
        ...,
        "--app-name",
        "-n",
        help="target application name."
    ),
    in_dir: Path = Option(
        ...,
        "--in-dir",
        "-i",
        exists=True, file_okay=False, dir_okay=True, readable=True,
        help="input directory, which is a root directory of the cloned application repo."
    ),
    out_dir: Path = Option(
        "/tmp/out",
        "--out-dir", "-o",
        help="output directory of generated files"),
    lang: str = Option(
        None,
        "--lang",
        "-l",
        help="Convert SQL files based on the dialect specified by this option. Currently only \"oracle\" is supported."
    ),
) -> None:
    "Analyzes a specified app and generates ConfigMap manifests for the app."
    main(app_name=app_name, in_dir=in_dir, out_dir=out_dir, lang=lang)


if __name__ == '__main__':
    app()
