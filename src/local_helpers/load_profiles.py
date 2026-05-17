## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from dataclasses import dataclass
import tomllib
from typing import cast

## local
from local_helpers import project_dirs

##
## === PROFILE CONFIG
##

THIS_SYSTEM_PROFILE_PATH = project_dirs.SOURCES.root / "this-system.toml"

##
## === PROFILE TYPES
##


@dataclass(frozen=True)
class SystemProfile:
    """Selected configuration groups for one system."""

    shell: str | None
    platforms: tuple[str, ...]
    editors: tuple[str, ...]
    tools: tuple[str, ...]
    extras: tuple[str, ...]
    link_rules: bool
    set_login_shell: bool


##
## === PROFILE HELPERS
##


def load_profile(
    *,
    required: bool = False,
) -> SystemProfile | None:
    """Load the local `this-system.toml` profile."""
    if not THIS_SYSTEM_PROFILE_PATH.exists():
        if required:
            raise FileNotFoundError(
                "No system profile found. Create `this-system.toml` from a tracked profile.",
            )
        return None
    raw_profile = cast(dict[str, object], tomllib.loads(THIS_SYSTEM_PROFILE_PATH.read_text()))
    return create_profile(raw_profile=raw_profile)


def create_profile(
    *,
    raw_profile: dict[str, object],
) -> SystemProfile:
    """Create a typed system profile from parsed TOML data."""
    return SystemProfile(
        shell=_get_optional_string(
            raw_profile=raw_profile,
            key="shell",
        ),
        platforms=_get_string_tuple(
            raw_profile=raw_profile,
            key="platforms",
        ),
        editors=_get_string_tuple(
            raw_profile=raw_profile,
            key="editors",
        ),
        tools=_get_string_tuple(
            raw_profile=raw_profile,
            key="tools",
        ),
        extras=_get_string_tuple(
            raw_profile=raw_profile,
            key="extras",
        ),
        link_rules=_get_bool(
            raw_profile=raw_profile,
            key="link_rules",
            default=False,
        ),
        set_login_shell=_get_bool(
            raw_profile=raw_profile,
            key="set_login_shell",
            default=True,
        ),
    )


def _get_optional_string(
    *,
    raw_profile: dict[str, object],
    key: str,
) -> str | None:
    value = raw_profile.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"`{key}` must be a string when set.")
    return value


def _get_bool(
    *,
    raw_profile: dict[str, object],
    key: str,
    default: bool,
) -> bool:
    value = raw_profile.get(key, default)
    if not isinstance(value, bool):
        raise TypeError(f"`{key}` must be a boolean when set.")
    return value


def _get_string_tuple(
    *,
    raw_profile: dict[str, object],
    key: str,
) -> tuple[str, ...]:
    value = raw_profile.get(key, [])
    if not isinstance(value, list):
        raise TypeError(f"`{key}` must be a list of strings.")
    value_items = cast(list[object], value)
    if not all(isinstance(item, str) for item in value_items):
        raise TypeError(f"`{key}` must contain only strings.")
    return tuple(
        cast(
            list[str],
            value_items,
        ),
    )


## } MODULE
