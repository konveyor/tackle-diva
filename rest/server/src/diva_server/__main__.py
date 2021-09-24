import logging
from os import environ
from tempfile import TemporaryDirectory

from environs import Env

from . import main_app

with TemporaryDirectory(prefix='db_') as d:
    environ['DRY_RUN'] = 'false'
    environ['PERSISTENT'] = 'tempdir'
    environ['TEMP_DIR'] = d

    # read from .env and normal environment variables
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.INFO)
    app = main_app(env)
    app.run(port=8080)
