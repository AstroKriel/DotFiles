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
CONFIG_FILE = SSH_DIR / "config"
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


def heading(message: str) -> None:
    print(f"\n{_BOLD}{_CYAN}==> {message}{_RESET}")


def info(message: str) -> None:
    print(f"{_DIM}{message}{_RESET}")


def warn(message: str) -> None:
    print(f"{_YELLOW}!! {message}{_RESET}", file=sys.stderr)


def success(message: str) -> None:
    print(f"{_GREEN}OK{_RESET} {message}")


def fail(message: str) -> NoReturn:
    print(f"{_RED}ERROR: {message}{_RESET}", file=sys.stderr)
    sys.exit(1)


##
## === PROMPT HELPERS
##


def prompt_required(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        response = input(f"{label}{suffix}: ").strip()
        if response:
            return response
        if default is not None:
            return default
        warn("value required")


def prompt_yes_no(label: str, default_yes: bool = False) -> bool:
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
            "Generate a new ed25519 SSH key with a standardised comment, "
            "optionally append a ~/.ssh/config entry, push the public key, "
            "and write a notes file under ~/.ssh/notes/."
        ),
    )
    parser.add_argument("--name", help="suffix for ~/.ssh/id_ed25519_NAME")
    parser.add_argument("--purpose", help="short description of what the key is for")
    parser.add_argument("--device", help="device the key is from (default: hostname)")
    parser.add_argument("--host", help="remote hostname")
    parser.add_argument("--user", help="remote username")
    parser.add_argument("--alias", help="~/.ssh/config Host alias (default: --name)")
    parser.add_argument(
        "--upload",
        choices=["ssh-copy-id", "manual", "skip"],
        help="how to deliver the public key",
    )
    parser.add_argument("--upload-url", help="URL to display in manual mode")
    parser.add_argument(
        "--no-config",
        action="store_true",
        help="skip the ~/.ssh/config block",
    )
    return parser


##
## === PRE-FLIGHT
##


def ensure_ssh_dir() -> None:
    SSH_DIR.mkdir(mode=0o700, exist_ok=True)
    SSH_DIR.chmod(0o700)


def check_key_collision(key_file: Path, pub_file: Path) -> None:
    if not key_file.exists():
        return
    if not prompt_yes_no(f"Key {key_file} already exists. Overwrite?"):
        fail("aborted (key file exists)")
    key_file.unlink(missing_ok=True)
    pub_file.unlink(missing_ok=True)


def check_alias_collision(alias: str) -> None:
    if not CONFIG_FILE.exists():
        return
    pattern = re.compile(rf"^\s*Host\s+{re.escape(alias)}(\s|$)", re.MULTILINE)
    if not pattern.search(CONFIG_FILE.read_text()):
        return
    warn(f"an entry with Host '{alias}' already exists in {CONFIG_FILE}")
    if not prompt_yes_no("Continue anyway (you may need to clean up the duplicate)?"):
        fail("aborted (config alias collision)")


##
## === STEP 1: GENERATE KEY
##


def generate_key(key_file: Path, comment: str) -> None:
    command = [
        "ssh-keygen",
        "-t", "ed25519",
        "-a", "100",
        "-f", str(key_file),
        "-C", comment,
    ]
    info(" ".join(command))
    subprocess.run(command, check=True)
    key_file.chmod(0o600)
    success(f"key created at {key_file}")


##
## === STEP 2: CONFIG BLOCK
##


def build_config_block(alias: str, host: str, user: str, key_file: Path) -> str:
    return (
        f"Host {alias}\n"
        f"  HostName {host}\n"
        f"  User {user}\n"
        f"  IdentityFile {key_file}\n"
        f"  IdentitiesOnly yes"
    )


def maybe_append_config(config_block: str) -> bool:
    print(config_block + "\n")
    if not prompt_yes_no(f"Append this block to {CONFIG_FILE}?", default_yes=True):
        info("skipped (block saved to notes file)")
        return False
    with CONFIG_FILE.open("a") as config_stream:
        config_stream.write(f"\n{config_block}\n")
    CONFIG_FILE.chmod(0o600)
    success(f"appended to {CONFIG_FILE}")
    return True


##
## === STEP 3: UPLOAD
##


def prompt_upload_mode() -> str:
    print("  1) ssh-copy-id   (push to remote with current password)")
    print("  2) manual        (display key; you paste it elsewhere)")
    print("  3) skip")
    choice = input("Choose [1/2/3]: ").strip()
    mode_map = {"1": "ssh-copy-id", "2": "manual", "3": "skip", "": "skip"}
    mode = mode_map.get(choice)
    if mode is None:
        fail(f"invalid choice: {choice}")
    return mode


