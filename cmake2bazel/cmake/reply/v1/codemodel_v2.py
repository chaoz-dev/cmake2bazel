from filesystem import JsonObject
from pathlib import Path, PurePath
from typing import Dict, List, Optional

from .codemodel_v2_target import CodeModelV2Target, TargetType
from .json import CodeModelV2Json, ConfigurationJson


class Configuration():
    def __init__(self, json: ConfigurationJson, filepath: Path):
        self._json = json
        self._filepath = filepath
        self._targets = None

    @property
    def filepath(self) -> Path:
        return self._filepath

    @property
    def json(self) -> ConfigurationJson:
        return self._json

    @property
    def name(self) -> str:
        return self.json.name

    @property
    def targets(self) -> Dict[str, CodeModelV2Target]:
        if not self._targets:
            self._targets = {target.id: CodeModelV2Target(
                self.filepath.parent / target.json_file)
                for target in self.json.targets}
        return self._targets

    def get_target(self, id: str) -> Optional[CodeModelV2Target]:
        return self.targets[id] if self.has_target(id) else None

    def get_targets(self, types: List[TargetType]) -> List[CodeModelV2Target]:
        if not types:
            return self.targets.values()

        types = set(types)
        return [target for target in self.targets.values() if target.type in types]

    def has_target(self, id: str) -> bool:
        return id in self.targets


class CodeModelV2():
    def __init__(self, filepath: Path):
        self._json = CodeModelV2Json(filepath)

        self._configurations = None

    @property
    def configurations(self) -> Dict[str, Configuration]:
        if not self._configurations:
            self._configurations = {
                config.name: Configuration(config, self.json.filepath)
                for config in self.json.configurations}
        return self._configurations

    @property
    def json(self) -> CodeModelV2Json:
        return self._json

    @property
    def path_to_build(self) -> PurePath:
        return PurePath(self.json.paths.build)

    @property
    def path_to_source(self) -> PurePath:
        return PurePath(self.json.paths.source)

    def get_configuration(self, name: str) -> Optional[Configuration]:
        return self.configurations[name] if self.has_configuration(name) else None

    def has_configuration(self, name: str) -> bool:
        return name in self.configurations
