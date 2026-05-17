## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import shutil
import sys
from typing import cast

## local
from local_helpers import load_profiles
from local_helpers import log_messages, apply_shell_actions
from local_helpers import project_dirs

##
## === EDITOR REGISTRY
##

SCRIPT_NAME = Path(__file__).name
EDITORS_DIR = project_dirs.SOURCES.editors
CONFIG_DIR = project_dirs.TARGETS.config

LOG_MESSAGE = log_messages.make_logger_fn(SCRIPT_NAME)

if sys.platform == "darwin":
    ## macOS
    _vscode_target_dir = Path.home() / "Library/Application Support/Code/User"
else:
    ## linux
    _vscode_target_dir = Path.home() / ".config/Code/User"
_VSCODE_TARGET_DIR = _vscode_target_dir


@dataclass
class EditorConfig:
    name: str
    command: str
    source_dir: Path
    target_dir: Path
    files: dict[str, str] | None = None
    extensions: Path | None = None


EDITORS: dict[str, EditorConfig] = {
    "vscode":
    EditorConfig(
        name="Visual Studio Code",
        command="code",
        source_dir=EDITORS_DIR / "vscode",
        target_dir=_VSCODE_TARGET_DIR,
        files={
            "settings": "dict",
            "keybindings": "list",
        },
        extensions=EDITORS_DIR / "vscode" / "extensions.txt",
    ),
    "nvim":
    EditorConfig(
        name="Neovim",
        command="nvim",
        source_dir=EDITORS_DIR / "nvim",
        target_dir=CONFIG_DIR / "nvim",
    ),
    "zed":
    EditorConfig(
        name="Zed",
        command="zed" if sys.platform == "darwin" else "zeditor",
        source_dir=EDITORS_DIR / "zed",
        target_dir=Path.home() / ".config/zed/",
        files={
            "settings": "dict",
            "keymap": "list",
        },
    ),
}

##
## === EDITOR HELPERS
##


def filter_jsonc_comments(
    content: str,
) -> str:
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)  # remove block comments
    content = re.sub(r'//[^\n\r]*', '', content)  # remove line comments
    content = re.sub(r',(\s*[}\]])', r'\1', content)  # remove trailing commas
    return content


def merge_config_modules(
    *,
    modules_dir: Path,
    output_mode: str,
) -> dict[str, object] | list[object] | None:
    """Merge all `*.jsonc` files under `modules_dir` into one dict or list."""
    if not modules_dir.exists():
        LOG_MESSAGE(f"Skipping. No module directory found: {modules_dir}")
        return None
    ## `dict` mode: each module is a JSON object; later keys overwrite earlier ones in sort order
    if output_mode == "dict":
        merged_dict: dict[str, object] = {}
        for module in sorted(modules_dir.glob("*.jsonc")):
            with module.open("r", encoding="utf-8") as module_file:
                raw_content = module_file.read()
                filtered_content = filter_jsonc_comments(raw_content)
                dict_content = cast(object, json.loads(filtered_content))
                if not isinstance(dict_content, dict):
                    LOG_MESSAGE(f"Skipping. Expected object config in: {module}")
                    return None
                merged_dict.update(
                    cast(
                        dict[str, object],
                        dict_content,
                    ),
                )
        return merged_dict
    ## `list` mode: each module is a JSON array; entries are concatenated in sort order
    elif output_mode == "list":
        merged_list: list[object] = []
        for module in sorted(modules_dir.glob("*.jsonc")):
            with module.open("r", encoding="utf-8") as module_file:
                raw_content = module_file.read()
                filtered_content = filter_jsonc_comments(raw_content)
                list_content = cast(object, json.loads(filtered_content))
                if not isinstance(list_content, list):
                    LOG_MESSAGE(f"Skipping. Expected list config in: {module}")
                    return None
                merged_list.extend(
                    cast(
                        list[object],
                        list_content,
                    ),
                )
        return merged_list
    else:
        LOG_MESSAGE(f"Error: Unsupported output mode `{output_mode}`")
        return None


def install_extensions(
    *,
    command: str,
    extensions_file: Path,
    dry_run: bool,
):
    if not extensions_file.exists():
        LOG_MESSAGE(f"No extensions file found at: {extensions_file}")
        return
    extensions = [extension for extension in extensions_file.read_text().splitlines() if extension.strip()]
    for extension in extensions:
        apply_shell_actions.run_command(
            args=[command, "--install-extension", extension],
            logger_fn=LOG_MESSAGE,
            description=f"install extension: {extension}",
            dry_run=dry_run,
        )


def setup_editor(
    *,
    editor: EditorConfig,
    dry_run: bool,
):
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message=f"Started setting up {editor.name}",
            dry_run=dry_run,
        ),
    )
    if shutil.which(editor.command):
        LOG_MESSAGE(
            log_messages.format_dry_run(
                message=f"Found {editor.name} ({editor.command}) in your `$PATH`.",
                dry_run=dry_run,
            ),
        )
    else:
        LOG_MESSAGE(
            log_messages.format_dry_run(
                message=f"{editor.command} was not found in your `$PATH`.",
                dry_run=dry_run,
            ),
        )
        return
    if editor.files is None:
        apply_shell_actions.ensure_dir_exists(
            directory=editor.target_dir.parent,
            logger_fn=LOG_MESSAGE,
            dry_run=dry_run,
        )
        apply_shell_actions.create_symlink(
            source_path=editor.source_dir,
            target_path=editor.target_dir,
            logger_fn=LOG_MESSAGE,
            dry_run=dry_run,
        )
    else:
        setup_editor_files(
            editor=editor,
            dry_run=dry_run,
        )
    ## install extensions if defined
    if editor.extensions is not None:
        install_extensions(
            command=editor.command,
            extensions_file=editor.extensions,
            dry_run=dry_run,
        )


