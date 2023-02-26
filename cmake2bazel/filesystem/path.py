import glob
import logging
import os

from contextlib import contextmanager
from pathlib import Path
from typing import List

log = logging.getLogger(__name__)


def assert_exists(path: Path):
    assert path.exists(), f"Cannot access '{path}': No such file or directory."


def assert_resolve(path: Path) -> Path:
    path = path.resolve()
    assert_exists(path)
    return path


@contextmanager
def change_working_directory(path: Path) -> Path:
    assert_exists(path)

    cwd = os.getcwd()
    log.debug(f"cwd={cwd}")

    log.debug(f"cd {path}")
    os.chdir(path)

    try:
        yield Path(os.getcwd())
    finally:
        log.debug(f"cd {cwd}")
        os.chdir(cwd)


def list_files(path: Path, pattern: str = "*") -> List[str]:
    assert_exists(path)
    return glob.glob(str(path / pattern))
