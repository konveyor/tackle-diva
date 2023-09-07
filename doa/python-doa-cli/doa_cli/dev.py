"""
Sub-commands for developers.
"""
from functools import partial
from logging import (CRITICAL, DEBUG, INFO, WARNING, basicConfig, getLevelName,
                     getLogger)
from pathlib import Path
from subprocess import run, DEVNULL
from typing import List
from pygments import highlight

from rich.logging import RichHandler
from rich.text import Text
from typer import Option, Typer

from . import __app_name__, __app_ver_rich__, console

app = Typer(help="Useful commands for developers.")
logger = getLogger(__name__)


def sprint_(silent, message, **kwargs):
    "print string if not in slient mode"
    if not silent:
        console.print(message, **kwargs)


def reinit_logger(silent: bool, verbose: int):
    "re-initialize the root logger according to CLI options."
    if silent:
        _level = CRITICAL
    else:
        if verbose == 1:
            _level = INFO
        elif verbose >= 2:
            _level = DEBUG
        else:
            _level = WARNING
    # getLogger(None).setLevel(_level)
    basicConfig(level=_level, format="%(message)s",
                datefmt="[%X]", handlers=[RichHandler()], force=True)
    sprint_(silent, __app_ver_rich__)
    logger.debug("log level set to %s (%d)", getLevelName(_level), _level)
    # logger.info(f"log level set to {_level}")
    # logger.warning(f"log level set to {_level}")
    # logger.error(f"log level set to {_level}")
    # logger.critical(f"log level set to {_level}")


def add_sudo(sudo: bool, args: List[str]) -> List[str]:
    "add 'sudo' to an argument list if sudo flag is True."
    if sudo:
        return ["sudo"] + args
    return args


@app.command(help=f"Build a Docker image of {__app_name__}.")
def build(
    no_cache: bool = Option(
        False, "--no-cache", help="Run docker build with the '--no-cache' option."),
    sudo: bool = Option(
        False, "--sudo", help="Prefix 'sudo' to docker commands executed. Use this option when executing docker needs root previlege."),
    ls: bool = Option(
        False, "--ls", help="Show generated images."),
    silent: bool = Option(False, "--silent", "-s",
                          help="Output nothing to console. This sets log level to CRITICAL."),
    verbose: int = Option(
        0,
        "--verbose",
        "-v",
        help="Control log level. By default greater level than WARNING will be shown."
        "Specifying '-v' shows INFO and higher level logs and '-vv' shows DEBUG and higher ones. "
        "If you specify '-s', log level is set to CRITICAL.",
        count=True
    )
):
    """
    Build a Docker image of DOA.
    """
    reinit_logger(silent=silent, verbose=verbose)
    sprint = partial(sprint_, silent)

    IMAGE_NAME = "diva-doa"  # name of the image built
    IMAGE_TAG = "2.3.0"  # tag (= version) of the image built
    # options passed to "docker build" command
    DOCKER_BUILD_OPT = ["--no-cache"] if no_cache else []

    # Path to the Dockerfile used to build
    DOCKER_FILE: Path = Path(".devcontainer/Dockerfile")
    # Path to the directory for docker build context
    DOCKER_CONTEXT: Path = Path("doa")
    # TODO: currently above two variable are relateive to the project root (= tackle-diva/doa directory).

    name_tag: Text = Text.assemble((f"{IMAGE_NAME}:{IMAGE_TAG}", "magenta"))
    sprint(f"building image {IMAGE_NAME}:{IMAGE_TAG}...\n", highlight=False)

    args: List[str] = add_sudo(sudo, ["docker", "build"] + DOCKER_BUILD_OPT +
                               ["-t", f"{IMAGE_NAME}:{IMAGE_TAG}"] +
                               # build arg no longer needed?
                               ["--build-arg", f"IMAGE_VER={IMAGE_TAG}"] +
                               ["--target", "doa"] +
                               ["-f", f"{DOCKER_FILE}"] +
                               [str(DOCKER_CONTEXT)]
                               )
    logger.debug("build argment array: %s", args)
    logger.debug("build comman line: %s", " ".join(args))
    if verbose >= 1:  # -v or -vv
        run(args, check=True)
        sprint("")
    else:
        run(args, stdout=DEVNULL, stderr=DEVNULL, check=True)

    sprint(Text.assemble("docker image ", name_tag, " has been built."))
    sprint(f"docker image [magenta]{IMAGE_NAME}:latest[/] has been built.\n")
    if ls:
        sprint(f"Current {IMAGE_NAME} images:\n")
        run(add_sudo(sudo, ["sudo", "docker",
            "image", "ls", IMAGE_NAME]), check=True)
        sprint("")

    sprint("[green][OK] build completed.[/]")
