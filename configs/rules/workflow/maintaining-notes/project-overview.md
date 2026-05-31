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

## Structure

Each project directory should contain:

```text
<paper>/
├── README.md       current status, one-paragraph summary, open questions
├── log.md          dated entries: decisions, findings, dead ends
└── refs/           notes on specific papers, datasets, or tools used
```

The `README.md` is the entry point. It should answer: what is this project, where does it stand, and what are the immediate open questions.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Current status and blockers | Line-by-line code documentation |
| Key findings and decisions | Raw simulation output |
| Notes on sources and references | Working convention (promote to `~/.rules/`) |
| Reproduction steps for a result | Configuration files (those go in the project repo) |

A fact or finding goes in the log. Once it becomes a binding convention that applies beyond this project, promote it to `~/.rules/`.

---

## Keeping notes current

Update `README.md` when the project status changes: new results, a direction change, a paper submission, or a supervision milestone. The log is append-only; never edit past entries.

When a project concludes, add a final log entry marking the outcome (accepted, rejected, student graduated, etc.) and archive the directory. Do not delete it.
