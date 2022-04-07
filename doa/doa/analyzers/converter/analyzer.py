"""
PL/SQL analyzer for transformation
"""
from logging import getLogger
from pathlib import Path

from antlr4.tree.Tree import ParseTree
from more_itertools import ilen
from typer import Argument, Option, Typer
from wasabi import msg

from .parser import main as _parse
from .plsql.PlSqlLexer import PlSqlLexer
from .plsql.PlSqlParser import *
from .plsql.PlSqlParserListener import PlSqlParserListener
from .plsql.PlSqlParserVisitor import PlSqlParserVisitor

app = Typer()
_logger = getLogger(__name__)


class DebugListener(PlSqlParserListener):
    "Listener class useful for debugging."

    def __init__(self, parser, input_stream, ignore_physprop=True, verbose=False):
        super()
        self.ignore_physprop = ignore_physprop

        self.parser = parser
        self.verbose = verbose
        self.token_stream = input_stream
        self.has_physical_properties = False
        self.has_dialect = False
        self.solidus = False
        self.remark = False
        self.has_alter_table_modify = False
        self.has_global_temp_table = False
        self.has_bitmap = False
        self.has_varchar2 = False
        self.has_local_index = False

    def show(self, rule, ctx):
        "utility: dump context info for rules."
        _logger.debug('"' + rule + '"')
        _logger.debug(f"tree: {ctx.toStringTree(recog=self.parser)}")

    # Exit a parse tree produced by PlSqlParser#sql_script.
    def exitSql_script(self, ctx: PlSqlParser.Sql_scriptContext):
        self.show("sql_script", ctx)
        x = self.token_stream.getTokens(
            ctx.start.tokenIndex, ctx.stop.tokenIndex+1, [PlSqlLexer.SOLIDUS])
        if ilen(x) > 0:
            self.has_dialect = True
            self.solidus = True
        y = self.token_stream.getTokens(
            0, 10000000, [PlSqlLexer.REMARK_COMMENT])
        if ilen(y) > 0:
            self.has_dialect = True
            self.remark = True
        z = self.token_stream.getTokens(
            0, 10000000, [PlSqlLexer.BITMAP])
        if ilen(z) > 0:
            self.has_dialect = True
            self.has_bitmap = True
        zz = self.token_stream.getTokens(
            0, 10000000, [PlSqlLexer.VARCHAR2])
        if ilen(zz) > 0:
            self.has_dialect = True
            self.has_varchar2 = True
        # _logger.debug(list(map(str, x)))

    # Exit a parse tree produced by PlSqlParser#unit_statement.
    def exitUnit_statement(self, ctx: PlSqlParser.Unit_statementContext):
        self.show("unit_statement", ctx)

    # Exit a parse tree produced by PlSqlParser#sql_plus_command.
    def exitSql_plus_command(self, ctx: PlSqlParser.Sql_plus_commandContext):
        self.show("sql_plus_command", ctx)

    # Exit a parse tree produced by PlSqlParser#physical_properties.
    def exitPhysical_properties(self, ctx: PlSqlParser.Physical_propertiesContext):
        self.show("physical_properties", ctx)
        if not self.ignore_physprop:
            self.has_physical_properties = True
            self.has_dialect = True

    # Exit a parse tree produced by PlSqlParser#create_table.
    def exitCreate_table(self, ctx: PlSqlParser.Create_tableContext):
        self.show("create_table", ctx)
        if ctx.GLOBAL():
            self.has_dialect = True
            self.has_global_temp_table = True

    # Exit a parse tree produced by PlSqlParser#alter_table.
    def exitAlter_table(self, ctx: PlSqlParser.Alter_tableContext):
        self.show("alter_table", ctx)
        x = self.token_stream.getTokens(
            ctx.start.tokenIndex, ctx.stop.tokenIndex+1, [PlSqlLexer.MODIFY])
        if ilen(x) > 0:
            self.has_dialect = True
            self.has_alter_table_modify = True

    # Enter a parse tree produced by PlSqlParser#create_index.
    def enterCreate_index(self, ctx: PlSqlParser.Create_indexContext):
        self.show("alter_table", ctx)
        x = self.token_stream.getTokens(
            ctx.start.tokenIndex, ctx.stop.tokenIndex+1, [PlSqlLexer.LOCAL])
        if ilen(x) > 0:
            self.has_dialect = True
            self.has_local_index = True


class MyVisitor(PlSqlParserVisitor):
    "sample visitor"

    def __init__(self, parser, input_stream, verbose=False):
        super()
        self.parser = parser
        self.verbose = verbose
        self.token_stream = input_stream

    def show(self, rule, ctx):
        "dump context info for rules."
        msg.info(f"{rule} ({ctx.getRuleIndex()})")
        if self.verbose:
            print(f"ctx.getText: {ctx.getText()}")
            print(f"start: {ctx.start}")
            print(f"stop: {ctx.stop}")
            print(f"interval: {ctx.getSourceInterval()}")
            (start, stop) = ctx.getSourceInterval()
            print("tokens (hidden left):")
            for token in (self.token_stream.getHiddenTokensToLeft(start) or []):
                print(f"  {token}")
            print("tokens:")
            for token in self.token_stream.getTokens(start, stop+1):
                print(f"  {token}")
            print("tokens (hidden right):")
            for token in (self.token_stream.getHiddenTokensToRight(stop) or []):
                print(f"  {token}")
            print(f"tree: {ctx.toStringTree(recog=self.parser)}")
        print(f"text: [[{self.token_stream.getText(ctx.start, ctx.stop)}]]")

    def visitUnit_statement(self, ctx: PlSqlParser.Unit_statementContext):
        "Visit a parse tree produced by PlSqlParser#unit_statement."
        tmp = self.visitChildren(ctx)
        self.show("unit_statement", ctx)
        return tmp

    def visitSql_plus_command(self, ctx: PlSqlParser.Sql_plus_commandContext):
        "Visit a parse tree produced by PlSqlParser#sql_plus_command."
        self.show("sql_plus_command", ctx)
        return self.visitChildren(ctx)

    def visitPhysical_properties(self, ctx: PlSqlParser.Physical_propertiesContext):
        "Visit a parse tree produced by PlSqlParser#physical_properties."
        self.show("physical_properties", ctx)
        # msg.info("deleting subtree tokens...")
        # del self.token_stream.tokens[ctx.start.tokenIndex:ctx.stop.tokenIndex+1]
        msg.info("replacing tokens under subtree with WS...")
        for token in self.token_stream.getTokens(ctx.start.tokenIndex, ctx.stop.tokenIndex+1):
            token.text = ""
        # return self.visitChildren(ctx)


@app.command()
def main(
    infile: Path = Argument(..., exists=True, readable=True,
                            help="An input PL/SQL file to be parsed."),
    silent: bool = Option(
        False, "--silent", "-s", help="setting to true supresses output of parsed tree."),
    verbose: bool = Option(False, "--verbose", "-v",
                           help="show debug info of RuleContexts."),
    to_console: bool =
        Option(False, "--err-console/--err-file", "-c/-f",
               help="by default, stderr is directed to a file. Setting true to make it display on console.")
):
    "Parses the given PL/SQL file."
    tree, parser = _parse(infile, silent, to_console)
    ist = parser.getTokenStream()
    visitor = MyVisitor(parser, ist, verbose)
    msg.info("visiting parse tree...")
    visitor.visit(tree)
    msg.good("successfully visited.")


if __name__ == "__main__":
    app()
