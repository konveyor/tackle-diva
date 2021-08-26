# make sure that local server is running
# (to be fixed)
from subprocess import Popen
from time import sleep

import pytest
import requests
from importlib_metadata import version
from requests import Response


def is_json(r: Response) -> bool:
    """returns if contentn type of the response would be JSON or not."""
    return r.headers['content-type'].split(';')[0] == 'application/json'


@pytest.fixture(scope="module")
def server_process() -> Popen:
    """start a server via CLI using subprocess."""
    p = Popen(args=["connexion", "run", "-p", "8080",
                    "--mock=notimplemented", "--strict-validation", "--validate-responses",
                    "--debug", "spec/openapi.yaml"])
    sleep(2)  # wait until server is ready
    yield p
    p.terminate()  # send SIGINT
    p.wait()  # wait termination


def test_server_starts(server_process: Popen):
    """checks if server process is running."""
    assert server_process.poll() is None  # None means "running"


def test_basepath_fails(server_process: Popen):
    """accesing basepath returns 404 (should it return something?)."""
    assert server_process.poll() is None
    r = requests.get('http://localhost:8080/')
    assert r.status_code == requests.codes.not_found


class TestAPI:
    """Test implemented APIs."""

    def test_healthcheck(self, server_process: Popen) -> None:
        """accessing health check API."""
        assert server_process.poll() is None
        r = requests.get('http://localhost:8080/healthz')
        print(r.json())
        assert r.status_code == requests.codes.ok
        assert is_json(r)
        j = r.json()
        assert j == {'status_code': 0,
                     'detail': 'Server is working', 'version': version('diva_server')}


class TestGenerated:
    """Test automatically-generated APIs."""

    def test_swagger_ui(self, server_process: Popen) -> None:
        """accessing `/ui` returns a generated Swagger UI page."""
        assert server_process.poll() is None
        r = requests.get('http://localhost:8080/ui')
        assert r.status_code == requests.codes.ok
        assert r.headers['content-type'].split(';')[0] == 'text/html'

    def test_swagger_json(self, server_process: Popen) -> None:
        """accessing `/openapi.json` returns the OpenAPI JSON spec file."""
        assert server_process.poll() is None
        r = requests.get('http://localhost:8080/openapi.json')
        assert r.status_code == requests.codes.ok
        assert is_json(r)
