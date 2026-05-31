# HPC Workflow

Conventions for working on HPC clusters: onboarding, module loading, job submission, and data management.

---

## Storage Tiers

Clusters vary in what storage tiers they provide and what they are called. The concepts below are used throughout this file; the actual paths for a specific cluster are recorded in its `README.md` under `ProjectNotes/hpcs/<cluster>/`.

| Concept | Role | Typical names |
|---|---|---|
| `home` | Persistent, backed up, small quota; for configs and code checkouts | `/home/<user>` |
| `fast-storage` | High-throughput, large capacity, not backed up; for active runs and outputs | `scratch`, `work`, `lustre`, `nobackup` |
| `project` | Shared with collaborators, larger quota; not available on all clusters | `project`, `group` |

When working on a specific cluster, resolve these concepts from the cluster notes before acting.

---

## Onboarding a New Cluster

When access to a new cluster is gained:

1. Create the cluster notes at `~/Documents/ProjectNotes/hpcs/<cluster>/` following `../maintaining-notes/hpc.md`
2. Add a host entry to `~/.ssh/config` per `./ssh.md`
3. Log in and identify the available storage tiers; map each to its actual path
4. Survey the module environment: compiler toolchain, MPI, HDF5/parallel I/O stack
5. Submit a minimal test job to verify scheduling and I/O work
6. Record the storage tier paths and working module stack in the cluster `README.md`

---

## Job Scripts

Directives are scheduler-specific (SLURM uses `#SBATCH`, PBS uses `#PBS`); check the cluster `README.md` for the scheduler type.

**Naming:** `<project>-<descriptor>`, short enough to read in the queue. Examples: `kriel-mhd-512`, `kriel-cs-test`.

**Working directory:** set explicitly to the run directory using `--chdir` (SLURM) or `-d` (PBS). Do not rely on submission directory or home directory defaults.

**Module loading:** always `module purge` before loading. Pin the full module string (name and version) from the cluster `README.md` and use it verbatim across all jobs for that cluster. Log any version changes in `log.md`.

---

## Run Directory Layout

Simulations go under `<fast-storage>/<project>/`. Sim directories are grouped by scientific concept; each sim directory is self-contained (no symlinks) so it can be moved or archived without breaking.

| Concept | Role | Name defined by |
|---|---|---|
| `<sim-inputs>` | Config and input files the simulation reads | Code rules |
| `<sim-outputs>` | Raw output written by the simulation | Code rules |
| `<derived>` | Reduced data from analysis tools; what gets transferred locally | Code rules |

```text
<project>/
├── <concept>/
│   └── <sim-name>/
│       ├── jobs/
│       ├── <sim-inputs>
│       ├── logs/
│       ├── <sim-outputs>/
│       └── <derived>/
└── tmp/
```

`jobs/` holds one submission script per workflow step (running the simulation, extracting datasets, post-processing, etc).

`logs/` is the unified place to check on a run: job stdout/stderr (scheduler output and error directives point here) and any sim-level diagnostic output. Code rules document what lands here vs. inside `<sim-outputs>/`.

`tmp/` is for short-lived diagnostic work: quick test runs, exploratory plots. Organise by concept and date: `tmp/<concept>/<YYYYMMDD>-<sub-topic>/`.

Each simulation code's rules define the actual directory names for `<sim-inputs>`, `<sim-outputs>`, and `<derived>`, and how its output maps to these concepts.

---

## Code Deployment

Deploy only what the cluster needs to execute the job: typically the project repo or the relevant `ww-*-sims` interface layer. Record what was deployed and any build steps in the cluster `log.md`.

---

## Data Transfer

Transfer only reduced data to a local machine; never transfer raw output. Use `rsync` and preserve directory structure.
