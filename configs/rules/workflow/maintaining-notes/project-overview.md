# Project Notes

Notes for active research and teaching projects. Each project has its own directory under `~/Documents/ProjectNotes/`.

---

## Scope

A project note covers the context, status, tasks, and accumulated knowledge for a single research paper, teaching project, or supervision case.

Covered by this file:

| Category | Location |
|---|---|
| Research papers | `ProjectNotes/<paper>/` |
| Teaching projects | `ProjectNotes/student-projects/`, `ProjectNotes/bitesize-python/` |
| Student supervision | `ProjectNotes/student-projects/<student>/` |

---

## Structure: Research Papers

Start with just `README.md`. Add files only as the project grows. Two guiding principles:

- The entry point for any folder is always `README.md`.
- A file splits into a folder of the same name when its content spans multiple domains or grows too large.

```text
<paper>/
├── README.md           overview; becomes index as project grows
├── log.md              session trail
├── tasks.md            task list; splits into tasks/ when tasks span multiple domains
├── threads/            active explorations and open questions
└── notes/              refs, background material, stable context
```

### README.md

Answers: who is involved, where the project stands, what the immediate open questions are. Updated when the project status changes.

When the project grows beyond a single file, `README.md` becomes an index listing every file it points to, including files in `notes/`.

### log.md

A session trail. Append-only; never edit past entries. One date block per session, one to three bullet points summarising what was done and the key outcome.

```
2026-05-31
- AlfvenWave convergence at 512: FS17 stable, Quokka2026 blows up above 256 with PPM-EP.
- Started resistivity sweep; first run segfaulted on missing ghost cell init.
```

### tasks.md / tasks/

Active task lists. A single `tasks.md` at the root when tasks are unified; splits into `tasks/` with one file per domain when the project spans multiple workstreams.

### threads/

One subfolder per open question or idea being actively explored. Each subfolder contains a `README.md` and, if needed, a `figures/` directory alongside it.

```text
threads/
└── <topic>/
    ├── README.md
    └── figures/
```

When a question is settled, add a `**Resolved:**` line at the top of the thread `README.md` with the conclusion in one sentence. The conclusion lands in the project `README.md` or `log.md`; the thread stays as a record of the reasoning.

Figures not tied to any thread belong in the project repo, not ProjectNotes.

### notes/

Reference material, background context, and stable expanded content that overflowed from `README.md`. When `README.md` becomes an index, it links to files here.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Current status and open questions | Line-by-line code documentation |
| Key findings and decisions | Raw simulation output |
| Task lists | Configuration files (those go in the project repo) |
| Notes on sources and references | Working conventions (promote to `~/.rules/`) |
| Reproduction steps for a result | |

A fact or finding goes in the log. Once it becomes a binding convention that applies beyond this project, promote it to `~/.rules/`.

---

## Concluding a project

Add a final log entry marking the outcome (accepted, rejected, etc.) and archive the directory. Do not delete it.
