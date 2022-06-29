"Perform syntax verification."
from dataclasses import asdict, dataclass, field
from functools import partial
from logging import getLogger
from pathlib import Path

import psycopg2
from psycopg2.extras import NamedTupleCursor
from rich.pretty import pretty_repr
from typer import Option, Typer
from yaml import safe_dump, safe_load

from .. import reinit_logger, sprint_
from ..analysis import SCHEMA_INFO_FILE
from ..data import TableAnalysisResult
from ..util import timer
from . import SEM_VERIFICATION_FILE

app = Typer()
_logger = getLogger(__name__)


# @dataclass
# class TableVerification:
#     """
#     Dataclass to store verification results for a table.
#     """
#     cp: str = None
#     returncode: int = None
#     stdout: str = None
#     stderr: str = None


@dataclass
class SemanticsVerificationResult:
    """
    Dataclass to store results of semantics verification.
    """
    tables: list[TableAnalysisResult] = field(init=False, default_factory=list)


def verify_table(in_dir: Path, table: str, out_dir: Path, connection=None,
                 silent: bool = False, verbose: int = 0) -> TableAnalysisResult:
    """
    Verify a table in a schema.
    """
    sprint = partial(sprint_, silent)  # pylint: disable=unused-variable

    # infile: Path = in_dir/file_name
    _logger.info('analyzing table "%s"...', table)
    info = TableAnalysisResult(table_name=table.upper())

    with connection.cursor(cursor_factory=NamedTupleCursor) as cur:
        _logger.info("scanning columns...")
        cur.execute(
            "select column_name from information_schema.columns where table_schema='public' and table_name=%s", (table,))
        for t in cur:
            _logger.debug(t)
            info.add_column(t.column_name.upper())
            _logger.info('  column "%s" found', t.column_name)
        _logger.info("scanning FK (and corresponding PK) constraints...")
        query2 = """
        select 
            rc.constraint_catalog, 
            rc.constraint_schema, 
            rc.constraint_name,
            cu1.table_name as constraint_table,
            rc.unique_constraint_catalog, 
            rc.unique_constraint_schema, 
            rc.unique_constraint_name,
            cu2.table_name as unique_constraint_table,
            array_agg(cu1.column_name)::varchar[] as constraint_columns, 
            array_agg(cu2.column_name)::varchar[] as unique_constraint_columns 
        from 
            information_schema.table_constraints as tc, 
            information_schema.referential_constraints as rc, 
            information_schema.key_column_usage as cu1, 
            information_schema.key_column_usage as cu2 
        where 
            tc.table_name=%s and 
            tc.constraint_type='FOREIGN KEY' and 
            rc.constraint_name=tc.constraint_name and 
            cu1.constraint_name=rc.constraint_name and 
            cu2.constraint_name=rc.unique_constraint_name and 
            cu1.position_in_unique_constraint=cu2.ordinal_position 
        group by 
            rc.constraint_catalog, 
            rc.constraint_schema, 
            rc.constraint_name,
            rc.unique_constraint_catalog, 
            rc.unique_constraint_schema, 
            rc.unique_constraint_name,
            cu1.table_name, 
            cu2.table_name;
        """
        cur.execute(query2, (table,))
        for t in cur:  # pylint: disable=invalid-name
            _logger.info(' FK constraint "%s" found', t.constraint_name)
            _logger.debug(pretty_repr(t, indent_size=2))
            info.add_FK([s.upper() for s in t.constraint_columns],
                        t.unique_constraint_table.upper(),
                        [s.upper() for s in t.unique_constraint_columns])

    # # deprecated: show table description using psql
    # args = ["psql", "-c", f"\\d {table}"]
    # completed_process: CompletedProcess = run(  # pylint: disable=subprocess-run-check
    #     args=args, text=True, capture_output=True)
    # _logger.debug(completed_process)
    # _logger.info(completed_process.stdout)

    _logger.info("analysys result of table (raw):")
    _logger.info(pretty_repr(asdict(info), indent_size=2))
    return info


def dice(a: set, b: set) -> float:
    return (2 * len(a & b)) / (len(a)+len(b))


