"Schema analyzer(s)."
from dataclasses import dataclass, field
from logging import getLogger

from antlr4 import ParserRuleContext

from ..data import TableAnalysisResult
from ..plsql.PlSqlParser import *
from ..plsql.PlSqlParserListener import PlSqlParserListener

_logger = getLogger(__name__)


@dataclass
class AnalysisResult:
    """
    FK analysis results for a SQL file.

    It may contain multiple SQL statements.
    """
    sub_path: str
    tables: list[TableAnalysisResult] = field(init=False, default_factory=list)

    # def exitCreate_table(self):
    #     # entry = self.table.exit()
    #     # self.tables.append(entry)
    #     entry = self.table.exit()
    #     self.tables.append(asdict(self.table))
    #     del self.table


class FKAnalyzer(PlSqlParserListener):
    "Listener class that analyze FK relations."

    def __init__(self, parser, input_stream, arg_ctor: dict):
        self.parser = parser
        self.input_stream = input_stream

        self.result: AnalysisResult = AnalysisResult(**arg_ctor)
        self.table: TableAnalysisResult = None  # intermediate result

        self.show_tree = True

    def show(self, ctx: ParserRuleContext, show_tree=True) -> None:
        """
        utility: dump context info for the given rule.

        It shows S-exp style of parsed tree for the context.
        """
        # is there a method to show string rule name (not number)?
        rule_index = ctx.getRuleIndex()
        _logger.debug('Rule "%s" (%d)',
                      self.parser.ruleNames[rule_index], rule_index)
        if show_tree:
            _logger.debug("tree: %s", ctx.toStringTree(recog=self.parser))

    def text(self, ctx) -> str:
        "get text of a context including tokens in other channels"
        return self.input_stream.getText(ctx.start, ctx.stop)

    # Enter a parse tree produced by PlSqlParser#unit_statement.
    def enterUnit_statement(self, ctx: PlSqlParser.Unit_statementContext):
        self.show_tree = True

    # Exit a parse tree produced by PlSqlParser#unit_statement.
    def exitUnit_statement(self, ctx: PlSqlParser.Unit_statementContext):
        self.show(ctx, show_tree=self.show_tree)

    # Enter a parse tree produced by PlSqlParser#create_table.
    def enterCreate_table(self, ctx: PlSqlParser.Create_tableContext):
        table_name = self.text(ctx.tableview_name())
        self.table = TableAnalysisResult(table_name)

    # Exit a parse tree produced by PlSqlParser#create_table.
    def exitCreate_table(self, ctx: PlSqlParser.Create_tableContext):
        self.show(ctx)
        self.show_tree = False  # do not show tree in exitUnit_statement
        table_name = self.text(ctx.tableview_name())
        _logger.info('table: name = "%s"', table_name)
        self.result.tables.append(self.table)

    # Enter a parse tree produced by PlSqlParser#column_definition.
    def enterColumn_definition(self, ctx: PlSqlParser.Column_definitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_definition.
    def exitColumn_definition(self, ctx: PlSqlParser.Column_definitionContext):
        self.show(ctx)
        if not self.table:
            _logger.debug("this is not a column_definition in create_statement. skipped.")
        else:
            column_name = self.text(ctx.column_name())
            _logger.info("  column: name = %s", column_name)
            self.table.add_column(column_name)

    # Enter a parse tree produced by PlSqlParser#out_of_line_constraint.
    def enterOut_of_line_constraint(self, ctx: PlSqlParser.Out_of_line_constraintContext):
        pass

    def _parse_paren_col_list(self, ctx: PlSqlParser.Paren_column_listContext) -> list[str]:
        # returns a list of column names
        return [self.text(ctx_cols) for ctx_cols in ctx.column_list().column_name()]

    # Exit a parse tree produced by PlSqlParser#out_of_line_constraint.
    def exitOut_of_line_constraint(self, ctx: PlSqlParser.Out_of_line_constraintContext):
        self.show(ctx)
        if ctx.foreign_key_clause():
            _logger.info('  [red]FK constraint:[/] name = "%s"',
                         self.text(ctx.constraint_name()), extra={"markup": True})
            # _logger.debug(ctx.getText()) # no WS between tokens
            _logger.info("    %s", self.text(ctx), extra={"highlight": False})
            ctx_fk: PlSqlParser.Foreign_key_clauseContext = ctx.foreign_key_clause()
            assert ctx_fk
            ctx_cols = ctx_fk.paren_column_list()
            ctx_refs: PlSqlParser.References_clauseContext = ctx_fk.references_clause()
            assert ctx_cols
            assert ctx_refs
            # _logger.info(self.text(ctx_cols))
            # _logger.info(self.text(ctx_refs))
            col_names = self._parse_paren_col_list(ctx_cols)
            ref_table = self.text(ctx_refs.tableview_name())
            ref_col_names = self._parse_paren_col_list(
                ctx_refs.paren_column_list())
            _logger.info("    columns = %s", col_names)
            _logger.info("    refernced table = %s", ref_table)
            _logger.info("    referenced columns = %s", ref_col_names)
            assert len(col_names) == len(ref_col_names)
            self.table.add_FK(col_names, ref_table, ref_col_names)
        elif ctx.PRIMARY():
            _logger.debug('  PK constraint: name = "%s"',
                          self.text(ctx.constraint_name()))
            _logger.debug(self.text(ctx))
        else:
            _logger.debug("  unsupported constraint. skipped.")
