## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
import datetime
import re
import socket

from dataclasses import dataclass
from pathlib import Path
from typing import cast

## local
from local_helpers import apply_shell_actions
from local_helpers import log_messages
from local_helpers import project_dirs

##
## === GLOBAL PARAMS
##

SCRIPT_NAME = Path(__file__).name
SSH_DIR = project_dirs.TARGETS.ssh
NOTES_DIR = project_dirs.TARGETS.ssh_notes

LOG_MESSAGE = log_messages.make_logger_fn(SCRIPT_NAME)
FAIL_WITH_MESSAGE = log_messages.make_fail_fn(SCRIPT_NAME)

##
## === DATA MODELS
##


@dataclass(frozen=True)
class Inputs:
    """Resolved inputs needed to generate a key and write its notes file."""

    name: str
    purpose: str
    device: str
    today: str
    comment: str
    key_file: Path
    pub_file: Path
    notes_file: Path


##
## === CLI
##


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=(
            "Generate a new ed25519 SSH key with a standardised comment, and "
            "write a notes file under ~/.ssh/notes/ containing the public key "
            "and a placeholder ~/.ssh/config block you can copy. Never modifies "
            "~/.ssh/config or pushes the key to any remote."
        ),
    )
    parser.add_argument(
        "--name",
        required=True,
        help="suffix for ~/.ssh/id_ed25519_NAME",
    )
    parser.add_argument(
        "--purpose",
        required=True,
        help="short description of what the key is for",
    )
    parser.add_argument(
        "--device",
        help="device the key is from (default: hostname)",
    )
    return parser.parse_args()


##
## === PIPELINE STEPS
##


def ensure_name_is_valid(
    name: str,
) -> None:
    name_pattern = re.compile(r"^[A-Za-z0-9_-]+$")
    if not name_pattern.fullmatch(name):
        FAIL_WITH_MESSAGE(f"`--name` must be alphanumeric, dash, or underscore; got `{name}`.")


def collect_inputs(
    *,
    name: str,
    purpose: str,
    device: str,
) -> Inputs:
    LOG_MESSAGE("Resolving inputs")
    today = datetime.date.today().strftime("%Y-%m-%d")
    key_file = SSH_DIR / f"id_ed25519_{name}"
    pub_file = key_file.with_suffix(".pub")
    notes_file = NOTES_DIR / f"{name}-{today}.txt"
    comment = f"for {purpose} from {device} created on {today}"
    return Inputs(
        name=name,
        purpose=purpose,
        device=device,
        today=today,
        comment=comment,
        key_file=key_file,
        pub_file=pub_file,
        notes_file=notes_file,
    )


def ensure_ssh_dir() -> None:
    SSH_DIR.mkdir(
        mode=0o700,
        exist_ok=True,
    )
    SSH_DIR.chmod(0o700)
    LOG_MESSAGE(f"{SSH_DIR} ok")


def print_summary(
    *,
    inputs: Inputs,
) -> None:
    LOG_MESSAGE("Summary:")
    print(f"  Name:     {inputs.name}")
    print(f"  Purpose:  {inputs.purpose}")
    print(f"  Device:   {inputs.device}")
    print(f"  Date:     {inputs.today}")
    print(f"  Key file: {inputs.key_file}")
    print(f"  Comment:  {inputs.comment}")
    print(f"  Notes:    {inputs.notes_file}")


def generate_key(
    *,
    key_file: Path,
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
    succeeded = apply_shell_actions.run_command(
        args=command,
        logger_fn=LOG_MESSAGE,
        description=f"generate ed25519 ssh key at {key_file}",
        capture_output=False,
    )
    if not succeeded:
        FAIL_WITH_MESSAGE("ssh-keygen failed")
    key_file.chmod(0o600)
    LOG_MESSAGE(f"Key created at {key_file}")


def write_notes(
    *,
    inputs: Inputs,
) -> None:
    NOTES_DIR.mkdir(
        mode=0o700,
        exist_ok=True,
    )
    NOTES_DIR.chmod(0o700)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    public_key = inputs.pub_file.read_text().rstrip("\n")
    inputs.notes_file.write_text(
        f"# SSH Key Notes: {inputs.name}\n"
        f"# Created: {timestamp}\n"
        f"\n"
        f"## Key files\n"
        f"{inputs.key_file}   (private; never share)\n"
        f"{inputs.pub_file}   (public)\n"
        f"\n"
        f"## Public key\n"
        f"{public_key}\n"
        f"\n"
        f"## Keygen command\n"
        f'ssh-keygen -t ed25519 -a 100 -f "{inputs.key_file}" -C "{inputs.comment}"\n'
        f"\n"
        f"## Suggested ~/.ssh/config block (fill in placeholders)\n"
        f"Host <ALIAS>\n"
        f"  HostName <REMOTE_HOST>\n"
        f"  User <REMOTE_USER>\n"
        f"  IdentityFile {inputs.key_file}\n"
        f"  IdentitiesOnly yes\n"
        f"\n"
        f"## Suggested upload command (fill in placeholders)\n"
        f"ssh-copy-id -i {inputs.pub_file} <REMOTE_USER>@<REMOTE_HOST>\n"
        f"## Or upload the public key manually (e.g. via FreeIPA or GitHub web UI).\n"
        f"\n"
        f"## Verify\n"
        f"ssh <ALIAS>\n",
    )
    inputs.notes_file.chmod(0o600)
    LOG_MESSAGE(f"Notes saved to {inputs.notes_file}")


##
## === MAIN ROUTINE
##


def main() -> int:
    args = parse_args()
    arg_name = cast(str, args.name)
    arg_purpose = cast(str, args.purpose)
    arg_device = cast(str | None, args.device)

    ensure_name_is_valid(arg_name)

    key_file = SSH_DIR / f"id_ed25519_{arg_name}"
    if key_file.exists():
        LOG_MESSAGE(f"Key already exists at {key_file}. Nothing to do.")
        return 0

    inputs = collect_inputs(
        name=arg_name,
        purpose=arg_purpose,
        device=arg_device or socket.gethostname(),
    )
    ensure_ssh_dir()
    print_summary(inputs=inputs)
    generate_key(
        key_file=inputs.key_file,
        comment=inputs.comment,
    )
    write_notes(inputs=inputs)
    LOG_MESSAGE("Done")
    return 0


##
## === ENTRY POINT
##

if __name__ == "__main__":
    raise SystemExit(main())

## } SCRIPT
