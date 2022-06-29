"PL/SQL analyzer and transformer (to be integrated with DiVA-DOA)"
import os
from functools import partial
from glob import iglob
from itertools import zip_longest
from json import dump
from logging import getLogger
from multiprocessing.pool import Pool
from operator import itemgetter
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import indent

from antlr4 import ParseTreeWalker
from more_itertools import ilen
from more_itertools import take as _take
from rich import print as rprint
from typer import Option, Typer

from . import __version__, reinit_logger, sprint_
from .analyzer import MyVisitor, PLSQLAnalyzer
from .parser import main as _parse
from .preprocess import preprocess_file
from .util import timer

msg = getLogger(__name__)
# msg = Printer()
app = Typer()

IGNORE_PHYSPROP = True


def stats(obj: PLSQLAnalyzer):
    "get stats from Listener object."
    if IGNORE_PHYSPROP:
        s = {
            "has_dialect": obj.has_dialect,
            "has_only_safe_dialect":  obj.has_dialect and (
                not obj.has_bitmap and not obj.has_local_index
            ),

            # safe dialects
            "has_solidus": obj.solidus,
            "has_remark": obj.remark,
            "has_alter_table_modify": obj.has_alter_table_modify,
            "has_global_temp_table": obj.has_global_temp_table,
            "has_varchar2": obj.has_varchar2,
            "has_non_std_type": obj.has_non_std_type,
            "has_non_rsvd_keyword": obj.has_non_rsvd_keyword,

            # unsafe dialects
            "has_bitmap": obj.has_bitmap,
            "has_local_index": obj.has_local_index
        }
    else:
        s = {
            "has_dialect": obj.has_dialect,
            "has_only_safe_dialect":  obj.has_dialect and (
                not obj.has_bitmap and not obj.has_physical_properties and not obj.has_local_index
            ),

            # safe dialects
            "has_solidus": obj.solidus,
            "has_remark": obj.remark,
            "has_alter_table_modify": obj.has_alter_table_modify,
            "has_global_temp_table": obj.has_global_temp_table,
            "has_varchar2": obj.has_varchar2,
            "has_non_std_type": obj.has_non_std_type,
            "has_non_rsvd_keyword": obj.has_non_rsvd_keyword,

            # unsafe dialects
            "has_bitmap": obj.has_bitmap,
            "has_physical_properties": obj.has_physical_properties,
            "has_local_index": obj.has_local_index
        }
    return s


def process_file(args):
    """
    Parse the specified file using PL/SQL parser and returns an analysis status.
    """
    ((in_dir, out_dir, use_debug_listener, preprocess), file_path) = args
    msg.info('processing file = %s', file_path)
    msg.debug('  in_dir = %s', in_dir)
    msg.debug('  out_dir = %s (%s)', out_dir, out_dir.resolve())
    msg.info('  file path = %s', in_dir / file_path)
    msg.info('  preprocess = %s', preprocess)

    show_tree = False

    if preprocess:
        with TemporaryDirectory() as tempdir:
            msg.debug(tempdir)
            preprocess_file(in_dir, tempdir, file_path)
            tree, parser = _parse(Path(tempdir, file_path),
                                  silent=True, to_console=True)
    else:
        tree, parser = _parse(in_dir/file_path, silent=True, to_console=True)
    ist = parser.getTokenStream()

    if show_tree:
        msg.debug(tree.toStringTree(recog=parser))
    # msg.debug(tree.getText())

    # tree.start
    # tree.stop
    # (s, e) = tree.getSourceInterval()
    msg.debug(ist.getText(tree.start, tree.stop))

    if use_debug_listener:
        walker = ParseTreeWalker()
        collector = PLSQLAnalyzer(parser, ist, ignore_physprop=IGNORE_PHYSPROP)
        msg.debug("walking parse tree...")
        walker.walk(collector, tree)
        msg.debug("successfully walked.")
    else:
        visitor = MyVisitor(parser, ist, verbose=True)
        msg.debug("visiting parse tree...")
        visitor.visit(tree)
        msg.debug("successfully visited.")

    msg.debug("after conversion:")
    msg.debug(ist.getText(tree.start, tree.stop))

    if use_debug_listener:
        msg.info("analysis result of %s", in_dir / file_path)
        status = stats(collector)
        msg.info(status)

        # if collector.has_dialect:
        #     # msg.warning(
        #     #     "SQL file contains dialect(s) which cannot be converted to an equivalent PSQL file. Conversion skipped.")
        #     return (str(file_path), False, status)
        # else:
        msg.info("writing to file...")
        with open(out_dir/file_path, "w", encoding="utf-8") as f:  # pylint: disable=invalid-name
            f.write(ist.getText(tree.start, tree.stop))
        msg.info("successfully written to %s.", out_dir/file_path)
        return (str(file_path), True, status)
    else:
        return (str(file_path), False, {})


