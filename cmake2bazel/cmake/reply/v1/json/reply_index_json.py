from dataclasses import dataclass
from filesystem import JsonObject
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, Optional


@dataclass
class VersionJson():
    major: int
    minor: int

    def __init__(self, json: SimpleNamespace):
        self.major = json.major
        self.minor = json.minor


@dataclass
class ReplyJson():
    json_file: str
    kind: str
    version: VersionJson

    def __init__(self, json: SimpleNamespace):
        self.json_file = json.jsonFile
        self.kind = json.kind
        self.version = VersionJson(json.version)


class ReplyIndexJson(JsonObject):
    def __init__(self, filepath: Path, client: Optional[str] = None):
        super().__init__(filepath)

        self._client = client
        self._reply = None

    @property
    def reply(self) -> Dict[str, ReplyJson]:
        if not self._reply:
            if self._client:
                assert self._client in self.json.reply.__dict__, (
                    f"No reply found for client '{self._client}'.")
            replies = (self.json.reply.__dict__[self._client].__dict__
                       if self._client else self.json.reply.__dict__)
            self._reply = {obj_kind: ReplyJson(reply)
                           for obj_kind, reply in replies.items()}
        return self._reply
