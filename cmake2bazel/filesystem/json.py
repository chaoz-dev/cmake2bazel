import json

from filesystem import path
from pathlib import Path
from types import SimpleNamespace


class JsonObject():
    def __init__(self, filepath: Path):
        self._filepath = path.assert_resolve(filepath)
        self._json = None

    @property
    def json(self):
        if not self._json:
            with open(self._filepath, "r") as json_file:
                self._json = json.loads(
                    json_file.read(),
                    object_hook=lambda data: SimpleNamespace(**data))

        return self._json

    @property
    def filepath(self):
        return self._filepath
