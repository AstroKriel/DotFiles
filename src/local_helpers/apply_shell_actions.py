## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from pathlib import Path
import subprocess
from typing import Callable, cast

## local
from local_helpers import log_messages

##
## === PUBLIC ACTIONS
##


def run_command(
    *,
    args: list[str],
    log: Callable[[str], None],
    description: str,
    dry_run: bool = False,
    capture_output: bool = True,
) -> bool:
    """Run a shell command with logging; return `True` on success, `False` on failure."""
    if dry_run:
        log(f"[dry-run] Would run: {description}")
        return True
    log(f"Running: {description}")
    try:
        subprocess.run(
            args=args,
            check=True,
            capture_output=capture_output,
            text=capture_output,
        )
        log(f"Done: {description}")
        return True
    except subprocess.CalledProcessError as error:
        stderr_value = cast(object, error.stderr)
        stderr = stderr_value if isinstance(stderr_value, str) else ""
        error_output = stderr.strip() if (capture_output and stderr) else "(no output captured)"
        log(f"Failed: {description}\n{error_output}")
        return False


def ensure_dir_exists(
    *,
    directory: Path,
    log: Callable[[str], None],
    dry_run: bool = False,
) -> None:
    """Ensure that the directory exists; create it if it does not."""
    if directory.exists():
        return
    if dry_run:
        log(f"[dry-run] Would create directory: {directory}")
    else:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )
        log(f"Created directory: {directory}")


def backup_file(
    *,
    target_path: Path,
    log: Callable[[str], None],
    dry_run: bool = False,
) -> Path | None:
    """
    Backup a file or symlink at the given path.

    If the target is a symlink, remove it. If it is a real file or directory, rename it with a timestamp.
    Return the backup path if a rename was performed, otherwise return None.
    """
    if not target_path.exists() and not target_path.is_symlink():
        return None
    if target_path.is_symlink():
        try:
            resolved = target_path.resolve()
            log(
                log_messages.format_dry_run(
                    message=f"{target_path} (symlink) -> {resolved}",
                    dry_run=dry_run,
                ),
            )
        except Exception as error:
            log(f"Warning: failed to resolve symlink {target_path}: {error}")
        if dry_run:
            log(f"[dry-run] Would remove symlink: {target_path}")
        else:
            target_path.unlink()
            log(f"Removed symlink: {target_path}")
        return None
    backup_path = _rename_with_timestamp(
        target_path=target_path,
        log=log,
        dry_run=dry_run,
    )
    if backup_path:
        log(
            log_messages.format_dry_run(
                message=f"{target_path} -> {backup_path}",
                dry_run=dry_run,
            ),
        )
    return backup_path


def create_symlink(
    *,
    source_path: Path,
    target_path: Path,
    log: Callable[[str], None],
    dry_run: bool = False,
) -> None:
    """Create a symlink from `target_path` to `source_path`; back up existing files first."""
    if not source_path.exists():
        log(f"Skipping. {source_path} does not exist.")
        return
    if _path_is_missing(target_path):
        _make_symlink(
            source_path=source_path,
            target_path=target_path,
            log=log,
            dry_run=dry_run,
        )
        return
    if _already_linked_correctly(
            target_path=target_path,
            source_path=source_path,
    ):
        log(
            log_messages.format_dry_run(
                message=f"Already correctly linked: {target_path}",
                dry_run=dry_run,
            ),
        )
        return
    if _symlink_is_broken(target_path):
        log(f"Skipping. {target_path} is a broken symlink.")
        return
    if not _types_match(
            source_path=source_path,
            target_path=target_path,
    ):
        log(
            f"Skipping due to a type mismatch. {target_path} is {_get_path_type(target_path)}, "
            f"but source is {_get_path_type(source_path)}.",
        )
        return
    backup_file(
        target_path=target_path,
        log=log,
        dry_run=dry_run,
    )
    _make_symlink(
        source_path=source_path,
        target_path=target_path,
        log=log,
        dry_run=dry_run,
    )


def remove_symlink(
    *,
    target_path: Path,
    log: Callable[[str], None],
    dry_run: bool = False,
) -> None:
    """Remove a symlink at the given path; do nothing if the path is not a symlink."""
    if not target_path.is_symlink():
        return
    if dry_run:
        log(f"[dry-run] Would remove symlink: {target_path}")
    else:
        target_path.unlink()
        log(f"Removed symlink: {target_path}")


##
## === INTERNAL HELPERS
##


def _rename_with_timestamp(
    *,
    target_path: Path,
    log: Callable[[str], None],
    dry_run: bool = False,
) -> Path | None:
    """Rename a file or directory in place by appending a timestamp; return the new path or None."""
    if not target_path.exists() and not target_path.is_symlink():
        return None
    timestamp = log_messages.get_timestamp().replace(" ", ".")
    backup_path = target_path.with_stem(f"{target_path.stem}.{timestamp}")
    if dry_run:
        log(f"[dry-run] Would rename {target_path} -> {backup_path}")
    else:
        log(f"Renaming {target_path} -> {backup_path}")
        target_path.rename(backup_path)
    return backup_path


def _path_is_missing(
    path: Path,
) -> bool:
    """Return `True` iff the path does not exist and is not a symlink."""
    return not path.exists() and not path.is_symlink()


def _symlink_is_broken(
    path: Path,
) -> bool:
    """Return `True` iff the path is a symlink but its target does not exist."""
    return path.is_symlink() and not path.exists()


def _get_path_type(
    path: Path,
) -> str:
    """Return a description of the path type: file, dir, symlink, broken symlink, or unknown."""
    if path.is_dir():
        return "dir"
    elif path.is_file():
        return "file"
    elif path.is_symlink():
        return "broken symlink" if not path.exists() else "symlink"
    return "unknown"


def _make_symlink(
    *,
    source_path: Path,
    target_path: Path,
    log: Callable[[str], None],
    dry_run: bool,
) -> None:
    """Create a symlink from `target_path` to `source_path`."""
    if dry_run:
        log(f"[dry-run] Would symlink: {source_path} -> {target_path}")
    else:
        target_path.symlink_to(source_path)
        log(f"Symlinked: {source_path} -> {target_path}")


def _already_linked_correctly(
    *,
    target_path: Path,
    source_path: Path,
) -> bool:
    """Return `True` iff the target is a symlink that resolves to the given source path."""
    try:
        return target_path.is_symlink() and (target_path.resolve() == source_path.resolve())
    except Exception:
        return False


def _types_match(
    *,
    source_path: Path,
    target_path: Path,
) -> bool:
    """Return `True` iff both paths point to the same type (file or dir)."""
    if source_path.is_file() and target_path.is_file():
        return True
    if source_path.is_dir() and target_path.is_dir():
        return True
    return False


## } MODULE
