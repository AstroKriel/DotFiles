## { MODULE

from pathlib import Path
from setup._extras.config import ExtraConfig, EXTRAS_DIR

EXTRAS: dict[str, ExtraConfig] = {
    "personal-machine/path-aliases.sh":
    ExtraConfig(
        name="personal machine path aliases",
        source_path=EXTRAS_DIR / "personal-machine" / "path-aliases.sh",
        target_path=Path.home() / ".path_aliases",
    ),
}

## } MODULE
