# Quokka: Local Workflow

Build, run, and compute-tier workflow for Quokka development.

---

## Environment layers

| Layer | Purpose | Example |
|---|---|---|
| CMake build tree | One compiled Quokka configuration: cache, generated build files, and binaries. | `build/3d-release`, `build/3d-debug` |
| Container or devcontainer | Machine-level toolchain and OS environment. | `.devcontainer/gcc-container` |

| Rule | |
|---|---|
| No Python inside Quokka | `QUOKKA_PYTHON` is always disabled (`-DQUOKKA_PYTHON=OFF`). It is a separate failure surface from the solver and is not needed. All analysis goes through `ww-quokka-sims/`. |
| No Python environment in `quokka/` | Do not create one. |

---

## Two-tier compute model

| Tier | Machine | Purpose |
|---|---|---|
| Local | Arch AMD laptop | Low-resolution 3D tests for development validation. |
| HPC | Supercomputer via SSH | Production simulations at full resolution. |

Local runs validate solver behaviour cheaply. HPC runs produce data for analysis. Input `.toml` files are the same across both tiers; resolution and domain size are adjusted via the input file.

---

## Data pipeline

```
Quokka (C++) -> HDF5 plotfiles -> ww-quokka-sims/ -> kriel-quokka-mhd
```

No analysis or plotting is done inside `quokka/` itself. See `diagnostics.md` for the extraction workflow.

---

## The `quokka` script

`scripts/bash/quokka` is a thin wrapper around CMake, Ninja, and CTest.

| Command | What it does |
|---|---|
| `quokka config` | Configure a build tree with CMake. |
| `quokka build` | Compile one or more targets with Ninja. |
| `quokka run` | Run a built problem executable or a CTest selection. |
| `quokka buildrun` | Build and then run. |
| `quokka list` | List problem directories under `src/problems/`. |
| `quokka target` | Print the raw CMake target list; usually too noisy for daily use. |

Preset names:

| Preset | Build dir | Meaning |
|---|---|---|
| `3d` | `build/3d-release` | 3D Release |
| `3d-debug` | `build/3d-debug` | 3D Debug |

---

## Typical workflow

```bash
cd ~/Projects/quokka
scripts/bash/quokka config -d 3d --delete -DQUOKKA_PYTHON=OFF
scripts/bash/quokka build -d 3d <ProblemName>
scripts/bash/quokka run   -d 3d <ProblemName>
```

| Step | Effect |
|---|---|
| `config -d 3d --delete` | Recreates `build/3d-release` as a fresh 3D Release build tree. |
| `build -d 3d <ProblemName>` | Compiles the target in `build/3d-release`. |
| `run -d 3d <ProblemName>` | Runs the executable using `inputs/<ProblemName>.toml` by default. |

Pass `--input <file>` to `run` or `buildrun` to override the default input file.

---

## Per-host environment

When a host needs a non-default toolchain or env vars (e.g. a backport `gcc` for C++20 `<format>`), drop a shell file at `~/.config/quokka/profile.sh` on that host. Pass `--source ~/.config/quokka/profile.sh` to `quokka config/build/buildrun/run` so it gets sourced before each step.

The file is machine-local and never committed. Per-host specifics (which compiler, which modules, which env vars) live in `~/Documents/ProjectNotes/hpcs/<host>/`.

---

## MHD problem selection

For local MHD development, use targeted low-cost problems rather than a broad sweep.

| Problem | Use |
|---|---|
| `AlfvenWaveLinear` | First local 3D MHD validation; narrow and cheap. |
| `AlfvenWaveLinearConvergence` | Convergence-oriented follow-up. |
| `OrszagTang` | Stronger MHD follow-up after the Alfven wave check. |
| `MHDBalsaraVortex` | Additional 3D MHD validation. |

---

## Build variants

| Need | Use |
|---|---|
| Standard 3D Release | `-d 3d` |
| Standard 3D Debug | `-d 3d-debug` |
| Multiple 3D variants side by side | Raw CMake with explicit build directories. |

When multiple variants are needed:

```bash
cmake -S . -B build/3d-release -G Ninja -DCMAKE_BUILD_TYPE=Release -DAMReX_SPACEDIM=3
cmake -S . -B build/3d-debug   -G Ninja -DCMAKE_BUILD_TYPE=Debug   -DAMReX_SPACEDIM=3
cmake -S . -B build/3d-asan    -G Ninja -DCMAKE_BUILD_TYPE=Debug   -DAMReX_SPACEDIM=3 -DENABLE_ASAN=ON
```
