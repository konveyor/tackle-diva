"""
PL/SQL parser interface (to be production)
"""
import sys
from contextlib import nullcontext
from logging import getLogger
from pathlib import Path

import typer
from antlr4 import *
from typer import Argument, Option
from wasabi import msg

from .plsql.PlSqlLexer import PlSqlLexer
from .plsql.PlSqlParser import PlSqlParser

app = typer.Typer()
_logger = getLogger(__name__)


@app.command()
def main(
    infile: Path = Argument(..., exists=True, readable=True,
                            help="An input PL/SQL file to be parsed."),
    silent: bool = Option(
        False, "--silent", "-s", help="setting to true supresses output of parsed tree."),
    to_console: bool = Option(False, "--err-console/--err-file", "-c/-f",
                              help="by default, stderr is directed to a file. Setting true to make it display on console.")
):
    "Parses the given PL/SQL file."

    with nullcontext(sys.stderr) if to_console else open("logs/" + infile.with_suffix(".log").name, encoding="utf-8", mode="w") as f:
        sys.stderr = f
        _logger.info(f"parsing file {infile}...")
        stream = FileStream(infile, encoding="utf-8")
        lexer = PlSqlLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = PlSqlParser(stream)
        tree = parser.sql_script()
        _logger.info("parsing completed")
        if not silent:
            print(tree.toStringTree(recog=parser))
        return tree, parser


if __name__ == "__main__":
    app()
