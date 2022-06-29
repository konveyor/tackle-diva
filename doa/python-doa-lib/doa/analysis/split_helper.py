"Split helper."
from dataclasses import asdict, dataclass, field
from logging import getLogger
from pathlib import Path
from typing import Any

from antlr4 import ParserRuleContext

from ..plsql.PlSqlParser import *
from ..plsql.PlSqlParserListener import PlSqlParserListener

_logger = getLogger(__name__)


class SplitHelper(PlSqlParserListener):
    "Listener class that extract statements and split."

    def __init__(self, parser, input_stream):
        self.parser = parser
        self.input_stream = input_stream
        self.statements = []
        self.show_tree = True

    def show(self, ctx: ParserRuleContext, show_tree=True):
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

    def text(self, ctx):
        "get text of a context including tokens in other channels"
        return self.input_stream.getText(ctx.start, ctx.stop)

    def exitUnit_statement(self, ctx: PlSqlParser.Unit_statementContext):
        self.show(ctx)
        self.statements.append(ctx)

    def len_statements(self):
        return len(self.statements)

    def statements_text(self):
        return map(self.text, self.statements)
