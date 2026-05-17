## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
import datetime
import re
import socket
import subprocess
import sys

from pathlib import Path
from typing import NoReturn, cast

##
## === SCRIPT CONFIG
##

SCRIPT_NAME = Path(__file__).name
HOME_DIR = Path.home()
SSH_DIR = HOME_DIR / ".ssh"
NOTES_DIR = SSH_DIR / "notes"
NAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")

## --- colours, only when stdout is a tty
_IS_TTY = sys.stdout.isatty()
_BOLD = "\033[1m" if _IS_TTY else ""
_CYAN = "\033[36m" if _IS_TTY else ""
_YELLOW = "\033[33m" if _IS_TTY else ""
_RED = "\033[31m" if _IS_TTY else ""
_GREEN = "\033[32m" if _IS_TTY else ""
_DIM = "\033[2m" if _IS_TTY else ""
_RESET = "\033[0m" if _IS_TTY else ""

##
## === OUTPUT HELPERS
##


def heading(
    message: str,
) -> None:
    print(f"\n{_BOLD}{_CYAN}==> {message}{_RESET}")


def info(
    message: str,
) -> None:
    print(f"{_DIM}{message}{_RESET}")


def warn(
    message: str,
) -> None:
    print(f"{_YELLOW}!! {message}{_RESET}", file=sys.stderr)


def success(
    message: str,
) -> None:
    print(f"{_GREEN}OK{_RESET} {message}")


def fail(
    message: str,
) -> NoReturn:
    print(f"{_RED}ERROR: {message}{_RESET}", file=sys.stderr)
    sys.exit(1)


##
## === PROMPT HELPERS
##


def prompt_required(
    label: str,
    *,
    default: str | None = None,
) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        response = input(f"{label}{suffix}: ").strip()
        if response:
            return response
        if default is not None:
            return default
        warn("value required")


def prompt_optional(
    label: str,
) -> str:
    return input(f"{label} (press Enter to skip): ").strip()


def prompt_yes_no(
    label: str,
    *,
    default_yes: bool = False,
) -> bool:
    suffix = "[Y/n]" if default_yes else "[y/N]"
    response = input(f"{label} {suffix}: ").strip().lower()
    if not response:
        return default_yes
    return response.startswith("y")


##
## === ARG PARSER
##


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=(
            "Generate a new ed25519 SSH key with a standardised comment. "
            "Optionally write a notes file under ~/.ssh/notes/ containing the "
            "public key, suggested ~/.ssh/config block, and upload commands "
            "for later reference. Never modifies ~/.ssh/config or pushes the "
            "key to any remote."
        ),
    )
    parser.add_argument("--name", help="suffix for ~/.ssh/id_ed25519_NAME")
    parser.add_argument("--purpose", help="short description of what the key is for")
    parser.add_argument("--device", help="device the key is from (default: hostname)")
    parser.add_argument("--host", help="remote hostname (used in notes file only)")
    parser.add_argument("--user", help="remote username (used in notes file only)")
    parser.add_argument("--alias", help="ssh config Host alias (default: --name)")
    parser.add_argument(
        "--notes",
        action="store_true",
        help="write a notes file without prompting",
    )
    parser.add_argument(
        "--no-notes",
        action="store_true",
        help="skip notes file without prompting",
    )
    return parser


##
## === PRE-FLIGHT
##


def ensure_ssh_dir() -> None:
    SSH_DIR.mkdir(
        mode=0o700,
        exist_ok=True,
    )
    SSH_DIR.chmod(0o700)


##
## === GENERATE KEY
##


def generate_key(
    key_file: Path,
    *,
    comment: str,
) -> None:
    command = [
        "ssh-keygen",
        "-t",
        "ed25519",
        "-a",
        "100",
        "-f",
        str(key_file),
        "-C",
        comment,
    ]
    info(" ".join(command))
    subprocess.run(
        command,
        check=True,
    )
    key_file.chmod(0o600)
    success(f"key created at {key_file}")


##
## === WRITE NOTES
##


def build_config_block(
    *,
    alias: str,
    host: str,
    user: str,
    key_file: Path,
) -> str:
    return (
        f"Host {alias}\n"
        f"  HostName {host or '<REMOTE_HOST>'}\n"
        f"  User {user or '<REMOTE_USER>'}\n"
        f"  IdentityFile {key_file}\n"
        f"  IdentitiesOnly yes"
    )


