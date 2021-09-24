"""
Implementation of the REST APIs.

Also useful for modular testing.
"""
import json
import logging
from abc import abstractmethod
from contextlib import nullcontext
from glob import glob, iglob
from operator import attrgetter
from pathlib import Path
from subprocess import CompletedProcess, run
from tempfile import TemporaryDirectory, mkdtemp
from typing import Any, Tuple

import docker
from docker.types import LogConfig

from ..postprocess import db_extractor
from ..util import dry_run, get_logger, temp_dir

(debug, info, warning, _, exception) = get_logger(__name__)


class SourceLoader:
    """
    Abstract source code loader.
    """

    @abstractmethod
    def load(self, tempdir: str) -> None:
        """load source code under specified directory."""
        ...


class GitHubLoader(SourceLoader):
    def __init__(self, source: dict) -> None:
        self.repo = source['github_url']

    def load(self, clone_to: str) -> None:
        """loads source under the specified tempdir."""
        debug('executing git clone command...')
        cp: CompletedProcess = run(args=["git", "clone",  # "--depth=1",
                                         self.repo, clone_to], capture_output=True, text=True, check=True)
        assert cp.returncode == 0
        debug(f'return code = {cp.returncode}')
        debug('stdout:')
        debug('--> ' + cp.stdout)
        debug('stderr:')
        debug('==> ' + cp.stderr)
        # debug
        # debug("dump content:")
        # for f in glob(f"{tempdir}/*/*", recursive=True):
        #     debug(f)


def source_loader(source: dict) -> SourceLoader:
    return GitHubLoader(source)


class Analyzer:
    @abstractmethod
    def analyze(self, input, output) -> None:
        pass


class OnDockerAnalyzer(Analyzer):
    def analyze(self, input_dir: str, output_dir: str) -> None:
        """Analyze source code in a Docker container."""
        client = docker.from_env()

        lc = LogConfig(type=LogConfig.types.JSON)
        _image = "diva:latest"
        _name = "diva"
        _command = 'bash -c "java -jar /diva-distribution/bin/diva.jar -s /app && ls -al"'
        _vols = {
            input_dir: {'bind': '/app', 'mode': 'rw'},
            output_dir: {'bind': '/out', 'mode': 'rw'}
        }

        debug(
            f'executing command "{_command}"" on docker container {_image}...')
        debug(f"volumes mounted:")
        debug(_vols)
        info('running container... (takes time)')
        res = client.containers.run(
            image=_image,
            name=_name,
            volumes=_vols,
            working_dir="/out",
            command=_command,
            log_config=lc,
            stdout=True, stderr=True,
            # do not use auto_remove=True, which cannot take container logs out.
            remove=True,
        )
        info('done.')
        debug("--- container output ---")
        debug(res.decode('utf-8'))
        debug("------------------------")
        info(f"analysis results are created at {output_dir}")


def gen_analyzer(spec: Any) -> Analyzer:
    return OnDockerAnalyzer()


def main(body):
    return main_(**body)


def main_(id: str, source: dict, name: str = None, in_dir=None, out_dir=None, **kwargs) -> Tuple[str, str]:
    """
    create new analysis result for speciied app.
    """
    if dry_run():
        warning(
            'dry run flag is true. skips actual business logic and returns dummy response.')
        return None, 204  # 204 = No Content

    info('starting new app analysis...')
    info(f"id = {id}")
    if name:
        info(f"name = {name}")
    info(f"source = {source}")

    loader: SourceLoader = source_loader(source)
    info(f'loader for the given source is created: {loader}')

    analyzer: Analyzer = gen_analyzer(None)
    info(f'analyzer is created: {analyzer}')

    # use the argument or config var for output directory (for persistent)
    out_path = Path(out_dir or temp_dir(), id)
    try:
        out_path.mkdir(exist_ok=False)
    except FileExistsError as e:
        exception(e)
        return f"application {id} already exists. Use PUT method to update the resource.", 409

    analysis_out: str = str(out_path)

    # if in_dir is specified, use the directory. otherwise, use a temp directory generated.
    with TemporaryDirectory() if in_dir is None else nullcontext(None) as d:
        if d:
            debug(f"tempdir {d} created")
        app_root: str = in_dir or str(Path(d, 'repo'))
        # output: str = out_dir or str(Path(d, 'output'))

        info(f'input  dir = {app_root}')
        info(f'output dir = {analysis_out}')

        info(f'loading source to {app_root}...')
        loader.load(app_root)
        info('successfully loaded.')

        info('analyzing...')
        analyzer.analyze(app_root, analysis_out)
        info(f'analysis results are created at {analysis_out}.')

        info('creating database JSON file...')
        db_extractor.main(
            in_file=analysis_out + "/transaction.json",
            app_path="/app",
            out_file=analysis_out + "/database.json"
        )

        info('writing metadata...')
        meta: dict = {"id": id, "name": name,
                      "source": source, "status": "available"}
        with open(out_path / '_meta.json', mode='w') as f:
            json.dump(meta, fp=f)

        debug('listing resulting files:')
        for f in iglob(analysis_out + "/**"):
            debug('  ' + f)

        info(f"app resource created at /apps/{id}")

        # return (app_root, analysis_out)
        return meta, 201, {"location": f"/apps/{id}"}
