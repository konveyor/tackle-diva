"""PDF generator from a dot file."""
from logging import getLogger
from subprocess import CompletedProcess, run

debug = getLogger(__name__).debug


def convert(in_file: str, out_file: str, format='pdf') -> None:
    """converts a dot file into a PDF file."""
    debug('convert:')
    debug(f'  in_file  = {in_file}')
    debug(f'  out_file = {in_file}')
    debug(f'  output format = {format}')

    args = ["dot", f"-T{format}", "-o", out_file, in_file]
    debug(f"args = {args}")

    cp: CompletedProcess = run(
        args=args,
        capture_output=True, text=True, check=True
    )

    assert cp.returncode == 0
    debug(f'return code = {cp.returncode}')
    debug('stdout:')
    debug('--> ' + cp.stdout)
    debug('stderr:')
    debug('==> ' + cp.stderr)
