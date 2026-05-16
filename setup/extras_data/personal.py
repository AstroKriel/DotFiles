## { SCRIPT

from pathlib import Path
from setup.extras_data.extra_config import ExtraConfig, EXTRAS_DIR

EXTRAS: dict[str, ExtraConfig] = {
    "personal/project-aliases.sh":
    ExtraConfig(
        name="personal project aliases",
        source_path=EXTRAS_DIR / "personal" / "project-aliases.sh",
        target_path=Path.home() / ".project_aliases",
    ),
}

## } SCRIPT
