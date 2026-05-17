## { MODULE

##
## === DEPENDENCIES
##

## stdlib
import datetime
import sys

from pathlib import Path
from typing import Callable, NoReturn

## local
from local_helpers import project_dirs

##
## === MODULE CONFIG
##

LOG_FILE = project_dirs.DIRS.root / "history.log"
_should_write_to_file = True  # dry-runs auto-disable this

##
## === LOG FUNCTIONS
##


def get_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _log_message(
    *,
    script_name: str,
    message: str,
    log_file: Path = LOG_FILE,
) -> None:
    ## get time
    timestamp = get_timestamp()
    log_entry = f"[{timestamp}] ({script_name}): {message}\n"
    print(log_entry)
    if not _should_write_to_file:
        return
    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with open(log_file, "a") as log_stream:
        log_stream.write(log_entry)


def configure_logger(
    *,
    write_to_file: bool,
) -> None:
    global _should_write_to_file
    _should_write_to_file = write_to_file


def format_dry_run(
    *,
    message: str,
    dry_run: bool,
) -> str:
    if dry_run:
        return f"[dry-run] {message}"
    return message


def make_logger_fn(
    script_name: str,
) -> Callable[[str], None]:

    def _log(
        message: str,
    ) -> None:
        _log_message(
            script_name=script_name,
            message=message,
        )

    return _log


def make_fail_fn(
    script_name: str,
) -> Callable[[str], NoReturn]:

    def _fail(
        message: str,
    ) -> NoReturn:
        _log_message(
            script_name=script_name,
            message=f"ERROR: {message}",
        )
        sys.exit(1)

    return _fail


## } MODULE
