## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
import datetime
import re

from dataclasses import dataclass, field
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
SSH_CONFIG_DIR = project_dirs.TARGETS.ssh
SSH_RECORDS_DIR = project_dirs.SSH_RECORDS

LOG_MESSAGE = log_messages.make_logger_fn(SCRIPT_NAME)
FAIL_WITH_MESSAGE = log_messages.make_fail_fn(SCRIPT_NAME)

##
## === DATA MODELS
##


@dataclass
class SSHKeyConfig:
    name: str
    purpose: str
    device: str
    today: str = field(init=False)
    comment: str = field(init=False)
    file_path: Path = field(init=False)
    pub_file: Path = field(init=False)
    record_file: Path = field(init=False)

    def __post_init__(self) -> None:
        self.today = datetime.date.today().strftime("%Y-%m-%d")
        self.comment = f"for {self.purpose} from {self.device} created on {self.today}"
        self.file_path = SSH_CONFIG_DIR / f"id_ed25519_{self.name}"
        self.pub_file = self.file_path.with_suffix(".pub")
        self.record_file = SSH_RECORDS_DIR / f"{self.name}-{self.today}.txt"


##
## === PIPELINE STEPS
##


def ensure_name_is_valid(
    *,
    name: str,
) -> None:
    valid_pattern = re.compile(r"^[A-Za-z0-9_-]+$")
    if not valid_pattern.fullmatch(name):
        FAIL_WITH_MESSAGE(f"`--name` must be alphanumeric, dash, or underscore; got `{name}`.")


def ensure_ssh_dir() -> None:
    SSH_CONFIG_DIR.mkdir(
        mode=0o700,
        exist_ok=True,
    )
    SSH_CONFIG_DIR.chmod(0o700)
    LOG_MESSAGE(f"{SSH_CONFIG_DIR} ok")


def print_summary(
    *,
    ssh_key_config: SSHKeyConfig,
) -> None:
    LOG_MESSAGE("Summary:")
    LOG_MESSAGE(f"Name: {ssh_key_config.name}")
    LOG_MESSAGE(f"Purpose: {ssh_key_config.purpose}")
    LOG_MESSAGE(f"Device: {ssh_key_config.device}")
    LOG_MESSAGE(f"Date: {ssh_key_config.today}")
    LOG_MESSAGE(f"Key file: {ssh_key_config.file_path}")
    LOG_MESSAGE(f"Comment: {ssh_key_config.comment}")
    LOG_MESSAGE(f"Notes: {ssh_key_config.record_file}")


def generate_key(
    *,
    file_path: Path,
    comment: str,
) -> None:
    command = [
        "ssh-keygen",
        "-t",
        "ed25519",
        "-a",
        "100",
        "-f",
        str(file_path),
        "-C",
        comment,
    ]
    succeeded = apply_shell_actions.run_command(
        args=command,
        logger_fn=LOG_MESSAGE,
        description=f"generate ed25519 ssh key at {file_path}",
        capture_output=False,
    )
    if not succeeded:
        FAIL_WITH_MESSAGE("ssh-keygen failed")
    file_path.chmod(0o600)
    LOG_MESSAGE(f"Key created at {file_path}")


def write_key_record(
    *,
    ssh_key_config: SSHKeyConfig,
) -> None:
    SSH_RECORDS_DIR.mkdir(
        mode=0o700,
        exist_ok=True,
    )
    SSH_RECORDS_DIR.chmod(0o700)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    public_key = ssh_key_config.pub_file.read_text().rstrip("\n")
    ssh_key_config.record_file.write_text(
        f"# SSH Key Notes: {ssh_key_config.name}\n"
        f"# Created: {timestamp}\n"
        f"\n"
        f"## Key files\n"
        f"{ssh_key_config.file_path}   (private; never share)\n"
        f"{ssh_key_config.pub_file}   (public)\n"
        f"\n"
        f"## Public key\n"
        f"{public_key}\n"
        f"\n"
        f"## Keygen command\n"
        f'ssh-keygen -t ed25519 -a 100 -f "{ssh_key_config.file_path}" -C "{ssh_key_config.comment}"\n'
        f"\n"
        f"## Suggested ~/.ssh/config block (fill in placeholders)\n"
        f"Host <ALIAS>\n"
        f"  HostName <REMOTE_HOST>\n"
        f"  User <REMOTE_USER>\n"
        f"  IdentityFile {ssh_key_config.file_path}\n"
        f"  IdentitiesOnly yes\n"
        f"\n"
        f"## Suggested upload command (fill in placeholders)\n"
        f"ssh-copy-id -i {ssh_key_config.pub_file} <REMOTE_USER>@<REMOTE_HOST>\n"
        f"## Or upload the public key manually (e.g. via FreeIPA or GitHub web UI).\n"
        f"\n"
        f"## Verify\n"
        f"ssh <ALIAS>\n",
    )
    ssh_key_config.record_file.chmod(0o600)
    LOG_MESSAGE(f"Notes saved to {ssh_key_config.record_file}")


##
## === MAIN ROUTINE
##


def main() -> None:
    log_messages.configure_logger(write_to_file=True)
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
        required=True,
        help="device the key is from",
    )
    args = parser.parse_args()
    arg_name = cast(str, args.name)
    arg_purpose = cast(str, args.purpose)
    arg_device = cast(str, args.device)
    ensure_name_is_valid(name=arg_name)
    file_path = SSH_CONFIG_DIR / f"id_ed25519_{arg_name}"
    if file_path.exists():
        FAIL_WITH_MESSAGE(f"SSH-Key already exists at {file_path}.")
    ssh_key_config = SSHKeyConfig(
        name=arg_name,
        purpose=arg_purpose,
        device=arg_device,
    )
    ensure_ssh_dir()
    print_summary(ssh_key_config=ssh_key_config)
    generate_key(
        file_path=ssh_key_config.file_path,
        comment=ssh_key_config.comment,
    )
    write_key_record(ssh_key_config=ssh_key_config)
    LOG_MESSAGE(f"Finished creating {file_path}")


##
## === ENTRY POINT
##

if __name__ == "__main__":
    raise SystemExit(main())

## } SCRIPT
