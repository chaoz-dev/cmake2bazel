from enum import Enum
from pathlib import Path
from typing import Dict, Optional

from .codemodel_v2 import CodeModelV2
from .json import ReplyIndexJson, ReplyJson


class ObjectKind(Enum):
    CACHE_V2 = "cache-v2"
    CMAKEFILES_V1 = "cmakeFiles-v1"
    CODEMODEL_V2 = "codemodel-v2"


class ReplyIndex():
    def __init__(self, filepath: Path, client: Optional[str] = None):
        self._json = ReplyIndexJson(filepath, client)
        self._json_reply = None

    @property
    def _reply(self) -> Dict[ObjectKind, ReplyJson]:
        if not self._json_reply:
            self._json_reply = {ObjectKind(obj_kind): reply
                                for obj_kind, reply in self.json.reply.items()}
        return self._json_reply

    @property
    def codemodel_v2(self) -> CodeModelV2:
        object_kind = ObjectKind.CODEMODEL_V2
        reply = self._get_reply(object_kind)
        assert reply, f"No reply found for object kind '{object_kind.value}'."
        return CodeModelV2(self.json.filepath.parent / reply.json_file)

    @property
    def json(self) -> ReplyIndexJson:
        return self._json

    def _get_reply(self, object_kind: ObjectKind) -> Optional[ReplyJson]:
        return self._reply[object_kind] if self._has_reply(object_kind) else None

    def _has_reply(self, object_kind: ObjectKind) -> bool:
        return object_kind in self._reply