def write_notes(
    *,
    notes_file: Path,
    name: str,
    key_file: Path,
    pub_file: Path,
    comment: str,
    host: str,
    user: str,
    alias: str,
) -> None:
    NOTES_DIR.mkdir(
        mode=0o700,
        exist_ok=True,
    )
    NOTES_DIR.chmod(0o700)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    public_key = pub_file.read_text().rstrip("\n")
    config_block = build_config_block(
        alias=alias,
        host=host,
        user=user,
        key_file=key_file,
    )
    upload_target = f"{user or '<REMOTE_USER>'}@{host or '<REMOTE_HOST>'}"
    notes_file.write_text(
        f"# SSH Key Notes: {name}\n"
        f"# Created: {timestamp}\n"
        f"\n"
        f"## Key files\n"
        f"{key_file}   (private; never share)\n"
        f"{pub_file}   (public)\n"
        f"\n"
        f"## Public key\n"
        f"{public_key}\n"
        f"\n"
        f"## Keygen command\n"
        f'ssh-keygen -t ed25519 -a 100 -f "{key_file}" -C "{comment}"\n'
        f"\n"
        f"## Suggested ~/.ssh/config block\n"
        f"{config_block}\n"
        f"\n"
        f"## Suggested upload command\n"
        f"ssh-copy-id -i {pub_file} {upload_target}\n"
        f"## Or upload the public key manually (e.g. via FreeIPA or GitHub web UI).\n"
        f"\n"
        f"## Verify\n"
        f"ssh {alias}\n",
    )
    notes_file.chmod(0o600)
    success(f"notes saved to {notes_file}")


##
## === PROGRAM MAIN
##


def main() -> None:
    args = build_arg_parser().parse_args()
    arg_name = cast(str | None, args.name)
    arg_purpose = cast(str | None, args.purpose)
    arg_device = cast(str | None, args.device)
    arg_host = cast(str | None, args.host)
    arg_user = cast(str | None, args.user)
    arg_alias = cast(str | None, args.alias)
    arg_notes = cast(bool, args.notes)
    arg_no_notes = cast(bool, args.no_notes)

    if arg_notes and arg_no_notes:
        fail("--notes and --no-notes are mutually exclusive")

    heading("Gather inputs")
    name = arg_name or prompt_required("Unique name (suffix for id_ed25519_<name>)")
    if not NAME_PATTERN.fullmatch(name):
        fail(f"name must be alphanumeric, dash, or underscore (got: {name})")

    key_file = SSH_DIR / f"id_ed25519_{name}"
    if key_file.exists():
        info(f"Key already exists at {key_file}. Nothing to do.")
        return

    purpose = arg_purpose or prompt_required("Purpose")
    device = arg_device or prompt_required("Device", default=socket.gethostname())

    if arg_notes:
        will_write_notes = True
    elif arg_no_notes:
        will_write_notes = False
    else:
        will_write_notes = prompt_yes_no(
            "Write a notes file with the public key and config snippet?",
            default_yes=True,
        )

    host = arg_host or ""
    user = arg_user or ""
    alias = arg_alias or name
    if will_write_notes:
        if not host:
            host = prompt_optional("Remote host")
        if not user:
            user = prompt_optional("Remote user")

    today = datetime.date.today().strftime("%Y-%m-%d")
    pub_file = key_file.with_suffix(".pub")
    notes_file = NOTES_DIR / f"{name}-{today}.txt"
    comment = f"for {purpose} from {device} created on {today}"

    heading("Pre-flight")
    ensure_ssh_dir()
    info(f"{SSH_DIR} ok")

    heading("Summary")
    print(f"  Name:     {name}")
    print(f"  Purpose:  {purpose}")
    print(f"  Device:   {device}")
    print(f"  Date:     {today}")
    print(f"  Key file: {key_file}")
    print(f"  Comment:  {comment}")
    if will_write_notes:
        print(f"  Notes:    {notes_file}")
        print(f"  Alias:    {alias}")
        print(f"  Host:     {host or '(not set; placeholder used in notes)'}")
        print(f"  User:     {user or '(not set; placeholder used in notes)'}")
    if not prompt_yes_no("Proceed?"):
        fail("aborted")

    heading("Generate key")
    generate_key(
        key_file,
        comment=comment,
    )

    if will_write_notes:
        heading("Write notes")
        write_notes(
            notes_file=notes_file,
            name=name,
            key_file=key_file,
            pub_file=pub_file,
            comment=comment,
            host=host,
            user=user,
            alias=alias,
        )

    heading("Done")


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()

## } SCRIPT
