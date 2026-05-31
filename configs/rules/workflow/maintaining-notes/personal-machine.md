# Personal Machine Notes

Notes for machines that are owned and actively maintained. Each machine has its own setup repository, separate from `ProjectNotes/`.

---

## Scope

A personal machine note is a per-machine setup repository: a standalone repo that records the configuration, installation history, and operational knowledge for one owned machine. It is the manual for that specific machine.

This is distinct from HPC notes (see `hpc.md`): HPC notes record how to use a shared cluster; personal machine notes record how a machine is configured and how to reproduce that configuration.

---

## Structure

Each machine has its own repository, stored wherever is convenient on that machine (e.g. `~/Projects/<MachineName>/`). The repository structure:

```text
<MachineName>/
├── README.md           machine name, OS, hardware summary, purpose
├── setup.md            installation steps: OS, packages, dotfiles, services
├── pending-issues.md   open issues and unresolved configuration problems
└── debug-diary/        retrospective entries for resolved issues
    └── YYYY-MM-DD.md
```

The `README.md` is the orientation document: what the machine is and what it is used for. `setup.md` is the reproduction guide: following it from a clean OS install should reproduce the working configuration.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Hardware specs and OS version | Dotfiles themselves (those go in `~/Projects/DotFiles/`) |
| Package and service installation steps | Project data or results |
| Non-obvious configuration decisions | HPC cluster details (see `hpc.md`) |
| Open and resolved configuration issues | Binding conventions (promote to `~/.rules/`) |

---

## Open issues vs. debug diary

`pending-issues.md` is for issues that are currently open: unresolved problems, known workarounds in place, or configuration gaps. It is a live document; entries are added and removed as issues open and close.

`debug-diary/` is retrospective: each file records a resolved issue, what caused it, and how it was fixed. Entries are append-only and are never edited after the fact.

When an issue is resolved, remove it from `pending-issues.md` and add a dated entry to `debug-diary/`.

---

## Keeping notes current

Update `setup.md` when a significant configuration change is made: a new service, a package upgrade that required intervention, a dotfiles change with machine-specific implications. The goal is that `setup.md` remains reproducible at any point in time.

When a machine is retired, add a final `README.md` note marking the retirement date and disposition.
