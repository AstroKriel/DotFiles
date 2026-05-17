## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from dataclasses import dataclass
from pathlib import Path

##
## === PATH ANCHORS
##

## src/local_helpers/project_dirs.py -> parent.parent.parent is the repo root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_HOME = Path.home()

##
## === DIRS
##


@dataclass(frozen=True)
class ProjectDirs:
    """Well-known directories within the dotfiles project."""

    root: Path
    shell: Path
    extras: Path
    editors: Path
    tools: Path
    rules: Path


DIRS = ProjectDirs(
    root=_PROJECT_ROOT,
    shell=_PROJECT_ROOT / "configs" / "shell",
    extras=_PROJECT_ROOT / "configs" / "extras",
    editors=_PROJECT_ROOT / "configs" / "editors",
    tools=_PROJECT_ROOT / "configs" / "tools",
    rules=_PROJECT_ROOT / "configs" / "rules",
)

##
## === TARGETS
##


@dataclass(frozen=True)
class TargetDirs:
    """Well-known user-side directories referenced by the dotfiles project."""

    home: Path
    config: Path
    local_bin: Path
    rules: Path
    ssh: Path
    ssh_notes: Path


TARGETS = TargetDirs(
    home=_HOME,
    config=_HOME / ".config",
    local_bin=_HOME / ".local" / "bin",
    rules=_HOME / ".rules",
    ssh=_HOME / ".ssh",
    ssh_notes=_HOME / ".ssh" / "notes",
)

## } MODULE