def setup_editor_files(
    *,
    editor: EditorConfig,
    dry_run: bool,
) -> None:
    if editor.files is None:
        return
    for config_name, output_mode in editor.files.items():
        modules_dir = editor.source_dir / config_name
        merged_config = merge_config_modules(
            modules_dir=modules_dir,
            output_mode=output_mode,
        )
        if merged_config is None:
            return
        output_path = editor.source_dir / f"{config_name}.json"
        target_path = editor.target_dir / f"{config_name}.json"
        if dry_run:
            LOG_MESSAGE(f"[dry-run] Would write merged settings to: {output_path}")
        else:
            with output_path.open("w", encoding="utf-8") as output_file:
                json.dump(merged_config, output_file, indent=2)
            LOG_MESSAGE(f"Wrote merged config to: {output_path}")
        ## ensure target directory exists
        apply_shell_actions.ensure_dir_exists(
            directory=editor.target_dir,
            logger_fn=LOG_MESSAGE,
            dry_run=dry_run,
        )
        ## symlink merged config
        apply_shell_actions.create_symlink(
            source_path=output_path,
            target_path=target_path,
            logger_fn=LOG_MESSAGE,
            dry_run=dry_run,
        )


def get_selected_editors(
    *,
    editor_keys: tuple[str, ...] | None,
) -> dict[str, EditorConfig]:
    """Return editor configs selected by the active system profile."""
    if editor_keys is None:
        return EDITORS
    unknown_editor_keys = sorted(set(editor_keys) - set(EDITORS))
    if unknown_editor_keys:
        raise KeyError(f"Unknown `--which` editor(s): {', '.join(unknown_editor_keys)}")
    return {editor_key: EDITORS[editor_key] for editor_key in editor_keys}


def resolve_selected_editors(
    *,
    subscribed_editor_keys: tuple[str, ...],
    requested_editor_keys: tuple[str, ...],
    include_all: bool,
) -> tuple[str, ...]:
    if include_all:
        return subscribed_editor_keys
    get_selected_editors(editor_keys=requested_editor_keys)
    unsubscribed_editor_keys = sorted(set(requested_editor_keys) - set(subscribed_editor_keys))
    if unsubscribed_editor_keys:
        raise KeyError(
            "Requested `--which` editor(s) are not subscribed in `this-system.toml`: "
            f"{', '.join(unsubscribed_editor_keys)}",
        )
    return requested_editor_keys


##
## === PROGRAM MAIN
##


def remove_symlinks(
    *,
    dry_run: bool,
    editor_keys: tuple[str, ...] | None = None,
):
    log_messages.configure_logger(write_to_file=not dry_run)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Started removing editor config symlinks",
            dry_run=dry_run,
        ),
    )
    selected_editor_configs = get_selected_editors(editor_keys=editor_keys)
    for editor in selected_editor_configs.values():
        if editor.files is None:
            apply_shell_actions.remove_symlink(
                target_path=editor.target_dir,
                logger_fn=LOG_MESSAGE,
                dry_run=dry_run,
            )
        else:
            for config_name in editor.files:
                apply_shell_actions.remove_symlink(
                    target_path=editor.target_dir / f"{config_name}.json",
                    logger_fn=LOG_MESSAGE,
                    dry_run=dry_run,
                )
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Finished removing editor config symlinks",
            dry_run=dry_run,
        ),
    )


def run(
    *,
    dry_run: bool,
    editor_keys: tuple[str, ...] | None = None,
):
    log_messages.configure_logger(write_to_file=not dry_run)
    selected_editor_configs = get_selected_editors(editor_keys=editor_keys)
    for editor in selected_editor_configs.values():
        setup_editor(
            editor=editor,
            dry_run=dry_run,
        )
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Finished setting up editors.",
            dry_run=dry_run,
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate and symlink subscribed editor settings.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without applying them",
    )
    parser.add_argument(
        "--which",
        action="append",
        choices=sorted(EDITORS),
        default=[],
        metavar="EDITOR",
        help="Apply one subscribed editor. Can be passed multiple times",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Apply all subscribed editors from `this-system.toml`",
    )
    args = parser.parse_args()
    include_all = cast(bool, args.all)
    requested_editor_keys = tuple(
        cast(
            list[str],
            args.which,
        ),
    )
    dry_run = cast(bool, args.dry_run)
    if include_all and requested_editor_keys:
        parser.error("`--all` cannot be combined with `--which`")
    if not include_all and not requested_editor_keys:
        parser.error("pass `--all` or at least one `--which`")
    profile = load_profiles.load_profile(required=True)
    if profile is None:
        parser.error("`this-system.toml` is required")
    editor_keys = resolve_selected_editors(
        subscribed_editor_keys=profile.editors,
        requested_editor_keys=requested_editor_keys,
        include_all=include_all,
    )
    run(
        dry_run=dry_run,
        editor_keys=editor_keys,
    )


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()

## } SCRIPT
