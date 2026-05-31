# LaTeX Project Structure

How a LaTeX project is laid out: file structure, figure organisation, tables, bibliography management, and submission versioning.

The project is hosted on Overleaf and synced to GitHub.

---

## File Structure

```text
<project>/
├── main.tex
├── response.tex
├── header/
│   ├── imports.tex
│   ├── aliases.tex
│   ├── refs.bib
│   ├── <journal>.cls
│   └── <journal>.bst
├── figures/
│   ├── results/
│   │   └── <name>.pdf
│   └── schematics/
│       └── <name>.pdf
├── tables/
│   └── <name>.tex
├── notes/
│   └── <name>.tex
└── version-<N>/
    └── main.tex
```

`main.tex` holds the document class declaration, `\input{header/imports}`, `\input{header/aliases}`, and all paper content. Content is not split into per-section files.

---

## Header Directory

`header/` groups all preamble material and bibliography into one place:

| File | Purpose |
|---|---|
| `imports.tex` | package imports |
| `aliases.tex` | custom macros and commands |
| `refs.bib` | bibliography database |
| `<journal>.cls`, `<journal>.bst` | journal class and bibliography style files |

Define macros in `aliases.tex`, grouped by purpose with a comment line. Do not define macros inline in `main.tex`.

---

## Figures

`figures/` is split by how the figure was produced:

| Directory | Contents |
|---|---|
| `figures/results/` | data-driven plots produced by Python scripts |
| `figures/schematics/` | hand-drawn diagrams produced in Inkscape or Blender |

Both directories contain PDF files for inclusion and SVG (or `.blend`) source files alongside them. Blender-sourced figures also retain their `.blend` file.

Name figure files descriptively using hyphens: `bw-profiles.pdf`, `wave-convergence.pdf`. The source file (SVG or Blender) lives in the same directory as the compiled PDF.

---

## Tables

Long or generated tables go in `tables/` as separate `.tex` files and are pulled in with `\input{tables/<name>}`. Short inline tables can stay in `main.tex`.

---

## Notes

`notes/` holds standalone technical derivations that inform the paper but are not part of it. Each is a self-contained `.tex` file that compiles independently.

---

## Submission and Versioning

On submission, copy the current state of `main.tex` (and `response.tex` from version 2 onwards) into `version-<N>/`. The root `main.tex` continues to be the working file.

`response.tex` is the referee response document. It appears in the root from version 2 onwards and is versioned alongside `main.tex`.

---

## Bibliography

Use a single `refs.bib` in `header/`. Do not split the bibliography across multiple files.
