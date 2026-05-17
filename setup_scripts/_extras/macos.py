## { MODULE

from pathlib import Path
from setup_scripts._extras.config import ExtraConfig, EXTRAS_DIR

EXTRAS: dict[str, ExtraConfig] = {
    "macos/disable-navigation-keys.dict":
    ExtraConfig(
        name="macOS disabled navigation keys",
        source_path=EXTRAS_DIR / "macos" / "disable-navigation-keys.dict",
        target_path=Path.home() / "Library" / "KeyBindings" / "DefaultKeyBinding.dict",
        requires=("macos", ),
    ),
}

## } MODULE
