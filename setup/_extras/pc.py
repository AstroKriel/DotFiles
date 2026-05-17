## { MODULE

from pathlib import Path
from setup._extras.config import ExtraConfig, EXTRAS_DIR

EXTRAS: dict[str, ExtraConfig] = {
    "pc/path-aliases.sh":
    ExtraConfig(
        name="pc path aliases",
        source_path=EXTRAS_DIR / "pc" / "path-aliases.sh",
        target_path=Path.home() / ".path_aliases",
    ),
}

## } MODULE
