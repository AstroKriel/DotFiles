# Python: Naming and Imports

How to name things: files, modules, functions, classes, variables, mathematical variables, and constants.

---

## Files and Modules

Filename conventions follow `~/.rules/code/naming.md`, applied with `_` as the word delimiter.

| Rule | |
|---|---|
| Casing | `snake_case` for all filenames |
| Pattern | verb-noun: `<verb>_<noun>.py` |
| Private modules | leading underscore: `_<verb>_<noun>.py` |
| Packages | named for the concept they expose: `arrays`, `fields`, `plots` |

### Module Growth

| Rule | |
|---|---|
| Name on promotion | a module promoted to a package keeps its original name |
| Sub-module naming | same verb-noun convention: `<verb>_<noun>.py` |
| Sub-module responsibility | each sub-module owns one narrow responsibility |
| Typical size | 50-300 lines; approaching 400 lines is a signal to split |

```
<concept>/
    __init__.py
    <verb>_<noun>.py
    <verb>_<noun>.py
    ...
```

---

## Functions

Always use strong, specific verb prefixes. Avoid weak or generic leading words that do not communicate what the function does or returns:

| Prefix | Purpose |
|---|---|
| `compute_*` | mathematical/numerical operations |
| `check_*` | returns `bool`, may raise or warn |
| `ensure_*` | raises on failure, no return value; covers both atomic single-constraint checks and compound multi-condition validation; name must reflect both the subject and the criteria being ensured: `ensure_<criteria>_<subject>` or `ensure_<subject>_<criteria>` |
| `as_*` | validates an input and returns it resolved to a canonical type; raises on failure |
| `load_*` | I/O that returns data |
| `save_*` | I/O that writes data |
| `create_*` / `make_*` | object construction |
| `get_*` | query or lookup |
| `resolve_*` | disambiguation between options |
| `extract_*` | pull data from a larger structure |

| Rule | |
|---|---|
| Module private helpers | leading underscore: `_<verb>_<noun>()` |
| Script helpers | no underscore prefix, even when internal to the script |
| Cross-module calls | no underscore prefix if called from another module, even if the function lives in a private module |

---

## Classes

| Rule | |
|---|---|
| Casing | `PascalCase` for all class, enum, and dataclass names |
| Private classes | leading underscore: `_<Name>` |

---

## Variables

| Rule | |
|---|---|
| Casing | `snake_case` exclusively, never camelCase |
| Abbreviations | acceptable when well-known within the domain |
| Descriptive names | use qualified names that read as subscript notation: `<qualifier>_<noun>` |
| Single-letter names | never; names must always indicate what is being worked with |
| Abbreviated names | never; `language` not `lang`, `index` not `idx` |
| Directories | `directory` when only one in scope; `_dir` suffix when multiple: `source_dir`, `target_dir` |
| Comprehension variables | prepend `_` if the name would conflict with an existing name in scope |
| Booleans | `is_*` or `has_*` prefix |
| Receiver variables | name after the noun in the called function: `<noun> = <verb>_<noun>(...)`, not `result` |

---

### Mathematical Variables

When code, comments, and docstrings use mathematical notation, keep naming aligned with Einstein-style conventions.

| Rule | |
|---|---|
| Scalars | lower-case: `<scalar>` |
| Vectors | lower-case with an index: `<vector>_<index>` |
| Tensors | upper-case with indices: `<Tensor>_<index><index>` |
| Code names | preserve the same distinction in variable names where practical |

| Rule | |
|---|---|
| Separators | underscores between all components: subscript labels, operators, and qualifiers |
| Prefer | `<symbol>_<label>`, `<operation>_<quantity>`, `<symbol>_<label>_<qualifier>` |
| Avoid | `<symbol><label>`, `<operation><quantity>`, `<symbol><label><qualifier>` |
| Scope | apply to variable names, comments, docstrings, and user-facing labels; preserve established public labels |

### Field Identifiers (`field_name`)

The `field_name` string on `Field` objects is a plain-text snake_case identifier, not a LaTeX expression. Three rules cover most cases:

| Kind | Pattern |
|---|---|
| Primitive physical quantity | `<quantity>` |
| Scalar magnitude of a field | `<field>_magnitude` |
| Differential operator applied to a field | `<operation>_<field>` |

For synthetic or intermediate fields without a fixed physical identity, use a qualifier that names what the field *is*, not how it was computed. Prefer a word that describes mathematical content over an abbreviation of a process.

### Field Labels (`latex_label`)

The `latex_label` string follows two rules based on field type:

| Field type | Notation |
|---|---|
| Vector field | `\vec{<field>}` notation: `\vec{q}`, `(\nabla\times\vec{q})\times\vec{q}` |
| Scalar from index contraction | index notation: `q_i p_j \partial_i u_j`, `\partial_i q_i` |

---

### Constants

`UPPER_CASE` at module level:

```python
MAX_COUNT: int = 1000
DEFAULT_TOL: float = 1e-6
```
