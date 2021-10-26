# Python 3.7 does not have importlib.metadata, so need to install importlib_metadata
import logging
from operator import attrgetter

from environs import Env
from flask import current_app
from importlib_metadata import version

from ..util import dry_run

(debug, info, warning) = attrgetter(
    'debug', 'info', 'warning')(logging.getLogger(__name__))


def main(config_=None):
    """
    returns health-check result.
    """
    if dry_run():
        warning(
            'dry run flag is true. skips actual business logic and returns dummy response.')
        return {
            "status_code": 0,
            "detail": "Server is working",
            "version": "0.0.0",
        }

    # normal operation
    return {
        "status_code": 0,
        "detail": "Server is working",
        "version": version('diva_server'),
    }