def main(app_name: str, in_dir: Path, out_dir: Path, stat_dir: Path,
         use_debug_listener: bool = False,
         take: int = -1, file: str = None, preprocess=True, silent: bool = False) -> None:
    """
    Convert SQL files.

    It finds and reads SQL files from "in_dir" and convert them if necessary.
    Converted files are saved in "out_dir".
    It also stores a statistics file under "stat_dir".
    This is the main logic called from cli_main().
    """
    with timer() as t:
        sprint = partial(sprint_, silent)

        msg.info('DiVA-DOA: SQL files analyzer v%s', __version__)
        msg.debug('  module name = "%s"', __name__)
        msg.debug('  package name = "%s"', __package__)

        msg.info('setting up...')
        msg.info("  cpu count = %d", os.cpu_count())
        msg.info("    cpu affinity = %s", os.sched_getaffinity(0))
        num_proc = max(len(os.sched_getaffinity(0))-1, 1)
        msg.info("  setting up process pool (size = %s)...", num_proc)
        with Pool(num_proc) as pool:
            msg.info('  application name = "%s"', app_name)
            msg.info('  input dir = %s (%s)', in_dir, in_dir.resolve())
            sprint(
                f'converting SQL files of app "{app_name}" in {in_dir.resolve()}...')
            assert isinstance(out_dir, Path)
            msg.info('  output dir = %s', out_dir)
            if not out_dir.exists():
                msg.info('  create output directory %s', out_dir)
                out_dir.mkdir(parents=True)
            if stat_dir is None:
                stat_dir = out_dir
            if not stat_dir.exists():
                msg.info('  create stat directory %s', stat_dir)
                stat_dir.mkdir(parents=True)
            # out_file: Path = out_dir / 'cm-sqls.yaml'
            # msg.info(f'  output yaml file = {out_file}')

            msg.info('processing SQL file(s)...')
            if file:
                files_ = [file]
            else:
                files_ = iglob('**/*.sql', root_dir=in_dir, recursive=True)
                if take >= 0:
                    files_ = _take(take, files_)
            zipped_ = zip_longest([], files_, fillvalue=(
                in_dir, out_dir, use_debug_listener, preprocess))
            # for i in zipped_:
            #     print(i)
            # for res in pool.imap_unordered(process_file, files_):
            #     msg.info(res)
            # iterable consumed here
            res = list(pool.imap_unordered(process_file, zipped_))
            num_files = len(res)
            msg.debug(res)
            # processed = filter(lambda x: x[1], res)
            # skipped = filterfalse(lambda x: x[1], res)
            if IGNORE_PHYSPROP:
                stats_ = {
                    "num_files": num_files,
                    "has_dialect": ilen(filter(lambda x: x[2]["has_dialect"], res)),
                    "has_only_safe_dialect": ilen(filter(lambda x: x[2]["has_only_safe_dialect"], res)),
                    "has_solidus": ilen(filter(lambda x: x[2]["has_solidus"], res)),
                    "has_remark": ilen(filter(lambda x: x[2]["has_remark"], res)),
                    "has_alter_table_modify": ilen(filter(lambda x: x[2]["has_alter_table_modify"], res)),
                    "has_global_temp_table": ilen(filter(lambda x: x[2]["has_global_temp_table"], res)),
                    "has_bitmap": ilen(filter(lambda x: x[2]["has_bitmap"], res)),
                    "has_varchar2": ilen(filter(lambda x: x[2]["has_varchar2"], res)),
                    "has_local_index": ilen(filter(lambda x: x[2]["has_local_index"], res)),
                    "has_non_std_type": ilen(filter(lambda x: x[2]["has_non_std_type"], res)),
                    "has_non_rsvd_keyword": ilen(filter(lambda x: x[2]["has_non_rsvd_keyword"], res))
                }
            else:
                stats_ = {
                    "num_files": num_files,
                    "has_dialect": ilen(filter(lambda x: x[2]["has_dialect"], res)),
                    "has_only_safe_dialect": ilen(filter(lambda x: x[2]["has_only_safe_dialect"], res)),
                    "has_physical_properties": ilen(filter(lambda x: x[2]["has_physical_properties"], res)),
                    "has_solidus": ilen(filter(lambda x: x[2]["has_solidus"], res)),
                    "has_remark": ilen(filter(lambda x: x[2]["has_remark"], res)),
                    "has_alter_table_modify": ilen(filter(lambda x: x[2]["has_alter_table_modify"], res)),
                    "has_global_temp_table": ilen(filter(lambda x: x[2]["has_global_temp_table"], res)),
                    "has_bitmap": ilen(filter(lambda x: x[2]["has_bitmap"], res)),
                    "has_varchar2": ilen(filter(lambda x: x[2]["has_varchar2"], res)),
                    "has_local_index": ilen(filter(lambda x: x[2]["has_local_index"], res)),
                    "has_non_std_type": ilen(filter(lambda x: x[2]["has_non_std_type"], res)),
                    "has_non_rsvd_keyword": ilen(filter(lambda x: x[2]["has_non_rsvd_keyword"], res))
                }
            stats_["has_not_dialect"] = stats_["num_files"]-stats_["has_dialect"]
            # stats_['unsafe'] = stats_['num_files'] - stats_['safe']

            # msg.info(f"processed {num_files} file(s)")
            # msg.info(f"  can be converted: {stats_['safe']} file(s)")
            # msg.info(f"  cannot be converted: {stats_['unsafe']} file(s)")
            msg.info("stats:")
            msg.info(stats_)

            rprint()
            rprint("Analysis results:")
            rprint()

            rprint(f"Total number of SQL files: {stats_['num_files']}")
            rprint()
            rprint(
                f"Number of SQL files (Oracle dialects): {stats_['has_dialect']} ({stats_['has_dialect']/stats_['num_files']:.1%})")
            rprint(
                f"Number of SQL files (Generic): {stats_['has_not_dialect']} ({stats_['has_not_dialect']/stats_['num_files']:.1%})")

            if stats_['has_dialect'] > 0:
                rprint()
                rprint(
                    f"Number of SQLs automatically translated for Postgres: {stats_['has_only_safe_dialect']} ({stats_['has_only_safe_dialect']/stats_['has_dialect']:.1%})")
                num_manual_fix = stats_['has_dialect'] - \
                    stats_['has_only_safe_dialect']
                rprint(
                    f"Number of SQLs requires manual revisions: {num_manual_fix} ({num_manual_fix/stats_['has_dialect']:.1%})")
                rprint(indent(f"Local Index: {stats_['has_local_index']}", "  "))
                for nam in map(itemgetter(0), filter(
                        lambda x: x[2]["has_local_index"], res)):
                    rprint(indent(nam, "    "))
                rprint(indent(f"Bitmap Index: {stats_['has_bitmap']}", "  "))
                for nam in map(itemgetter(0), filter(
                        lambda x: x[2]["has_bitmap"], res)):
                    rprint(indent(nam, "    "))

            with open(stat_dir/"stats.json", mode="w", encoding="utf-8") as f:
                # some cases, this program cannot write other than out_dir.
                dump(stats_, f, indent=2)
                rprint()
                sprint(
                    f"stats file {(stat_dir/'stats.json').resolve()} has been generated.")
            sprint(f"({t.sec_str()})")
    msg.info("all OK.")


