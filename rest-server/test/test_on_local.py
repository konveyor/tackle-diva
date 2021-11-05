"""
Tests diva_server app using Flask testing APIs.
All implemenation will be executed, except that Java-related part will be ran on Docker container.
"""
import json
from os import environ
from pathlib import Path
from pprint import pprint
from tempfile import TemporaryDirectory

import pytest
from diva_server import main_app
from diva_server.util import get_logger
from environs import Env
from flask import Flask, url_for
from flask.testing import FlaskClient

_, info, _, _, _ = get_logger(__name__)


@pytest.fixture(scope="function")
def app() -> Flask:
    with TemporaryDirectory(prefix='db_') as d:
        environ['DRY_RUN'] = 'false'
        environ['PERSISTENT'] = 'tempdir'
        environ['TEMP_DIR'] = d
        env = Env()
        env.read_env()
        yield main_app(env=env)


@pytest.fixture()
def apps_json() -> str:
    json_file = Path(__file__).parent / 'fixtures' / 'post_apps.json'
    return open(json_file).read()


def test_get_healthz(app):
    "tests GET /healthz endpoint. this test assumes use of Flask-based app."
    client: FlaskClient = app.app.test_client()

    res = client.get('/healthz')
    assert res.status_code == 200
    assert res.mimetype == 'application/json'
    # TODO: schema checking comes here
    print(res.get_json())


def test_post_apps(app, apps_json: str):
    "tests POST /apps endpoint. this test assumes use of Flask-based app."
    # info(apps_json)
    # assert isinstance(app.app, Flask)

    client: FlaskClient = app.app.test_client()
    res = client.post('/apps', data=apps_json,
                      headers={'content-type': 'application/json'})
    assert res.status_code == 201  # 201 Created
    assert res.location == 'http://localhost/apps/day_trader'
    # 204 response does not return Content-Length field in the header,
    # thus the property value results in None, not 0.
    assert res.content_length > 0

    # print(res.status)
    # print(res.headers)
    # print(res.mimetype)
    # print(res.mimetype_params)
    # print(res.data)
    # print(res.content_length)
    # pprint(res)
    # print(type(res))

    res2 = client.get('/apps/day_trader')
    assert res2.status_code == 200
    print(res2.get_json())

    res3 = client.get('/apps/day_trader/database')
    assert res3.status_code == 200
    print(res3.get_json())

    res4 = client.get('/apps/day_trader/transaction')
    assert res4.status_code == 200
    # print(res4.get_json())


def test_get_app(app):
    client: FlaskClient = app.app.test_client()
    res = client.get('/apps/day_trader')
    assert res.status_code == 404
    print(res.get_json())


def test_get_db(app):
    client: FlaskClient = app.app.test_client()
    res = client.get('/apps/day_trader/database')
    assert res.status_code == 404
    print(res.data)
