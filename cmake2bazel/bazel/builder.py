# import rules
import filesystem

from bazel import rules
from cmake.reply.v1 import CodeModelV2, CodeModelV2Target, Configuration, TargetType
from pathlib import Path
from typing import List, Union


class BuildFileBuilder():
    def __init__(self):
        self._targets = []

    def add_target(self, rule: rules.CcRule):
        self._targets.append(rule)

    def _add_target(self, target: CodeModelV2Target, configuration: Configuration):
        copts = set()
        defines = set()
        includes = set()
        sources = set()

        for compile_group in target.compile_groups:
            [copts.add(fragment)
             for fragment in compile_group.compile_command_fragments]
            [defines.add(define) for define in compile_group.defines]
            [includes.add(str(include)) for include in compile_group.includes]
            [sources.add(str(source)) for source in compile_group.sources]

        dependencies = [f":{configuration.get_target(id).name}"
                        for id in target.dependencies]

        linkopts = list(target.link.command_fragments) if target.link else []

        copts = list(copts)
        defines = list(defines)
        includes = list(includes)
        sources = list(includes)

        if target.type is TargetType.EXECUTABLE:
            rule = rules.CcBinary(
                target.name,
                dependencies,
                sources,
                copts,
                includes,
                linkopts,
                defines)
        elif target.type is TargetType.UTILITY:
            raise NotImplementedError()
        else:
            rule = rules.CcLibrary(
                target.name,
                dependencies,
                sources,
                [],
                copts,
                includes,
                linkopts,
                defines)
        self.add_target(rule)

    def build(self, codemodel: CodeModelV2):
        CMAKE_CONFIGURATION = "Release"
        assert codemodel.has_configuration(CMAKE_CONFIGURATION), (
            f"Only {CMAKE_CONFIGURATION} configuration is currently supported.")
        configuration = codemodel.get_configuration(CMAKE_CONFIGURATION)

        for target in configuration.targets.values():
            if target.type is TargetType.UTILITY:
                continue
            self._add_target(target, configuration)

    def write(self, path: Path, filename: str = "BUILD"):
        data = "\n".join([target.value() for target in self._targets])
        # data = data.replace("\'", "\"")
        filesystem.write(path, filename, data)
