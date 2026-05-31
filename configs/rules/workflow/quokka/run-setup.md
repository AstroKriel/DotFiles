# Quokka: HPC Run Setup

How a Quokka run maps onto the standard run directory structure from `workflow/remote-work/hpc.md`.

---

## Directory Mapping

| Concept | Quokka name | Notes |
|---|---|---|
| `<sim-inputs>` | `<problem>.toml` | TOML input file for the problem |
| `<sim-outputs>` | `plotfiles/` | AMReX HDF5 plotfiles |
| `<derived>` | `derived/` | Extracted data from `ww-quokka-sims` diagnostic commands |

```text
sims/<sim-name>/
├── jobs/
│   ├── sim.sh
│   └── extract.sh
├── <problem>.toml
├── logs/
├── plotfiles/
└── derived/
```

---

## TOML Configuration

Point AMReX output to `plotfiles/` in the run TOML:

```toml
amr.plot_file = "plotfiles/plt"
```

AMReX writes `plotfiles/plt00000`, `plotfiles/plt00001`, etc.

---

## Logs

AMReX writes timestep and solver progress to stdout, captured into `logs/` by the scheduler output directive. AMReX profiling output (`ProfData_*`) lands in the working directory; with `--chdir`/`-d` set to the run directory, this goes to the run root rather than `logs/`.

---

## Job Steps

| Script | Purpose |
|---|---|
| `jobs/sim.sh` | Run the Quokka executable with the problem TOML |
| `jobs/extract.sh` | Run `ww-quokka-sims` diagnostics; output goes to `derived/` |