def do_upload(
    *,
    mode: str,
    pub_file: Path,
    host: str,
    user: str,
    url: str | None,
) -> str:
    if mode == "ssh-copy-id":
        if not (host and user):
            fail("ssh-copy-id needs --host and --user")
        heading("Step 3: Push key with ssh-copy-id")
        command = ["ssh-copy-id", "-i", str(pub_file), f"{user}@{host}"]
        info(" ".join(command))
        result = subprocess.run(command, check=False)
        if result.returncode == 0:
            success("key pushed")
            return f"pushed via ssh-copy-id to {user}@{host}"
        warn("ssh-copy-id returned non-zero; retry or upload manually")
        return "ssh-copy-id failed; verify manually"
    if mode == "manual":
        heading("Step 3: Manual upload")
        if url:
            print(f"Open: {url}\n")
        print("Paste this public key:\n")
        print(pub_file.read_text())
        return f"manual upload{f' at {url}' if url else ''}"
    if mode == "skip":
        heading("Step 3: Upload skipped")
        return "skipped"
    fail(f"unknown --upload mode: {mode}")


##
## === STEP 4: WRITE NOTES
##


def write_notes(
    *,
    notes_file: Path,
    name: str,
    key_file: Path,
    pub_file: Path,
    comment: str,
    config_block: str,
    config_appended: bool,
    upload_result: str,
    verify_command: str,
) -> None:
    NOTES_DIR.mkdir(mode=0o700, exist_ok=True)
    NOTES_DIR.chmod(0o700)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    public_key = pub_file.read_text().rstrip("\n")
    if config_block:
        appended_note = f"appended to {CONFIG_FILE}" if config_appended else "not appended"
        config_section = f"{config_block}\n({appended_note})"
    else:
        config_section = "(none)"
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
        f"## SSH config entry\n"
        f"{config_section}\n"
        f"\n"
        f"## Upload\n"
        f"{upload_result}\n"
        f"\n"
        f"## Verify\n"
        f"{verify_command}\n",
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
    arg_upload = cast(str | None, args.upload)
    arg_upload_url = cast(str | None, args.upload_url)
    arg_no_config = cast(bool, args.no_config)

    heading("Gather inputs")
    name = arg_name or prompt_required("Unique name (suffix for id_ed25519_<name>)")
    if not NAME_PATTERN.fullmatch(name):
        fail(f"name must be alphanumeric, dash, or underscore (got: {name})")
    purpose = arg_purpose or prompt_required("Purpose")
    device = arg_device or prompt_required("Device", socket.gethostname())
    alias = arg_alias or prompt_required("SSH config alias", name)

    needs_remote = not (arg_no_config and arg_upload == "skip")
    host = arg_host or ""
    user = arg_user or ""
    if needs_remote:
        if not host:
            host = prompt_required("Remote host")
        if not user:
            user = prompt_required("Remote user")

    today = datetime.date.today().strftime("%Y-%m-%d")
    key_file = SSH_DIR / f"id_ed25519_{name}"
    pub_file = key_file.with_suffix(".pub")
    notes_file = NOTES_DIR / f"{name}-{today}.txt"
    comment = f"for {purpose} from {device} created on {today}"

    heading("Pre-flight checks")
    ensure_ssh_dir()
    info(f"{SSH_DIR} ok")
    check_key_collision(key_file, pub_file)
    check_alias_collision(alias)

    heading("Summary")
    print(f"  Name:     {name}")
    print(f"  Purpose:  {purpose}")
    print(f"  Device:   {device}")
    print(f"  Date:     {today}")
    print(f"  Key file: {key_file}")
    print(f"  Comment:  {comment}")
    if host:
        print(f"  Host:     {host}")
        print(f"  User:     {user}")
        print(f"  Alias:    {alias}")
    if not prompt_yes_no("Proceed?"):
        fail("aborted")

    heading("Step 1: Generate key")
    generate_key(key_file, comment)

    config_block = ""
    config_appended = False
    if host and not arg_no_config:
        heading("Step 2: ~/.ssh/config entry")
        config_block = build_config_block(alias, host, user, key_file)
        config_appended = maybe_append_config(config_block)

    upload_mode = arg_upload
    if upload_mode is None:
        heading("Step 3: Upload public key")
        upload_mode = prompt_upload_mode()
    upload_result = do_upload(
        mode=upload_mode,
        pub_file=pub_file,
        host=host,
        user=user,
        url=arg_upload_url,
    )

    if host and config_appended:
        verify_command = f"ssh {alias}"
    elif host:
        verify_command = f"ssh -i {key_file} {user}@{host}"
    else:
        verify_command = "(no remote configured)"

    heading("Step 4: Write notes")
    write_notes(
        notes_file=notes_file,
        name=name,
        key_file=key_file,
        pub_file=pub_file,
        comment=comment,
        config_block=config_block,
        config_appended=config_appended,
        upload_result=upload_result,
        verify_command=verify_command,
    )

    heading("Done")
    print(f"Run `{verify_command}` to test.")


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()

## } SCRIPT