def verify_schema(in_dir: Path, out_dir: Path, silent: bool = False, verbose: int = 0):
    "Verify a schema in DB and write results."
    with timer() as tm:
        sprint = partial(sprint_, silent)
        _logger.info("input dir = %s", in_dir.resolve())
        _logger.info("output dir = %s", out_dir.resolve())

        if not out_dir.exists():
            _logger.info("  create output directory %s", out_dir)
            out_dir.mkdir(parents=True)

        # _logger.info("initializing database...")
        # # delete public schema and recreate it.
        # cp = run(args=["psql", "-c", "drop schema public cascade; create schema public;"],
        #          capture_output=True, text=True, check=True)
        # _logger.info(cp)

        sprint("starting semantics verification...")
        info = SemanticsVerificationResult()

        g = partial(verify_table, in_dir=in_dir, out_dir=out_dir,
                    silent=silent, verbose=verbose)

        sprint("looking for and analyzing tables...")

        _logger.info("[experimental] using psycopg2 to fetch tables")
        try:
            _logger.debug("establishing connection...")
            conn = psycopg2.connect()
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(
                    "select table_name, table_type from information_schema.tables "
                    "where table_schema='public'")
                for t in cur:  # pylint: disable=invalid-name
                    _logger.debug(t)
                    if t.table_type != "BASE TABLE":
                        _logger.warning(
                            "table type %s is not supported. skipped.", t.table_type)
                    result: TableAnalysisResult = g(
                        table=t.table_name, connection=conn)
                    info.tables.append(result)
        finally:
            _logger.debug("closing connection...")
            if conn is not None:
                conn.close()

        # cp = run(args=["psql", "-At", "-F", ",", "-c", "\\dt"],
        #          capture_output=True, text=True, check=True)
        # _logger.info(cp)
        # for line in cp.stdout.splitlines():
        #     _logger.info(line.split(","))
        #     g(table=line.split(",")[1])

        # summarize
        # pylint: disable=invalid-name
        with open(in_dir/SCHEMA_INFO_FILE, mode="r", encoding="utf-8") as f:
            schema_info = safe_load(f)
            table_set_a = {table['table_name'] for a_file in schema_info['files']
                           for table in a_file['tables']}
            table_set_b = {table.table_name for table in info.tables}
            _logger.debug(table_set_a)
            _logger.debug(table_set_b)

        sprint("")
        sprint("Analysis results:\n")
        n_FKs = sum([len(table.FKs) for table in info.tables])
        sprint(f"{len(info.tables)} table(s) are found")
        sprint(f"{n_FKs} FK/PK relations are found")
        sprint("")
        sprint(
            f"Table preservation (Dice similarity): {dice(table_set_a,table_set_b):.2%}")
        sprint(f"FK/PK preservation (avg. Dice similarity): {1:.2%}")

        # save
        outfile = out_dir/SEM_VERIFICATION_FILE
        with open(outfile, mode="w", encoding="utf-8") as f:
            _logger.debug("analysis result of database (raw):")
            _logger.debug(pretty_repr(asdict(info), indent_size=2))
            safe_dump(asdict(info), stream=f)
            sprint("")
            sprint(
                f"verification results {outfile.resolve()} has been saved.")
        sprint(f"({tm.sec_str()})")


@app.command()
def cli_main(
    in_dir: Path = Option(None, "-i", "--in-dir",
                          help="directory of the target SQL files."),
    out_dir: Path = Option(None, "-o", "--out-dir",
                           help="directory for the result files. It will be created if not exist."),
    silent: bool = Option(
        False,
        "--silent",
        "-s",
        help="Output nothing to console. This sets log level to CRITICAL."
    ),
    verbose: int = Option(
        0,
        "--verbose",
        "-v",
        help="Control log level. By default greater level than WARNING will be shown."
        "Specifying '-v' shows INFO and higher level logs and '-vv' shows DEBUG and higher ones. "
        "If you specify '-s', log level is set to CRITICAL.",
        count=True
    )
):
    """
    Perform semantics verification.
    """
    reinit_logger(_logger, silent=silent, verbose=verbose,
                  tool_name="Semantics verifier")
    sprint = partial(sprint_, silent)
    verify_schema(in_dir=in_dir, out_dir=out_dir,
                  silent=silent, verbose=verbose)
    sprint("[green][OK] semantics verification completed.[/]")


if __name__ == "__main__":
    app()
