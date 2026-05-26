# Notes

Rules for personal note-taking systems. Each file defines one system: its scope, structure, what belongs in it, and how it relates to the others.

---

## Stores

| Store | Where | Answers |
|---|---|---|
| Rules | `~/.rules/` | What is the convention for this? |
| Notes | `~/Documents/ProjectNotes/`, per-machine repos | What is going on? What is known? |
| Configs | `~/Projects/DotFiles/` | What settings does this machine use? |
| Auto-memory | `~/.claude/projects/*/memory/` | Claude collaboration preferences |

A fact (something learned about the world) goes in a note. A decision (the working convention going forward) goes in `~/.rules/`. A config (a setting applied on machine install) goes in DotFiles.

When an investigation resolves and leaves a binding convention, it promotes from a note to a rule.

---

## Files

| File | Covers |
|---|---|
| `rules.md` | The `~/.rules/` system: structure, scope, how to add and promote rules |
| `project.md` | Papers, teaching projects, student supervision (`ProjectNotes/<paper>/`, `student-projects/`, `bitesize-python/`) |
| `code.md` | Tools and codebases in active use (`ProjectNotes/codes/<code>/`) |
| `hpc.md` | HPC machines in use, not owned or maintained (`ProjectNotes/hpcs/<cluster>/`) |
| `meetings.md` | Meeting notes: recurring groups and ad-hoc (`ProjectNotes/meetings/`) |
| `personal-machine.md` | Machines owned and maintained (per-machine setup repos) |
