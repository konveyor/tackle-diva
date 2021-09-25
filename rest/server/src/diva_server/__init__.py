"""
Entry point of diva_server.

Each API endpoint is automatically dispatched to methods below by connexion.
For the implementation of each endpoint, see modules under 'business_logic' package.
"""
import logging
from enum import Enum, auto
from operator import attrgetter
from pathlib import Path
from typing import Callable

import connexion
from environs import Env

from .business_logic import app_analysis as analysis_
from .business_logic import get_app as get_app_
from .business_logic import health_check as health_check_
from .util import JavaExecution, Persistent

(debug, info) = attrgetter('debug', 'info')(logging.getLogger(__name__))


def spec_dir() -> str:
    "construct full path of specification directory"
    return str(Path(__file__).parent / 'spec')
    # return str(Path(__file__).parent.parent.parent / 'spec')


def main_app(env: Env):
    "creates main app. (by default Flask-based)"
    app: connexion.AbstractApp = connexion.App(
        __name__, specification_dir=spec_dir(), debug=True)
    app.add_api('openapi.yaml', resolver_error=501,
                strict_validation=True, validate_responses=True)
    app.app.config['env'] = env  # store Env object to Flash app

    persis = env.enum("PERSISTENT", Persistent.database.name,
                      type=Persistent, ignore_case=True)
    javaexec = env.enum("JAVA_EXEC", JavaExecution.local.name,
                        type=JavaExecution, ignore_case=True)
    info('application config:')
    info(f'  DRY_RUN = {env.bool("DRY_RUN", False)}')
    info(f'  PERSISTENT = {persis}')
    info(f'  TEMP_DIR = {env.str("TEMP_DIR", None)}')
    info(f'  JAVA_EXEC = {javaexec}')
    return app


# defines API endpoints
health_check: Callable = health_check_.main
new_app: Callable = analysis_.main
get_app: Callable = get_app_.main
get_database: Callable = get_app_.get_db
get_transaction: Callable = get_app_.get_tx

# def health_check():
#     """
#     API for GET /healthz.
#     """
#     return health_check_.main()

# def new_app(body):
#     """API for POST /apps."""
#     # info('starting new app analysis...')
#     # info(f"id = {body['id']}")
#     # if 'name' in body:
#     #     info(f"name = {body['name']}")
#     # info(f"source = {body['source']}")
#     return analysis_.main(**body)


__all__ = ['main_app', 'spec_dir']

if __name__ == '__main__':
    # read from .env and normal environment variables
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.INFO)
    app = main_app(env)
    app.run(port=8080)
