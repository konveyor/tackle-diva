"""test for operating docker using docker package."""
from pathlib import Path
from tempfile import mkdtemp

import docker
import pytest
from docker.types import LogConfig


@pytest.fixture
def repo_root() -> str:
    return str(Path(__file__, '../fixtures/sample.daytrader7'))


@pytest.fixture
def tmp_outdir() -> Path:
    d = mkdtemp()
    return Path(d)


def test_run(repo_root: str, tmp_outdir: Path):
    client = docker.from_env()
    lc = LogConfig(type=LogConfig.types.JSON)
    print(repo_root)
    print(tmp_outdir)
    vols = {
        repo_root: {'bind': '/app', 'mode': 'rw'},
        tmp_outdir: {'bind': '/out', 'mode': 'rw'}
    }
    print('running container...')
    res = client.containers.run(
        image="diva:latest",
        name="diva",
        volumes=vols,
        working_dir="/out",
        # command='bash -c "pwd && ls -al"',
        command='bash -c "java -jar /diva-distribution/bin/diva.jar -s /app && ls -al"',
        log_config=lc,
        stdout=True, stderr=True,
        # do not use auto_remove=True, which cannot take container logs out.
        remove=True,
    )
    print('done.')
    print("--- container output ---")
    print(res.decode('utf-8'))
    print("------------------------")
    print(f"results are created at {tmp_outdir}")
    #   command="ls && java -jar ./diva.jar")
