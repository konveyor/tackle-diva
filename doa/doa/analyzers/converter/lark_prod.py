"""
Lark parsing code for production release.

Grammar is ported from ANTLR v4 to Lark for easy of development.
"""
from logging import basicConfig
from pathlib import Path

from lark import Tree
from rich import print  # pylint: disable=redefined-builtin
from typer import Typer

from .lark_lib.parser import parse_file, plsql_parser

app = Typer()


@app.command()
def main(file: Path):
    "parse the given PL/SQL file"
    parser = plsql_parser()
    # parser = plsql_parser(parser='lalr')  # experimenting
    tree: Tree = parse_file(parser, file)
    print(tree)


if __name__ == "__main__":
    basicConfig(
        level="INFO", format='{asctime} [{levelname:.4}] {name}: {message}', style='{')
    app()
