## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
from dataclasses import dataclass
from pathlib import Path
import shutil
import sys
from typing import cast

## local
from local_helpers import load_profiles
from local_helpers import log_messages, apply_shell_actions
from local_helpers import project_dirs

##
## === TOOL REGISTRY
##

SCRIPT_NAME = Path(__file__).name
TOOLS_DIR = project_dirs.DIRS.tools
CONFIG_DIR = project_dirs.TARGETS.config

LOG_MESSAGE = log_messages.make_logger_fn(SCRIPT_NAME)


@dataclass
class ToolConfig:
    name: str
    dotfiles_dir: Path
    target_dir: Path
    mac_app: str | None = None


TOOLS: dict[str, ToolConfig] = {
    "tmux":
    ToolConfig(
        name="Tmux",
        dotfiles_dir=TOOLS_DIR / "tmux",
        target_dir=CONFIG_DIR / "tmux",
    ),
    "kitty":
    ToolConfig(
        name="Kitty terminal",
        mac_app="kitty.app",
        dotfiles_dir=TOOLS_DIR / "kitty",
        target_dir=CONFIG_DIR / "kitty",
    ),
    "ghostty":
    ToolConfig(
        name="Ghostty terminal",
        mac_app="Ghostty.app",
        dotfiles_dir=TOOLS_DIR / "ghostty",
        target_dir=CONFIG_DIR / "ghostty",
    ),
    "yazi":
    ToolConfig(
        name="Yazi",
        dotfiles_dir=TOOLS_DIR / "yazi",
        target_dir=CONFIG_DIR / "yazi",
    ),
}

##
## === TOOL HELPERS
##


def get_selected_tools(
    *,
    tool_keys: tuple[str, ...] | None,
) -> dict[str, ToolConfig]:
    """Return tool configs selected by the active system profile."""
    if tool_keys is None:
        return TOOLS
    unknown_tool_keys = sorted(set(tool_keys) - set(TOOLS))
    if unknown_tool_keys:
        raise KeyError(f"Unknown `--which` tool(s): {', '.join(unknown_tool_keys)}")
    return {tool_key: TOOLS[tool_key] for tool_key in tool_keys}


def resolve_selected_tools(
    *,
    subscribed_tool_keys: tuple[str, ...],
    requested_tool_keys: tuple[str, ...],
    include_all: bool,
) -> tuple[str, ...]:
    if include_all:
        return subscribed_tool_keys
    get_selected_tools(tool_keys=requested_tool_keys)
    unsubscribed_tool_keys = sorted(set(requested_tool_keys) - set(subscribed_tool_keys))
    if unsubscribed_tool_keys:
        raise KeyError(
            "Requested `--which` tool(s) are not subscribed in `this-system.toml`: "
            f"{', '.join(unsubscribed_tool_keys)}",
        )
    return requested_tool_keys


def check_installed_tools(
    *,
    tool_keys: tuple[str, ...] | None,
    dry_run: bool,
) -> set[str]:
    """Return subscribed tools that are installed on this system."""
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Checking installed tools...",
            dry_run=dry_run,
        ),
    )
    installed_tool_keys: set[str] = set()
    selected_tool_configs = get_selected_tools(tool_keys=tool_keys)
    for command, tool in selected_tool_configs.items():
        found_via_app = (
            sys.platform == "darwin" and tool.mac_app is not None
            and (Path("/Applications") / tool.mac_app).exists()
        )
        if shutil.which(command) or found_via_app:
            LOG_MESSAGE(
                log_messages.format_dry_run(
                    message=f"Found {tool.name} ({command}) in your `$PATH`.",
                    dry_run=dry_run,
                ),
            )
            installed_tool_keys.add(command)
        else:
            LOG_MESSAGE(
                log_messages.format_dry_run(
                    message=f"{tool.name} was not found in your `$PATH`.",
                    dry_run=dry_run,
                ),
            )
    return installed_tool_keys


##
## === PROGRAM MAIN
##


def remove_symlinks(
    *,
    dry_run: bool,
    tool_keys: tuple[str, ...] | None = None,
):
    log_messages.configure_logger(write_to_file=not dry_run)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Started removing tool config symlinks",
            dry_run=dry_run,
        ),
    )
    selected_tool_configs = get_selected_tools(tool_keys=tool_keys)
    for tool in selected_tool_configs.values():
        apply_shell_actions.remove_symlink(
            target_path=tool.target_dir,
            logger_fn=LOG_MESSAGE,
            dry_run=dry_run,
        )
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Finished removing tool config symlinks",
            dry_run=dry_run,
        ),
    )


def run(
    *,
    dry_run: bool,
    check_only: bool = False,
    tool_keys: tuple[str, ...] | None = None,
):
    log_messages.configure_logger(write_to_file=not dry_run)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Started setting up tool configs",
            dry_run=dry_run,
        ),
    )
    installed_tool_keys = check_installed_tools(
        tool_keys=tool_keys,
        dry_run=dry_run,
    )
    if check_only:
        LOG_MESSAGE(
            log_messages.format_dry_run(
                message="Check complete. Exiting due to `--check-only`",
                dry_run=dry_run,
            ),
        )
        return
    for command in sorted(installed_tool_keys):
        tool = TOOLS[command]
        apply_shell_actions.ensure_dir_exists(
            directory=tool.target_dir.parent,
            logger_fn=LOG_MESSAGE,
            dry_run=dry_run,
        )
        apply_shell_actions.create_symlink(
            source_path=tool.dotfiles_dir,
            target_path=tool.target_dir,
            logger_fn=LOG_MESSAGE,
            dry_run=dry_run,
        )
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Finished setting up tool configs",
            dry_run=dry_run,
        ),
    )


def main() -> None:
    ## parse user inputs
    parser = argparse.ArgumentParser(
        description="Symlink subscribed tool config folders and clone needed repos.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without applying them",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check installed tools and exit",
    )
    parser.add_argument(
        "--which",
        action="append",
        choices=sorted(TOOLS),
        default=[],
        metavar="TOOL",
        help="Apply one subscribed tool. Can be passed multiple times",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Apply all subscribed tools from `this-system.toml`",
    )
    args = parser.parse_args()
    include_all = cast(bool, args.all)
    requested_tool_keys = tuple(
        cast(
            list[str],
            args.which,
        ),
    )
    dry_run = cast(bool, args.dry_run)
    check_only = cast(bool, args.check_only)
    if include_all and requested_tool_keys:
        parser.error("`--all` cannot be combined with `--which`")
    if not include_all and not requested_tool_keys:
        parser.error("pass `--all` or at least one `--which`")
    profile = load_profiles.load_profile(required=True)
    if profile is None:
        parser.error("`this-system.toml` is required")
    tool_keys = resolve_selected_tools(
        subscribed_tool_keys=profile.tools,
        requested_tool_keys=requested_tool_keys,
        include_all=include_all,
    )
    run(
        dry_run=dry_run,
        check_only=check_only,
        tool_keys=tool_keys,
    )


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()

## } SCRIPT
