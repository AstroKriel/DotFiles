# LaTeX Writing Style

Rules for formatting LaTeX documents, particularly scientific notes and papers.

---

## Document Structure

| Rule | |
|---|---|
| No paragraph indentation | add `\setlength{\parindent}{0pt}` and `\setlength{\parskip}{6pt}` to the preamble |
| No `\paragraph*{}` headings | fold the label into running prose instead |

---

## Cross-references

| Rule | |
|---|---|
| Equation, figure, and table references | use `\cref{...}` standalone (from `cleveref`); never `equation~\ref{...}`, `figure~\ref{...}`, etc.; do not precede `\cref` with a descriptive name |
| Section references | use `§\ref{sec:...}` |

---

## Labels

Labels follow a three-part hierarchy: `type:group:name`.

| Type prefix | Use |
|---|---|
| `eqn:` | equations |
| `sec:` | sections, subsections, subsubsections |
| `fig:` | figures |
| `tab:` | tables |

The group identifies the context (e.g. `mhd`, `mhd-linear`, `mhd-planewave`). The name identifies the specific item (e.g. `continuity`, `momentum`). Sub-groups are separated by `-` within the group field, not by additional colons.

Examples: `eqn:mhd:continuity`, `eqn:mhd-linear:momentum`, `sec:mhd-waves:linearise`.

---

## Mathematics

| Rule | |
|---|---|
| Inline math | use `$ ... $` |
| All display math | use `align` or `align*`; never `$$` or `equation` |
| Unnumbered blocks | if no line in the block needs a label, use `align*` rather than `align` with `\nonumber` on every line |
| Roman (upright) text in math | use `\mathrm{}`, never `{\rm ...}` -- `{\rm ...}` is a deprecated plain TeX mode switch |
| Exponentials | use `\exp(...)` rather than `e^{...}` |
| Coordinate planes | write planes as `(x,y)` or `$(\mVectorUnit{e}_1,\mVectorUnit{e}_2)$`, not `x--y` or `x\text{-}y` |
| Symbol case | lower-case for scalars and vectors (including placeholder/dummy variables); upper-case for rank-2 tensors and collections |
| Equation layout (single equation) | LHS on its own line; `&= RHS` indented below; long RHS terms broken across lines, indented to show structure; `, \label{}` on its own final line |
| Equation layout (multi-equation, with `\\`) | `, \label{}` must appear on the same source line as `\\`, not on a separate line; for short RHS append inline (`&= 0 , \label{...} \\`); for long RHS put on the last continuation line before `\\` |

Single-equation example:
```latex
\begin{align}
    \text{LHS term one}
        + \text{LHS term two}
        &= \text{RHS term one}
            + \text{RHS term two}
    , \label{eqn:group:name}
\end{align}
```

Multi-equation example:
```latex
\begin{align}
    \text{short LHS}
        &= \text{short RHS} , \label{eqn:group:name-a} \\
    \text{short LHS}
        &= \text{long RHS term one}
            + \text{long RHS term two}
        , \label{eqn:group:name-b}
\end{align}
```

---

## Footnotes

Content goes on its own indented line; the closing brace goes on its own line. Never attach a footnote directly to a math expression (`$...$\footnote{}`); the marker reads as an exponent. Rephrase so the marker attaches to a word.

```latex
\footnote{
    note text
}
```
