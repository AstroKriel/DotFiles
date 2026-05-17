## { MODULE

from pathlib import Path
from setup_scripts._extras.config import ExtraConfig, EXTRAS_DIR

EXTRAS: dict[str, ExtraConfig] = {
    "hpc/pbs.sh":
    ExtraConfig(
        name="PBS scheduler aliases",
        source_path=EXTRAS_DIR / "hpc" / "pbs.sh",
        target_path=Path.home() / ".shell_hpc",
        requires=("linux", "remote", "hpc", "pbs"),
    ),
    "hpc/slurm.sh":
    ExtraConfig(
        name="Slurm scheduler aliases",
        source_path=EXTRAS_DIR / "hpc" / "slurm.sh",
        target_path=Path.home() / ".shell_hpc",
        requires=("linux", "remote", "hpc", "slurm"),
    ),
}

## } MODULE
