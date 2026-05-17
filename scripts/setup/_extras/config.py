## { MODULE

from dataclasses import dataclass
from pathlib import Path

from local_helpers import project_dirs

EXTRAS_DIR = project_dirs.SOURCES.extras


@dataclass
class ExtraConfig:
    name: str
    source_path: Path
    target_path: Path
    requires: tuple[str, ...] = ()


## } MODULE
