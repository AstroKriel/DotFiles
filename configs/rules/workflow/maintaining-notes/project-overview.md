# Project Notes

Notes for active research and teaching projects. Each project has its own directory under `~/Documents/ProjectNotes/`.

---

## Scope

A project note covers the context, status, and accumulated knowledge for a single research paper, teaching project, or supervision case. It records what is going on and what is known, not what to do next (that belongs in a task tracker or issue list).

Covered by this file:

| Category | Location |
|---|---|
| Research papers | `ProjectNotes/<paper>/` |
| Teaching projects | `ProjectNotes/student-projects/`, `ProjectNotes/bitesize-python/` |
| Student supervision | `ProjectNotes/student-projects/<student>/` |

---

## Structure: Research Papers

Every project starts with just `README.md`. Add files only when the content outgrows a single file. When `README.md` becomes an index, it lists every file it points to.

```text
<paper>/
├── README.md         who is involved, current status, open questions
├── log.md            session trail (add when history starts to accumulate)
├── threads/          idea explorations (add when ideas need sustained space)
└── refs/             reference notes (add when reference material builds up)
```

### README.md

The entry point. Answers: who is involved, where the project stands, what the immediate open questions are. Updated when the project status changes: new results, a direction change, a submission.

When the project grows beyond a single file, `README.md` becomes an index. Each section becomes a link to its own file.

### log.md

A session trail. Append-only; never edit past entries. One date block per session worked, with one to three bullet points summarising what was done and the key outcome.

```
2026-05-31
- AlfvenWave convergence at 512: FS17 stable, Quokka2026 blows up above 256 with PPM-EP.
- Started resistivity sweep; first run segfaulted on missing ghost cell init.
```

### threads/

One file per question or idea being actively explored. A thread accumulates context, hypotheses, and findings around a single open question. When a question is settled, add a `**Resolved:**` line at the top with the conclusion in one sentence. The conclusion then lands in `README.md` or `log.md`; the thread stays as a record of the reasoning.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Current status and blockers | Line-by-line code documentation |
| Key findings and decisions | Raw simulation output |
| Notes on sources and references | Task lists and to-dos |
| Reproduction steps for a result | Configuration files (those go in the project repo) |

A fact or finding goes in the log. Once it becomes a binding convention that applies beyond this project, promote it to `~/.rules/`.

---

## Concluding a project

Add a final log entry marking the outcome (accepted, rejected, etc.) and archive the directory. Do not delete it.
