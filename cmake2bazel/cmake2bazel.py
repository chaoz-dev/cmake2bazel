import argparse
import cmake
import filesystem
import logging
import sys

from dataclasses import dataclass
from pathlib import Path
from typing import List

from bazel import builder

log = logging.getLogger(__name__)


_CLIENT_NAME = "cmake2bazel"


@dataclass
class CMake2BazelArgs:
    path_to_build: Path
    cmake_command: List[str]


def _parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="cmake2bazel", description="")

    parser.add_argument("path_to_src", type=str)
    parser.add_argument("--path-to-build", "-b",
                        type=str, default="build/")
    parser.add_argument("--cmake-command", "-c", nargs="+",
                        type=str, default=["cmake", ".."])
    parser.add_argument("--log-level", "-l", type=str,
                        choices=[k.lower() for k in logging._nameToLevel.keys()], default="info")

    return parser.parse_args()


def _preprocess(args: argparse.Namespace) -> CMake2BazelArgs:
    # Init logging.
    log_level = args.log_level.upper()
    logging.basicConfig(format="[%(asctime)s][%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=log_level)
    log.debug(f"log_level: {log_level}")

    # Init path to src.
    path_to_src = Path(args.path_to_src)
    filesystem.assert_exists(path_to_src)
    path_to_src = path_to_src.resolve()
    log.debug(f"path_to_src: {path_to_src}")

    # Init path to build.
    path_to_build = Path(args.path_to_build)
    path_to_build = (path_to_build if path_to_build.is_absolute()
                     else path_to_src / path_to_build)
    path_to_build.mkdir(parents=True, exist_ok=True)
    filesystem.assert_exists(path_to_build)
    log.debug(f"path_to_build: {path_to_build}")

    # Init cmake command.
    cmake_command = args.cmake_command
    log.debug(f"cmake_command: {cmake_command}")

    return CMake2BazelArgs(path_to_build, cmake_command)


def cmake2bazel(path_to_build: Path, cmake_command: List[str]):
    cmake_file_api = cmake.CMakeFileAPI(
        path_to_build, client=_CLIENT_NAME)
    index = cmake_file_api.run_query(
        cmake_command, cmake.ObjectKind.CODEMODEL_V2)

    bfb = builder.BuildFileBuilder()
    bfb.build(index.codemodel_v2)
    bfb.write(Path(index.codemodel_v2.path_to_source))


def main(args: List[str]):
    args = _parse_args(args)
    args = _preprocess(args)
    cmake2bazel(args.path_to_build, args.cmake_command)


if __name__ == "__main__":
    main(sys.argv)
