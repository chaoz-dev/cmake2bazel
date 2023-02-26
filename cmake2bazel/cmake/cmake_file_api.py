import filesystem
import logging
import subprocess

from enum import Enum
from pathlib import Path
from typing import List, Optional

from .reply.v1 import ReplyIndex, ObjectKind

log = logging.getLogger(__name__)

_CMAKE_CLIENT = "client-{client}"
_CMAKE_FILE_API_DIR = ".cmake/api/v1"
_CMAKE_INDEX_FILE = "index-*.json"


class _Request(Enum):
    QUERY = "query"
    REPLY = "reply"


class CMakeFileAPI():
    def __init__(self, path_to_build: Path, client: Optional[str] = None):
        self.build_path = filesystem.assert_resolve(path_to_build)

        self.client = _CMAKE_CLIENT.format(client=client) if client else None

    def _query(self, object_kind: ObjectKind):
        query = self._request(_Request.QUERY)
        return (query / self.client / object_kind.value
                if self.client else query / object_kind.value)

    def _request(self, request: _Request) -> Path:
        request = (self.build_path
                   / _CMAKE_FILE_API_DIR
                   / request.value)
        return request

    def query(self, *object_kinds: ObjectKind):
        for object_kind in object_kinds:
            query_path = self._query(object_kind)
            log.info(f"Creating CMake query '{query_path}'.")
            query_path.mkdir(parents=True, exist_ok=True)
            filesystem.assert_exists(query_path)

    def cmake(self, cmake_command: List[str]):
        with filesystem.change_working_directory(self.build_path) as cwd:
            log.info(
                f"Running '{' '.join(cmake_command)}' from '{cwd}'.")
            status = subprocess.run(cmake_command, capture_output=True)
            if status.stdout:
                log.info(f"\n\n{status.stdout.decode()}")
            if status.stderr:
                log.warning(f"\n\n{status.stderr.decode()}")
            status.check_returncode()

    def reply(self) -> ReplyIndex:
        reply_path = self._request(_Request.REPLY)
        log.info(f"Reading CMake reply '{reply_path}'.")
        filesystem.assert_exists(reply_path)

        index_files = filesystem.list_files(reply_path, _CMAKE_INDEX_FILE)
        assert len(index_files) > 0, "No index files found."

        # If there are multiple index files, return the newest one.
        index_files.sort()
        index_file = Path(index_files.pop())

        return ReplyIndex(index_file, self.client)

    def run_query(self, cmake_command: List[str], *object_kinds: ObjectKind) -> ReplyIndex:
        self.query(*object_kinds)
        self.cmake(cmake_command)
        return self.reply()
