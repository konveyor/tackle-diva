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


class PLSQLAnalyzer(PlSqlParserListener):
    "Listener class useful for debugging."

    def __init__(self, parser, input_stream, remove_physprop=True, ignore_physprop=True, verbose=False):
        super()
        self.remove_physprop = remove_physprop
        self.ignore_physprop = ignore_physprop

        self.parser = parser
        self.verbose = verbose
        self.token_stream = input_stream
        self.has_physical_properties = False
        self.has_dialect = False
        self.solidus = False
        self.remark = False
        self.has_alter_table_modify = False
        self.has_alter_table_add = False
        self.has_global_temp_table = False
        self.has_bitmap = False
        self.has_varchar2 = False
        self.has_local_index = False
        self.has_non_std_type = False
        self.has_non_rsvd_keyword = False

        # used to keep state during traversal
        self.modifiers = None
        self.additions = None

    def show(self, rule, ctx, show_tree=True):
        "utility: dump context info for rules."
        _logger.debug('"' + rule + '"')
        if show_tree:
            _logger.debug(f"tree: {ctx.toStringTree(recog=self.parser)}")

    def text(self, ctx):
        "get text of a context including tokens in other channels"
        return self.token_stream.getText(ctx.start, ctx.stop)

    # Exit a parse tree produced by PlSqlParser#sql_script.
    def exitSql_script(self, ctx: PlSqlParser.Sql_scriptContext):
        self.show("sql_script", ctx, show_tree=False)
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
        self.show("unit_statement", ctx, show_tree=False)

    # Exit a parse tree produced by PlSqlParser#sql_plus_command.
    def exitSql_plus_command(self, ctx: PlSqlParser.Sql_plus_commandContext):
        self.show("sql_plus_command", ctx)
        if (x := ctx.SOLIDUS()):
            _logger.warning("removing redundant '/'...")
            x.getSymbol().text = ""

    # Exit a parse tree produced by PlSqlParser#physical_properties.
    def exitPhysical_properties(self, ctx: PlSqlParser.Physical_propertiesContext):
        self.show("physical_properties", ctx)
        if not self.ignore_physprop:
            self.has_physical_properties = True
            self.has_dialect = True
        if self.remove_physprop:
            _logger.warning("removing physical_properties...")
            for token in self.token_stream.getTokens(ctx.start.tokenIndex, ctx.stop.tokenIndex+1):
                token.text = ""

    # Exit a parse tree produced by PlSqlParser#native_datatype_element.
    def exitNative_datatype_element(self, ctx: PlSqlParser.Native_datatype_elementContext):
        self.show("native_datatype_element", ctx)
        if (x := ctx.NUMBER()):
            self.has_dialect = True
            self.has_non_std_type = True
            _logger.warning("replacing 'NUMBER' with 'DECIMAL'...")
            x.getSymbol().text = "DECIMAL"
        elif (x := ctx.VARCHAR2()):
            self.has_dialect = True
            self.has_non_std_type = True
            _logger.warning("replacing 'VARCHAR2' with 'VARCHAR'...")
            x.getSymbol().text = "VARCHAR"
        elif (x := ctx.BLOB()):
            self.has_dialect = True
            self.has_non_std_type = True
            _logger.warning("replacing 'BLOB' with 'BYTEA'...")
            x.getSymbol().text = "BYTEA"

    # Exit a parse tree produced by PlSqlParser#non_reserved_keywords_pre12c.
    def exitNon_reserved_keywords_pre12c(self, ctx: PlSqlParser.Non_reserved_keywords_pre12cContext):
        self.show("non_reserved_keywords_pre12c", ctx)
        if ctx.LIMIT():
            self.has_dialect = True
            self.has_non_rsvd_keyword = True
            _logger.warning("quote keyword LIMIT...")
            ctx.LIMIT().getSymbol().text = '"LIMIT"'

    # Exit a parse tree produced by PlSqlParser#column_name.
    def exitColumn_name(self, ctx: PlSqlParser.Column_nameContext):
        self.show("column_name", ctx)

    # Exit a parse tree produced by PlSqlParser#column_definition.
    def exitColumn_definition(self, ctx: PlSqlParser.Column_definitionContext):
        self.show("column_definition", ctx)

        # for alter table add
        if self.additions is not None:
            self.additions.append(
                (self.text(ctx.column_name()), self.text(ctx.datatype()))
            )


    # Exit a parse tree produced by PlSqlParser#lob_storage_clause.
    def exitLob_storage_clause(self, ctx: PlSqlParser.Lob_storage_clauseContext):
        self.show("lob_storage_clause", ctx)
        if self.remove_physprop:
            _logger.warning("removing lob_storage_clause...")
            for token in self.token_stream.getTokens(ctx.start.tokenIndex, ctx.stop.tokenIndex+1):
                token.text = ""

    # Exit a parse tree produced by PlSqlParser#create_table.
    def exitCreate_table(self, ctx: PlSqlParser.Create_tableContext):
        self.show("create_table", ctx)
        if ctx.GLOBAL():
            self.has_dialect = True
            self.has_global_temp_table = True
        if (x := ctx.SOLIDUS()):
            _logger.warning("replacing '/' with ';'...")
            x.getSymbol().text = ";"

    # Enter a parse tree produced by PlSqlParser#using_index_clause.
    # def enterUsing_index_clause(self, ctx: PlSqlParser.Using_index_clauseContext):
    #     self.show("[enter] using_index_clause", ctx)
    #     _logger.debug(ctx.index_properties())
    #     _logger.debug(ctx.create_index())
    #     _logger.debug(ctx.index_name())

    # Exit a parse tree produced by PlSqlParser#using_index_clause.
    def exitUsing_index_clause(self, ctx: PlSqlParser.Using_index_clauseContext):
        self.show("using_index_clause", ctx)
        if ctx.index_properties() and self.remove_physprop:
            _logger.warning("removing using_index...")
            for token in self.token_stream.getTokens(ctx.start.tokenIndex, ctx.stop.tokenIndex+1):
                token.text = ""

    # # Enter a parse tree produced by PlSqlParser#modify_column_clauses.
    # def enterModify_column_clauses(self, ctx: PlSqlParser.Modify_column_clausesContext):
    #     self.show("[E] modify_column_clauses", ctx, show_tree=False)

    # Exit a parse tree produced by PlSqlParser#modify_col_properties.
    def exitModify_col_properties(self, ctx: PlSqlParser.Modify_col_propertiesContext):
        self.show("modify_col_properties", ctx)
        # _logger.debug(ctx.column_name().getText())
        # _logger.debug(ctx.datatype().getText())
        # _logger.debug(self.text(ctx))
        self.modifiers.append(
            (self.text(ctx.column_name()), self.text(ctx.datatype()))
        )
    # Exit a parse tree produced by PlSqlParser#modify_column_clauses.

    def exitModify_column_clauses(self, ctx: PlSqlParser.Modify_column_clausesContext):
        self.show("modify_column_clauses", ctx)
        self.has_dialect = True
        self.has_alter_table_modify = True
        # _logger.debug(self.modifiers)

    # Exit a parse tree produced by PlSqlParser#add_column_clause.
    def exitAdd_column_clause(self, ctx: PlSqlParser.Add_column_clauseContext):
        self.show("add_column_clause", ctx)
        self.has_dialect = True
        self.has_alter_table_add = True

    # Enter a parse tree produced by PlSqlParser#alter_table.
    def enterAlter_table(self, ctx: PlSqlParser.Alter_tableContext):
        self.show("[E] alter_table", ctx)
        self.modifiers = []
        self.additions = []

    # Exit a parse tree produced by PlSqlParser#alter_table.
    def exitAlter_table(self, ctx: PlSqlParser.Alter_tableContext):
        self.show("alter_table", ctx)
        # x = self.token_stream.getTokens(
        #     ctx.start.tokenIndex, ctx.stop.tokenIndex+1, [PlSqlLexer.MODIFY])
        # if ilen(x) > 0:
        #     self.has_dialect = True
        #     self.has_alter_table_modify = True
        if self.modifiers:
            _logger.warning("rewriting ALTER TABLE MODIFY statement...")
            # _logger.debug("modifiers: %s", self.modifiers)
            # _logger.debug(self.text(ctx.tableview_name()))
            t = ", ".join(f"ALTER COLUMN {col} TYPE {typ}" for (
                col, typ) in self.modifiers)
            replacement = f"ALTER TABLE {self.text(ctx.tableview_name())} {t};"
            _logger.debug(replacement)

            for token in self.token_stream.getTokens(ctx.start.tokenIndex, ctx.stop.tokenIndex+1):
                if token.tokenIndex == ctx.start.tokenIndex:
                    token.text = replacement
                else:
                    token.text = ""
        elif self.additions:
            _logger.warning("rewriting ALTER TABLE ADD statement...")
            # _logger.warning("(not implemented yet)")
            t = ", ".join(f"ADD COLUMN {col} {typ}" for (
                col, typ) in self.additions)
            replacement = f"ALTER TABLE {self.text(ctx.tableview_name())} {t};"
            _logger.debug(replacement)

            for token in self.token_stream.getTokens(ctx.start.tokenIndex, ctx.stop.tokenIndex+1):
                if token.tokenIndex == ctx.start.tokenIndex:
                    token.text = replacement
                else:
                    token.text = ""
        elif (x := ctx.SOLIDUS()):
            _logger.warning("replacing '/' with ';'...")
            x.getSymbol().text = ";"

    # Exit a parse tree produced by PlSqlParser#physical_attributes_clause.
    def exitPhysical_attributes_clause(self, ctx: PlSqlParser.Physical_attributes_clauseContext):
        self.show("physical_attributes_clause", ctx)

    # Exit a parse tree produced by PlSqlParser#index_attributes.
    def exitIndex_attributes(self, ctx: PlSqlParser.Index_attributesContext):
        self.show("index_attributes", ctx)

    # Exit a parse tree produced by PlSqlParser#index_properties.
    def exitIndex_properties(self, ctx: PlSqlParser.Index_propertiesContext):
        self.show("index_properties", ctx)
        if self.remove_physprop:
            _logger.warning("removing index_properties...")
            for token in self.token_stream.getTokens(ctx.start.tokenIndex, ctx.stop.tokenIndex+1):
                token.text = ""

    # Exit a parse tree produced by PlSqlParser#create_index.
    def exitCreate_index(self, ctx: PlSqlParser.Create_indexContext):
        self.show("create_index", ctx)
        x = self.token_stream.getTokens(
            ctx.start.tokenIndex, ctx.stop.tokenIndex+1, [PlSqlLexer.LOCAL])
        if ilen(x) > 0:
            self.has_dialect = True
            self.has_local_index = True
        if (x := ctx.SOLIDUS()):
            _logger.warning("replacing '/' with ';'...")
            x.getSymbol().text = ";"


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