@app.command()
def cli_main(
    # repo_url: str = Argument(...,
    #                          help="repository URL of tatget application."),
    app_name: str = Option(
        ...,
        "--app-name",
        "-n",
        help="target application name."
    ),
    in_dir: Path = Option(
        ...,
        "--in-dir",
        "-i",
        exists=True, file_okay=False, dir_okay=True, readable=True,
        help="input directory where SQL files are searched (recursively)."
    ),
    out_dir: Path = Option(
        "/tmp/out",
        "--out-dir",
        "-o",
        file_okay=False, dir_okay=True,
        help="output directory of generated files."
    ),
    stat_dir: Path = Option(
        None,
        file_okay=False, dir_okay=True,
        help="output directory of statistics."
    ),
    take: int = Option(
        -1,
        help="if specified, it processes only the specified files that are found."
    ),
    file: str = Option(
        None,
        "-f", "--file",
        help="process only the specified file."
    ),
    use_debug_listener: bool = Option(
        True,
        help="use custom listener for debug, instead of visitor"
    ),
    preprocess: bool = Option(
        False,
        help="if true, preprocessing (encoding conversion to UTF-8, and uppercase conversion) will be performed for each file."
    ),
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
        help="show log messages. -v shows INFO level logs, -vv shows DEBUG level",
        count=True
    )
) -> None:
    "Analyzes a specified app and generates ConfigMap manifests for the app."
    reinit_logger(msg, silent=silent, verbose=verbose,
                  tool_name="SQL converter")
    main(app_name=app_name,
         in_dir=in_dir, out_dir=out_dir, stat_dir=stat_dir, take=take, file=file,
         use_debug_listener=use_debug_listener, preprocess=preprocess, silent=silent)


if __name__ == '__main__':
    app()
