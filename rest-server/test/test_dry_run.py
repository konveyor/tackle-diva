"""
Does dry-run diva_server app using Flask testing APIs.
All implemenation will be skipped, just tests its sigunature (= I/O schemas).
"""
import json
from os import environ
from pathlib import Path
from pprint import pprint

import pytest
from diva_server import main_app
from diva_server.util import get_logger
from environs import Env
from flask import Flask, url_for
from flask.testing import FlaskClient

_, info, _, _, _ = get_logger(__name__)


@pytest.fixture(autouse=True, scope='module')
def set_dry_run() -> None:
    # setup
    environ['DRY_RUN'] = 'true'
    yield True
    # teardown
    del environ['DRY_RUN']


@pytest.fixture()
def apps_json() -> str:
    json_file = Path(__file__).parent / 'fixtures' / 'post_apps.json'
    return open(json_file).read()


def test_get_healthz():
    "tests GET /healthz endpoint. this test assumes use of Flask-based app."
    env = Env()
    env.read_env()
    print(env.dump())
    print(env.str('GOPATH'))
    app = main_app(env=env)
    assert isinstance(app.app, Flask)

    client: FlaskClient = app.app.test_client()
    assert client
    res = client.get('/healthz')
    print(res.status_code)
    print(res.status)
    print(res.headers)
    print(res.mimetype)
    print(res.mimetype_params)
    print(res.get_json())
    pprint(res)
    print(type(res))


def test_post_apps(apps_json: str):
    "tests POST /apps endpoint. this test assumes use of Flask-based app."
    info(apps_json)
    env = Env()
    env.read_env()
    app = main_app(env=env)
    assert isinstance(app.app, Flask)

    client: FlaskClient = app.app.test_client()
    res = client.post('/apps', data=apps_json,
                      headers={'content-type': 'application/json'})
    assert res.status_code == 204

    # 204 response does not return Content-Length field in the header,
    # thus the property value results in None, not 0.
    assert res.content_length is None

    # print(res.status)
    # print(res.headers)
    # print(res.mimetype)
    # print(res.mimetype_params)
    # print(res.data)
    # # print(res.get_json())
    # print(res.content_length)
    # pprint(res)
    # print(type(res))


def test_get_db():
    "tests GET /apps/{id}/database endpoint. this test assumes use of Flask-based app."
    env = Env()
    env.read_env()
    app = main_app(env=env)
    client: FlaskClient = app.app.test_client()

    res = client.get('/apps/day_trader/database')
    print(res.status_code)
    print(res.status)
    print(res.headers)
    print(res.mimetype)
    print(res.mimetype_params)
    print(res.get_json())
    pprint(res)
    print(type(res))
