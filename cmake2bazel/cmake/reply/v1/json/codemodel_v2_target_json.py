from dataclasses import dataclass
from filesystem import JsonObject
from pathlib import Path, PurePath
from types import SimpleNamespace
from typing import Optional, Tuple


@dataclass
class ArtifactJson():
    path: str

    def __init__(self, json: SimpleNamespace):
        self.path = json.path


@dataclass
class CommandFragmentJson():
    fragment: str
    role: str

    def __init__(self, json: SimpleNamespace):
        self.fragment = json.fragment
        self.role = json.role


@dataclass
class CompileCommandFragmentJson():
    fragment: str

    def __init__(self, json: SimpleNamespace):
        self.fragment = json.fragment


@dataclass
class DefineJson():
    define: str

    def __init__(self, json: SimpleNamespace):
        self.define = json.define


@dataclass
class DependencyJson():
    id: str

    def __init__(self, json: SimpleNamespace):
        self.id = json.id


@dataclass
class IncludeJson():
    path: str

    def __init__(self, json: SimpleNamespace):
        self.path = json.path


@dataclass
class LinkJson():
    language: str
    command_fragments: Tuple[CommandFragmentJson]

    def __init__(self, json: SimpleNamespace):
        self.language = json.language
        self.command_fragments = ((CommandFragmentJson(fragment)
                                  for fragment in json.commandFragments) if hasattr(json, "commandFragments") else ())


@dataclass
class SourceJson():
    compile_group_index: Optional[int]
    path: str
    source_group_index: Optional[int]

    def __init__(self, json: SimpleNamespace):
        self.compile_group_index = (json.compileGroupIndex if hasattr(
            json, "compileGroupIndex") else None)
        self.path = json.path
        self.source_group_index = (json.sourceGroupIndex if hasattr(
            json, "sourceGroupIndex") else None)


@dataclass
class CompileGroupJson():
    language: str
    compile_command_fragments: Tuple[CompileCommandFragmentJson]
    defines: Tuple[DefineJson]
    includes: Tuple[IncludeJson]
    source_indexes: Tuple[int]

    def __init__(self, json: SimpleNamespace):
        self.language = json.language
        self.compile_command_fragments = (
            (CompileCommandFragmentJson(fragment)
             for fragment in json.compileCommandFragments)
            if hasattr(json, "compileCommandFragments") else ())
        self.defines = ((DefineJson(define) for define in json.defines)
                        if hasattr(json, "defines") else ())
        self.includes = ((IncludeJson(include) for include in json.includes)
                         if hasattr(json, "includes") else ())
        self.source_indexes = (index for index in json.sourceIndexes)


class CodeModelV2TargetJson(JsonObject):
    def __init__(self, filepath: Path):
        super().__init__(filepath)

    @property
    def artifacts(self) -> Tuple[ArtifactJson]:
        return ((ArtifactJson(artifact) for artifact in self.json.artifacts)
                if hasattr(self.json, "artifacts") else ())

    @property
    def compile_groups(self) -> Tuple[CompileGroupJson]:
        return ((CompileGroupJson(group) for group in self.json.compileGroups)
                if hasattr(self.json, "compileGroups") else ())

    @property
    def dependencies(self) -> Tuple[DependencyJson]:
        return ((DependencyJson(dep) for dep in self.json.dependencies)
                if hasattr(self.json, "dependencies") else ())

    @property
    def id(self) -> str:
        return self.json.id

    @property
    def link(self) -> Optional[LinkJson]:
        return (LinkJson(self.json.link)
                if hasattr(self.json, "link") else None)

    @property
    def name(self) -> str:
        return self.json.name

    @property
    def sources(self) -> Tuple[SourceJson]:
        return (SourceJson(src) for src in self.json.sources)

    @property
    def type(self) -> str:
        return self.json.type
