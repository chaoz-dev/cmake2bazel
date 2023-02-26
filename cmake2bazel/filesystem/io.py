from filesystem import path
from pathlib import Path


def write(path: Path, filename: str, data: str):
    path = path.resolve()
    path.mkdir(parents=True, exist_ok=True)

    with open(path / filename, "w") as f:
        f.write(data)
