## { MODULE

from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
EXTRAS_DIR = ROOT_DIR / "configs" / "extras"


@dataclass
class ExtraConfig:
    name: str
    source_path: Path
    target_path: Path
    requires: tuple[str, ...] = ()


## } MODULE
