## { MODULE

from pathlib import Path
from setup_scripts._extras.config import ExtraConfig, EXTRAS_DIR

EXTRAS: dict[str, ExtraConfig] = {
    "arch-x11/lightdm-locale.xprofile":
    ExtraConfig(
        name="LightDM xprofile locale",
        source_path=EXTRAS_DIR / "arch-x11" / "lightdm-locale.xprofile",
        target_path=Path.home() / ".xprofile",
        requires=("linux", "x11", "lightdm"),
    ),
    "arch-x11/mouse-workspace-buttons.xbindkeysrc":
    ExtraConfig(
        name="xbindkeys mouse buttons",
        source_path=EXTRAS_DIR / "arch-x11" / "mouse-workspace-buttons.xbindkeysrc",
        target_path=Path.home() / ".xbindkeysrc",
        requires=("linux", "x11"),
    ),
    "arch-x11/touchpad-workspace-gestures.conf":
    ExtraConfig(
        name="libinput-gestures workspaces",
        source_path=EXTRAS_DIR / "arch-x11" / "touchpad-workspace-gestures.conf",
        target_path=Path.home() / ".config" / "libinput-gestures.conf",
        requires=("linux", "x11", "xfce"),
    ),
    "arch-x11/xfce-theme-toggle":
    ExtraConfig(
        name="XFCE theme toggle",
        source_path=EXTRAS_DIR / "arch-x11" / "xfce-theme-toggle",
        target_path=Path.home() / ".local" / "bin" / "xfce-theme-toggle",
        requires=("linux", "x11", "xfce"),
    ),
    "arch-x11/conky/conky.conf":
    ExtraConfig(
        name="conky config",
        source_path=EXTRAS_DIR / "arch-x11" / "conky" / "conky.conf",
        target_path=Path.home() / ".config" / "conky" / "conky.conf",
        requires=("linux", "x11"),
    ),
    "arch-x11/conky/conky.desktop":
    ExtraConfig(
        name="conky autostart",
        source_path=EXTRAS_DIR / "arch-x11" / "conky" / "conky.desktop",
        target_path=Path.home() / ".config" / "autostart" / "conky.desktop",
        requires=("linux", "x11"),
    ),
    "arch-x11/conky/conky-battery":
    ExtraConfig(
        name="conky battery script",
        source_path=EXTRAS_DIR / "arch-x11" / "conky" / "conky-battery",
        target_path=Path.home() / ".local" / "bin" / "conky-battery",
        requires=("linux", "x11"),
    ),
    "arch-x11/conky/conky-gpu":
    ExtraConfig(
        name="conky GPU script",
        source_path=EXTRAS_DIR / "arch-x11" / "conky" / "conky-gpu",
        target_path=Path.home() / ".local" / "bin" / "conky-gpu",
        requires=("linux", "x11"),
    ),
    "arch-x11/conky/conky-cpu-temp":
    ExtraConfig(
        name="conky CPU temp script",
        source_path=EXTRAS_DIR / "arch-x11" / "conky" / "conky-cpu-temp",
        target_path=Path.home() / ".local" / "bin" / "conky-cpu-temp",
        requires=("linux", "x11"),
    ),
    "arch-x11/conky/conky-gpu-temp":
    ExtraConfig(
        name="conky GPU temp script",
        source_path=EXTRAS_DIR / "arch-x11" / "conky" / "conky-gpu-temp",
        target_path=Path.home() / ".local" / "bin" / "conky-gpu-temp",
        requires=("linux", "x11"),
    ),
    "arch-x11/window-management/center-window":
    ExtraConfig(
        name="center-window script",
        source_path=EXTRAS_DIR / "arch-x11" / "window-management" / "center-window",
        target_path=Path.home() / ".local" / "bin" / "center-window",
        requires=("linux", "x11"),
    ),
    "arch-x11/window-management/tile-window":
    ExtraConfig(
        name="tile-window script",
        source_path=EXTRAS_DIR / "arch-x11" / "window-management" / "tile-window",
        target_path=Path.home() / ".local" / "bin" / "tile-window",
        requires=("linux", "x11"),
    ),
    "arch-x11/zathura/zathurarc":
    ExtraConfig(
        name="zathura config",
        source_path=EXTRAS_DIR / "arch-x11" / "zathura" / "zathurarc",
        target_path=Path.home() / ".config" / "zathura" / "zathurarc",
        requires=("linux", "x11"),
    ),
}

## } MODULE
