# Quokka: Build and Run

Build, configure, and run Quokka.

---

## Build Directories

Each configuration gets its own named build tree under `build/`. Never share a build tree between configurations. Always pass `-DQUOKKA_PYTHON=OFF`; do not create a Python environment inside `quokka/`. All analysis goes through `ww-quokka-sims/`.

Remove the build directory first when starting fresh. Common configurations:

```bash
cmake -S . -B build/3d-release -G Ninja -DCMAKE_BUILD_TYPE=Release -DAMReX_SPACEDIM=3 -DQUOKKA_PYTHON=OFF
cmake -S . -B build/3d-debug   -G Ninja -DCMAKE_BUILD_TYPE=Debug   -DAMReX_SPACEDIM=3 -DQUOKKA_PYTHON=OFF
cmake -S . -B build/3d-asan    -G Ninja -DCMAKE_BUILD_TYPE=Debug   -DAMReX_SPACEDIM=3 -DQUOKKA_PYTHON=OFF -DENABLE_ASAN=ON
```

When a host needs a non-default toolchain, source `~/.config/quokka/profile.sh` before running CMake or Ninja. Per-host specifics live in `~/Documents/ProjectNotes/hpcs/<host>/`.

---

## The `quokka` Script

`scripts/bash/quokka` is a thin wrapper around CMake, Ninja, and CTest. Use it for listing problems, running tests, and CTest operations. Config and build use raw CMake and Ninja directly.

| Command | What it does |
|---|---|
| `quokka list` | List problem directories under `src/problems/`. |
| `quokka target` | Print the raw CMake target list. |
| `quokka clean` | Remove plotfiles, checkpoints, and output files from `tests/`. |

Typical workflow (after configuring a build tree):

```bash
# Build
ninja -C build/3d-release <ProblemName>

# Run
cd tests && ../build/3d-release/src/problems/<ProblemName>/<ProblemName> ../inputs/<ProblemName>.toml
```

---

## MHD Configuration

### Build requirement

`AMReX_SPACEDIM=3` is mandatory for all MHD problems. A 1D or 2D build silently omits all MHD targets with no warning. Changing `SPACEDIM` requires a fresh build directory.

### TOML parameters

**MHD schemes:**

| Parameter | Values | Notes |
|---|---|---|
| `mhd.emf_compute_scheme` | `"FelkerStone2017"`, `"Balsara2025"`, `"Quokka2026"` | How edge-centred EMFs are computed from face-centred fluxes. |
| `mhd.emf_averaging_scheme` | `"LondrilloDelZanna2004"`, `"Balsara2025"` | How EMFs are averaged at shared edges between adjacent faces. |
| `mhd.resistivity` | float, default `0` | Physical resistivity; enforces parabolic timestep limit `dt < dx^2 / (2 * eta)`. |

**Reconstruction and integration:**

| Parameter | Values | Notes |
|---|---|---|
| `hydro.reconstruction_order` | `2` (PPM), `3` (PPM+), `5` (PPM-EP) | Spatial reconstruction order. |
| `hydro.rk_integrator_order` | `2` | RK2 time integration. Standard for all MHD runs. |
| `hydro.use_dual_energy` | `0` | Disable for MHD. |

**Grid and AMR:**

| Parameter | Recommended | Notes |
|---|---|---|
| `amr.max_level` | `0` | Single-level for most MHD tests. |
| `amr.blocking_factor_x` | `16` | See MPI decomposition below. |
| `amr.max_grid_size` | `128` | See MPI decomposition below. |
| `do_reflux` | `0` | Disable for single-level runs. |
| `do_subcycle` | `0` | Disable for single-level runs. |

### EMF scheme reference

| Compute scheme | Stability | Notes |
|---|---|---|
| `FelkerStone2017` | Most stable | Safe default; well-validated reference. |
| `Balsara2025` | Stable | |
| `Quokka2026` | Least stable | Known to go unstable for the slow wave at high resolution with PPM-EP. |

| Averaging scheme | Notes |
|---|---|
| `LondrilloDelZanna2004` | Standard upwind averaging. |
| `Balsara2025` | |

### MPI decomposition

