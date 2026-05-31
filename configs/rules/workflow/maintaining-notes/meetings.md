# Meeting Notes

Notes for recurring group meetings and ad-hoc discussions. Stored under `~/Documents/ProjectNotes/meetings/`.

---

## Scope

A meeting note captures what was discussed, decided, or assigned in a single meeting or a recurring series. It is the written record of the meeting, not a task list or a minutes document.

Location: `ProjectNotes/meetings/`

---

## Structure

```text
meetings/
├── <group>/            one directory per recurring series
│   ├── README.md       group name, cadence, participants, purpose
│   └── YYYY-MM-DD.md   one file per session
└── ad-hoc/             one-off meetings that do not belong to a series
    └── YYYY-MM-DD-<topic>.md
```

For recurring series, the `README.md` is the persistent reference: who attends, how often, and what the group is for. Individual session files are append-only records.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| What was discussed and by whom | Action items managed elsewhere (task tracker, issue) |
| Decisions reached in the meeting | Slides or supporting materials (link, do not embed) |
| Open questions raised | Background context that pre-dates the meeting |
| Follow-up commitments noted | Binding conventions (promote to `~/.rules/`) |

---

## Session file format

Each session file should open with the date and attendees, then follow the meeting structure:

```markdown
# YYYY-MM-DD

**Attendees:** ...

## Topic 1
...

## Topic 2
...

## Follow-ups
- ...
```

Keep entries factual. Record what was said and decided; do not editorialise. If a decision reached in a meeting becomes a binding convention, promote it to `~/.rules/`.
