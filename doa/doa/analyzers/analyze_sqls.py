"""
analyzer and generator for SQL files.
"""
import subprocess
from glob import iglob
from logging import getLogger
from pathlib import Path
from subprocess import CompletedProcess, run

from rich import print as rprint
from rich.text import Text
from sqal.doa import main as convert
from typer import Abort, Option, Typer
from wasabi import Printer

from . import __version__

app = Typer()
msg = Printer()
logger = getLogger(__name__)


def main(app_name: str, in_dir: Path, out_dir: Path, lang: str) -> None:
    """
    Analyzes a specified app and generates ConfigMap manifests for the app.
    This is the main logic called from cli_main().
    """
    _args = ['kubectl', 'create', 'cm', f'{app_name}-cm-sqls',
             '--dry-run=client', '-o', 'yaml']

    # msg.good(f'DiVA-DOA: SQL files analyzer v{__version__}')
    # rprint(Text.assemble((f'DOA SQL file analyzer v{__version__}', "cyan")))

    logger.info('setting up...')
    logger.info(f'  application name = {app_name}')
    logger.info(f'  input directory = {in_dir}')
    logger.info(f'  output directory = {out_dir}')
    if not out_dir.exists():
        logger.warning('  creating output directory')
        out_dir.mkdir(parents=True)
    out_file: Path = out_dir / 'cm-sqls.yaml'
    # out_file: Path = out_dir / f'{app_name}-cm-sqls.yaml'
    logger.info(f'  output yaml file = {out_file}')

    if lang:
        msg.info(f"converting SQL files, from {lang} to Postgres...")
        convert(app_name=app_name, in_dir=in_dir, out_dir=Path("/tmp/out"),
                stat_dir=out_dir/"stat", use_debug_listener=True)
        msg.info("converted.")
        in_dir = Path("/tmp/out")  # overwrite

    logger.info('searching SQL files...')
    for pth in iglob('**/*.sql', root_dir=in_dir, recursive=True):
        logger.debug(f'  found: {pth}')
        logger.debug(f'  found: {in_dir / pth}')
        _args.extend(['--from-file', in_dir / pth])

    logger.info('generating manifest...')
    with open(out_file, mode='w', encoding='utf-8') as file:
        logger.info(f"  output file: {out_file}")
        logger.info(f"  command to create: {' '.join(map(str, _args))}")
        comp_proc: CompletedProcess = run(
            args=_args, stdout=file, stderr=subprocess.PIPE, text=True, check=False)
        if comp_proc.returncode == 0:
            # normal termination
            rprint(f'configmap manifest (SQL files) {out_file} has been generated.')
            logger.info('successfully generated')
        else:
            # abnormal termination
            msg.fail('generation failed')
            msg.fail(comp_proc.stderr)
            raise Abort()


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
