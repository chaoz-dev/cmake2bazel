from filesystem import JsonObject
from pathlib import Path
from types import SimpleNamespace
from typing import Tuple

from dataclasses import dataclass


@dataclass
class PathsJson():
    source: str
    build: str

    def __init__(self, json: SimpleNamespace):
        self.source = json.source
        self.build = json.build


@dataclass
class TargetJson():
    name: str
    id: str
    directory_index: int
    project_index: int
    json_file: str

    def __init__(self, json: SimpleNamespace):
        self.name = json.name
        self.id = json.id
        self.directory_index = json.directoryIndex
        self.project_index = json.projectIndex
        self.json_file = json.jsonFile


@dataclass
class ConfigurationJson():
    json: SimpleNamespace
    name: str
    targets: Tuple[TargetJson]

    def __init__(self, json: SimpleNamespace):
        self.json = json
        self.name = self.json.name
        self.targets = (TargetJson(target) for target in self.json.targets)


@dataclass
class CodeModelV2Json(JsonObject):
    def __init__(self, filepath: Path):
        super().__init__(filepath)

    @property
    def paths(self) -> PathsJson:
        return PathsJson(self.json.paths)

    @property
    def configurations(self) -> Tuple[ConfigurationJson]:
        return (ConfigurationJson(config) for config in self.json.configurations)
