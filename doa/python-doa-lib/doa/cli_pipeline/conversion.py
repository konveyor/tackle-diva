"Convertion pipeline, that will be called from cli.py."
from functools import partial
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

from .. import console, sprint_
from ..analysis import SCHEMA_INFO_FILE
from ..analysis.from_source import analyze_dir
from ..analysis.split import split_dir
from ..doa import main as convert
from ..verification.semantics import verify_schema
from ..verification.syntax import verify_dir


def _maybe_rule(title: str = None, use_rules: bool = False):
    if use_rules:
        console.rule(title=title)


def run_convert_pipeline(app_name: str, in_dir: Path, out_dir: Path,
                         init_command: str = None,
                         use_rules: bool = False, silent: bool = False, verbose: int = 0):
    "conversion pipeline."
    sprint = partial(sprint_, silent)
    maybe_rule = partial(_maybe_rule, use_rules=use_rules)
    sprint("running conversion pipeline...")
    sprint("")
    with TemporaryDirectory() as tmp_dir1:
        maybe_rule("preprocessing and splitting")
        split_dir(in_dir=in_dir, out_dir=Path(tmp_dir1), preprocess=True,
                  silent=silent, verbose=verbose)
        sprint("")
        maybe_rule("SQL analysis")
        analyze_dir(
            schema_name=app_name, in_dir=Path(tmp_dir1), out_dir=Path(tmp_dir1), preprocess=False,
            silent=silent, verbose=verbose)
        sprint("")
        maybe_rule("SQL conversion")
        convert(app_name=app_name, in_dir=Path(tmp_dir1),
                out_dir=out_dir, stat_dir=None, use_debug_listener=True, preprocess=False)
        sprint("")
        maybe_rule("syntactic verification")
        verify_dir(in_dir=out_dir, out_dir=out_dir,
                   init_command=init_command,
                   silent=silent, verbose=verbose)
        sprint("")
        maybe_rule("semantic verification")
        copyfile(Path(tmp_dir1)/SCHEMA_INFO_FILE, out_dir/SCHEMA_INFO_FILE)
        verify_schema(in_dir=out_dir,  out_dir=out_dir,
                      silent=silent, verbose=verbose)
        sprint("")