Setting `amr.blocking_factor_x` to `max(16, nx)` and `amr.max_grid_size` to `nx` forces a single AMReX box at every resolution, making all MPI ranks beyond the first idle with no warning. Always set:

```toml
amr.blocking_factor_x = 16
amr.max_grid_size = 128
```

This allows AMReX to split a 512-cell domain into up to 32 boxes.

### Minimum cell count

The hydro stencil uses `nghost = 4`. A single-box periodic grid below 8 cells per dim has opposite-side ghosts overlapping inside the valid region. Use at least 8 cells per dim under periodic boundary conditions.

### Resistivity

Enable with `mhd.resistivity = <eta>`. The parabolic timestep limit is enforced automatically.

| Rule | |
|---|---|
| No resistivity in Richardson convergence tests | `FastWaveConvergence` and `SlowWaveConvergence` abort if `mhd.resistivity != 0`. Resistivity validation uses `AlfvenWaveLinear`. |
| Reference input | `inputs/AlfvenWaveLinear_resistive.toml` (eta=0.01, grid-aligned, FS17+LD04). |
| Analytic reference | Amplitude decays as `exp(-gamma*t)` where `gamma = eta*k^2/2`. Velocity lags B by `phi = arctan(gamma/omega_real)`. |

---

## HPC Run Setup

Quokka maps onto the standard project layout from `workflow/remote-work/hpc.md`:

| Concept | Quokka name | Notes |
|---|---|---|
| `<sim-inputs>` | `<problem>.toml` | TOML input file for the problem |
| `<sim-outputs>` | `plotfiles/` | AMReX HDF5 plotfiles |
| `<derived>` | `derived/` | Extracted data from `ww-quokka-sims` |

```text
<concept>/<sim-name>/
├── jobs/
│   ├── sim.sh
│   └── extract.sh
├── <problem>.toml
├── logs/
├── plotfiles/
└── derived/
```

Point AMReX output to `plotfiles/` in the run TOML:

```toml
amr.plot_file = "plotfiles/plt"
```

AMReX profiling output (`ProfData_*`) lands in the working directory; with `--chdir`/`-d` set to the run directory, this goes to the run root rather than `logs/`.

| Script | Purpose |
|---|---|
| `jobs/sim.sh` | Run the Quokka executable with the problem TOML |
| `jobs/extract.sh` | Run `ww-quokka-sims` diagnostics; output goes to `derived/` |

---

## Testing

### Pass/fail signal

| Test type | Signal |
|---|---|
| `*Convergence` problems | Exit code from `quokka::richardson::run()`. Nonzero means measured order of accuracy fell below tolerance. |
| All other problems | Exit code `0` on clean integration. Internal asserts trip on NaN, negative pressure, FPE, and similar conditions. |

A clean exit is consistent with a silently broken solver. Always include at least one `*Convergence` problem when validating a build or code change.

### MHD smoke-test set

| Problem | n_cell | stop_time | What it exercises |
|---|---|---|---|
| `AlfvenWaveLinearConvergence` | sweeps `nx` 16..128 | per-resolution | Richardson convergence sweep; the only test with a real correctness signal. |
| `BrioWuShockTube` | `512x16x16` | `0.15` | 1D MHD Riemann problem; shock-capturing baseline. |
| `OrszagTang` | `128x128x8` | `1.0` | 2D MHD vortex; constrained-transport stress test. |

Run each with:

```bash
ninja -C build/3d-release <ProblemName>
cd tests && ../build/3d-release/src/problems/<ProblemName>/<ProblemName> ../inputs/<ProblemName>.toml
```

### Convergence tests

| Rule | |
|---|---|
| Correctness gate | The `*Convergence` problems are the only tests that fail the exit code when the solver is wrong. Treat a nonzero exit as a real regression, not flakiness. |
| Richardson refines nx only | Oblique modes (`num_modes_y != 0` or `num_modes_z != 0`) will not converge under this strategy. The tests abort on nonzero transverse modes. |
| No resistivity | `FastWaveConvergence` and `SlowWaveConvergence` abort if `mhd.resistivity != 0`. |
| MPI decomposition | Set `amr.blocking_factor_x = 16` and `amr.max_grid_size = 128`. |
| TOML overrides | Set `setup.machine_precision_target = 0` to disable early exit and run the full resolution sweep. |
