"Utilities for the Lark library."
from logging import getLogger
# from os import environ
from pathlib import Path

from lark import Lark, Tree

_logger = getLogger(__name__)
info = _logger.info


def parse(grammar: str = None, grammar_file: str = None, text: str = None, text_file=None,
          ret_tree=False, **kwargs) -> (str | Tree):
    """utility to parse the given string by a parser generated from the given grammar string."""
    # parser ctor
    if grammar_file:
        parser: Lark = Lark.open(
            grammar_filename=grammar_file, rel_to=__file__, **kwargs)
    else:
        parser: Lark = Lark(grammar, **kwargs)

    # prepare input and parse
    if text_file:
        with open(text_file, mode="r", encoding="utf-8") as f:
            tree: Tree = parser.parse(f.read())
    else:
        tree: Tree = parser.parse(text)

    if ret_tree:
        return tree
    return tree.pretty()


def gen_parser(grammar: str = None, grammar_file: str = None, parser_file: Path = None, **kwargs) -> Lark:
    """
    create a parser and returns it.

    if grammar is specified, parser will be created from the string.
    if grammar_file is specified, parser will be reated from the file.
    if parser_file is specified, the created parser will be saved to the file.
    """
    info("constructing parser...")
    if grammar_file:
        parser_: Lark = Lark.open(
            grammar_filename=grammar_file, rel_to=__file__, **kwargs)
    else:
        parser_: Lark = Lark(grammar, **kwargs)
    info("parser created.")
    if kwargs == "lalr" and parser_file:
        info(f"saving parser data to {parser_file}...")
        with open(parser_file, mode="wb") as f:
            parser_.save(f)
        info("saved.")
    return parser_


def plsql_parser(parser: str = None, **kwargs) -> Lark:
    "returns a default PL/SQL grammar"
    info("constructing parser...")
    if parser == 'lalr':
        parser_: Lark = gen_parser(grammar_file="plsql.lark",
                                   start="sql_script", parser=parser,
                                   parser_file=Path("./plsql-parser.pickle"), **kwargs)
    else:
        parser_: Lark = gen_parser(grammar_file="plsql.lark",
                                   start="sql_script", ambiguity="explicit",
                                   parser_file=Path("./plsql-parser.pickle"), **kwargs)
    info("constructed.")
    return parser_


def parse_file(parser: Lark, file: str) -> Tree:
    "parse the given text file using the given parser"
    with open(file, mode="r", encoding="utf-8") as f:
        info(f"parsing file {file}...")
        tree: Tree = parser.parse(f.read())
        info("parsed.")
        return tree
