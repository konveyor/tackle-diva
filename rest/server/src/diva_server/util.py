from enum import Enum, auto
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


class Persistent(Enum):
    tempdir = auto()  # use temporary directory for storing files
    database = auto()  # use database for storing files # not implemented


class JavaExecution(Enum):
    # use local Java runtime, which will be invoked by subprocess.run() (for production).
    local = auto()
    # use Java runtime in diva docker image (for local development).
    docker = auto()


def dry_run(env: Env = None) -> bool:
    "checks if DRY_RUN env. var. is true."
    if env is None:
        env = current_app.config['env']
    return env.bool('DRY_RUN', False)


def persistent(env: Env = None) -> Persistent:
    "returns PERSISTENT mode."
    if env is None:
        env = current_app.config['env']
    return env.enum('PERSISTENT', Persistent.database.name, type=Persistent, ignore_case=True)


def temp_dir(env: Env = None) -> str:
    "returns TEMP_DIR value (temporally directory for persistent)."
    if env is None:
        env = current_app.config['env']
    return env.str('TEMP_DIR')


def java_exec(env: Env = None) -> JavaExecution:
    "returns JAVA_EXEC mode."
    if env is None:
        env = current_app.config['env']
    return env.enum('JAVA_EXEC', JavaExecution.local.name, type=JavaExecution, ignore_case=True)
