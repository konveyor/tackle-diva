"""
Try to parse Oracle SQL files using Lark and sqlite grammar.
"""
from logging import basicConfig
from os import environ
from pathlib import Path

from lark import Lark
from rich import print
from typer import Abort, Typer

from .lark_lib.parser import parse, gen_parser

app = Typer()


@app.command()
def main(mode: int):
    "main routine"
    if mode == 0:
        print("importing grammar and construct a parser...")
        parser_ = Lark.open_from_package(
            "lark_grammars", "sqlite.lark", ["grammars"], start="start")
        root = Path(environ["TQ_NET_ROOT"]) / "02.定義/02_DB_UTF/tq01_cre_tab"
        infile = root / "cer01e800.sql"
        with open(infile, encoding="utf-8") as f:
            print("start parsing...")
            parser_.parse(f.read())
    elif mode == 1:
        print(parse(
            grammar="""
            %import common.WS
            %import common.INT
            %ignore WS

            e : INT
            | e "+" e
            """,
            start="e",
            ambiguity="explicit",
            text="1 + 2 + 3"))
    elif mode == 2:
        print(parse(
            grammar="""
            %import common.WS
            %import common.INT
            %ignore WS

            e : INT
            | e "+" e
            """,
            start="e",
            parser="lalr",
            ambiguity="explicit",
            text="1 + 2 + 3"))
    elif mode == 3:
        print(parse(
            grammar="""
            %import common.WS
            %import common.INT
            %ignore WS

            e : INT
            | e "+" e
            """,
            start="e",
            parser="lalr",
            text="1 + 2 + 3"))
    elif mode == 4:
        tree = parse(
            grammar="""
            %import common.WS
            %import common.INT
            %ignore WS

            e : INT
              | e "+" INT
            """,
            start="e",
            ambiguity="explicit",
            text="1 + 2 + 3",
            ret_tree=True)
        print(tree)
        print(tree.pretty())
    elif mode == 5:
        tree = parse(
            grammar="""
            %import common.WS
            %import common.INT
            %ignore WS

            exp : INT ("+" INT)*
            """,
            start="exp",
            ambiguity="explicit",
            text="1 + 2 + 3",
            ret_tree=True)
        print(tree)
        print(tree.pretty())
    elif mode == 6:
        tree = parse(
            grammar_file="sample_grammar.lark",
            start="exp",
            ambiguity="explicit",
            text="1 + 2 + 3 // sample comment",
            ret_tree=True)
        print(tree)
    elif mode == 7:
        tree = parse(
            grammar_file="sample_grammar.lark",
            start="exp",
            ambiguity="explicit",
            text_file="sample-input.txt",
            ret_tree=True)
        print(tree)
    elif mode == 8:
        print(parse(
            grammar="""
            %import common.WS
            %import common.INT
            %ignore WS

            s   : ITEM | ITEM2
            ITEM: /[a-z0-9]+/i
            ITEM2: /[^a]/+
            """,
            start="s",
            ambiguity="explicit",
            text="0123aBc",
            ret_tree=True))
    elif mode == 9:
        print(parse(
            grammar="""
            %import common.WS
            %import common.INT
            %ignore WS

            s   : ITEM
            ITEM: /[^a]/+
            """,
            start="s",
            ambiguity="explicit",
            text="0123aBc",
            ret_tree=True))
    elif mode == 10:
        tree = parse(
            grammar="""
            %import common.WS
            %import common.INT
            %ignore WS

            exp : \
                term ("+" term)*
            term: \
                atom ("*" atom)*
            atom: \
                INT -> int
                | "(" exp ")" -> compound
            """,
            start="exp",
            ambiguity="explicit",
            text="1 + 2*3 + 4 * (5+6)",
            ret_tree=True)
        print(tree)
    elif mode == 11:
        tree = gen_parser(
            grammar="""
            %import common.WS
            %import common.INT
            %ignore WS

            exp : \
                term ("+" term)*
            term: \
                atom ("*" atom)*
            atom: \
                INT -> int
                | "(" exp ")" -> compound
            """,
            parser_file=Path("./parser.pickle"),
            # parser='lalr', 
            start="exp")
    elif mode == 12:
        tree = gen_parser(
            grammar="""
            %ignore WS
            WS: /[ \\t\\f\\r\\n]/+
            INT: ("0".."9")+

            exp : \
                term ("+" term)*
            term: \
                atom ("*" atom)*
            atom: \
                INT -> int
                | "(" exp ")" -> compound
            """,
            parser_file=Path("./parser.pickle"),
            parser='lalr',
            start="exp")
    else:
        print(f'Error: unknown mode: {mode}')
        raise Abort()


if __name__ == "__main__":
    basicConfig(
        level="DEBUG", format='{asctime} [{levelname:.4}] {name}: {message}', style='{')
    app()
