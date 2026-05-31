# Quokka: Data Extraction and Diagnostics

Rules for extracting and working with Quokka simulation output using `ww-quokka-sims`.

---

## Tool

**Package:** `~/Projects/Asgard/sindri/submodules/ww-quokka-sims/`

**Virtual environment:** activate before running any command.

```bash
source ~/Projects/Asgard/mimir/kriel-quokka-mhd/.venv/bin/activate
```

---

## Workflow

| Rule | |
|---|---|
| Diagnostics first | The diagnostic commands are the primary interface with simulation data; use them before writing any custom extraction code. |
| Plot on the host | When sim data lives on a remote host, run the diagnostic commands there. Copy only the derived outputs back. |
| Post-analysis from derived | For comparisons or derived quantities, load the extracted file from `derived/`; do not re-read the plotfile. |

**Extraction:**

1. **Inspect.** Call `quokka-inspect-snapshot <plt_dir>` to confirm which field keys are available before running anything else.
2. **Extract.** Run the appropriate plot command with `--save-data`. This writes the figure and data to the sim's `derived/` subdirectory. Raw plotfiles stay on the cluster or in `/tmp/`; only derived products are committed.
3. **Sanity-check.** Run `quokka-plot-vi-evolution` to check volume-integrated energy and momentum before extracting detailed field data.

**Post-analysis:**

4. **Load the data.** Write a problem-specific script that loads the extracted file from `derived/`; do not re-read the plotfile.
5. **Compare runs.** Use `quokka-compare-snapshots` for field-level regression checks between two snapshot directories.

---

## Commands

| Command | Purpose |
|---|---|
| `quokka-inspect-snapshot` | List all field keys available in a plotfile. |
| `quokka-plot-profiles` | Midplane 1D profiles of scalar or vector field components along any axis. |
| `quokka-plot-slices` | Midplane 2D slices of field components; auto-generates MP4 animations over a snapshot series. |
| `quokka-plot-pdfs` | Probability distribution functions of field components over a snapshot or series. |
| `quokka-plot-spectra` | Isotropic power spectra of scalar fields. |
| `quokka-plot-vi-evolution` | Volume-integrated field quantities as a time series. |
| `quokka-plot-vi-comparison` | Fractional difference in volume-integrated quantities between two simulation runs. |
| `quokka-compare-snapshots` | Field-by-field numerical comparison between two snapshot directories. |

---

## Flags

| Flag | Applies to | Meaning |
|---|---|---|
| `--tag` | all commands | Glob pattern to select a subset of plotfiles (e.g. `plt000*`). Omit to use all. |
| `-f` | plot commands | Field name(s) to extract (e.g. `magnetic`, `density`, `velocity`). |
| `-c` | profile, slice, pdf | Component index for vector fields: `x_0`, `x_1`, `x_2`. |
| `-a` | profile, slice | Axis along which to profile or slice (e.g. `x_0` for the x-axis). |
| `--save-data` | plot commands | Write extracted values to JSON alongside the figure. |
| `-o` | plot commands | Output directory for figures and JSON. |

---

## Field names

| Field name | What it is |
|---|---|
| `density` | Gas density |
| `velocity` | Velocity vector |
| `magnetic` | Magnetic field vector |
| `momentum` | Momentum vector |
| `total_energy` | Total energy (internal + kinetic + magnetic) |

Run `quokka-inspect-snapshot` to see the full list for a given run.
