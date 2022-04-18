"""
Experiments on parsing PL/SQL files using an ANTLR grammar.
"""
from os import environ
from pathlib import Path

from antlr4 import *
from wasabi import msg

from .antlr_grammar.HelloLexer import HelloLexer
from .antlr_grammar.HelloParser import HelloParser
from .plsql.PlSqlLexer import PlSqlLexer
from .plsql.PlSqlParser import PlSqlParser

PLSQL = True
UPPER = True


class CaseChangingStream():
    """
    stream to convert uppercases,
    from https://github.com/antlr/antlr4/blob/master/doc/case-insensitive-lexing.md
    """

    def __init__(self, stream, upper):
        self._stream = stream
        self._upper = upper

    def __getattr__(self, name):
        return self._stream.__getattribute__(name)

    def LA(self, offset):
        c = self._stream.LA(offset)
        if c <= 0:
            return c
        return ord(chr(c).upper() if self._upper else chr(c).lower())


def main_hello():
    "test using simple grammar. main routine copied from the manual"
    # root = Path(environ["TQ_NET_ROOT"]) / "02.定義/02_DB_UTF/tq01_cre_tab"
    # infile = root / "cer01e800.sql"
    infile = Path('./hello.txt')
    input_stream = FileStream(infile, encoding="utf-8")
    lexer = HelloLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.r()
    print(tree.toStringTree(recog=parser))


def main_plsql():
    "experiment using PL/SQL grammar. main routine copied from the manual"
    infile = Path(".") / "cer01e800-upper.sql"
    input_stream = FileStream(infile, encoding="utf-8")
    # stream = CaseChangingStream(input_stream, upper=True)
    stream = input_stream
    lexer = PlSqlLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = PlSqlParser(stream)
    tree = parser.sql_script()
    msg.good("parsing completed:")
    print(tree.toStringTree(recog=parser))


def main_plsql_orig():
    "experiment using PL/SQL grammar. main routine copied from the manual"
    root = Path(environ["TQ_NET_ROOT"]) / "02.定義/02_DB_UTF/tq01_cre_tab"
    infile = root / "cer01e800.sql"
    input_stream = FileStream(infile, encoding="utf-8")
    stream = input_stream
    lexer = PlSqlLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = PlSqlParser(stream)
    tree = parser.sql_script()
    print(tree.toStringTree(recog=parser))


if __name__ == '__main__':
    if PLSQL:
        if UPPER:
            main_plsql()
        else:
            main_plsql_orig()
    else:
        main_hello()
