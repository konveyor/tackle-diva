"""
analyzer and generator for SQL files.
"""
import subprocess
from glob import iglob
from pathlib import Path
from subprocess import CompletedProcess, run

from typer import Abort, Option, Typer
from wasabi import Printer

from . import __version__

app = Typer()
msg = Printer()


def main(app_name: str, in_dir: Path, out_dir: Path) -> None:
    """
    Analyzes a specified app and generates ConfigMap manifests for the app.
    This is the main logic called from cli_main().
    """
    _args = ['kubectl', 'create', 'cm', f'{app_name}-cm-sqls',
             '--dry-run=client', '-o', 'yaml']

    msg.good(f'DiVA-DOA: SQL files analyzer v{__version__}')

    msg.info('setting up...')
    msg.info(f'  application name = {app_name}')
    msg.info(f'  input directory = {in_dir}')
    msg.info(f'  output directory = {out_dir}')
    if not out_dir.exists():
        msg.warn('  creating output directory')
        out_dir.mkdir(parents=True)
    out_file: Path = out_dir / 'cm-sqls.yaml'
    # out_file: Path = out_dir / f'{app_name}-cm-sqls.yaml'
    msg.info(f'  output yaml file = {out_file}')

    msg.info('searching SQL files...')
    for pth in iglob('**/*.sql', root_dir=in_dir, recursive=True):
        msg.info(f'  found: {pth}')
        msg.info(f'  found: {in_dir / pth}')
        _args.extend(['--from-file', in_dir / pth])

    msg.info('generating manifest...')
    with open(out_file, mode='w', encoding='utf-8') as file:
        msg.info(f"  output file: {out_file}")
        msg.info(f"  command to create: {' '.join(map(str, _args))}")
        comp_proc: CompletedProcess = run(
            args=_args, stdout=file, stderr=subprocess.PIPE, text=True, check=False)
        if comp_proc.returncode == 0:
            # normal termination
            msg.good('successfully generated')
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
        help="output directory of generated files")
) -> None:
    "Analyzes a specified app and generates ConfigMap manifests for the app."
    main(app_name=app_name, in_dir=in_dir, out_dir=out_dir)


if __name__ == '__main__':
    app()
