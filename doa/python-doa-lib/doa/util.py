"Utilities."
from contextlib import contextmanager
from functools import partial
from logging import DEBUG, basicConfig, getLogger
from multiprocessing.pool import Pool
from os import cpu_count, sched_getaffinity
from pathlib import Path
from random import random
from time import sleep, time

from antlr4 import CommonTokenStream, FileStream

from . import console
from .plsql.PlSqlLexer import PlSqlLexer
from .plsql.PlSqlParser import PlSqlParser

# app = typer.Typer()
_logger = getLogger(__name__)


def parse(infile: Path, verbose: int = 0, silent: bool = False):
    """
    Parses the given PL/SQL file.

    This function returns the parser and the parsed tree.
    """
    _logger.info("parsing file %s...", infile)
    stream = FileStream(infile, encoding="utf-8")
    lexer = PlSqlLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = PlSqlParser(stream)
    tree = parser.sql_script()
    _logger.info("parsing completed.")
    if _logger.isEnabledFor(DEBUG):
        _logger.debug(tree.toStringTree(recog=parser))
    return tree, parser


@contextmanager
def process_pool():
    "returns an well-tuned process pool using CPU affinity."
    _logger.info("setting up for process pool...")
    _logger.info("  cpu count = %d", cpu_count())
    affinity = sched_getaffinity(0)
    _logger.info("  cpu affinity = %s", affinity)
    num_proc = max(len(affinity)-1, 1)
    with Pool(num_proc) as pool:
        try:
            _logger.info("created a process pool (size = %s)", num_proc)
            yield pool
        finally:
            _logger.info("cleaning up process pool...")


class _MyTimer:
    def __init__(self):
        self.start = time()

    def sec(self):
        "returns timer value in unit of seconds."
        return time() - self.start

    def sec_str(self):
        "returns timer value in unit of seconds."
        delta = time() - self.start
        return f"{delta:.2f}s"


@contextmanager
def timer():
    "timer to measure performance."
    try:
        yield _MyTimer()
    except BaseException:
        raise
    finally:
        pass


if __name__ == "__main__":
    basicConfig(level="INFO")

    # define local function for test
    def inc(x, prefix=None):  # pylint: disable=invalid-name
        "test program for process_pool."
        wait = random()*5
        sleep(wait)
        return f"{prefix} {x + 1} (waited {wait:.2}s)"

    with timer() as t1:
        f = partial(inc, prefix="the answer is")
        with process_pool() as pp:
            with console.status("executing ordered parallel processes...", spinner="line"):
                for ans in pp.imap(f, range(30)):
                    print(ans)
            with console.status("executing unordered parallel processes...", spinner="line"):
                for ans in pp.imap_unordered(f, range(30)):
                    print(ans)
        print(f"in {t1.sec_str()}")
