from abc import ABC, abstractproperty
from typing import List

_CC_BINARY = """
cc_binary({attributes}\n)
"""

_CC_LIBRARY = """
cc_library({attributes}\n)
"""


class CcRule(ABC):
    @property
    def attributes(self) -> str:
        attrs = []
        for key, value in self.__dict__.items():
            if isinstance(value, str):
                value = f"\"{value}\""
            if isinstance(value, (list, tuple)):
                value = [f"\t\t\"{v}\"," for v in value]
                value = "[\n{}\n\t]".format("\n".join(value))
            attrs.append(f"\n\t{key} = {value},")

        return "".join(attrs)

    @property
    @abstractproperty
    def value(self) -> str:
        pass


class CcBinary(CcRule):
    def __init__(self,
                 name: str,
                 deps: List[str] = [],
                 srcs: List[str] = [],
                 copts: List[str] = [],
                 includes: List[str] = [],
                 linkopts: List[str] = [],
                 local_defines: List[str] = [],
                 ):
        self.name = name
        self.deps = deps
        self.srcs = srcs
        self.copts = copts
        self.includes = includes
        self.linkopts = linkopts
        self.local_defines = local_defines

    def value(self) -> str:
        return _CC_BINARY.format(attributes=self.attributes)


class CcLibrary(CcRule):
    def __init__(self,
                 name: str,
                 deps: List[str] = [],
                 srcs: List[str] = [],
                 hdrs: List[str] = [],
                 copts: List[str] = [],
                 includes: List[str] = [],
                 linkopts: List[str] = [],
                 local_defines: List[str] = [],
                 ):
        self.name = name
        self.deps = deps
        self.srcs = srcs
        self.hdrs = hdrs
        self.copts = copts
        self.includes = includes
        self.linkopts = linkopts
        self.local_defines = local_defines

    def value(self) -> str:
        return _CC_LIBRARY.format(attributes=self.attributes)
