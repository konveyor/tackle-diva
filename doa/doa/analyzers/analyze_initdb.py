"""
analyzer and generator for SQL startup.
"""
import subprocess
from dataclasses import dataclass
from os import getcwd
from pathlib import Path
from shutil import copyfile
from subprocess import CompletedProcess, run
from tempfile import TemporaryDirectory

from lark import Lark, Tree
from lark.visitors import Visitor
from typer import Abort, Option, Typer
from wasabi import msg

from . import __version__

# from glob import iglob
# from typing import Any
# from ast import parse

app = Typer()


def main(app_name: str, in_dir: Path, out_dir: Path, init_file: Path) -> None:
    """
    Analyzes a specified app and generates ConfigMap manifests for the app.
    This is the main logic called from cli_main().
    """
    _args = ['kubectl', 'create', 'cm', f'{app_name}-cm-init-db',
             '--dry-run=client', '-o', 'yaml']

    msg.good(f'DiVA-DOA: SQL init file analyzer v{__version__}')

    msg.info('setting up...')
    msg.info(f'  current directory = {getcwd()}')
    msg.info(f'  application name = {app_name}')
    msg.info(f'  input directory = {in_dir}')
    msg.info(f'  output directory = {out_dir}')
    msg.info(f'  init file = {init_file}')

    with TemporaryDirectory() as d:  # create tempdir
        # read from init_file and write to init_db.sh
        init_db_file = Path(d) / 'init_db.sh'

        if init_file:
            msg.info('scanning init file for lines containing "psql"...')
            with (open(in_dir / init_file, mode="r", encoding="utf-8") as f,
                  open(init_db_file, mode="w", encoding="utf-8") as g):
                for line in f.readlines():  # type: str
                    if line.startswith("psql"):
                        msg.info(f'  found: {line}')
                        parsed: PsqlStatement = parse_psql(line)
                        # msg.info(f"  {parsed}")
                        msg.info(f"  converted to: {parsed.to_statement()}")
                        g.write(parsed.to_statement()+"\n")
        else:
            msg.info('using general init file...')
            copyfile(Path(__file__).parent/"init-db.sh", init_db_file)

        out_file = out_dir / "cm-init-db.yaml"
        msg.info('generating manifest...')
        with open(out_file, mode='w', encoding='utf-8') as file:
            _args.extend(['--from-file', init_db_file])
            msg.info(f"  output file: {out_file}")
            msg.info(f"  k8s command to create: {' '.join(map(str, _args))}")
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


@dataclass
class PsqlStatement:
    "class represents parameters of psql statement."
    host: str = None
    user: str = None
    database: str = None
    file: str = None
    basename: str = None  # basename of value of file

    def to_statement(self) -> str:
        "convert to psql statement used in Pods."
        args = ["psql", "-h", "${DB_HOST}", "-U", "postgres"]
        if self.database:
            args.extend(["-d", self.database])
        args.extend(["-f", f'${{SQL_ROOT}}/{self.basename}'])
        return ' '.join(args)


class MyVisitor(Visitor):
    "Visitor for parse tree of psql statement."

    def __init__(self):
        self.data = PsqlStatement()

    def host(self, tree: Tree):
        "visitor handler for host subtree"
        assert tree.data == 'host'
        # print(tree)
        self.data.host = str(tree.children[0])

    def user(self, tree: Tree):
        "visitor handler for user subtree"
        # print(tree)
        self.data.user = str(tree.children[0])

    def database(self, tree: Tree):
        "visitor handler for database subtree"
        # print(tree)
        self.data.database = str(tree.children[0])

    def file(self, tree: Tree):
        "visitor handler for file subtree"
        # print(tree)
        self.data.file = str(tree.children[0])
        self.data.basename = Path(self.data.file).name


def parse_psql(line: str) -> PsqlStatement:
    """
    parse a psql statement and returns parameters extracted.
    """
    parser = Lark(r"""
    start: "psql" option*
    ?option: host | user | database | file 
    host: "-h" ARG 
    user: "-U" ARG
    database: "-d" ARG
    file: "-f" ARG 
    ARG: /\S+/

    %import common.WS
    %ignore WS
    """)
    tree = parser.parse(line)
    # print(tree.pretty())
    v = MyVisitor()
    v.visit(tree)
    return v.data


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
    init_file: Path = Option(
        None,
        "--init-file",
        help="init file under the repository that includes DB init code")
) -> None:
    "Analyzes a specified app and generates ConfigMap manifests for the app."
    main(app_name=app_name, in_dir=in_dir, out_dir=out_dir, init_file=init_file)


if __name__ == '__main__':
    app()
