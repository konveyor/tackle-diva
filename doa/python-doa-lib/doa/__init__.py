"An SQL analyzer (SQl AnaLyzer) for assessment and migration to PostgreSQL."
from importlib.metadata import version
from logging import (CRITICAL, DEBUG, INFO, WARNING, Logger, basicConfig,
                     getLevelName)
from xmlrpc.client import Boolean

from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text

__version__ = version(__name__)
__app_name__ = 'DiVA DOA'
__app_ver__ = f"{__app_name__} v{__version__}"
__app_ver_rich__ = Text().assemble(
    f"{__app_name__} ", (f"v{__version__}", "cyan"))

console = Console()  # console object that is commonly used by modules


def sprint_(silent: Boolean, message: str, **kwargs):
    "print string if not in slient mode"
    if not silent:
        console.print(message, **kwargs)


def reinit_logger(logger: Logger, silent: bool, verbose: int, tool_name: str = None):
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
    sprint_(silent, "")
    if tool_name:
        sprint_(silent, __app_ver_rich__ + ": " + tool_name)
    else:
        sprint_(silent, __app_ver_rich__)
    logger.debug("log level set to %s (%d)", getLevelName(_level), _level)
    # logger.info(f"log level set to {_level}")
    # logger.warning(f"log level set to {_level}")
    # logger.error(f"log level set to {_level}")
    # logger.critical(f"log level set to {_level}")
