from logging import Logger, getLogger
from operator import attrgetter
from typing import Tuple

from environs import Env
from flask import current_app


def get_logger(mod_name: str) -> Tuple[Logger, ...]:
    """
    Returns a tuple of loggers (debug, info, warning, error, exception)
    for the given module name (typically value of the '__name__').

    Args:
        mod_name (str): [description]

    Returns:
        tuple[Logger, ...]: [description]
    """
    return attrgetter('debug', 'info', 'warning', 'error', 'exception')(getLogger(mod_name))


def dry_run(env: Env = None) -> bool:
    "checks if DRY_RUN env. var. is true."
    if env is None:
        env = current_app.config['env']
    return env.bool('DRY_RUN', False)

def persistent(env: Env = None) -> str:
    "returns PERSISTENT mode."
    if env is None:
        env = current_app.config['env']
    return env.str('PERSISTENT', 'database')

def temp_dir(env: Env = None) -> str:
    "returns TEMP_DIR value (temporally directory for persistent)."
    if env is None:
        env = current_app.config['env']
    return env.str('TEMP_DIR')
