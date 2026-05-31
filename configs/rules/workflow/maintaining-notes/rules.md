# Rules

The `~/.rules/` system: what it is, what belongs in it, and how to add, extend, and promote rules.

---

## What it is

`~/.rules/` holds personal conventions for code, writing, and workflow. Rules are prescriptive and stable: they define the working convention, not what is underway or what has been discovered.

The canonical source is `~/Projects/DotFiles/configs/rules/`. All `.md` files there are symlinked into `~/.rules/` by `uv run -m scripts.setup.rules_files` run from the DotFiles repo. Edit the source; never edit through a symlink.

---

## Structure

```text
~/.rules/
├── dev/            conventions for producing code and scripts
│   ├── python/     Python language bundle
│   └── quokka/     Quokka project bundle
├── writing/        conventions for producing text
└── workflow/       conventions for how to work
    └── maintaining-notes/      this bundle
```

Each directory has a `README.md` that indexes its contents. The READMEs are the up-to-date map; the tree above shows the current top-level shape.

---

## What belongs here

A rule belongs in `~/.rules/` when it is a binding convention: it applies across future uses of a tool, language, or context, and it prescribes how to do something.

| Belongs in `~/.rules/` | Does not belong |
|---|---|
| How to write a docstring | What a specific function does |
| Commit message format | Status of an ongoing investigation |
| Agent collaboration modes | HPC machine hardware specs |
| File and folder naming conventions | Lessons learned from a specific simulation run |

When in doubt: a rule answers "what is the convention?" A note answers "what is known?". See `README.md` in this bundle for the full decision rubric.

---

## Adding a rule

1. Find the right file. Read `~/.rules/README.md` for the full index. Use an existing file if the topic fits; create a new one if nothing covers it.
2. Edit the source under `~/Projects/DotFiles/configs/rules/`.
3. From `~/Projects/DotFiles/`, run `uv run -m scripts.setup.rules_files` to relink and `uv run -m scripts.setup.rules_index` to regenerate the index.
4. Commit following `workflow/git.md`.

**New file:** name it `<concept>.md`; one word or a short phrase naming the subject. Open with a title and a one-line description so the map entry is meaningful.

**Promoting a file to a bundle:** when a single file grows to cover sub-topics that each warrant their own section, convert it to a subdirectory. Create a `README.md` inside it for any context that applies to the bundle as a whole, and split the content into per-topic files.

**New bundle:** when the concept is large from the start, create the subdirectory directly. Add a `README.md` if there is bundle-level context to capture. Follow the existing bundle pattern in `code/python/` or `code/quokka/`.

---

## Promoting a finding

A finding in the notes system becomes a rule when it can be stated as "always X" or "never Y" and applies to future work, not just to the instance that produced it.

To promote:

1. Identify which `~/.rules/` file the convention belongs in.
2. Phrase it as a rule: prescriptive, not descriptive. The rule stands alone without reference to the investigation that produced it.
3. In the notes source, note the promotion if the investigation entry is still live. The rule itself carries no back-reference.
4. Commit following `workflow/git.md`.
