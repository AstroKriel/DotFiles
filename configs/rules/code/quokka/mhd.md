# Quokka: MHD Setup

Rules and reference for configuring and running MHD simulations.

---

## Build requirement

| Rule | |
|---|---|
| `AMReX_SPACEDIM=3` is mandatory | Every MHD problem's CMakeLists is gated by `if(AMReX_SPACEDIM EQUAL 3)`. A 1D or 2D build silently omits all MHD targets with no warning. Changing `SPACEDIM` requires a fresh build directory. |

---

## TOML parameters

### MHD schemes

| Parameter | Values | Notes |
|---|---|---|
| `mhd.emf_compute_scheme` | `"FelkerStone2017"`, `"Balsara2025"`, `"Quokka2026"` | How edge-centred EMFs are computed from face-centred fluxes. |
| `mhd.emf_averaging_scheme` | `"LondrilloDelZanna2004"`, `"Balsara2025"` | How EMFs are averaged at shared edges between adjacent faces. |
| `mhd.resistivity` | float, default `0` | Physical resistivity. Adds ohmic diffusion to the induction equation; enforces parabolic timestep limit `dt < dx^2 / (2 * eta)`. |

### Reconstruction and integration

| Parameter | Values | Notes |
|---|---|---|
| `hydro.reconstruction_order` | `2` (PPM), `3` (PPM+), `5` (PPM-EP) | Spatial reconstruction order. |
| `hydro.rk_integrator_order` | `2` | RK2 time integration. Standard for all MHD runs. |
| `hydro.use_dual_energy` | `0` | Disable for MHD. |

### Grid and AMR

| Parameter | Recommended | Notes |
|---|---|---|
| `amr.max_level` | `0` | Single-level for most MHD tests. |
| `amr.blocking_factor_x` | `16` | See MPI decomposition section below. |
| `amr.max_grid_size` | `128` | See MPI decomposition section below. |
| `do_reflux` | `0` | Disable for single-level runs. |
| `do_subcycle` | `0` | Disable for single-level runs. |

---

## EMF scheme reference

| Compute scheme | Stability | Notes |
|---|---|---|
| `FelkerStone2017` | Most stable | Safe default; well-validated reference. |
| `Balsara2025` | Stable | |
| `Quokka2026` | Least stable | Most efficient; known to go unstable for the slow wave at high resolution with PPM-EP. Artificial resistivity is the planned fix. |

| Averaging scheme | Notes |
|---|---|
| `LondrilloDelZanna2004` | Standard upwind averaging. |
| `Balsara2025` | |

---

## MPI decomposition

Setting `amr.blocking_factor_x` to `max(16, nx)` and `amr.max_grid_size` to `nx` forces a single AMReX box at every resolution, making all MPI ranks beyond the first idle with no warning. Always set:

```toml
amr.blocking_factor_x = 16
amr.max_grid_size = 128
```

This allows AMReX to split a 512-cell domain into up to 32 boxes.

---

## Minimum cell count

The hydro stencil uses `nghost = 4`. A single-box periodic grid below 8 cells per dim has opposite-side ghosts overlapping inside the valid region. Use at least 8 cells per dim under periodic boundary conditions.

---

## Resistivity

Enable with `mhd.resistivity = <eta>`. The parabolic timestep limit is enforced automatically.

| Rule | |
|---|---|
| No resistivity in Richardson convergence tests | `FastWaveConvergence` and `SlowWaveConvergence` abort if `mhd.resistivity != 0`. Resistivity validation uses the fixed-resolution `AlfvenWaveLinear` test. |
| Reference input | `inputs/AlfvenWaveLinear_resistive.toml` (eta=0.01, grid-aligned, FS17+LD04). |
| Analytic reference | Amplitude decays as `exp(-gamma*t)` where `gamma = eta*k^2/2`. Velocity lags B by `phi = arctan(gamma/omega_real)`. |
