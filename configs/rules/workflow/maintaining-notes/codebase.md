# Codebase Notes

Notes for tools and codebases in active use. Each code has its own directory under `~/Documents/ProjectNotes/codebases/`.

---

## Scope

A code note covers a tool, library, or codebase that is used regularly but not owned or primarily developed here. It records how to use it, known quirks, and accumulated troubleshooting knowledge.

This is distinct from project notes: a code note is about the tool itself, not about a project that happens to use it.

Location: `ProjectNotes/codebases/<code>/`

---

## Structure

```text
codebases/<code>/
├── README.md       what the code is, version in use, how to install and invoke
├── log.md          dated entries: discovered behaviours, workarounds, version changes
└── recipes/        reusable invocation patterns and configuration snippets
```

The `README.md` covers the essential facts: what the code does, which version is current, and the canonical invocation. A new user of the notes should be able to orient quickly from the README alone.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Installation and environment setup | Source code for the tool itself |
| Known bugs and workarounds | Results produced by running the tool |
| Invocation patterns and flags | Project-specific analysis using the tool |
| Version-specific behaviour | Binding conventions (promote to `~/.rules/`) |

When a workaround solidifies into a binding convention, promote it to the appropriate file in `~/.rules/code/`.

---

## Keeping notes current

Update `README.md` when the installed version changes or the canonical invocation changes. Add a log entry for any non-obvious behaviour discovered during use, even if it seems minor: future debugging often traces back to behaviour first noticed in passing.
