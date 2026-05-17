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

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_HOME = Path.home()

##
## === FILES
##

LOG_FILE = _PROJECT_ROOT / "history.log"

##
## === DIRECTORIES
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
    ssh_keys: Path


DIRS = ProjectDirs(
    root=_PROJECT_ROOT,
    shell=_PROJECT_ROOT / "configs" / "shell",
    extras=_PROJECT_ROOT / "configs" / "extras",
    editors=_PROJECT_ROOT / "configs" / "editors",
    tools=_PROJECT_ROOT / "configs" / "tools",
    rules=_PROJECT_ROOT / "configs" / "rules",
    ssh_keys=_PROJECT_ROOT / "ssh_keys",
)

##
## === TARGETS
##


@dataclass(frozen=True)
class TargetDirs:
    """Well-known user-side directories referenced by the dotfiles project."""

    home: Path
    config: Path
    rules: Path
    ssh: Path


TARGETS = TargetDirs(
    home=_HOME,
    config=_HOME / ".config",
    rules=_HOME / ".rules",
    ssh=_HOME / ".ssh",
)

## } MODULE
