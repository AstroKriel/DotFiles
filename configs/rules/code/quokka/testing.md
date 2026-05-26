# Quokka: Testing

Rules for validating MHD solver correctness.

---

## Pass/fail signal

| Test type | Signal |
|---|---|
| `*Convergence` problems | Exit code from `quokka::richardson::run()`. Nonzero means measured order of accuracy fell below tolerance. |
| All other problems | Exit code `0` on clean integration. Internal asserts trip on NaN, negative pressure, FPE, and similar conditions. |

A clean exit is consistent with a silently broken solver. Always include at least one `*Convergence` problem when validating a build or code change.

---

## MHD smoke-test set

| Problem | n_cell | stop_time | What it exercises |
|---|---|---|---|
| `BrioWuShockTube` | `512x16x16` | `0.15` | 1D MHD Riemann problem; shock-capturing baseline. |
| `OrszagTang` | `128x128x8` | `1.0` | 2D MHD vortex; constrained-transport stress test. |
| `MHDBlast` | `64x64x64` + AMR | `0.05` | 3D blast with AMR; exercises divB-preserving prolongation and restriction. |
| `AlfvenWaveLinearConvergence` | sweeps `nx` 16..128 | per-resolution | Richardson convergence sweep; the only test in this set with a real correctness signal. |

Run each with:

```bash
quokka buildrun -d 3d <ProblemName>
```

---

## Convergence tests

| Rule | |
|---|---|
| Correctness gate | The `*Convergence` problems are the only tests that fail the exit code when the solver is wrong. Treat a nonzero exit as a real regression, not flakiness. |
| Richardson refines nx only | Oblique modes (`num_modes_y != 0` or `num_modes_z != 0`) will not converge under this strategy. The tests abort on nonzero transverse modes. |
| No resistivity | `FastWaveConvergence` and `SlowWaveConvergence` abort if `mhd.resistivity != 0`. See `mhd.md`. |
| MPI decomposition | Set `amr.blocking_factor_x = 16` and `amr.max_grid_size = 128`. See `mhd.md`. |
| TOML overrides | `setup.nx_max` and `setup.machine_precision_target` are queryable from the input file. Set `setup.machine_precision_target = 0` to disable early exit and run the full resolution sweep. |
