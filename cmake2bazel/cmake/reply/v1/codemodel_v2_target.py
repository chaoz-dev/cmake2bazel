from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePath
from typing import Optional, Tuple

from .json import (
    CompileGroupJson,
    CommandFragmentJson,
    CodeModelV2TargetJson,
    SourceJson,
    LinkJson
)


class CommandFragmentRole(Enum):
    FLAGS = "flags"
    LIBRARIES = "libraries"
    LIBRARY_PATH = "libraryPath"
    FRAMEWORK_PATH = "frameworkPath"


class TargetType(Enum):
    EXECUTABLE = "EXECUTABLE"
    STATIC_LIBRARY = "STATIC_LIBRARY"
    SHARED_LIBRARY = "SHARED_LIBRARY"
    MODULE_LIBRARY = "MODULE_LIBRARY"
    OBJECT_LIBRARY = "OBJECT_LIBRARY"
    UTILITY = "UTILITY"


@dataclass
class CommandFragment():
    fragment: str
    role: CommandFragmentRole

    def __init__(self, json: CommandFragmentJson):
        self.fragment = json.fragment
        self.role = CommandFragmentRole(json.role)


@dataclass
class CompileGroup():
    language: str

    compile_command_fragments: Tuple[str]
    defines: Tuple[str]
    includes: Tuple[PurePath]
    sources: Tuple[PurePath]

    def __init__(self, json: CompileGroupJson, sources_json: Tuple[SourceJson]):
        self.language = json.language

        cc_fragments = []
        [cc_fragments.extend(json.fragment.split(" "))
         for json in json.compile_command_fragments]
        self.compile_command_fragments = tuple(sorted(
            cc_fragment for cc_fragment in cc_fragments if cc_fragment))

        self.defines = tuple(sorted(json.define for json in json.defines))
        self.includes = tuple(sorted(PurePath(include.path)
                                     for include in json.includes))
        self.sources = tuple(sorted(PurePath(sources_json[index].path)
                                    for index in json.source_indexes))


@dataclass
class Link():
    language: str

    command_fragments: Tuple[CommandFragment]

    def __init__(self, json: LinkJson):
        self.language = json.language

        fragments = []
        [fragments.extend(json.fragment.split(" "))
         for json in json.command_fragments]
        self.command_fragments = tuple(sorted(
            fragment for fragment in fragments if fragment))


class CodeModelV2Target():
    def __init__(self, filepath: Path):
        self._json = CodeModelV2TargetJson(filepath)

        self._artifacts = None
        self._compile_groups = None
        self._dependencies = None
        self._link = None

    @property
    def artifacts(self) -> Tuple[PurePath]:
        if not self._artifacts:
            self._artifacts = tuple(sorted(PurePath(artifact.path)
                                    for artifact in self.json.artifacts))
        return self._artifacts

    @property
    def compile_groups(self) -> Tuple[CompileGroup]:
        if not self._compile_groups:
            sources = tuple(self.json.sources)
            self._compile_groups = (CompileGroup(group, sources)
                                    for group in self.json.compile_groups)
        return self._compile_groups

    @property
    def dependencies(self) -> Tuple[str]:
        if not self._dependencies:
            self._dependencies = tuple(
                sorted(dep.id for dep in self.json.dependencies))
        return self._dependencies

    @property
    def id(self) -> str:
        return self.json.id

    @property
    def json(self) -> CodeModelV2TargetJson:
        return self._json

    @property
    def link(self) -> Optional[Link]:
        if not self._link:
            self._link = Link(self.json.link) if self.json.link else None
        return self._link

    @property
    def name(self) -> str:
        return self.json.name

    @property
    def type(self) -> TargetType:
        return TargetType(self.json.type)
